from flask import flash, redirect, render_template, request, send_file, url_for
from app.main import main_bp
from app.main.import_data import generate_template
from app.require import jwt_required
from app.main.forms import ImportForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/download_template/<entity>')
@jwt_required
def download_template(entity: str):
    if entity not in ['specialties', 'groups']:
        flash('Недопустимая сущность', 'danger')
        return redirect(request.referrer or url_for('main.index'))

    buffer = generate_template(entity, CATALOG)
    filename = f"{entity}_template.xlsx"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


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
