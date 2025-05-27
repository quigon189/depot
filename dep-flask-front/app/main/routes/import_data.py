from flask import flash, render_template
from app.main import main_bp
from app.require import jwt_required
from app.main.forms import ImportForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/export', methods=['POST', 'GET'])
@jwt_required
def import_data():
    form = ImportForm()

    if form.validate_on_submit():
        flash("Данный принятны")

    return render_template(
        'control/import.html',
        form=form
    )
