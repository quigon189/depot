from flask import Flask
from config import Config, configure_logging, make_upload_folder

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
make_upload_folder(app)
configure_logging(app)

from app import befor_request


def is_list(value):
    return isinstance(value, list)

app.jinja_env.tests['is_list'] = is_list

from app.login import login_bp
app.register_blueprint(login_bp)


from app.main import main_bp
app.register_blueprint(main_bp)
