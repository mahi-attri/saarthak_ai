# config.py - SaarthakAI Configuration

import os
from pathlib import Path

class Config:
    """Configuration settings for SaarthakAI"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    SRC_DIR = BASE_DIR / "src"
    STATIC_DIR = BASE_DIR / "static"
    
    # LLM Settings
    OLLAMA_MODEL = "llama3.1:3b"  # Fast model for demo
    OLLAMA_URL = "http://localhost:11434"
    OLLAMA_TIMEOUT = 10  # seconds
    
    # Database Settings
    SCHEMES_DB_PATH = DATA_DIR / "schemes_database.json"
    CONVERSATIONS_DB_PATH = DATA_DIR / "user_conversations.json"
    ANALYTICS_DB_PATH = DATA_DIR / "analytics.json"
    
    # Language Settings
    SUPPORTED_LANGUAGES = ["hindi", "english"]
    DEFAULT_LANGUAGE = "hindi"
    LANGUAGE_CODES = {
        "hindi": "hi",
        "english": "en"
    }
    
    # Voice Settings
    VOICE_ENABLED = True
    TTS_SPEED = 150
    TTS_LANGUAGE_HINDI = "hi-IN"
    TTS_LANGUAGE_ENGLISH = "en-IN"
    STT_TIMEOUT = 5  # seconds
    
    # Mobile Settings
    MOBILE_OPTIMIZED = True
    PWA_ENABLED = True
    TOUCH_FRIENDLY = True
    
    # Demo Settings (for hackathon)
    DEMO_MODE = True
    FAST_RESPONSES = True
    CACHED_RESPONSES = True
    MAX_RESPONSE_TIME = 3  # seconds
    
    # UI Settings
    PRIMARY_COLOR = "#4CAF50"
    SECONDARY_COLOR = "#45a049"
    BACKGROUND_COLOR = "#FFFFFF"
    TEXT_COLOR = "#262730"
    
    # Scheme Matching Settings
    MAX_SCHEMES_RETURNED = 3
    MIN_MATCH_SCORE = 1
    KEYWORD_WEIGHT = 2
    CATEGORY_WEIGHT = 5
    CONTEXT_WEIGHT = 3
    
    # API Settings (if needed later)
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 10
    
    # Logging Settings
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance Settings
    CACHE_SIZE = 100  # Number of cached responses
    PRELOAD_SCHEMES = True
    ASYNC_PROCESSING = False
    
    # Security Settings
    RATE_LIMIT = 60  # requests per minute per user
    MAX_MESSAGE_LENGTH = 500
    ALLOWED_FILE_TYPES = [".txt", ".json"]
    
    # Feature Flags
    ENABLE_VOICE = True
    ENABLE_TRANSLATION = True
    ENABLE_ANALYTICS = True
    ENABLE_FEEDBACK = True
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.SRC_DIR.mkdir(exist_ok=True)
        cls.STATIC_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_database_path(cls, db_type="schemes"):
        """Get database path for specific type"""
        paths = {
            "schemes": cls.SCHEMES_DB_PATH,
            "conversations": cls.CONVERSATIONS_DB_PATH,
            "analytics": cls.ANALYTICS_DB_PATH
        }
        return paths.get(db_type, cls.SCHEMES_DB_PATH)
    
    @classmethod
    def is_ollama_available(cls):
        """Check if Ollama is running"""
        try:
            import requests
            response = requests.get(f"{cls.OLLAMA_URL}/api/version", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    @classmethod
    def get_language_config(cls, language):
        """Get language-specific configuration"""
        if language.lower() in ["hindi", "हिंदी"]:
            return {
                "code": "hi",
                "tts_lang": cls.TTS_LANGUAGE_HINDI,
                "display_name": "हिंदी"
            }
        else:
            return {
                "code": "en", 
                "tts_lang": cls.TTS_LANGUAGE_ENGLISH,
                "display_name": "English"
            }

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    CACHE_SIZE = 10

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    CACHE_SIZE = 1000
    RATE_LIMIT = 30

class HackathonConfig(Config):
    """Hackathon demo configuration"""
    DEBUG = False
    DEMO_MODE = True
    FAST_RESPONSES = True
    CACHED_RESPONSES = True
    MAX_RESPONSE_TIME = 2
    PRELOAD_SCHEMES = True

# Select configuration based on environment
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('SAARTHAK_ENV', 'hackathon').lower()
    
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'hackathon': HackathonConfig
    }
    
    return configs.get(env, HackathonConfig)