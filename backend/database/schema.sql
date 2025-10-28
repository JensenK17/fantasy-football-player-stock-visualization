-- Database schema for Fantasy Football Player Stock Visualization
-- TODO: Choose between SQLite (simple, file-based) or PostgreSQL (production-ready)

-- Players table
CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    team TEXT,
    sleeper_id TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weekly stats table (actual points)
CREATE TABLE IF NOT EXISTS weekly_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    week INTEGER NOT NULL,
    actual_points REAL NOT NULL,
    projected_points REAL,
    stats_json TEXT, -- Raw stats from Sleeper API
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE(player_id, season, week)
);

-- Projections table (snapshot at market open)
CREATE TABLE IF NOT EXISTS projections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    week INTEGER NOT NULL,
    projected_points REAL NOT NULL,
    snapshot_time TIMESTAMP NOT NULL,
    data_source TEXT DEFAULT 'sleeper',
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE(player_id, season, week)
);

-- User portfolio (buy/sell tracking)
CREATE TABLE IF NOT EXISTS user_portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK(action IN ('buy', 'sell')),
    entry_price REAL NOT NULL,
    exit_price REAL,
    entry_timestamp TIMESTAMP NOT NULL,
    exit_timestamp TIMESTAMP,
    week INTEGER NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_weekly_stats_player_season ON weekly_stats(player_id, season);
CREATE INDEX IF NOT EXISTS idx_projections_player_week ON projections(player_id, week);
CREATE INDEX IF NOT EXISTS idx_portfolio_player_week ON user_portfolio(player_id, week);

