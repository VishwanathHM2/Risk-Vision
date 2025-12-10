import React from "react";
import Plot from "react-plotly.js";

export default function CorrHeatmap({ corr }) {
  if (!corr) return null;

  const tickers = Object.keys(corr);
  const z = tickers.map((a) => tickers.map((b) => corr[a][b]));

  return (
    <>
      <h2>Correlation Matrix</h2>
      <Plot
        data={[
          {
            z,
            x: tickers,
            y: tickers,
            type: "heatmap",
            colorscale: "RdBu",
            zmin: -1,
            zmax: 1
          }
        ]}
        layout={{ height: 430, margin: { t: 30 } }}
        style={{ width: "100%" }}
      />
    </>
  );
}
