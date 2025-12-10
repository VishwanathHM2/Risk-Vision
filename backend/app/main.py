# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date
from typing import List
import pandas as pd

from .data_fetch import fetch_prices
from .analysis import daily_returns, portfolio_stats, historical_var, parametric_var, sharpe_ratio
from .schemas import AnalysisRequest

app = FastAPI(title="Portfolio Risk API")

# Allow CORS from React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://172.21.160.1:3000",
        "*"  # allow all (safe for development)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder to serve uploaded image(s)
# Developer provided path: /mnt/data/d290aa88-d782-4028-a0fb-922e5a5ac5e8.png
# we mount the directory /mnt/data at /static so the frontend can request
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/api/prices")
def get_prices(request: AnalysisRequest):
    try:
        tickers = [t.upper().strip() for t in request.tickers]
        df = fetch_prices(tickers, request.start_date.isoformat(), request.end_date.isoformat())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # return JSON-friendly structure: list of dates, tickers, matrix of prices
    dates = [d.strftime("%Y-%m-%d") for d in df.index]
    prices_matrix = df.fillna(method="ffill").fillna(method="bfill").values.tolist()
    return {"dates": dates, "tickers": list(df.columns), "prices": prices_matrix}


@app.post("/api/analyze")
def analyze(request: AnalysisRequest):
    try:
        tickers = [t.upper().strip() for t in request.tickers]
        df = fetch_prices(tickers, request.start_date.isoformat(), request.end_date.isoformat())
        returns = daily_returns(df)
        # normalize weights
        n = len(df.columns)
        if request.weights is None:
            weights = [1.0 / n] * n
        else:
            w = list(request.weights)
            if len(w) != n:
                raise ValueError("Weights length mismatch")
            s = sum(w)
            if s == 0:
                raise ValueError("Sum of weights is zero")
            weights = [float(x) / s for x in w]

        stats = portfolio_stats(returns, weights)
        hist = historical_var(returns, weights, confidence=request.confidence)
        param = parametric_var(returns, weights, confidence=request.confidence)
        sr = sharpe_ratio(stats["mean_annual"], stats["std_annual"], risk_free_rate=0.03)

        # convert cov and corr to serializable dicts
        cov = stats["cov_daily"].round(8).to_dict()
        corr = stats["corr"].round(4).to_dict()

        return {
            "mean_annual": stats["mean_annual"],
            "std_annual": stats["std_annual"],
            "historical_var": hist,
            "parametric_var": param,
            "sharpe": sr,
            "cov": cov,
            "corr": corr
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def root():
    return {"msg": "Portfolio Risk API running"}
