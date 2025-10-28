import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import MarketStatus from './components/MarketStatus';
import PlayerSearch from './components/PlayerSearch';
import StockChart from './components/StockChart';
import PortfolioTracker from './components/PortfolioTracker';
import Dashboard from './components/Dashboard';
import { getMarketStatus, getPlayers, getPlayerStats } from './services/api';

function App() {
  const [marketStatus, setMarketStatus] = useState({
    current_week: 0,
    is_market_open: false,
    locked_players: [],
    time_until_close: null
  });

  useEffect(() => {
    // Fetch market status on load
    const fetchMarketStatus = async () => {
      try {
        const status = await getMarketStatus();
        setMarketStatus(status);
      } catch (error) {
        console.error('Failed to fetch market status:', error);
      }
    };

    fetchMarketStatus();
  }, []);

  return (
    <Router>
      <div className="App min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold text-gray-900">
              Fantasy Football Stock Market
            </h1>
          </div>
          <MarketStatus 
            currentWeek={marketStatus.current_week}
            isMarketOpen={marketStatus.is_market_open}
            lockedPlayers={marketStatus.locked_players}
            timeUntilClose={marketStatus.time_until_close}
          />
        </header>

        <main className="max-w-7xl mx-auto px-4 py-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/player/:playerId" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

