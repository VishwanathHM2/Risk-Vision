import React, { useState } from "react";
import Header from "./components/Header";
import Controls from "./components/Controls";
import PriceChart from "./components/PriceChart";
import CorrHeatmap from "./components/CorrHeatmap";
import { fetchPrices, analyze } from "./api";
import "./styles.css";

function App() {
  const [pricesData, setPricesData] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleAnalyze(payload) {
    setLoading(true);
    setError(null);

    try {
      const prices = await fetchPrices(payload);
      const res = await analyze(payload);

      setPricesData(prices);
      setAnalysis(res);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      setPricesData(null);
      setAnalysis(null);
    }

    setLoading(false);
  }

  return (
    <div className="container">
      <Header />

      <div className="main">
        {/* LEFT SIDEBAR */}
        <aside>
          <Controls onAnalyze={handleAnalyze} loading={loading} />

          {error && <div className="error">{error}</div>}

          {analysis && (
            <div className="stats-grid">

              <div className="stat-card stat-blue">
                <h4>Annual Return</h4>
                <p>{(analysis.mean_annual * 100).toFixed(2)}%</p>
              </div>

              <div className="stat-card stat-purple">
                <h4>Volatility</h4>
                <p>{(analysis.std_annual * 100).toFixed(2)}%</p>
              </div>

              <div className="stat-card stat-red">
                <h4>Historical VaR</h4>
                <p>{(analysis.historical_var * 100).toFixed(2)}%</p>
              </div>

              <div className="stat-card stat-orange">
                <h4>Parametric VaR</h4>
                <p>{(analysis.parametric_var * 100).toFixed(2)}%</p>
              </div>

              <div className="stat-card stat-green">
                <h4>Sharpe Ratio</h4>
                <p>{analysis.sharpe.toFixed(2)}</p>
              </div>

            </div>
          )}
        </aside>

        {/* RIGHT CONTENT AREA */}
        <div className="content">
          {pricesData && (
            <div className="chart">
              <PriceChart pricesData={pricesData} />
            </div>
          )}

          {analysis && (
            <div className="chart">
              <CorrHeatmap corr={analysis.corr} />
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;
