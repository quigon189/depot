from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.require import jwt_required
from app.main import services
from app.main.forms import ClassForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/classes')
@jwt_required
def classes():
    classes = services.get_classes(CATALOG)

    for error in classes.errors:
        flash(error, 'danger')

    return render_template('control/list.html', presenter=classes)


@main_bp.route('/classes/<int:id>')
@jwt_required
def class_info(id):
    cl = services.get_class(CATALOG, id)

    for error in cl.errors:
        flash(error, 'danger')

    return render_template(
        'control/view.html',
        presenter=cl,
        nested=[]
    )


@main_bp.route('/classes/create', methods=['GET', 'POST'])
@jwt_required
def create_class():
    form = ClassForm().with_choices(CATALOG)

    if form.validate_on_submit():
        message, category = services.send_class(CATALOG, form)
        flash(message, category)
        return redirect(url_for('main.classes'))

    return render_template(
        'control/form.html',
        header='Добавить аудиторию',
        form=form,
        entity_type='classes'
    )


@main_bp.route('/classes/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_class(id):
    form = ClassForm().with_choices(CATALOG)
    if form.validate_on_submit():
        message, category = services.update_classroom(CATALOG, id, form)
        flash(message, category)
        return redirect(url_for('main.classes'))

    cl = services.get_class(CATALOG, id).items[0]

    form.number.data = cl.number
    form.name.data = cl.name
    form.type.data = cl.type
    form.capacity.data = cl.capacity
    form.equipment.data = cl.equipment
    form.teacher_id.data = str(cl.teacher_id)

    return render_template(
        'control/form.html',
        header='Изменить аудиторию',
        form=form,
        entity_type='classes',
    )


@main_bp.route('/classes/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_class(id):
    classroom = services.get_class(CATALOG, id).items[0]
    message, category = services.delete_entity(
        CATALOG,
        classroom,
        'classes',
        f'Удалена аудитория: {classroom.name}'
    )
    flash(message, category)
    return redirect(url_for('main.classes'))
