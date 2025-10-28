"""
Configuration settings for the application
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Sleeper API Configuration
    SLEEPER_API_BASE_URL = "https://api.sleeper.app/v1"
    
    # Optional: Add API keys if needed for future features
    # SLEEPER_API_KEY = os.getenv('SLEEPER_API_KEY')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')


