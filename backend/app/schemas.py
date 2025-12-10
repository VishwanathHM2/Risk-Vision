# backend/app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class AnalysisRequest(BaseModel):
    tickers: List[str]
    weights: Optional[List[float]] = None
    start_date: date
    end_date: date
    confidence: float = 0.95

class PriceResponse(BaseModel):
    dates: List[str]
    tickers: List[str]
    prices: List[List[float]]  # matrix: dates x tickers

class AnalysisResponse(BaseModel):
    mean_annual: float
    std_annual: float
    historical_var: float
    parametric_var: float
    sharpe: float
    cov: dict
    corr: dict
