# Fantasy Football Player Stock Visualization - Detailed Implementation Plan

## Executive Summary

This document outlines the complete implementation plan for a fantasy football player visualization tool that displays weekly point totals as stock prices, with projected points as dotted lines and color-coded performance gaps (green for exceeding, red for underperforming).

## Market Mechanics

### Market Timing
- **Market Opens**: Monday/Tuesday when weekly projections become available
- **Market Closes**: Sunday morning before the first game
- **Thursday Night Exception**: Players who played Thursday have their market close Thursday night
- **Data Type**: Current week projections (what was available at market open), NOT future week projections

### Key Concepts
- **Stock Price**: Player's current weekly point total (PPR)
- **Projected Line**: Dotted line showing what was projected for the current week
- **Fill Areas**: 
  - Green when actual > projected (over-performance)
  - Red when actual < projected (under-performance)
- **Historical Data**: Shows past weeks' performance vs projections

## Technical Architecture

### Backend (Python Flask)

#### Data Flow
1. Fetch current week number from Sleeper API
2. Get player historical stats (weeks 1 through current-1)
3. Get player projections for current week (snapshot at market open)
4. Calculate PPR points from raw NFL stats
5. Serve data to frontend via REST API

#### Core Modules

**1. Sleeper API Client (`backend/data/sleeper_client.py`)**
- Purpose: Interface with Sleeper Fantasy API
- **Rate Limit**: 1000 calls/minute (must implement throttling)
- Key Methods:
  - `get_current_week()`: Determine current NFL week
  - `get_player_historical_stats(player_id, season, week)`: Get actual points scored
  - `get_player_projection(player_id, week)`: Get projected points for a week
  - `get_historical_projections(season, week)`: Get old projections from Sleeper
  - `get_all_nfl_players()`: Fetch player master list
- Data Source: `https://api.sleeper.app/v1`
- Caching Strategy: Cache responses for 5 minutes to reduce API calls

**1b. ESPN API Client (`backend/data/espn_client.py`)** [NEW]
- Purpose: Fallback projection source when Sleeper unavailable
- Key Methods:
  - `get_projections(player_id, week)`: Fetch ESPN projections
  - `convert_to_sleeper_format(espn_data)`: Convert ESPN data to unified format
- Authentication: May require API key depending on endpoint

**2. PPR Calculator (`backend/data/ppr_calculator.py`)**
- Purpose: Calculate full PPR points from raw NFL stats
- Scoring Rules (Full PPR):
  - Passing Yards: 1 point per 25 yards
  - Passing TDs: 6 points
  - Interceptions: -2 points
  - Rushing Yards: 1 point per 10 yards
  - Rushing TDs: 6 points
  - Receptions: 1 point
  - Receiving Yards: 1 point per 10 yards
  - Receiving TDs: 6 points
  - Fumbles Lost: -2 points
  - 2PT Conversions: 2 points
- Method: `calculate_ppr_points(raw_stats)` - Takes dict of stats, returns total PPR points

**3. Projection Service (`backend/data/projection_service.py`)**
- Purpose: Handle projection retrieval and caching
- Strategy:
  - Snapshot projections Monday/Tuesday when available
  - Store in database with week number and timestamp
  - Use cached projections for rest of week
- Data Sources:
  - **Primary**: Sleeper API historical projections via `/projections/nfl/<season>/<week>`
  - **Fallback**: ESPN API when Sleeper unavailable
- Methods:
  - `get_current_week_projection(player_id)`: Returns projection for current open week
  - `get_historical_projection(player_id, season, week)`: Fetch old projections from Sleeper
  - `snapshot_projections(week)`: Fetch and store all projections for a week
  - `get_espn_projections(player_id, week)`: Fetch ESPN projections as fallback
  - `is_market_open()`: Check if market should be open based on day and time

**4. Data Models (`backend/models/player.py`)**
- `PlayerStats`: Represents a single week's stats
  - Attributes: week, actual_points, projected_points, stats_dict
  - Methods: calculate_ppr_from_stats()
- `Player`: Represents a player across multiple weeks
  - Attributes: player_id, name, position, team, weekly_stats[]
  - Methods: get_season_average(), get_weekly_performance()
- `MarketStatus`: Represents current market state
  - Attributes: is_open, current_week, lock_times{}, eligible_players[]

**5. API Endpoints (`backend/app.py`)**
- `GET /api/current-week` - Return current week number
- `GET /api/players` - List all available players
- `GET /api/players/:id/stats` - Get player's weekly stats + projections
- `GET /api/players/:id/current-projection` - Get projection for current week
- `GET /api/market-status` - Check if market is open, locked players
- `GET /api/week-projections/:week` - Get all projections for a specific week
- `GET /api/realtime/:player_id` - Get live scoring during game (NEW)
- `WS /api/live-updates` - WebSocket endpoint for real-time updates (NEW)

