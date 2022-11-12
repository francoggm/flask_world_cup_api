from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = True
TESTING = True
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True
