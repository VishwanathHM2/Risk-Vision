# backend/app/data_fetch.py
import yfinance as yf
import pandas as pd

def fetch_prices(tickers, start, end):
    """
    Universal fetcher for Yahoo Finance.
    tickers: list[str]
    start/end: iso date strings or date objects
    returns: DataFrame with columns = ticker symbols and datetime index
    """
    if isinstance(tickers, str):
        tickers = [tickers]

    raw = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False,
        group_by='ticker',
        threads=True,
        auto_adjust=False
    )

    if raw is None or raw.empty:
        raise ValueError("Yahoo Finance returned no data for this range/tickers.")

    # If MultiIndex columns (common when multiple tickers)
    if isinstance(raw.columns, pd.MultiIndex):
        # Try the common positions
        cols0 = list(raw.columns.get_level_values(0))
        cols1 = list(raw.columns.get_level_values(1))

        # Preferred: ('Adj Close', TICKER) or (TICKER, 'Adj Close')
        if "Adj Close" in cols0:
            df = raw["Adj Close"]
        elif "Adj Close" in cols1:
            # xs selects level=1 == 'Adj Close' across tickers
            df = raw.xs("Adj Close", level=1, axis=1)
        elif "Close" in cols0:
            df = raw["Close"]
        elif "Close" in cols1:
            df = raw.xs("Close", level=1, axis=1)
        else:
            # Brutal fallback: try to find any price-like column
            possible = {"Close", "Adj Close", "close", "adjclose", "Open"}
            found = None
            for p in possible:
                if p in cols0:
                    found = p
                    break
                if p in cols1:
                    found = p
                    break
            if found is not None:
                if found in cols0:
                    df = raw[found]
                else:
                    df = raw.xs(found, level=1, axis=1)
            else:
                raise ValueError("No usable price columns returned by yfinance (multiindex).")

    else:
        # Single ticker download commonly returns single-level columns
        cols = list(raw.columns)
        if "Adj Close" in cols:
            df = raw[["Adj Close"]].rename(columns={"Adj Close": tickers[0]})
        elif "Close" in cols:
            df = raw[["Close"]].rename(columns={"Close": tickers[0]})
        else:
            # fallback, pick first numeric column
            numeric_cols = [c for c in cols if raw[c].dtype.kind in "fiu"]
            if numeric_cols:
                df = raw[[numeric_cols[0]]].rename(columns={numeric_cols[0]: tickers[0]})
            else:
                raise ValueError("No usable price columns returned by yfinance (singleindex).")

    df = df.dropna(how="all")
    if df.empty:
        raise ValueError("Fetched price data is empty after cleaning.")
    df.index = pd.to_datetime(df.index)
    # Ensure column order matches tickers list (sometimes yfinance reorders)
    cols_final = [c for c in tickers if c in df.columns] + [c for c in df.columns if c not in tickers]
    df = df.loc[:, cols_final]
    return df
