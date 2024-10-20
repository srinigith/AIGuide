from dotenv import load_dotenv
load_dotenv()
from decouple import config
import os 

#APP_SETTINGS = os.environ.get("APP_SETTINGS")#config("APP_SETTINGS")
#GROQ_API_KEY = os.environ.get("GROQ_API_KEY")#config("GROQ_API_KEY")

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    #SECRET_KEY = config("SECRET_KEY", default="guess-me")
    #SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    APP_SETTINGS = config("APP_SETTINGS")
    GROQ_API_KEY = config("GROQ_API_KEY")
    LLMINDEX_API_KEY = config("LLMINDEX_API_KEY")

class DevelopmentConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False


class TestingConfig(Config):
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config): 
    DEBUG = False
    DEBUG_TB_ENABLED = False