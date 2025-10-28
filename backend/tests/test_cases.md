# Test Cases - Fantasy Football Player Stock Visualization

## Overview

This document defines comprehensive test cases for validating the functionality of the fantasy football player stock visualization system. These tests will be implemented in Phase 5 of development.

## Testing Framework

- **Backend**: pytest for Python unit and integration tests
- **Frontend**: Jest + React Testing Library for component tests
- **E2E**: Playwright or Cypress for end-to-end tests

---

## Category 1: Data Retrieval and Processing

### TC-001: PPR Scoring Calculation - Passing Stats
**Description**: Verify correct PPR calculation for passing statistics  
**Input**:  
```json
{
  "passing_yds": 350,
  "passing_tds": 3,
  "passing_int": 1
}
```
**Expected Output**: `(350/25) + (3*6) + (-1*2) = 14 + 18 - 2 = 30.0 points`  
**Priority**: HIGH

### TC-002: PPR Scoring Calculation - Receiving Stats (Full PPR)
**Description**: Verify full PPR adds 1 point per reception  
**Input**:
```json
{
  "receptions": 8,
  "receiving_yds": 120,
  "receiving_tds": 1
}
```
**Expected Output**: `8 + (120/10) + (1*6) = 8 + 12 + 6 = 26.0 points`  
**Priority**: HIGH

### TC-003: PPR Scoring Calculation - Rushing Stats
**Description**: Verify rushing statistics calculation  
**Input**:
```json
{
  "rushing_yds": 85,
  "rushing_tds": 2
}
```
**Expected Output**: `(85/10) + (2*6) = 8.5 + 12 = 20.5 points`  
**Priority**: HIGH

### TC-004: PPR Scoring - Edge Cases
**Description**: Test zero stats, negative stats, fumbles  
**Input**:
```json
{
  "receptions": 0,
  "fumbles_lost": 1,
  "passing_int": 0
}
```
**Expected Output**: `-2.0 points`  
**Priority**: MEDIUM

### TC-005: Fetch Historical Player Stats from Sleeper
**Description**: Verify retrieval of past week stats  
**Preconditions**: Valid player_id, season=2023, week=1  
**Expected Behavior**: Returns dict with actual_points calculated  
**Assertions**: 
- Response contains player_id, week, actual_points
- actual_points > 0
- data matches Sleeper API format
**Priority**: HIGH

### TC-006: Fetch Current Week Projections from Sleeper
**Description**: Verify projection retrieval  
**Preconditions**: Current week is week 5  
**Expected Behavior**: Returns projections for all players for week 5  
**Assertions**:
- Projections exist for QB, RB, WR, TE positions
- Projected points are positive numbers
- Timestamp shows Monday/Tuesday snapshot
**Priority**: HIGH

### TC-007: ESPN Projections as Fallback
**Description**: Use ESPN API when Sleeper projections unavailable  
**Preconditions**: Sleeper API returns no projections  
**Expected Behavior**: Queries ESPN API and returns projections  
**Assertions**:
- ESPN data converted to same format as Sleeper
- Scoring system matches full PPR
**Priority**: MEDIUM

### TC-008: Historical Projections Retrieval
**Description**: Retrieve old projections from Sleeper  
**Preconditions**: Season 2022, Week 12  
**Expected Behavior**: Returns projections stored at time of that week  
**Assertions**:
- Projections match historical data
- Snapshot timestamp is from that week's Monday
**Priority**: HIGH

### TC-009: Rate Limiting - 1000 Calls/Minute
**Description**: Verify API calls stay within limit  
**Preconditions**: Multiple concurrent requests  
**Expected Behavior**: Max 1000 API calls per minute  
**Assertions**:
- Request counter increments correctly
- Throttling applied when limit reached
- Appropriate error returned
**Priority**: HIGH

---

## Category 2: Market Mechanics

### TC-010: Market Open Monday Morning
**Description**: Market opens when projections available  
**Preconditions**: Current day is Monday, time is 9:00 AM  
**Expected Behavior**: Market status = OPEN  
**Assertions**:
- is_market_open = True
- Projections snapshot taken
- All players available for trading
**Priority**: HIGH

### TC-011: Market Closed Sunday Morning
**Description**: Market closes before Sunday games  
**Preconditions**: Current day is Sunday, time is 12:00 PM  
**Expected Behavior**: Market status = CLOSED  
**Assertions**:
- is_market_open = False
- No new trades allowed
- Existing positions locked
**Priority**: HIGH

