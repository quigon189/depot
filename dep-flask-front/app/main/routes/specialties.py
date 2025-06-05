from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.main.service.view_services import GroupsPresenter, delete_entity, get_specialties, get_specialty, send_specialty, update_specialty
from app.require import jwt_required
from app.main.forms import SpecialityForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/specialties')
@jwt_required
def specialties():
    specialties = get_specialties(CATALOG)

    for err in specialties.errors:
        flash(err, 'danger')

    return render_template('control/list.html', presenter=specialties)


@main_bp.route('/specialties/<int:id>')
@jwt_required
def specialty_info(id):
    specialty = get_specialty(CATALOG, id)

    for error in specialty.errors:
        flash(error, 'danger')

    return render_template(
        'control/view.html',
        presenter=specialty,
        nested=[specialty.get_nested(GroupsPresenter, 'groups')]
    )


@main_bp.route('/specialties/create', methods=['GET', 'POST'])
@jwt_required
def create_specialty():
    form = SpecialityForm()

    if form.validate_on_submit():
        message, category = send_specialty(CATALOG, form)
        flash(message, category)
        return redirect(url_for('main.specialties'))

    return render_template(
        'control/form.html',
        header='Добавить специальность',
        form=form,
        entity_type='specialties'
    )


@main_bp.route('/specialties/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_specialty(id):
    form = SpecialityForm()

    if form.validate_on_submit():
        message, category = update_specialty(CATALOG, id, form)
        flash(message, category)
        return redirect(url_for('main.specialties'))

    specialty = get_specialty(CATALOG, id).items[0]

    form.code.data = specialty.code
    form.name.data = specialty.name
    form.short_name.data = specialty.short_name

    return render_template(
        'control/form.html',
        header='Изменить специальность',
        form=form,
        entity_type='specialties',
    )


@main_bp.route('/specialties/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_specialty(id):
    specialty = get_specialty(CATALOG, id).items[0]
    message, category = delete_entity(
        CATALOG,
        specialty,
        'specialties',
        f'Удаленна специальность: {specialty.view_name}'
    )
    flash(message, category)
    return redirect(url_for('main.specialties'))
