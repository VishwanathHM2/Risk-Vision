import React from "react";

export default function Header() {
  const logo = "http://localhost:8000/static/stock.png";

  return (
    <div className="header">
      <img src={logo} className="logo" alt="Logo" />
      <h1>Stock Market Portfolio Dashboard</h1>
    </div>
  );
}
