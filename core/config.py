# core/config.py - Simple configuration
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Basic configuration for Student Manager"""

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database - MySQL (đã cài cryptography)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # SQLite fallback (nếu MySQL không available)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///student_manager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AI Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

    # Email Configuration
    SMTP_SERVER = os.environ.get('SMTP_SERVER')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    # App settings
    DEBUG = True
