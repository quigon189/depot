from flask import request, g, make_response, redirect, url_for
from app import app
from app.require import validate


@app.before_request
def before_request():
    app.logger.info(f"Доступ к странице {request.url}")
    if "auth_token" in request.cookies:
        auth = request.cookies.get("auth_token")
        payload = validate(auth)
        if payload:
            g.user = payload
            return
        resp = make_response(redirect(url_for('login.login')))
        resp.delete_cookie("auth_token")
        return resp
