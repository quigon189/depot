from functools import wraps
from flask import request, flash, redirect, url_for, g
import jwt
from app import app


def validate(token):
    try:
        payload = jwt.decode(
            token,
            app.config["SECRET_KEY"],
            algorithms=["HS256"],
            issuer="depot-user-repo",
        )
    except Exception as e:
        flash(f"Ошибка авторизации: {str(e)}")
        return None

    return payload


# def jwt_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.cookies.get("auth_token")
#         if not auth:
#             flash("Для доступа к странице необходимо авторизоваться")
#             return redirect(url_for('login.login'))
#
#         return f(*args, **kwargs)
#
#     return decorated

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" in g:
            return f(*args, **kwargs)

        flash("Для доступа к странице необходимо авторизоваться", "danger")
        return redirect(url_for('login.login'))

    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated(*args, **kwargs):
            user_role = g.user.get("user_role")
            if user_role not in roles:
                flash("Доступ запрещен", "danger")
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated
    return decorator
