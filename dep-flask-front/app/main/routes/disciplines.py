from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.require import jwt_required
from app.main import services
from app.main.forms import DisciplineForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/disciplines')
@jwt_required
def disciplines():
    disciplines = services.get_disciplines(CATALOG)

    for error in disciplines.errors:
        flash(error, 'danger')

    return render_template('control/list.html', presenter=disciplines)


@main_bp.route('/disciplines/<int:id>')
@jwt_required
def discipline_info(id):
    discipline = services.get_discipline(CATALOG, id)

    for error in discipline.errors:
        flash(error, 'danger')

    return render_template(
        'control/view.html',
        presenter=discipline,
        nested=[]
    )


@main_bp.route('/disciplines/create', methods=['GET', 'POST'])
@jwt_required
def create_discipline():
    form = DisciplineForm().with_choices(CATALOG)

    if form.validate_on_submit():
        message, category = services.send_discipline(CATALOG, form)
        flash(message, category)
        return redirect(url_for('main.disciplines'))

    return render_template(
        'control/form.html',
        header='Добавить дисциплину',
        form=form,
        entity_type='disciplines'
    )


@main_bp.route('/disciplines/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_discipline(id):
    form = DisciplineForm().with_choices(CATALOG)
    if form.validate_on_submit():
        message, category = services.update_discipline(CATALOG, id, form)
        flash(message, category)
        return redirect(url_for('main.disciplines'))

    discipline = services.get_discipline(CATALOG, id).items[0]

    form.code.data = discipline.code
    form.name.data = discipline.name
    form.semester.data = discipline.semester
    form.hours.data = discipline.hours
    form.group_id.data = str(discipline.group_id)

    return render_template(
        'control/form.html',
        header='Изменить дисциплину',
        form=form,
        entity_type='disciplines',
    )


@main_bp.route('/disciplines/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_discipline(id):
    discipline = services.get_discipline(CATALOG, id).items[0]
    message, category = services.delete_entity(
        CATALOG,
        discipline,
        'disciplines',
        f'удалена дисциплина: {discipline.name}'
    )
    flash(message, category)
    return redirect(url_for('main.disciplines'))
