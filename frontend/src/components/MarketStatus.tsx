import React from 'react';

interface MarketStatusProps {
  currentWeek: number;
  isMarketOpen: boolean;
  lockedPlayers: string[];
  timeUntilClose?: string;
}

const MarketStatus: React.FC<MarketStatusProps> = ({ 
  currentWeek, 
  isMarketOpen, 
  lockedPlayers,
  timeUntilClose 
}) => {
  return (
    <div className="bg-gray-100 border-b border-gray-200 px-4 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-600">Week:</span>
            <span className="text-lg font-bold text-gray-900">{currentWeek}</span>
          </div>
          
          <div className="flex items-center gap-2">
            {isMarketOpen ? (
              <>
                <span className="flex h-3 w-3 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                </span>
                <span className="text-sm font-semibold text-green-700">Market Open</span>
              </>
            ) : (
              <>
                <span className="flex h-3 w-3 bg-red-500 rounded-full"></span>
                <span className="text-sm font-semibold text-red-700">Market Closed</span>
              </>
            )}
          </div>
        </div>

        {isMarketOpen && timeUntilClose && (
          <div className="text-sm text-gray-600">
            <span className="font-medium">Closes in:</span> {timeUntilClose}
          </div>
        )}

        {lockedPlayers.length > 0 && (
          <div className="text-sm text-gray-600">
            <span className="font-medium">{lockedPlayers.length}</span> players locked
          </div>
        )}
      </div>
    </div>
  );
};

export default MarketStatus;
