# backend/app/analysis.py
import numpy as np
import pandas as pd
from scipy.stats import norm

TRADING_DAYS = 252

def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()

def portfolio_stats(returns: pd.DataFrame, weights: list):
    """
    returns: DataFrame of daily returns
    weights: array-like matching returns.columns
    Returns dict with mean_annual, std_annual, cov, corr
    """
    w = np.array(weights, dtype=float)
    mean_daily = returns.mean()
    cov_daily = returns.cov()
    mean_ann = float(np.dot(w, mean_daily) * TRADING_DAYS)
    var_daily = float(np.dot(w, np.dot(cov_daily.values, w)))
    std_ann = float(np.sqrt(var_daily * TRADING_DAYS))
    return {
        "mean_annual": mean_ann,
        "std_annual": std_ann,
        "cov_daily": cov_daily,
        "corr": returns.corr()
    }

def historical_var(returns: pd.DataFrame, weights: list, confidence=0.95, days=1):
    w = np.array(weights, dtype=float)
    port = returns.dot(w)
    # lower tail quantile
    q = port.quantile(1 - confidence)
    var_1day = -q
    return float(var_1day * np.sqrt(days))

def parametric_var(returns: pd.DataFrame, weights: list, confidence=0.95, days=1):
    w = np.array(weights, dtype=float)
    port = returns.dot(w)
    mu = port.mean()
    sigma = port.std(ddof=1)
    # for 95% confidence we want z at alpha = 1-confidence (lower tail)
    z = norm.ppf(1 - confidence)
    var_1day = -(mu + z * sigma)
    return float(var_1day * np.sqrt(days))

def sharpe_ratio(annual_return, annual_std, risk_free_rate=0.03):
    if annual_std == 0:
        return None
    return (annual_return - risk_free_rate) / annual_std
