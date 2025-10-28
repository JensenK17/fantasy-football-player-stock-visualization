# System Architecture

## Overview

This document describes the system architecture for the Fantasy Football Player Stock Visualization application.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (React + TypeScript)                      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ MarketStatus │  │ PlayerSearch │  │ StockChart   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │ Portfolio    │  │ ChartControls│                       │
│  └──────────────┘  └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
                            ↕ API Calls
                    (JSON over HTTP)
┌─────────────────────────────────────────────────────────────┐
│                      Backend (Flask)                         │
│                       (Python)                               │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Sleeper      │  │ PPR          │  │ Market       │      │
│  │ Client       │  │ Calculator   │  │ Manager      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Database     │  │ API          │  │ Cron Jobs    │      │
│  │ (SQLite)     │  │ Endpoints    │  │ (Projections)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  External API (Sleeper)                      │
│              https://api.sleeper.app/v1                      │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Projection Snapshotting (Monday Morning)

```
Cron Job → Fetch Current Week → Get All Projections → Store in DB
```

### 2. User Views Chart

```
Frontend → Request Player Stats → Backend → Fetch from DB → Return JSON
         ← Receive Data ←         ← Data   ← Add PPR Calc
```

### 3. Market Status Check

```
Frontend → GET /api/market-status → Check Day/Time → Return Status
         ← {is_open, current_week, locked_players}
```

## Database Design

### Entities

- **Player**: Basic player info (name, position, team)
- **WeeklyStats**: Actual PPR points scored per week
- **Projections**: Snapshot of projected points per week
- **UserPortfolio**: Buy/sell transactions

### Relationships

```
Player 1---N WeeklyStats
Player 1---N Projections
Player 1---N UserPortfolio
```

## API Design

### Endpoints

| Method | Endpoint | Description |
|-------|----------|------------|
| GET | `/api/current-week` | Get current NFL week |
| GET | `/api/players` | List all players |
| GET | `/api/players/:id/stats` | Get player's weekly stats |
| GET | `/api/market-status` | Get market open/closed status |
| GET | `/api/week-projections/:week` | Get projections for a week |
| POST | `/api/portfolio/buy` | Buy a player position |
| POST | `/api/portfolio/sell` | Sell a player position |

### Response Format

```json
{
  "player_id": "1234",
  "name": "Patrick Mahomes",
  "position": "QB",
  "team": "KC",
  "weekly_stats": [
    {
      "week": 1,
      "actual": 25.3,
      "projected": 24.5,
      "diff": 0.8
    }
  ],
  "season_average": 26.5
}
```

## Component Responsibilities

### Backend Components

**Sleeper Client**
- Fetch data from Sleeper API
- Handle rate limiting
- Cache responses

**PPR Calculator**
- Parse raw NFL stats
- Apply full PPR scoring rules
- Return calculated points

**Market Manager**
- Determine market open/closed
- Identify locked players
- Calculate time until close

**Projection Service**
- Fetch projections from API
- Snapshot and store projections
- Retrieve cached projections

### Frontend Components

**StockChart**
- Render area chart with dual lines
- Apply green/red fills
- Handle tooltips and interactions

**MarketStatus**
- Display current week
- Show market status
- List locked players

**PlayerSearch**
- Search and filter players
- Handle player selection

**PortfolioTracker**
- Track positions
- Calculate P/L
- Display portfolio value

## Technology Stack

### Backend
- **Framework**: Flask
- **Database**: SQLite (dev) / PostgreSQL (production)
- **API Client**: sleeper-api-wrapper
- **Data Processing**: Pandas, NumPy

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Charting**: Recharts
- **Styling**: Tailwind CSS
- **Build**: React Scripts

### DevOps
- **Version Control**: Git
- **Package Management**: pip (Python), npm (Node)
- **Cron Jobs**: Python scripts
- **Deployment**: TBD (Vercel/Netlify for frontend, Heroku/Railway for backend)

## Security Considerations

- No API keys required (Sleeper API is public)
- CORS enabled for localhost:3000 in development
- Input validation on all API endpoints
- Rate limiting on API calls (TBD)
- SQL injection prevention via parameterized queries

## Performance Considerations

- Cache API responses (Redis or in-memory)
- Database indexing on frequently queried fields
- Lazy loading of player lists
- Debounce search input
- Virtual scrolling for large player lists

## Scalability

- Database can scale to PostgreSQL for production
- API can be load-balanced
- Frontend can be served via CDN
- Consider GraphQL for complex queries

## Future Enhancements

- Real-time updates via WebSockets
- User authentication and persistent portfolios
- Historical data from multiple seasons
- Advanced filtering and sorting
- Export charts as images/PDFs
- Mobile app version

