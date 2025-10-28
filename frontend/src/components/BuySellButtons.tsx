import React from 'react';

interface BuySellButtonsProps {
  playerName: string;
  currentPrice: number;
  isMarketOpen: boolean;
  isLocked: boolean;
  onBuy: () => void;
  onSell: () => void;
}

const BuySellButtons: React.FC<BuySellButtonsProps> = ({
  playerName,
  currentPrice,
  isMarketOpen,
  isLocked,
  onBuy,
  onSell
}) => {
  const handleBuy = () => {
    if (confirm(`Buy ${playerName} at ${currentPrice.toFixed(2)} points?`)) {
      onBuy();
    }
  };

  const handleSell = () => {
    if (confirm(`Sell ${playerName} position?`)) {
      onSell();
    }
  };

  return (
    <div className="flex gap-4 mt-4">
      <button
        onClick={handleBuy}
        disabled={!isMarketOpen || isLocked}
        className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-colors ${
          isMarketOpen && !isLocked
            ? 'bg-green-600 hover:bg-green-700 text-white'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        {isLocked ? '🚫 Locked' : isMarketOpen ? `💰 Buy at ${currentPrice.toFixed(1)} pts` : 'Market Closed'}
      </button>
      
      <button
        onClick={handleSell}
        disabled={!isMarketOpen || isLocked}
        className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-colors ${
          isMarketOpen && !isLocked
            ? 'bg-red-600 hover:bg-red-700 text-white'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        {isLocked ? '🚫 Locked' : isMarketOpen ? `📉 Sell at ${currentPrice.toFixed(1)} pts` : 'Market Closed'}
      </button>
    </div>
  );
};

export default BuySellButtons;

