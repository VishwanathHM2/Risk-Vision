import React, { useState } from "react";

export default function Controls({ onAnalyze, loading }) {
  const [tickers, setTickers] = useState("AAPL,MSFT,GOOGL");

  // MUST use YYYY-MM-DD format
  const [start, setStart] = useState("2020-01-01");
  const [end, setEnd] = useState("2024-12-31");

  const [weights, setWeights] = useState("33,33,34");
  const [confidence, setConfidence] = useState(0.95);

  const submit = (e) => {
    e.preventDefault();

    onAnalyze({
      tickers: tickers.split(",").map((t) => t.trim()),
      weights: weights.split(",").map((w) => parseFloat(w)),
      start_date: start,
      end_date: end,
      confidence,
    });
  };

  return (
    <div className="card controls">
      <h3>Settings</h3>

      <form onSubmit={submit}>
        <label>Tickers</label>
        <input value={tickers} onChange={(e) => setTickers(e.target.value)} />

        <label>Start Date</label>
        <input
          type="date"
          value={start}
          onChange={(e) => setStart(e.target.value)}
        />

        <label>End Date</label>
        <input
          type="date"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
        />

        <label>Weights</label>
        <input value={weights} onChange={(e) => setWeights(e.target.value)} />

        <label>VaR Confidence</label>
        <input
          type="number"
          min="0.80"
          max="0.99"
          step="0.01"
          value={confidence}
          onChange={(e) => setConfidence(parseFloat(e.target.value))}
        />

        <button type="submit">{loading ? "Analyzing..." : "Run Analysis"}</button>
      </form>
    </div>
  );
}
