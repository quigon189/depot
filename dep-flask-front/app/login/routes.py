from flask import render_template, flash
import requests

from app.login import login_bp
from app.login.forms import LoginForm
from app import app

BACKEND = f'http://{app.config["AUTH"]}'

@login_bp.route('/')
@login_bp.route('/index')
def index():
    return render_template('index.html')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        resp = requests.post(
                f"{BACKEND}/user/login",
                json={
                    "name":form.username.data,
                    "password":form.password.data
                    }
                )

        if resp.status_code == 200:
            flash(f"Авторизация прошла успешно. Token: {resp.json()}")

        else:
            flash(f"Ошибка авторизации {resp.status_code}: {resp.json()}")

    return render_template('login.html', form=form)

