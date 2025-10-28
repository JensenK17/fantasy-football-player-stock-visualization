# Fantasy Football Player Stock Visualization - Research

## Visualization Techniques

### Stock-Like Chart Recommendations

Based on research, the following visualization techniques are suitable for this project:

1. **Line Chart with Filled Areas** (Recommended)
   - Plot actual weekly points as a solid line
   - Plot projected points as a dotted line extending one week into the future
   - Fill the area between lines:
     - Green when actual > projected (over-performance)
     - Red when actual < projected (under-performance)
   - This approach is intuitive and clearly shows player value trends

2. **Alternative: Candlestick Charts**
   - Could represent weekly point ranges
   - More complex, less suitable for this simple projection comparison

### Implementation Libraries

- **Chart.js**: Simple, easy to use, good for basic line charts with area fills
- **D3.js**: More powerful, full customization, steeper learning curve
- **Plotly**: Good for interactive charts with built-in area fills
- **Recharts**: React-specific, component-based, modern approach

**Recommendation**: Start with **Recharts** if using React, or **Plotly** for a standalone solution.

## Sleeper API Research

### API Overview

Base URL: `https://api.sleeper.app/v1/`

### Key Endpoints

1. **Get All Players**
   ```
   GET https://api.sleeper.app/v1/players/nfl
   ```
   - Returns JSON object with all NFL players
   - Key: player_id, Value: player object with stats

2. **Get League Info**
   ```
   GET https://api.sleeper.app/v1/league/{league_id}
   ```
   - Returns league settings, scoring rules, roster settings

3. **Get Roster Stats (Historical)**
   ```
   GET https://api.sleeper.app/v1/stats/nfl/{season}/{week}
   ```
   - Returns player stats for a specific week
   - Includes points scored

4. **Get User Leagues**
   ```
   GET https://api.sleeper.app/v1/user/{user_id}/leagues/{sport}/{season}
   ```
   - Returns leagues for a user in a given season

### Data Retrieval Approach

1. **Authentication**: No API key required for most endpoints
2. **Rate Limiting**: Unknown, but should implement rate limiting in code
3. **Data Availability**:
   - Historical stats for completed weeks
   - Player information and stats
   - Projection data may require additional sources or manual entry

### Challenges

1. **Projections**: Sleeper API may not provide forward-looking projections
   - May need to source from ESPN, Yahoo, or NFL.com
   - Or implement a simple projection algorithm based on season averages
   
2. **Scoring**: League-specific scoring rules need to be considered
   - Custom scoring settings vary by league
   - Need to handle standard vs PPR vs half-PPR

### Python Wrapper Options

1. **sleeper-api-wrapper** (PyPI)
   - Object-oriented interface
   - Simplifies API interactions

2. **sleeper-fantasy-api** (PyPI)
   - Alternative wrapper with different features

## Project Architecture Options

### Option 1: Python Backend + Web Frontend
- Backend: Flask/FastAPI with Sleeper API integration
- Frontend: React/Vue with Chart.js/Plotly/Recharts
- Pros: Separation of concerns, scalable
- Cons: More complex setup

### Option 2: Full-Stack JavaScript
- Backend: Node.js/Express
- Frontend: React/Vue with visualization library
- Pros: Single language, consistent codebase
- Cons: May need to write Sleeper API client from scratch

### Option 3: Static Site with API Calls
- Frontend only: Vanilla JS or React
- Direct API calls to Sleeper API
- Pros: Simple, fast to deploy
- Cons: CORS issues, limited backend processing

## Data Model

### Player Data Structure

```json
{
  "player_id": "1234",
  "name": "Patrick Mahomes",
  "position": "QB",
  "team": "KC",
  "weekly_points": [
    {
      "week": 1,
      "actual": 25.3,
      "projected": 24.5,
      "opponent": "HOU"
    },
    {
      "week": 2,
      "actual": 28.7,
      "projected": 25.0,
      "opponent": "LAC"
    }
  ],
  "season_avg": 26.5,
  "current_stock": 26.5
}
```

## Recommendations

1. **Tech Stack**: React + Flask/Python Backend
   - Leverage Python wrappers for Sleeper API
   - React provides modern, interactive UI
   - Recharts for visualization

2. **Data Source**: 
   - Sleeper API for historical data
   - Consider ESPN or Yahoo for projections
   - Or calculate simple projections based on season averages

3. **Features to Include**:
   - Player search and selection
   - Week-by-week view with zoom/pan
   - Stock "price" calculation (could be season average, or market-value equivalent)
   - Buy/Sell simulation (track hypothetical positions)
   - Multi-player comparison

4. **Future Enhancements**:
   - Export charts as images
   - Historical season data
   - Mobile-responsive design
   - User authentication for saving portfolios


