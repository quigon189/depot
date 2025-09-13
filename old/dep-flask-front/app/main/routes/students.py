from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.main.service.view_services import delete_entity, get_student, get_students, send_student, update_student
from app.require import jwt_required
from app.main.forms import StudentForm
from app import app

CATALOG = f'http://{app.config["CATALOG"]}'


@main_bp.route('/students')
@jwt_required
def students():
    students = get_students(CATALOG)

    for error in students.errors:
        flash(error, 'danger')

    return render_template('control/list.html', presenter=students)


@main_bp.route('/students/<int:id>')
@jwt_required
def student_info(id):
    student = get_student(CATALOG, id)

    for error in student.errors:
        flash(error, 'danger')

    return render_template(
        'control/view.html',
        presenter=student,
        nested=[]
    )


@main_bp.route('/students/create', methods=['GET', 'POST'])
@jwt_required
def create_student():
    form = StudentForm().with_choices(CATALOG)

    if form.validate_on_submit():
        message, category = send_student(CATALOG, form)
        flash(message, category)
        return redirect(url_for('main.students'))

    return render_template(
        'control/form.html',
        header='Добавить студента',
        form=form,
        entity_type='students'
    )


@main_bp.route('/students/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_student(id):
    form = StudentForm().with_choices(CATALOG)

    if form.validate_on_submit():
        message, category = update_student(CATALOG, id, form)
        flash(message, category)
        return redirect(url_for('main.students'))

    student = get_student(CATALOG, id).items[0]

    form.last_name.data = student.last_name
    form.first_name.data = student.first_name
    form.middle_name.data = student.middle_name
    form.birth_date.data = student.birth_date
    form.phone.data = student.phone
    form.group_id.data = str(student.group_id)

    return render_template(
        'control/form.html',
        header='Изменить студента',
        form=form,
        entity_type='students',
    )


@main_bp.route('/students/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_student(id):
    student = get_student(CATALOG, id).items[0]
    message, category = delete_entity(
        CATALOG,
        student,
        'students',
        f'Удален студент: {student.name}'
    )
    flash(message, category)
    return redirect(url_for('main.students'))
