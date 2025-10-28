import React, { useState, useEffect } from 'react';
import PlayerSearch from './PlayerSearch';
import StockChart from './StockChart';
import PortfolioTracker from './PortfolioTracker';
import { getPlayerStats, PlayerStats } from '../services/api';

const Dashboard: React.FC = () => {
  const [selectedPlayerId, setSelectedPlayerId] = useState<string | null>(null);
  const [playerStats, setPlayerStats] = useState<PlayerStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (selectedPlayerId) {
      fetchPlayerStats(selectedPlayerId);
    }
  }, [selectedPlayerId]);

  const fetchPlayerStats = async (playerId: string) => {
    setLoading(true);
    setError(null);
    try {
      const stats = await getPlayerStats(playerId);
      setPlayerStats(stats);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch player stats');
      console.error('Error fetching player stats:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePlayerSelect = (playerId: string) => {
    setSelectedPlayerId(playerId);
  };

  return (
    <div className="dashboard-container">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-xl font-semibold mb-4">Players</h2>
            <PlayerSearch onPlayerSelect={handlePlayerSelect} selectedPlayer={selectedPlayerId || undefined} />
          </div>

          {/* Portfolio Tracker */}
          <div className="mt-6">
            <PortfolioTracker positions={[]} currentWeek={0} />
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow p-6">
            {loading && <div className="text-center py-8">Loading player data...</div>}
            
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
                Error: {error}
              </div>
            )}

            {!loading && !error && !selectedPlayerId && (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">Select a player to view their stats</p>
              </div>
            )}

            {!loading && !error && selectedPlayerId && playerStats && (
              <StockChart 
                playerData={playerStats}
                isMarketOpen={true}
                currentWeek={playerStats.weekly_stats.length > 0 ? playerStats.weekly_stats[playerStats.weekly_stats.length - 1].week : 0}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

