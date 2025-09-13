from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.main.service.view_services import delete_entity, get_group, get_groups, send_group, update_group, StudentsPresenter, DisciplinesPresenter
from app.require import jwt_required
from app.main.forms import GroupForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/groups')
@jwt_required
def groups():
    groups = get_groups(CATALOG)

    for error in groups.errors:
        flash(error, 'danger')

    return render_template('control/list.html', presenter=groups)


@main_bp.route('/groups/<int:id>')
@jwt_required
def group_info(id):
    group = get_group(CATALOG, id)

    for error in group.errors:
        flash(error, 'danger')

    return render_template(
        'control/view.html',
        presenter=group,
        nested=[
            group.get_nested(StudentsPresenter, 'students'),
            group.get_nested(DisciplinesPresenter, 'disciplines')
        ]
    )


@main_bp.route('/groups/create', methods=['GET', 'POST'])
@jwt_required
def create_group():
    form = GroupForm().with_choices(CATALOG)

    if form.validate_on_submit():
        message, category = send_group(CATALOG, form)
        flash(message, category)
        return redirect(url_for('main.groups'))

    return render_template(
        'control/form.html',
        header='Добавить группу',
        form=form,
        entity_type='groups'
    )


@main_bp.route('/groups/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_group(id):
    form = GroupForm().with_choices(CATALOG)

    if form.validate_on_submit():
        message, category = update_group(CATALOG, id, form)
        flash(message, category)
        return redirect(url_for('main.groups'))

    group = get_group(CATALOG, id).items[0]

    form.number.data = group.number
    form.year_formed.data = group.year_formed
    form.spec_id.data = str(group.spec_id)
    form.class_teacher_id.data = str(group.class_teacher_id)

    return render_template(
        'control/form.html',
        header='Изменить группу',
        form=form,
        entity_type='groups',
    )


@main_bp.route('/groups/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_group(id):
    group = get_group(CATALOG, id).items[0]
    message, category = delete_entity(
        CATALOG,
        group,
        'groups',
        f'Удалена группа: {group.name}'
    )
    flash(message, category)
    return redirect(url_for('main.groups'))
