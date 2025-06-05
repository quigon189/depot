from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.main.service.view_services import ClassesPresenter, GroupsPresenter, delete_entity, get_teacher, get_teachers, send_teacher, update_teacher
from app.require import jwt_required
from app.main.forms import TeacherForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/teachers')
@jwt_required
def teachers():
    teachers = get_teachers(CATALOG)

    for error in teachers.errors:
        flash(error, 'danger')

    return render_template('control/list.html', presenter=teachers)


@main_bp.route('/teachers/<int:id>')
@jwt_required
def teacher_info(id):
    teacher = get_teacher(CATALOG, id)

    for error in teacher.errors:
        flash(error, 'danger')

    return render_template(
        'control/view.html',
        presenter=teacher,
        nested=[
            teacher.get_nested(GroupsPresenter, 'groups'),
            teacher.get_nested(ClassesPresenter, 'classes'),
        ]
    )


@main_bp.route('/teachers/create', methods=['GET', 'POST'])
@jwt_required
def create_teacher():
    form = TeacherForm()

    if form.validate_on_submit():
        message, category = send_teacher(CATALOG, form)
        flash(message, category)
        return redirect(url_for('main.teachers'))

    return render_template(
        'control/form.html',
        header='Добавить преподавателя',
        form=form,
        entity_type='teachers'
    )


@main_bp.route('/teachers/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_teacher(id):
    form = TeacherForm()

    if form.validate_on_submit():
        message, category = update_teacher(CATALOG, id, form)
        flash(message, category)
        return redirect(url_for('main.teachers'))

    teacher = get_teacher(CATALOG, id).items[0]

    form.last_name.data = teacher.last_name
    form.first_name.data = teacher.first_name
    form.middle_name.data = teacher.middle_name
    form.birth_date.data = teacher.birth_date
    form.phone.data = teacher.phone

    return render_template(
        'control/form.html',
        header='Изменить преподавателя',
        form=form,
        entity_type='teachers',
    )


@main_bp.route('/teachers/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_teacher(id):
    teacher = get_teacher(CATALOG, id).items[0]
    message, category = delete_entity(
        CATALOG,
        teacher,
        'teachers',
        f'Удален преподаватель: {teacher.name}'
    )
    flash(message, category)
    return redirect(url_for('main.teachers'))
