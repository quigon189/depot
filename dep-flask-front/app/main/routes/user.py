from flask import redirect, url_for
from app.main import main_bp
from app.require import jwt_required


@main_bp.route('/user')
@jwt_required
def user():
    return redirect(url_for('main.index'))
