"""
Data models for players and their stats
"""

class Player:
    """Represents a fantasy football player"""
    
    def __init__(self, player_id, name, position, team=None):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.team = team
        self.weekly_stats = []
        self.season_average = 0.0
        
    def add_weekly_stat(self, week, actual_points, projected_points=None):
        """Add a week's statistics"""
        stat = {
            'week': week,
            'actual': actual_points,
            'projected': projected_points,
            'diff': actual_points - projected_points if projected_points else 0
        }
        self.weekly_stats.append(stat)
        
    def calculate_season_average(self):
        """Calculate the player's season average points"""
        if not self.weekly_stats:
            return 0.0
        total = sum(stat['actual'] for stat in self.weekly_stats)
        self.season_average = total / len(self.weekly_stats)
        return self.season_average
        
    def to_dict(self):
        """Convert player to dictionary for JSON serialization"""
        return {
            'player_id': self.player_id,
            'name': self.name,
            'position': self.position,
            'team': self.team,
            'weekly_stats': self.weekly_stats,
            'season_average': self.season_average
        }
        
class WeeklyProjection:
    """Represents a projected points value for a player"""
    
    def __init__(self, player_id, week, projected_points):
        self.player_id = player_id
        self.week = week
        self.projected_points = projected_points
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'player_id': self.player_id,
            'week': self.week,
            'projected_points': self.projected_points
        }
        
class MarketStatus:
    """Represents current market status"""
    
    def __init__(self, current_week, is_market_open, locked_players, time_until_close=None):
        self.current_week = current_week
        self.is_market_open = is_market_open
        self.locked_players = locked_players
        self.time_until_close = time_until_close
        
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'current_week': self.current_week,
            'is_market_open': self.is_market_open,
            'locked_players': self.locked_players,
            'time_until_close': self.time_until_close
        }


