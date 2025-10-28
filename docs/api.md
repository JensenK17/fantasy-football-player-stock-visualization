# API Documentation

## Backend API

Base URL: `http://localhost:5000/api`

## Endpoints

### Health Check
```
GET /
```
Returns application health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### Get Current Week
```
GET /api/current-week
```
Returns the current NFL week number.

**Query Parameters:**
- `season` (optional): NFL season year (default: 2024)

**Response:**
```json
{
  "week": 5,
  "season": 2024
}
```

---

### Get All Players
```
GET /api/players
```
Returns a list of all available NFL players.

**Response:**
```json
{
  "players": [
    {
      "player_id": "1897",
      "name": "Patrick Mahomes",
      "position": "QB",
      "team": "KC"
    }
  ]
}
```

---

### Get Player Stats
```
GET /api/players/:player_id/stats
```
Returns weekly stats and projections for a specific player.

**Path Parameters:**
- `player_id`: Player ID

**Query Parameters:**
- `season` (optional): NFL season year (default: 2024)

**Response:**
```json
{
  "player_id": "1897",
  "season": 2024,
  "weekly_stats": [
    {
      "week": 1,
      "actual": 25.3,
      "projected": 24.5,
      "diff": 0.8
    },
    {
      "week": 2,
      "actual": 28.7,
      "projected": 25.0,
      "diff": 3.7
    }
  ]
}
```

---

### Get Player Projection
```
GET /api/players/:player_id/projection
```
Returns projected points for a player in a specific week.

**Path Parameters:**
- `player_id`: Player ID

**Query Parameters:**
- `season` (optional): NFL season year (default: 2024)
- `week` (optional): Week number (default: current week)

**Response:**
```json
{
  "player_id": "1897",
  "week": 5,
  "projected_points": 24.5
}
```

---

### Get Market Status
```
GET /api/market-status
```
Returns current market status (open/closed, locked players, etc.).

**Response:**
```json
{
  "current_week": 5,
  "is_market_open": true,
  "locked_players": [],
  "time_until_close": "2 days, 3:45:32"
}
```

---

### Get Week Projections
```
GET /api/week-projections/:week
```
Returns all projections for a specific week.

**Path Parameters:**
- `week`: Week number

**Query Parameters:**
- `season` (optional): NFL season year (default: 2024)

**Response:**
```json
{
  "week": 5,
  "season": 2024,
  "projections": []
}
```

## Error Handling

All endpoints return errors in the following format:

```json
{
  "error": "Error message"
}
```

HTTP Status Codes:
- `200`: Success
- `404`: Not found
- `500`: Server error

## Rate Limiting

The API respects Sleeper's rate limit of **1000 calls per minute**. Responses are cached for 5 minutes to reduce API calls.

