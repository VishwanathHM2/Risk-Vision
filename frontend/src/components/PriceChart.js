import React from "react";
import Plot from "react-plotly.js";

export default function PriceChart({ pricesData }) {
  if (!pricesData) return null;

  const { dates, tickers, prices } = pricesData;

  const traces = tickers.map((t, i) => ({
    x: dates,
    y: prices.map((p) => p[i]),
    name: t,
    type: "scatter",
    mode: "lines",
    line: { width: 2 }
  }));

  return (
    <>
      <h2>Price Series</h2>
      <Plot
        data={traces}
        layout={{ height: 430, margin: { t: 30 } }}
        style={{ width: "100%" }}
      />
    </>
  );
}
