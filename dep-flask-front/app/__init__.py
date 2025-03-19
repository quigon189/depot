from flask import Flask
from config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

from app.login import login_bp
app.register_blueprint(login_bp)
