from flask import g, make_response, redirect, render_template, flash, url_for
import requests

from app.login import login_bp
from app.login.forms import LoginForm
from app import app
from app.require import jwt_required

BACKEND = f'http://{app.config["AUTH"]}'


@login_bp.route('/logout')
@jwt_required
def logout():
    resp = make_response(redirect(url_for('main.index')))
    resp.delete_cookie("auth_token")
    return resp


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in g:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        resp = requests.post(
            f"{BACKEND}",
            json={
                "name": form.username.data,
                "password": form.password.data
            }
        )

        if resp.status_code == 200:
            response = make_response(redirect(url_for("main.user")))
            response.set_cookie(
                "auth_token", resp.json()["token"],
                httponly=True,
                samesite='Lax'
            )
            return response
        else:
            flash(f"Ошибка авторизации {resp.status_code}: {resp.json()}", 'warning')

    return render_template('login.html', form=form)
