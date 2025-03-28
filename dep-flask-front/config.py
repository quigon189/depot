import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ghjgecr123'
    AUTH = os.environ.get('AUTH') or 'localhost:18080'
