"""
Market Manager - Handles market open/close logic and player locking
Implements bye week, injury, and game-time based locking
"""

import logging
from datetime import datetime, time, timedelta
from models.player import MarketStatus

logger = logging.getLogger(__name__)

def get_current_nfl_week(season: int = 2024) -> int:
    """
    Determine current NFL week
    Uses date-based calculation as fallback
    
    Args:
        season: NFL season year
        
    Returns:
        Current week number (1-18)
    """
    today = datetime.now()
    season_start = datetime(season, 9, 5)  # Approximate NFL season start
    
    if today < season_start:
        return 0
    
    # Calculate weeks elapsed since season start
    weeks_elapsed = (today - season_start).days // 7 + 1
    return min(weeks_elapsed, 18)

def is_market_open() -> bool:
    """
    Check if market is currently open
    Market is open Monday/Tuesday - Sunday before games
    Closed on game days (Thursday, Saturday, Sunday after 1pm ET)
    
    Returns:
        True if market is open, False if closed
    """
    now = datetime.now()
    day_of_week = now.weekday()  # 0=Monday, 6=Sunday
    hour = now.hour
    
    # Monday through Saturday morning: Market open
    if day_of_week < 6:
        return True
    
    # Saturday afternoon: Market open (might have Saturday games)
    if day_of_week == 5:
        return True
    
    # Sunday: Market closes at 1pm ET (13:00)
    if day_of_week == 6:
        # Convert to ET (simplified - should use proper timezone)
        # Market closes at 1 PM ET = 18:00 UTC (approx)
        if hour < 13:
            return True
        else:
            return False
    
    return False

def is_player_locked(player_id: str, current_week: int, bye_week: int = None, injury_status: str = None, game_time: datetime = None) -> bool:
    """
    Check if a player is locked from trading
    
    A player is locked if:
    1. They are on bye week (current_week == bye_week)
    2. They are injured and OUT (injury_status in ['O', 'IR', 'Out'])
    3. It's Thursday evening and they play Thursday
    4. Their game has started
    
    Args:
        player_id: Player ID to check
        current_week: Current NFL week number
        bye_week: Player's bye week (optional)
        injury_status: Player injury status (optional)
        game_time: When the player's game starts (optional)
        
    Returns:
        True if player is locked, False otherwise
    """
    # Check bye week
    if bye_week and current_week == bye_week:
        logger.debug(f"Player {player_id} is on bye week {bye_week}")
        return True
    
    # Check injury status (OUT or IR)
    if injury_status and injury_status in ['O', 'IR', 'Out', 'IR-R']:
        logger.debug(f"Player {player_id} is injured: {injury_status}")
        return True
    
    # Check if it's Thursday evening (8:20 PM) and player has Thursday game
    now = datetime.now()
    if now.weekday() == 3:  # Thursday
        # Check if it's after 8:20 PM (8 hours, 20 minutes)
        if now.hour >= 20 and now.minute >= 20:
            if game_time and game_time.weekday() == 3:
                logger.debug(f"Player {player_id} has Thursday game, locking")
                return True
    
    # Check if game has started
    if game_time:
        if now >= game_time:
            logger.debug(f"Player {player_id}'s game has started, locking")
            return True
    
    return False

def get_market_status(current_week: int = None) -> MarketStatus:
    """
    Get current market status including open/closed, locked players
    
    Args:
        current_week: Current NFL week (if None, will be calculated)
        
    Returns:
        MarketStatus object with current state
    """
    if not current_week:
        current_week = get_current_nfl_week()
    
    is_open = is_market_open()
    
    # Calculate time until market close if market is open
    time_until_close = None
    if is_open:
        now = datetime.now()
        # If it's Sunday, calculate time until 1 PM
        if now.weekday() == 6:
            market_close_time = now.replace(hour=13, minute=0, second=0, microsecond=0)
            if now < market_close_time:
                time_until_close = str(market_close_time - now)
        # Otherwise market closes Sunday at 1 PM
        elif now.weekday() < 6:
            days_until_sunday = (6 - now.weekday())
            market_close = now + timedelta(days=days_until_sunday)
            market_close_time = market_close.replace(hour=13, minute=0, second=0, microsecond=0)
            time_until_close = str(market_close_time - now)
    
    locked_players = []  # Would be populated from database
    
    return MarketStatus(
        current_week=current_week,
        is_market_open=is_open,
        locked_players=locked_players,
        time_until_close=time_until_close
    )

def should_lock_for_game(game_start: datetime, current_time: datetime = None) -> bool:
    """
    Check if player should be locked based on game start time
    
    Args:
        game_start: When the game starts
        current_time: Current time (defaults to now)
        
    Returns:
        True if player should be locked
    """
    if not current_time:
        current_time = datetime.now()
    
    # Lock if game has started or starts in < 5 minutes
    time_to_start = (game_start - current_time).total_seconds()
    return time_to_start < 300  # 5 minutes = 300 seconds