### TC-012: Thursday Players Lock During Game
**Description**: Thursday night players lock before game starts  
**Preconditions**: Player has Thursday game, game starts at 8:20 PM  
**Expected Behavior**: Player locked at 8:15 PM  
**Assertions**:
- locked_players list contains player_id
- Cannot buy/sell locked player
**Priority**: HIGH

### TC-013: Bye Week Player Price Lock
**Description**: Player on bye week - price locked  
**Preconditions**: Player has bye week, current week = bye week  
**Expected Behavior**: Stock price remains last week's value  
**Assertions**:
- No price change for that week
- Chart shows flat line at bye week
- Tooltip indicates "BYE"
**Priority**: HIGH

### TC-014: Injured Player Price Lock
**Description**: Injured player (OUT status) price locked  
**Preconditions**: Player has injury status = "O" (Out)  
**Expected Behavior**: Stock price locked, no projection shown  
**Assertions**:
- Price doesn't change during injury
- Chart shows flat line
- Market status shows player as locked
**Priority**: HIGH

### TC-015: Questionable Player Trading
**Description**: Player with Q (Questionable) status can trade  
**Preconditions**: Player injury status = "Q"  
**Expected Behavior**: Market open for player, warning shown  
**Assertions**:
- is_locked = False
- Warning banner displayed
- User can still buy/sell
**Priority**: MEDIUM

---

## Category 3: Visualization Output

### TC-016: Stock Chart Renders with Data
**Description**: Chart displays with actual data points  
**Preconditions**: Valid player with 5 weeks of data  
**Expected Behavior**: Chart shows line with 5 data points  
**Assertions**:
- X-axis shows week numbers
- Y-axis shows PPR points
- Line connects all data points
**Priority**: HIGH

### TC-017: Dual Line Display (Actual + Projected)
**Description**: Both lines render correctly  
**Preconditions**: Player has actual and projected points  
**Expected Behavior**: Solid line (actual) + dotted line (projected)  
**Assertions**:
- Two distinct line styles
- Projected line extends 1 week ahead
- Colors distinct (e.g., blue solid, orange dashed)
**Priority**: HIGH

