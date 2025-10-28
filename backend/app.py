"""
Flask application entry point for Fantasy Football Player Stock Visualization API
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime

from data.sleeper_client import SleeperClient
from data.ppr_calculator import calculate_ppr_points
from data.market_manager import get_market_status, get_current_nfl_week
from database import DatabaseConnection
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
sleeper_client = SleeperClient()
db = DatabaseConnection()

@app.route('/')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

@app.route('/api/current-week', methods=['GET'])
def get_current_week():
    """Get current NFL week number"""
    try:
        season = request.args.get('season', 2024, type=int)
        week = get_current_nfl_week(season)
        return jsonify({'week': week, 'season': season})
    except Exception as e:
        logger.error(f"Error getting current week: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/players', methods=['GET'])
def get_players():
    """Get all available players"""
    try:
        # Fetch from database first
        query = "SELECT player_id, name, position, team FROM players"
        db_players = db.execute_query(query)
        
        if not db_players:
            # If no players in DB, fetch from Sleeper API
            logger.info("No players in database, fetching from Sleeper API")
            players = sleeper_client.get_all_players()
            
            # Store in database
            for player_id, player_data in players.items():
                db.insert_player(
                    player_id=player_id,
                    name=player_data.get('full_name', 'Unknown'),
                    position=player_data.get('position'),
                    team=player_data.get('team'),
                    sleeper_id=player_id
                )
            
            return jsonify({'players': [{'player_id': k, 'name': v.get('full_name'), 
                                        'position': v.get('position'), 'team': v.get('team')} 
                                       for k, v in list(players.items())[:100]]})
        
        return jsonify({'players': db_players})
    except Exception as e:
        logger.error(f"Error getting players: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    """Get a specific player's weekly stats and projections"""
    try:
        season = request.args.get('season', 2024, type=int)
        
        # Get stats from database
        stats = db.get_player_stats(player_id, season)
        
        # Format response
        formatted_stats = []
        for stat in stats:
            diff = stat['actual_points'] - (stat['projected_points'] or 0)
            formatted_stats.append({
                'week': stat['week'],
                'actual': stat['actual_points'],
                'projected': stat['projected_points'],
                'diff': round(diff, 2)
            })
        
        return jsonify({
            'player_id': player_id,
            'season': season,
            'weekly_stats': formatted_stats
        })
    except Exception as e:
        logger.error(f"Error getting player stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<player_id>/projection', methods=['GET'])
def get_player_projection(player_id):
    """Get projected points for a player for upcoming week"""
    try:
        season = request.args.get('season', 2024, type=int)
        week = request.args.get('week', get_current_nfl_week(), type=int)
        
        projection = db.get_projection(player_id, season, week)
        
        if projection:
            return jsonify({
                'player_id': player_id,
                'week': week,
                'projected_points': projection['projected_points']
            })
        else:
            return jsonify({
                'player_id': player_id,
                'week': week,
                'projected_points': None,
                'message': 'No projection available'
            })
    except Exception as e:
        logger.error(f"Error getting projection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/market-status', methods=['GET'])
def get_market_status_endpoint():
    """Get current market status"""
    try:
        market = get_market_status()
        return jsonify(market.to_dict())
    except Exception as e:
        logger.error(f"Error getting market status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/week-projections/<int:week>', methods=['GET'])
def get_week_projections(week):
    """Get all projections for a specific week"""
    try:
        season = request.args.get('season', 2024, type=int)
        
        # This would fetch projections for the week
        # Implementation depends on how projections are stored
        return jsonify({
            'week': week,
            'season': season,
            'projections': []
        })
    except Exception as e:
        logger.error(f"Error getting week projections: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