**6. Real-Time Update Service (`backend/data/realtime_service.py`)** [NEW]
- Purpose: Handle live scoring updates during games
- Strategy:
  - Poll Sleeper API every 30 seconds for live stats
  - Use WebSocket for frontend push updates
  - Cache live data to prevent duplicate API calls
- Methods:
  - `get_live_stats(player_id)`: Fetch current game stats
  - `is_game_live(player_id)`: Check if player's game is in progress
  - `calculate_live_ppr(live_stats)`: Calculate PPR from live stats

#### Database Schema (SQLite or PostgreSQL)

**players table**
- player_id (PK)
- name
- position
- team
- sleeper_id (unique)
- created_at
- updated_at

**weekly_stats table**
- id (PK)
- player_id (FK)
- season
- week
- actual_points (calculated PPR)
- projected_points
- stats_json (raw stats from Sleeper)
- timestamp

**projections table**
- id (PK)
- player_id (FK)
- season
- week
- projected_points
- snapshot_time (when projection was captured)
- data_source

**user_portfolio table** (for buy/sell tracking)
- id (PK)
- player_id (FK)
- position (buy/sell)
- entry_price (points at time of entry)
- exit_price (points at time of exit)
- timestamp

### Frontend (React + TypeScript)

#### Core Components

**1. MarketStatus Bar (`frontend/src/components/MarketStatus.tsx`)**
- Display current week
- Show market open/closed status
- List locked players (Thursday players)
- Style: Status bar at top

**2. PlayerSearch/Filter (`frontend/src/components/PlayerSearch.tsx`)**
- Search by player name
- Filter by position (QB, RB, WR, TE, etc.)
- Filter by team
- Sort options
- Style: Sidebar or top bar

**3. StockChart Component (`frontend/src/components/StockChart.tsx`)**
- Library: Recharts
- Chart Type: Area Chart with dual lines
- Features:
  - Solid line: Actual weekly points
  - Dotted line: Projected points
  - Green fill: When actual > projected (area below)
  - Red fill: When actual < projected (area above)
  - Hover tooltip with detailed stats
  - Zoom/pan functionality
  - X-axis: Week numbers
  - Y-axis: PPR Points
- Extend dotted line one week into future
- For locked players, show final data without extending

**4. PortfolioTracker (`frontend/src/components/PortfolioTracker.tsx`)**
- Track "bought" players
- Track "sold" players
- Calculate P/L based on price movements
- Show total portfolio value

**5. ChartControls (`frontend/src/components/ChartControls.tsx`)**
- Compare multiple players (tabs or overlay)
- Toggle between season view and weekly zoom
- Export chart as image
- Adjust date range

#### Services

**API Service (`frontend/src/services/api.ts`)**
- Base URL configuration
- Methods:
  - `getCurrentWeek()`
  - `getPlayers(filters?)`
  - `getPlayerStats(playerId)`
  - `getMarketStatus()`
  - `getProjections(week)`

**State Management**
- Context API or Redux for:
  - Selected player
  - Market data
  - User portfolio
  - Chart preferences

#### Styling
- Framework: Tailwind CSS
- Theme: Modern, clean financial dashboard style
- Color Scheme:
  - Green: #10B981 (success/over-performance)
  - Red: #EF4444 (failure/under-performance)
  - Primary: #3B82F6 (blue)
  - Background: #F9FAFB (light gray)
  - Text: #111827 (dark gray)

## Implementation Phases

### Phase 1: Backend Data Pipeline
1. Implement Sleeper API client
2. Implement PPR calculator with full PPR scoring
3. Create database schema and models
4. Build projection snapshotting system
5. Create API endpoints for data retrieval
6. Add market status logic (open/closed/Thursday locks)

### Phase 2: Frontend Shell
1. Set up React + TypeScript project
2. Install and configure Recharts
3. Create basic layout and routing
4. Implement MarketStatus component
5. Implement PlayerSearch component
6. Create basic stock chart structure

### Phase 3: Visualization
1. Implement dual-line area chart (actual + projected)
2. Add color-coded fill areas (green/red)
3. Extend projected line one week ahead
4. Add hover tooltips
5. Implement zoom and pan
6. Add Thursday player lock logic

### Phase 4: Portfolio System
1. Implement buy/sell tracking
2. Create portfolio component
3. Calculate P/L based on point changes
4. Add transaction history
5. Display total portfolio value