### TC-018: Green Fill - Over Performance
**Description**: Area filled green when actual > projected  
**Preconditions**: Actual=25.3, Projected=22.0  
**Expected Behavior**: Green fill between lines  
**Assertions**:
- Fill color is green (#10B981)
- Fill appears above projected line
- Hover shows +3.3 difference
**Priority**: HIGH

### TC-019: Red Fill - Under Performance
**Description**: Area filled red when actual < projected  
**Preconditions**: Actual=15.2, Projected=20.0  
**Expected Behavior**: Red fill between lines  
**Assertions**:
- Fill color is red (#EF4444)
- Fill appears above actual line
- Hover shows -4.8 difference
**Priority**: HIGH

### TC-020: Empty State - No Data
**Description**: Chart handles missing data gracefully  
**Preconditions**: Player has no stats yet  
**Expected Behavior**: Shows "No data available" message  
**Assertions**:
- Chart component renders
- Message displayed
- No errors in console
**Priority**: MEDIUM

### TC-021: Bye Week Visualization
**Description**: Chart shows flat line during bye week  
**Preconditions**: Week 6 is bye week  
**Expected Behavior**: No data point, line continues from week 5 to 7  
**Assertions**:
- Label shows "BYE" on hover
- Line doesn't have gap
- Tooltip indicates bye week
**Priority**: MEDIUM

### TC-022: Multiple Players Comparison
**Description**: Overlay multiple players on same chart  
**Preconditions**: 3 players selected  
**Expected Behavior**: 3 lines with different colors  
**Assertions**:
- Each line unique color
- Legend shows player names
- Lines don't overlap confusingly
**Priority**: MEDIUM

### TC-023: Tooltip Shows Correct Data
**Description**: Hover displays week, actual, projected, diff  
**Preconditions**: Hover over week 3 data point  
**Expected Behavior**: Tooltip shows "Week 3: Actual 22.5, Projected 20.0, Diff +2.5"  
**Assertions**:
- All values displayed
- Formatting clear
- Appears on hover
**Priority**: MEDIUM

### TC-024: Zoom and Pan Functionality
**Description**: User can zoom into specific week range  
**Preconditions**: 10 weeks of data, user zooms weeks 3-7  
**Expected Behavior**: Chart displays only weeks 3-7  
**Assertions**:
- X-axis adjusts
- All points in range visible
- Can pan left/right
**Priority**: LOW

---

## Category 4: Real-Time Updates

### TC-025: Real-Time Points Update During Game
**Description**: Points update as game progresses  
**Preconditions**: Player is playing, game in progress  
**Expected Behavior**: Chart updates live without refresh  
**Assertions**:
- WebSocket connection active
- Points increment in real-time
- No page reload required
**Priority**: MEDIUM

### TC-026: WebSocket Connection Handling
**Description**: Handle disconnection and reconnect  
**Preconditions**: Connection drops  
**Expected Behavior**: Reconnects automatically  
**Assertions**:
- Shows "Reconnecting..." message
- Data syncs after reconnect
- No data lost
**Priority**: MEDIUM

### TC-027: Live Stats Update Frequency
**Description**: Points update every 30 seconds  
**Preconditions**: Game is live  
**Expected Behavior**: API polls every 30s  
**Assertions**:
- Update timer running
- New data fetches periodically
- Chart animates smoothly
**Priority**: LOW

---

## Category 5: Portfolio and Trading

### TC-028: Buy Player Position
**Description**: User can buy a player at current price  
**Preconditions**: Market open, player price = 22.5  
**Expected Behavior**: Position created with entry_price = 22.5  
**Assertions**:
- Portfolio increases by 1
- Entry price recorded correctly
- Timestamp saved
**Priority**: HIGH

### TC-029: Sell Player Position
**Description**: User can sell player at current price  
**Preconditions**: Have bought player, price now = 26.0  
**Expected Behavior**: Position closed with exit_price = 26.0  
**Assertions**:
- Exit price recorded
- P/L calculated: +3.5 points
**Priority**: HIGH

### TC-030: P/L Calculation
**Description**: Calculates profit/loss correctly  
**Preconditions**: Bought at 20.0, sold at 25.0  
**Expected Behavior**: P/L = +5.0 points  
**Assertions**:
- Calculation: exit_price - entry_price
- Displays as "+5.0" in green
**Priority**: HIGH

### TC-031: Multiple Positions Tracking
**Description**: Track multiple buy/sell transactions  
**Preconditions**: Bought 3 different players  
**Expected Behavior**: Portfolio shows 3 positions  
**Assertions**:
- Each position separate
- Total value calculated
- Can sell individually
**Priority**: MEDIUM

### TC-032: Prevent Double Buying
**Description**: Can't buy player you already own  
**Preconditions**: Player already in portfolio  
**Expected Behavior**: Error message "Already own this player"  
**Assertions**:
- Button disabled
- Error displayed
**Priority**: MEDIUM

---

## Category 6: API Endpoints

### TC-033: GET /api/current-week Returns Correct Week
**Description**: Endpoint returns current NFL week  
**Expected Output**: `{"week": 5}`  
**Assertions**: Week number is 1-18  
**Priority**: HIGH

### TC-034: GET /api/players Returns All Players
**Description**: Endpoint returns player list  
**Expected Output**: Array of 500+ player objects  
**Assertions**:
- Contains player_id, name, position, team
- Sorted by name or position
**Priority**: HIGH

### TC-035: GET /api/players/:id/stats Returns Correct Data
**Description**: Returns player weekly stats  
**Expected Output**:
```json
{
  "player_id": "1234",
  "weekly_stats": [
    {"week": 1, "actual": 22.5, "projected": 20.0}
  ]
}
```
**Assertions**: Data complete and accurate  
**Priority**: HIGH

### TC-036: GET /api/market-status Returns Status
**Description**: Returns current market state  
**Expected Output**:
```json
{
  "current_week": 5,
  "is_market_open": true,
  "locked_players": []
}
```
**Assertions**: All fields present  
**Priority**: HIGH

### TC-037: POST /api/portfolio/buy Creates Position
**Description**: Creates buy transaction  
**Input**:
```json
{"player_id": "1234"}
```
**Expected Output**: `{"success": true, "position_id": "abc123"}`  
**Assertions**: Position saved in database  
**Priority**: HIGH

### TC-038: Error Handling - Invalid Player ID
**Description**: Returns 404 for invalid ID  
**Preconditions**: Player_id doesn't exist  
**Expected Behavior**: HTTP 404 status  
**Assertions**: Error message descriptive  
**Priority**: MEDIUM

### TC-039: Error Handling - Market Closed Transaction
**Description**: Rejects trades when market closed  
**Preconditions**: Market closed, attempt to buy  
**Expected Behavior**: HTTP 403 Forbidden  
**Assertions**: Error: "Market is closed"  
**Priority**: HIGH

---

## Category 7: Edge Cases

### TC-040: Player Has 0 Receptions (Passing Only)
**Description**: QB with no receiving stats  
**Preconditions**: QB passing only  
**Expected Behavior**: Chart shows passing points only  
**Assertions**: No errors, displays correctly  
**Priority**: LOW

### TC-041: D/ST Position Handling
**Description**: Defense scoring works correctly  
**Preconditions**: D/ST scored 12 points  
**Expected Behavior**: Chart displays correctly  
**Assertions**: Special scoring rules applied  
**Priority**: LOW

### TC-042: Data Missing for Multiple Weeks
**Description**: Missing stats for weeks 3-5  
**Expected Behavior**: Line continues, gaps shown  
**Assertions**: No crash, handles gracefully  
**Priority**: MEDIUM

### TC-043: Very High Scoring Week
**Description**: Player scores 50+ points  
**Preconditions**: 8 TDs, 500 total yards  
**Expected Behavior**: Chart scales appropriately  
**Assertions**: Y-axis adjusts, all data visible  
**Priority**: LOW

### TC-044: Negative Points Week
**Description**: Player scores negative (multiple INTs, fumbles)  
**Preconditions**: 5 INTs, 3 fumbles lost  
**Expected Behavior**: Chart shows below 0  
**Assertions**: Chart handles negative values  
**Priority**: LOW

---

## Performance Tests

### TC-045: Load 100+ Players Quickly
**Description**: Fetch and display 100 players  
**Expected Behavior**: Completes in < 2 seconds  
**Assertions**: No lag, smooth rendering  
**Priority**: MEDIUM

### TC-046: API Rate Limit Handling
**Description**: Stay under 1000 calls/minute  
**Expected Behavior**: Throttling works  
**Assertions**: No 429 errors  
**Priority**: HIGH

### TC-047: Large Dataset Rendering
**Description**: 16 weeks of data for 200 players  
**Expected Behavior**: Renders without freezing  
**Assertions**: < 5 seconds to render  
**Priority**: MEDIUM

---

## Test Data Sets

### Sample Player Data
```json
{
  "player_id": "1897",
  "name": "Patrick Mahomes",
  "position": "QB",
  "team": "KC",
  "weekly_stats": [
    {"week": 1, "actual": 25.3, "projected": 24.5, "diff": 0.8},
    {"week": 2, "actual": 28.7, "projected": 25.0, "diff": 3.7},
    {"week": 3, "actual": 19.2, "projected": 23.0, "diff": -3.8},
    {"week": 4, "actual": 31.5, "projected": 26.0, "diff": 5.5}
  ],
  "season_average": 26.2
}
```

---

## Test Execution Plan

### Phase 5 Test Implementation

1. **Unit Tests** (Days 1-2)
   - PPR calculator tests
   - Market manager tests
   - API client tests

2. **Integration Tests** (Days 3-4)
   - API endpoint tests
   - Database operations
   - External API integration

3. **Frontend Tests** (Days 5-6)
   - Component rendering
   - User interactions
   - Chart functionality

4. **E2E Tests** (Day 7)
   - Full user flow
   - Buy/sell workflow
   - Real-time updates

5. **Performance Tests** (Day 8)
   - Load testing
   - Stress testing
   - Rate limit validation

**Total Estimated Time**: 8 days

---

## Test Coverage Goals

- **Backend**: 80%+ code coverage
- **Frontend**: 70%+ component coverage
- **Critical Paths**: 100% coverage
- **Edge Cases**: All identified cases tested

---

## Notes

- All test names follow TC-XXX format
- Priority: HIGH = Critical, MEDIUM = Important, LOW = Nice-to-have
- Test data should be realistic but anonymized
- Mock external APIs for unit tests
- Use real API data for integration tests

