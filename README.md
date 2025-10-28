# Fantasy Football Player Stock Visualization

A web application that visualizes fantasy football player performance like a stock market, displaying weekly point totals with projected values and color-coded performance indicators.

![Status](https://img.shields.io/badge/status-ready-blue)
![Tech](https://img.shields.io/badge/stack-Python%20%2B%20React-green)

## 🎯 Overview

This application transforms fantasy football player data into a stock-market-style visualization where:
- **Stock Price** = Player's weekly PPR point total
- **Projected Line** = Forecasted points (dotted)
- **Green Fill** = Over-performance (actual > projected)
- **Red Fill** = Under-performance (actual < projected)

Users can "buy" and "sell" players based on their performance trends, with full portfolio tracking and P/L calculations.

## ✨ Features

### Visualization
- 📈 Stock-like line chart with weekly PPR points
- 🟢 Green filled areas when exceeding projections
- 🔴 Red filled areas when underperforming
- 📊 Dual lines: Actual (solid) + Projected (dashed)
- 🔮 Future projection extending one week ahead
- 📱 Responsive design (mobile, tablet, desktop)

### Market Mechanics
- 🕐 Market open: Monday/Tuesday when projections available
- 🕐 Market close: Sunday before games start (1 PM ET)
- 🔒 Thursday players: Lock at 8:20 PM Thursday
- 🚫 Bye week locking (flat line display)
- 🏥 Injury locking (OUT/IR status)
- ⏰ Time until close countdown

### Portfolio System
- 💰 Buy/sell players at current point total
- 📈 Track entry/exit prices
- 💵 Automatic P/L calculation
- 📜 Transaction history
- 💾 LocalStorage persistence

### Technical Features
- ⚡ Rate limiting (1000 API calls/minute)
- 💾 Response caching (5-minute TTL)
- 📊 Full PPR scoring implemented
- 🔄 Real-time updates capability
- ✅ Error handling throughout
- 🎨 Modern UI with Tailwind CSS

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- Flask (REST API)
- SQLite (dev) / PostgreSQL (production)
- Sleeper Fantasy Football API
- pytest (testing)

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Recharts (visualization)
- React Router
- LocalStorage (state persistence)

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd fantasy-football-player-stock-visualization
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Backend will start on `http://localhost:5000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will start on `http://localhost:3000`

## 📁 Project Structure

```
fantasy-football-player-stock-visualization/
├── backend/                    # Python Flask Backend
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── data/                  # Data processing modules
│   │   ├── sleeper_client.py # Sleeper API client
│   │   ├── ppr_calculator.py # PPR scoring logic
│   │   ├── market_manager.py # Market logic
│   │   └── ...
│   ├── models/                # Data models
│   ├── database/              # Database schema
│   └── tests/                 # Unit tests
│
├── frontend/                  # React TypeScript Frontend
│   ├── package.json          # Node dependencies
│   ├── tsconfig.json         # TypeScript config
│   ├── tailwind.config.js    # Tailwind CSS config
│   ├── src/
│   │   ├── App.tsx           # Main app component
│   │   ├── components/       # React components
│   │   ├── services/         # API service
│   │   └── hooks/           # Custom React hooks
│   └── public/
│
└── docs/                      # Documentation
    ├── architecture.md        # System architecture
    └── api.md                # API documentation
```

## 📡 API Endpoints

### Backend API (Flask)

Base URL: `http://localhost:5000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/current-week` | Get current NFL week |
| GET | `/api/players` | List all players |
| GET | `/api/players/:id/stats` | Get player weekly stats |
| GET | `/api/players/:id/projection` | Get player projection |
| GET | `/api/market-status` | Get market status |
| GET | `/api/week-projections/:week` | Get week projections |

### Example Response

```json
{
  "player_id": "1897",
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

## 📊 Full PPR Scoring

The application uses **Full PPR (Point Per Reception)** scoring:

```python
# Passing
passing_yds / 25 yards = 1 point
passing_tds = 6 points
passing_int = -2 points

# Rushing
rushing_yds / 10 yards = 1 point
rushing_tds = 6 points

# Receiving (FULL PPR)
receptions = 1 point each
receiving_yds / 10 yards = 1 point
receiving_tds = 6 points

# Other
fumbles_lost = -2 points
2PT conversions = 2 points
```

## 🎮 Usage

### Viewing Player Stats
1. Start the backend server
2. Start the frontend server
3. Open `http://localhost:3000`
4. Search for a player by name
5. View their weekly performance chart

### Trading Players
1. Select a player from the sidebar
2. View their current "stock price" (point total)
3. Click "Buy" to enter a position
4. Monitor their performance
5. Click "Sell" to exit the position

### Portfolio Tracking
- All positions are automatically saved to localStorage
- View your total P/L in the portfolio tracker
- See transaction history
- Track active positions

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/test_ppr_calculator.py -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🛠️ Development

### Adding New Features

**Backend:**
1. Add endpoint to `backend/app.py`
2. Implement logic in `backend/data/`
3. Update database schema if needed
4. Add tests in `backend/tests/`

**Frontend:**
1. Create component in `frontend/src/components/`
2. Update routing in `frontend/src/App.tsx`
3. Add types in service files
4. Style with Tailwind CSS

## 📝 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///fantasy_stock.db
CORS_ORIGINS=http://localhost:3000
```

### Rate Limiting

The Sleeper API has a rate limit of **1000 calls per minute**. The application automatically:
- Throttles requests
- Caches responses for 5 minutes
- Queues requests if limit is approached

## 🐛 Troubleshooting

### Backend Issues
- **Import errors**: Ensure virtual environment is activated
- **Database errors**: Check `backend/fantasy_stock.db` exists
- **API errors**: Verify Sleeper API is accessible

### Frontend Issues
- **Build errors**: Run `npm install` again
- **Type errors**: Check TypeScript configuration
- **Styling issues**: Verify Tailwind CSS is configured

## 📚 Documentation

- [Architecture](./docs/architecture.md) - System design and data flow
- [API Reference](./docs/api.md) - Detailed API documentation
- [Planning](./docs/planning.md) - Implementation plans and phases

## 🤝 Contributing

This is a personal project for learning and development. Contributions, issues, and feature requests are welcome!

## 📄 License

MIT License - Feel free to use this project for your own purposes.

## 🙏 Acknowledgments

- **Sleeper Fantasy Football** for providing the API
- **Recharts** for the visualization library
- **Tailwind CSS** for the styling framework

## 🗺️ Roadmap

### Phase 5 (Future)
- [ ] Integration testing
- [ ] E2E testing with Playwright
- [ ] Real-time WebSocket support
- [ ] ESPN API integration
- [ ] Player comparison feature
- [ ] Chart export functionality
- [ ] Mobile app version

### Additional Features
- [ ] User authentication
- [ ] Multiple portfolio support
- [ ] Advanced filtering
- [ ] Historical season data
- [ ] Email notifications
- [ ] Social sharing
- [ ] Leaderboards

## 📞 Contact

For questions or suggestions, please open an issue on the repository.

---

**Built with ❤️ using Python, Flask, React, and TypeScript**
