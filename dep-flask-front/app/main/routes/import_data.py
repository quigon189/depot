import os
from flask import flash, redirect, render_template, request, send_file, url_for
from app.main import main_bp
from app.main.service.import_services import generate_template, import_from_template
from app.require import jwt_required
from app.main.forms import ImportForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/download_template/<entity>')
@jwt_required
def download_template(entity: str):
    if entity not in ['specialties', 'groups', 'students', 'teachers', 'disciplines', 'classes']:
        flash('Недопустимая сущность', 'danger')
        return redirect(request.referrer or url_for('main.index'))

    buffer = generate_template(entity, CATALOG)
    if not buffer:
        flash('Ошибка генерации шаблона', 'danger')
        return redirect(request.referrer or url_for('main.index'))

    filename = f"{entity}_template.xlsx"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@main_bp.route('/import', methods=['POST', 'GET'])
@jwt_required
def import_data():
    form = ImportForm()

    if form.validate_on_submit():
        entity = form.entity.data
        file = form.file.data
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            counter = 1
            while os.path.exists(file_path):
                file_path = f"{file_path}({counter})"
                counter += 1

            file.save(file_path)

            with open(file_path, 'rb') as f:
                message, category = import_from_template(CATALOG, entity, f)
                flash(message, category)

            os.remove(file_path)

        except Exception as e:
            flash(f"Ошибка при импорте данных: {str(e)}", "danger")

    return render_template(
        'control/import.html',
        form=form
    )
