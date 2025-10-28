import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface PlayerStats {
  player_id: string;
  name: string;
  position: string;
  team?: string;
  weekly_stats: WeeklyStat[];
  season_average: number;
}

interface WeeklyStat {
  week: number;
  actual: number;
  projected: number;
  diff: number;
}

interface StockChartProps {
  playerData: PlayerStats;
  isMarketOpen: boolean;
  currentWeek: number;
}

const StockChart: React.FC<StockChartProps> = ({ playerData, isMarketOpen, currentWeek }) => {
  // Transform data for chart with performance fills
  const chartData = playerData.weekly_stats.map((stat, index) => {
    const actual = stat.actual;
    const projected = stat.projected || 0;
    const diff = actual - projected;
    
    return {
      week: `Week ${stat.week}`,
      actual: actual,
      projected: projected,
      over: diff > 0 ? Math.abs(diff) : 0,  // Green fill area
      under: diff < 0 ? Math.abs(diff) : 0,  // Red fill area
      // For future projection display
      projectedFuture: index === playerData.weekly_stats.length - 1 && isMarketOpen ? projected : undefined
    };
  });

  return (
    <div className="stock-chart-container">
      <h2 className="text-xl font-semibold mb-4">{playerData.name}</h2>
      
      {chartData.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No data available for this player
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis dataKey="week" stroke="#6B7280" />
            <YAxis label={{ value: 'PPR Points', angle: -90, position: 'insideLeft' }} stroke="#6B7280" />
            <Tooltip 
              contentStyle={{ backgroundColor: 'white', border: '1px solid #E5E7EB', borderRadius: '6px' }}
              formatter={(value: any, name: string) => {
                if (name === 'over' || name === 'under') return null;
                return [value.toFixed(2), name];
              }}
            />
            <Legend />
            
            {/* Red fill for under-performance */}
            <Area
              type="monotone"
              dataKey="under"
              stackId="under"
              stroke="none"
              fill="#EF4444"
              fillOpacity={0.3}
              name="Under Projection"
            />
            
            {/* Green fill for over-performance */}
            <Area
              type="monotone"
              dataKey="over"
              stackId="over"
              stroke="none"
              fill="#10B981"
              fillOpacity={0.3}
              name="Over Projection"
            />
            
            {/* Projected Points (dotted line) */}
            <Area
              type="monotone"
              dataKey="projected"
              stroke="#3B82F6"
              strokeDasharray="5 5"
              fill="none"
              strokeWidth={2}
              name="Projected"
              dot={{ fill: '#3B82F6', r: 3 }}
            />
            
            {/* Actual Points (solid line) */}
            <Area
              type="monotone"
              dataKey="actual"
              stroke="#111827"
              fill="#111827"
              fillOpacity={0.6}
              strokeWidth={2}
              name="Actual"
              dot={{ fill: '#111827', r: 3 }}
            />
            
            {/* Future Projection (if market open) */}
            {isMarketOpen && chartData.length > 0 && chartData[chartData.length - 1].projectedFuture && (
              <Area
                type="monotone"
                dataKey="projectedFuture"
                stroke="#3B82F6"
                strokeDasharray="5 5"
                fill="none"
                strokeWidth={2}
                name="Next Week Projection"
              />
            )}
          </AreaChart>
        </ResponsiveContainer>
      )}
      
      {/* Player Info */}
      <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
        <div className="bg-gray-50 px-3 py-2 rounded">
          <span className="text-gray-600">Position: </span>
          <span className="font-semibold text-gray-900">{playerData.position}</span>
        </div>
        <div className="bg-gray-50 px-3 py-2 rounded">
          <span className="text-gray-600">Team: </span>
          <span className="font-semibold text-gray-900">{playerData.team || 'N/A'}</span>
        </div>
        <div className="bg-gray-50 px-3 py-2 rounded">
          <span className="text-gray-600">Season Avg: </span>
          <span className="font-semibold text-gray-900">{playerData.season_average.toFixed(1)}</span>
        </div>
      </div>
      
      {/* Performance Summary */}
      {playerData.weekly_stats.length > 0 && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Season Performance</h3>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Weeks: </span>
              <span className="font-semibold">{playerData.weekly_stats.length}</span>
            </div>
            <div>
              <span className="text-gray-600">Avg vs Proj: </span>
              <span className={`font-semibold ${
                playerData.season_average > 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {playerData.season_average > 0 ? '+' : ''}{playerData.season_average.toFixed(1)}
              </span>
            </div>
            <div>
              <span className="text-gray-600">Best Week: </span>
              <span className="font-semibold text-green-600">
                {Math.max(...playerData.weekly_stats.map(s => s.actual)).toFixed(1)}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockChart;
