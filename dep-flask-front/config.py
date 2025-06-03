import logging
import os
from flask import Flask


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ghjgecr123'
    AUTH = os.environ.get('AUTH') or 'localhost:18080'
    CATALOG = os.environ.get('CATALOG') or 'localhost:18081'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'

    LOG_LEVEL = logging.DEBUG


def make_upload_folder(app: Flask):
    path = app.config['UPLOAD_FOLDER']
    os.makedirs(path, exist_ok=True)


def configure_logging(app: Flask):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOG_LEVEL)

    app.logger.addHandler(console_handler)

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)
