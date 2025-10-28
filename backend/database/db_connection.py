"""
Database connection and operations
Uses SQLite for development, can be upgraded to PostgreSQL for production
"""

import sqlite3
import logging
import os
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    Manages database connections and operations
    """
    
    def __init__(self, db_path="fantasy_stock.db"):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database tables if they don't exist"""
        schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
        
        with self.get_connection() as conn:
            if os.path.exists(schema_file):
                with open(schema_file, 'r') as f:
                    schema = f.read()
                    conn.executescript(schema)
                logger.info("Database schema initialized")
            else:
                logger.warning("Schema file not found, tables must be created manually")
    
    @contextmanager
    def get_connection(self):
        """
        Get database connection with context manager
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(...)
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """
        Execute a SELECT query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_modify(self, query: str, params: tuple = None) -> int:
        """
        Execute INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of rows affected
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
    
    def get_player_by_id(self, player_id: str) -> dict:
        """Get player by player_id"""
        query = "SELECT * FROM players WHERE player_id = ?"
        results = self.execute_query(query, (player_id,))
        return results[0] if results else None
    
    def insert_player(self, player_id: str, name: str, position: str, team: str = None, sleeper_id: str = None) -> bool:
        """Insert or update a player"""
        query = """
        INSERT OR REPLACE INTO players (player_id, name, position, team, sleeper_id)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.execute_modify(query, (player_id, name, position, team, sleeper_id))
            return True
        except Exception as e:
            logger.error(f"Error inserting player: {e}")
            return False
    
    def insert_weekly_stat(self, player_id: str, season: int, week: int, actual_points: float, projected_points: float = None, stats_json: str = None) -> bool:
        """Insert or update weekly stats"""
        query = """
        INSERT OR REPLACE INTO weekly_stats (player_id, season, week, actual_points, projected_points, stats_json)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            self.execute_modify(query, (player_id, season, week, actual_points, projected_points, stats_json))
            return True
        except Exception as e:
            logger.error(f"Error inserting weekly stat: {e}")
            return False
    
    def get_player_stats(self, player_id: str, season: int = 2024) -> list:
        """Get all weekly stats for a player in a season"""
        query = """
        SELECT week, actual_points, projected_points, stats_json, timestamp
        FROM weekly_stats
        WHERE player_id = ? AND season = ?
        ORDER BY week
        """
        return self.execute_query(query, (player_id, season))
    
    def insert_projection(self, player_id: str, season: int, week: int, projected_points: float, data_source: str = "sleeper") -> bool:
        """Insert or update projections"""
        query = """
        INSERT OR REPLACE INTO projections (player_id, season, week, projected_points, data_source)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.execute_modify(query, (player_id, season, week, projected_points, data_source))
            return True
        except Exception as e:
            logger.error(f"Error inserting projection: {e}")
            return False
    
    def get_projection(self, player_id: str, season: int, week: int) -> dict:
        """Get projection for a player in a specific week"""
        query = """
        SELECT * FROM projections
        WHERE player_id = ? AND season = ? AND week = ?
        """
        results = self.execute_query(query, (player_id, season, week))
        return results[0] if results else None

