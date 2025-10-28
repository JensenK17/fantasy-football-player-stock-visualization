"""
Unit tests for PPR Calculator
Tests all scoring scenarios including edge cases
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.ppr_calculator import calculate_ppr_points

class TestPPRCalculator:
    """Test cases for PPR scoring calculation"""
    
    def test_passonly_stats(self):
        """Test TC-001: Passing stats calculation"""
        stats = {
            "passing_yds": 350,
            "passing_tds": 3,
            "passing_int": 1
        }
        result = calculate_ppr_points(stats)
        # (350/25) + (3*6) + (-1*2) = 14 + 18 - 2 = 30.0
        assert result == 30.0
    
    def test_full_ppr_receiving(self):
        """Test TC-002: Full PPR adds 1 point per reception"""
        stats = {
            "receptions": 8,
            "receiving_yds": 120,
            "receiving_tds": 1
        }
        result = calculate_ppr_points(stats)
        # 8 + (120/10) + (1*6) = 8 + 12 + 6 = 26.0
        assert result == 26.0
    
    def test_rushing_stats(self):
        """Test TC-003: Rushing stats calculation"""
        stats = {
            "rushing_yds": 85,
            "rushing_tds": 2
        }
        result = calculate_ppr_points(stats)
        # (85/10) + (2*6) = 8.5 + 12 = 20.5
        assert result == 20.5
    
    def test_negative_points(self):
        """Test TC-004: Negative stats (fumbles, interceptions)"""
        stats = {
            "receptions": 0,
            "fumbles_lost": 1,
            "passing_int": 0
        }
        result = calculate_ppr_points(stats)
        # -2 points for fumble
        assert result == -2.0
    
    def test_zero_stats(self):
        """Test edge case: Player with no stats"""
        stats = {}
        result = calculate_ppr_points(stats)
        assert result == 0.0
    
    def test_mixed_stats(self):
        """Test: Complete player with all stat types"""
        stats = {
            "passing_yds": 250,
            "passing_tds": 2,
            "passing_int": 1,
            "rushing_yds": 30,
            "rushing_tds": 1,
            "receptions": 5,
            "receiving_yds": 45,
            "receiving_tds": 1,
            "fumbles_lost": 1
        }
        result = calculate_ppr_points(stats)
        # Passing: (250/25) + (2*6) + (-1*2) = 10 + 12 - 2 = 20
        # Rushing: (30/10) + (1*6) = 3 + 6 = 9
        # Receiving: 5 + (45/10) + (1*6) = 5 + 4.5 + 6 = 15.5
        # Fumble: -2
        # Total: 20 + 9 + 15.5 - 2 = 42.5
        assert result == 42.5
    
    def test_invalid_input(self):
        """Test error handling: Invalid input type"""
        with pytest.raises(TypeError):
            calculate_ppr_points("not a dict")
    
    def test_two_point_conversions(self):
        """Test: 2PT conversions"""
        stats = {
            "passing_2pt": 1,
            "rushing_2pt": 1,
            "receiving_2pt": 1
        }
        result = calculate_ppr_points(stats)
        # 2 + 2 + 2 = 6.0 points
        assert result == 6.0
    
    def test_decimal_rounding(self):
        """Test: Proper rounding to 2 decimal places"""
        stats = {
            "passing_yds": 247,  # 247/25 = 9.88
            "rushing_yds": 33,   # 33/10 = 3.3
            "receiving_yds": 37  # 37/10 = 3.7
        }
        result = calculate_ppr_points(stats)
        # 9.88 + 3.3 + 3.7 = 16.88, rounded to 16.88
        assert result == 16.88
        assert isinstance(result, float)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

