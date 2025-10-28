import { useState, useEffect } from 'react';

export interface Position {
  id: string;
  playerId: string;
  playerName: string;
  action: 'buy' | 'sell';
  entryPrice: number;
  exitPrice?: number;
  entryTimestamp: Date;
  exitTimestamp?: Date;
}

export interface PortfolioHook {
  positions: Position[];
  addPosition: (playerId: string, playerName: string, action: 'buy' | 'sell', price: number) => void;
  closePosition: (positionId: string, exitPrice: number) => void;
  totalPL: number;
  activePositions: Position[];
}

export const usePortfolio = (): PortfolioHook => {
  const [positions, setPositions] = useState<Position[]>([]);

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('portfolio');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setPositions(parsed.map((p: any) => ({
          ...p,
          entryTimestamp: new Date(p.entryTimestamp),
          exitTimestamp: p.exitTimestamp ? new Date(p.exitTimestamp) : undefined
        })));
      } catch (e) {
        console.error('Failed to load portfolio:', e);
      }
    }
  }, []);

  // Save to localStorage whenever positions change
  useEffect(() => {
    if (positions.length > 0) {
      localStorage.setItem('portfolio', JSON.stringify(positions));
    }
  }, [positions]);

  const addPosition = (playerId: string, playerName: string, action: 'buy' | 'sell', price: number) => {
    const newPosition: Position = {
      id: `${playerId}-${Date.now()}`,
      playerId,
      playerName,
      action,
      entryPrice: price,
      entryTimestamp: new Date()
    };

    setPositions(prev => [...prev, newPosition]);
  };

  const closePosition = (positionId: string, exitPrice: number) => {
    setPositions(prev =>
      prev.map(pos =>
        pos.id === positionId && !pos.exitPrice
          ? {
              ...pos,
              exitPrice,
              exitTimestamp: new Date()
            }
          : pos
      )
    );
  };

  const totalPL = positions.reduce((sum, pos) => {
    if (pos.action === 'buy' && pos.exitPrice) {
      return sum + (pos.exitPrice - pos.entryPrice);
    }
    return sum;
  }, 0);

  const activePositions = positions.filter(pos => !pos.exitPrice);

  return {
    positions,
    addPosition,
    closePosition,
    totalPL,
    activePositions
  };
};

