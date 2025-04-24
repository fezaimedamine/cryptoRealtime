import React from 'react';
import './App.css';

function CryptoCard({ name, current, predicted }) {
  const isUp = predicted > current;
  const variation = ((predicted - current) / current * 100).toFixed(2);

  return (
    <div className="crypto-card">
      <h2>{name}</h2>
      <p>💰 Prix actuel : <strong>${current.toLocaleString()}</strong></p>
      <p>
        🔮 Prédiction : <strong className={isUp ? 'up' : 'down'}>${predicted.toLocaleString()}</strong>
      </p>
      <p className={`variation ${isUp ? 'up' : 'down'}`}>
        {isUp ? '📈 En hausse' : '📉 En baisse'} ({variation}%)
      </p>
    </div>
  );
}

export default CryptoCard;