### Phase 5: Polish & Testing
1. Responsive design for mobile
2. Error handling and loading states
3. Performance optimization
4. Add keyboard shortcuts
5. Write unit tests
6. End-to-end testing

## Data Retrieval Strategy

### Current Week Projections

**Problem**: Need to capture projections at market open (Monday/Tuesday) and display throughout the week

**Solution**:
1. Run daily cron job Monday morning
2. Query for latest projections from Sleeper
3. Store in `projections` table with:
   - `week` (current week number)
   - `snapshot_time` (Monday AM timestamp)
   - `projected_points`
4. Display cached projections all week
5. Don't update projections during the week (they represent "market opening" price)

### Historical Data

For any week in the past:
1. Query `weekly_stats` table
2. Find matching projection from `projections` table for same week
3. Return actual vs projected comparison

### Getting Actual Points

Sleeper API endpoint:
```
GET https://api.sleeper.app/v1/stats/nfl/{season}/{week}
```

Response format:
```json
{
  "player_id": {
    "passing_yds": 350,
    "passing_tds": 3,
    "passing_int": 1,
    "rushing_yds": 25,
    "rushing_tds": 0,
    "receptions": 0,
    "receiving_yds": 0,
    "receiving_tds": 0,
    "fumbles_lost": 0
  }
}
```

Convert to PPR points using scoring rules.

## Key Technical Decisions

### Why Full PPR?
- Standard scoring format across leagues
- Receptions provide consistent baseline value
- Makes projections more stable

### Why Snapshot Projections?
- Shows what the "market" thought at market open
- Fair comparison for all players
- Consistent data throughout the week

### Why One Week Ahead Extension?
- Visualizes future projection
- Helps users make buy/sell decisions
- Shows trend direction

### Market Lock Logic
```python
def is_player_locked(player_id, current_time, current_week):
    player = get_player(player_id)
    
    # Check if player is on bye week
    if player.bye_week == current_week:
        return True
    
    # Check if player is injured and OUT
    if player.injury_status in ['O', 'IR', 'Out']:
        return True
    
    # Check if Thursday game has started
    if is_thursday_gametime(current_time) and player.in_thursday_game():
        return True
    
    # Check if player's game has started
    if is_game_started(player.next_game_time, current_time):
        return True
        
    return False
```

### Lock Condition Summary
- **Bye Week**: Player price locked, no projection, flat line on chart
- **Injury (OUT/IR)**: Player price locked, show injury indicator, flat line on chart
- **Thursday Game**: Lock 5 minutes before game start (8:20 PM ET)
- **Sunday Game**: Lock when individual game starts
- **Market Close**: All remaining players lock Sunday 1 PM ET

## Resolved Questions

1. **Historical Projections**: ✅ Sleeper API provides historical projections via `/projections/nfl/<season>/<week>` endpoint. We can retrieve old projections from Sleeper's database. Fallback: Calculate season average if not available.

2. **Multiple Data Sources**: ✅ YES - ESPN projections are approved as alternative/fallback when Sleeper projections unavailable. Will need ESPN API integration.

3. **Player Injuries**: ✅ When player has OUT status, their stock price is LOCKED for that week. No price change, chart shows flat line. Same applies to IR (Injured Reserve) status.

4. **Bye Weeks**: ✅ Player price is LOCKED during bye week. Chart shows flat line continuation from previous week to next week. No data point for bye week.

5. **Rate Limiting**: ✅ Sleeper API limit = **1000 calls/minute**. Implement request throttling and caching layer.

6. **Real-time Updates**: ✅ YES - Real-time points should update during Sunday games. Use WebSocket or polling (every 30 seconds) to update live scores.

## Updated Requirements Summary

### Data Sources
- **Primary**: Sleeper API (historical and current projections)
- **Fallback**: ESPN API for projections
- **Rate Limit**: 1000 API calls/minute (must implement throttling)

### Lock Conditions
- **Bye Week**: Lock stock price (chart shows flat line, no data point)
- **Injury (OUT/IR)**: Lock stock price (chart shows flat line, display injury indicator)
- **Thursday Game**: Lock player at 8:20 PM Thursday before game
- **Sunday Game**: Lock player when their game starts

### Real-Time Features
- Live scoring updates every 30 seconds during games
- WebSocket connection to Sleeper API for real-time updates
- Chart animates smoothly as points update
- "Live" indicator shown during active games

### Market Status Indicators
- Show locked players with red badge
- Show BYE week in chart tooltip
- Show injury status in player card
- Display last updated timestamp for live data

## Next Steps

1. Review this plan with team
2. Confirm tech stack choices
3. Set up development environment
4. Begin Phase 1 implementation
5. Test with sample data

---

**Status**: Planning Complete - Ready for Review

