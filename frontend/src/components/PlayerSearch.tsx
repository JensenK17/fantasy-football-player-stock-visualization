import React, { useState, useEffect } from 'react';
import { getPlayers, Player } from '../services/api';

interface PlayerSearchProps {
  onPlayerSelect: (playerId: string) => void;
  selectedPlayer?: string;
}

const PlayerSearch: React.FC<PlayerSearchProps> = ({ onPlayerSelect, selectedPlayer }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [positionFilter, setPositionFilter] = useState('ALL');
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      const playerList = await getPlayers();
      setPlayers(playerList);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load players');
      console.error('Error fetching players:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredPlayers = players.filter(player => {
    const matchesSearch = player.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPosition = positionFilter === 'ALL' || player.position === positionFilter;
    return matchesSearch && matchesPosition;
  });

  if (loading) {
    return <div className="text-sm text-gray-500">Loading players...</div>;
  }

  if (error) {
    return <div className="text-sm text-red-600">Error: {error}</div>;
  }

  return (
    <div className="player-search-container">
      {/* Search Input */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search players..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />
      </div>

      {/* Position Filter */}
      <div className="mb-4">
        <select
          value={positionFilter}
          onChange={(e) => setPositionFilter(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="ALL">All Positions</option>
          <option value="QB">Quarterback</option>
          <option value="RB">Running Back</option>
          <option value="WR">Wide Receiver</option>
          <option value="TE">Tight End</option>
          <option value="K">Kicker</option>
          <option value="DEF">Defense</option>
        </select>
      </div>

      {/* Player List */}
      <div className="overflow-y-auto max-h-96">
        {filteredPlayers.length === 0 ? (
          <div className="text-sm text-gray-500 text-center py-4">No players found</div>
        ) : (
          <ul className="space-y-1">
            {filteredPlayers.slice(0, 50).map((player) => (
              <li key={player.player_id}>
                <button
                  onClick={() => onPlayerSelect(player.player_id)}
                  className={`w-full text-left px-3 py-2 rounded hover:bg-gray-100 transition-colors ${
                    selectedPlayer === player.player_id ? 'bg-primary text-white' : ''
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">{player.name}</span>
                    <span className="text-xs text-gray-500">
                      {player.position} {player.team ? `· ${player.team}` : ''}
                    </span>
                  </div>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default PlayerSearch;

