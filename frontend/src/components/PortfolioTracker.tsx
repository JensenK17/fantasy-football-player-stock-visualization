import React from 'react';

interface Position {
  playerId: string;
  playerName: string;
  action: 'buy' | 'sell';
  entryPrice: number;
  exitPrice?: number;
  timestamp: Date;
}

interface PortfolioTrackerProps {
  positions: Position[];
  currentWeek: number;
}

const PortfolioTracker: React.FC<PortfolioTrackerProps> = ({ positions, currentWeek }) => {
  const totalPL = positions.reduce((sum, pos) => {
    if (pos.action === 'buy' && pos.exitPrice) {
      return sum + (pos.exitPrice - pos.entryPrice);
    }
    return sum;
  }, 0);

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h2 className="text-xl font-semibold mb-4">Portfolio</h2>
      
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Total P/L:</span>
          <span className={`font-bold ${totalPL >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {totalPL > 0 ? '+' : ''}{totalPL.toFixed(2)} points
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Active Positions:</span>
          <span className="font-semibold">{positions.filter(p => !p.exitPrice).length}</span>
        </div>
      </div>

      {positions.length > 0 ? (
        <div className="mt-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Recent Transactions</h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {positions.slice(-5).map((pos, index) => (
              <div key={index} className="text-sm p-2 bg-gray-50 rounded">
                <div className="flex justify-between">
                  <span className="font-medium">{pos.playerName}</span>
                  <span className={pos.action === 'buy' ? 'text-green-600' : 'text-red-600'}>
                    {pos.action.toUpperCase()}
                  </span>
                </div>
                <div className="text-xs text-gray-500">
                  Entry: {pos.entryPrice.toFixed(1)} pts
                  {pos.exitPrice && ` → Exit: ${pos.exitPrice.toFixed(1)} pts`}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="mt-4 text-sm text-gray-500 text-center py-4">
          No portfolio positions yet
        </div>
      )}
    </div>
  );
};

export default PortfolioTracker;
