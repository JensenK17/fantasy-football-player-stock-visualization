"""
Cron job script to snapshot projections every Monday/Tuesday
This captures the "market opening" projections for the current week

Usage:
    python backend/scripts/snapshot_projections.py

Should be scheduled to run Monday mornings via cron:
    0 9 * * MON /path/to/venv/bin/python /path/to/backend/scripts/snapshot_projections.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.sleeper_client import SleeperClient
from data.projection_service import snapshot_projections
from config import Config

def main():
    """
    Main function to snapshot current week projections
    """
    print("Starting projection snapshot job...")
    
    # TODO: Get current week from Sleeper API
    # TODO: Fetch all player projections
    # TODO: Store in projections table
    # TODO: Log results
    
    print("Projection snapshot complete!")

if __name__ == '__main__':
    main()

