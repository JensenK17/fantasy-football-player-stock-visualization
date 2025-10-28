"""
PPR Calculator - Calculates Full PPR fantasy points from raw NFL stats
Full PPR (Point Per Reception) Scoring Rules:
- Passing Yards: 1 point per 25 yards
- Passing TDs: 6 points
- Interceptions: -2 points
- Rushing Yards: 1 point per 10 yards
- Rushing TDs: 6 points
- Receptions: 1 point each
- Receiving Yards: 1 point per 10 yards
- Receiving TDs: 6 points
- Fumbles Lost: -2 points
- 2PT Conversions: 2 points
"""

import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

logger = logging.getLogger(__name__)

def calculate_ppr_points(raw_stats: dict) -> float:
    """
    Calculate full PPR points from raw NFL stats
    
    Args:
        raw_stats: Dictionary containing player stats from Sleeper API
        
    Returns:
        Total PPR points as float
        
    Raises:
        TypeError: If raw_stats is not a dict
        ValueError: If stats contain invalid values
    """
    if not isinstance(raw_stats, dict):
        raise TypeError("raw_stats must be a dictionary")
    
    try:
        points = 0.0
        
        # Passing stats
        passing_yds = float(raw_stats.get('passing_yds', 0))
        passing_tds = float(raw_stats.get('passing_tds', 0))
        passing_int = float(raw_stats.get('passing_int', 0))
        points += (passing_yds / 25.0)  # 1 point per 25 yards
        points += passing_tds * 6
        points -= passing_int * 2
        
        # Rushing stats
        rushing_yds = float(raw_stats.get('rushing_yds', 0))
        rushing_tds = float(raw_stats.get('rushing_tds', 0))
        points += (rushing_yds / 10.0)  # 1 point per 10 yards
        points += rushing_tds * 6
        
        # Receiving stats (FULL PPR - 1 point per reception)
        receptions = float(raw_stats.get('receptions', 0))
        receiving_yds = float(raw_stats.get('receiving_yds', 0))
        receiving_tds = float(raw_stats.get('receiving_tds', 0))
        points += receptions  # 1 point per reception (FULL PPR)
        points += (receiving_yds / 10.0)  # 1 point per 10 yards
        points += receiving_tds * 6
        
        # Other stats
        fumbles_lost = float(raw_stats.get('fumbles_lost', 0))
        passing_2pt = float(raw_stats.get('passing_2pt', 0))
        rushing_2pt = float(raw_stats.get('rushing_2pt', 0))
        receiving_2pt = float(raw_stats.get('receiving_2pt', 0))
        points -= fumbles_lost * 2
        points += passing_2pt * 2
        points += rushing_2pt * 2
        points += receiving_2pt * 2
        
        return round(points, 2)
    
    except (ValueError, KeyError) as e:
        logger.error(f"Error calculating PPR points: {e}")
        raise ValueError(f"Invalid stat value in raw_stats: {e}")

def calculate_ppr_from_sleeper_stats(stats: dict) -> dict:
    """
    Convert Sleeper API stats to PPR points
    
    Args:
        stats: Full stats dictionary from Sleeper API
        
    Returns:
        Dictionary with player_id and calculated PPR points
    """
    player_points = {}
    
    for player_id, player_stats in stats.items():
        player_points[player_id] = calculate_ppr_points(player_stats)
    
    return player_points

