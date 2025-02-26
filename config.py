import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-testing-only'

    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # File upload config
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max upload

    # Determine if we're running on Posit Connect
    IS_CONNECT = 'CONNECT_SERVER' in os.environ

    # Subdirectory config - use Posit Connect path if available
    if IS_CONNECT:
        SUBDIRECTORY_PATH = os.environ.get('CONNECT_URL_PATH', '')
    else:
        # Use hardcoded path for local development
        SUBDIRECTORY_PATH = '/app-subdirectory'

    # OpenAI API configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OPENAI_API_URL = os.environ.get('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions')

    # Available models
    AVAILABLE_MODELS = [
        {'id': 'gpt-4o', 'name': 'GPT-4o'},
        {'id': 'gpt-4o-mini', 'name': 'GPT-4o Mini'}
    ]