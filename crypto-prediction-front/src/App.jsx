import React, { useEffect, useState } from 'react';
import CryptoCard from './CryptoCard';
import './App.css';

function CryptoDashboard() {
  const [data, setData] = useState({});
  const [status, setStatus] = useState('Déconnecté');

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onopen = () => setStatus('Connecté');
    ws.onmessage = (e) => setData(JSON.parse(e.data));
    ws.onclose = () => setStatus('Déconnecté');

    return () => ws.close();
  }, []);

  return (
    <div className="dashboard">
      <h1>📊 Tableau de bord des cryptomonnaies</h1>
      <p className={`status ${status.toLowerCase()}`}>Statut WebSocket : <strong>{status}</strong></p>
      <p className="update-time">
        Dernière mise à jour : {data.timestamp && new Date(data.timestamp).toLocaleTimeString()}
      </p>

      <div className="crypto-list">
        {data.BTC && (
          <CryptoCard
            name="Bitcoin (BTC)"
            current={data.BTC.current_price}
            predicted={data.BTC.predicted_price}
          />
        )}
        {data.ETH && (
          <CryptoCard
            name="Ethereum (ETH)"
            current={data.ETH.current}
            predicted={data.ETH.predicted}
          />
        )}
        {/* Tu peux ajouter d'autres cryptos ici */}
      </div>
    </div>
  );
}

export default CryptoDashboard;
