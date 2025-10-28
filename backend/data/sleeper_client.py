"""
Client for interacting with the Sleeper Fantasy Football API
Rate limit: 1000 calls/minute
Implements throttling and caching to stay within limits
"""
import requests
import time
import logging
from datetime import datetime, timedelta
from config import Config

logger = logging.getLogger(__name__)

class SleeperClient:
    """
    Client for fetching data from Sleeper API
    Includes rate limiting (1000 calls/minute) and caching
    """
    
    def __init__(self):
        self.base_url = Config.SLEEPER_API_BASE_URL
        self.rate_limit = 1000  # 1000 calls per minute
        self.calls_this_minute = 0
        self.minute_start = time.time()
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes cache TTL
        
    def _make_request(self, endpoint: str) -> dict:
        """
        Make API request with rate limiting
        
        Args:
            endpoint: API endpoint (without base URL)
            
        Returns:
            JSON response as dict
        """
        # Check rate limit
        current_time = time.time()
        if current_time - self.minute_start >= 60:
            # New minute, reset counter
            self.calls_this_minute = 0
            self.minute_start = current_time
        
        # Check if we've hit the limit
        if self.calls_this_minute >= self.rate_limit:
            wait_time = 60 - (current_time - self.minute_start)
            logger.warning(f"Rate limit reached. Waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
            self.calls_this_minute = 0
            self.minute_start = time.time()
        
        # Check cache
        cache_key = endpoint
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if (datetime.now() - cached_time).total_seconds() < self.cache_ttl:
                logger.debug(f"Cache hit for {endpoint}")
                return cached_data
        
        # Make API request
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache the response
            self.cache[cache_key] = (data, datetime.now())
            
            # Increment call counter
            self.calls_this_minute += 1
            
            logger.debug(f"API call to {endpoint} - Calls this minute: {self.calls_this_minute}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {endpoint}: {e}")
            raise
        
    def get_all_players(self):
        """
        Fetch all NFL players from Sleeper API
        Returns: dict of player data keyed by player_id
        """
        endpoint = "players/nfl"
        return self._make_request(endpoint)
        
    def get_player_stats(self, week: int, season: int = 2024) -> dict:
        """
        Get all player stats for a specific week
        
        Args:
            week: NFL week number
            season: NFL season year
            
        Returns:
            Dict of player stats keyed by player_id
        """
        endpoint = f"stats/nfl/{season}/{week}"
        return self._make_request(endpoint)
        
    def get_league_info(self, league_id: str):
        """
        Get league information including scoring settings
        
        Args:
            league_id: Sleeper league ID
            
        Returns:
            League information dict
        """
        endpoint = f"league/{league_id}"
        return self._make_request(endpoint)
    
    def get_current_week(self, season: int = 2024) -> int:
        """
        Get current NFL week number
        
        Args:
            season: NFL season year
            
        Returns:
            Current week number (1-18)
        """
        # Sleeper doesn't have a direct current week endpoint
        # We'll use a common approach: check which week has games
        for week in range(18, 0, -1):
            endpoint = f"schedule/nfl/{season}/{week}"
            data = self._make_request(endpoint)
            if data and len(data) > 0:
                logger.info(f"Current week determined: {week}")
                return week
        
        # Fallback: use date-based calculation
        # This is a simplified version
        today = datetime.now()
        season_start = datetime(season, 9, 5)  # Approximate start
        if today < season_start:
            return 0
        
        weeks_elapsed = (today - season_start).days // 7 + 1
        return min(weeks_elapsed, 18)
    
    def get_historical_projections(self, week: int, season: int = 2024) -> dict:
        """
        Get historical projections from Sleeper API
        
        Args:
            week: NFL week number
            season: NFL season year
            
        Returns:
            Dict of historical projections
        """
        # Note: Sleeper API structure may vary
        # This is a placeholder based on research
        # May need to adjust based on actual API response
        endpoint = f"projections/nfl/{season}/{week}"
        try:
            return self._make_request(endpoint)
        except Exception as e:
            logger.warning(f"Could not fetch projections: {e}")
            return {}
    
    def clear_cache(self):
        """Clear the API response cache"""
        self.cache.clear()
        logger.info("Cache cleared")


