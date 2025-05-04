from flask import redirect, render_template, url_for
from app.main import main_bp
from app.require import jwt_required
from app.services import services


@main_bp.route('/index')
@main_bp.route('/')
def index():
    return render_template('index.html')



@main_bp.route('/user')
@jwt_required
def user():
    return redirect(url_for('main.index'))


@main_bp.route('/specialties')
@jwt_required
def specialties():
    specs = services.get_specialties()

    return render_template(
        'view/table.html',
        header='Специализации',
        records=specs
    )


@main_bp.route('/groups')
@jwt_required
def groups():
    groups = services.get_groups()

    return render_template(
        'view/table.html',
        header='Группы',
        records=groups
    )


@main_bp.route('/students')
@jwt_required
def students():
    students = services.get_data('students')

    return render_template(
        'view/table.html',
        header='Студенты',
        records=students
    )


@main_bp.route('/disciplines')
@jwt_required
def disciplines():
    disciplines = services.get_data('disciplines')

    return render_template(
        'view/table.html',
        header='Дисциплины',
        records=disciplines
    )


@main_bp.route('/teachers')
@jwt_required
def teachers():
    teachers = services.get_data('teachers')

    return render_template(
        'view/table.html',
        header='Преподаватели',
        records=teachers
    )


@main_bp.route('/classes')
@jwt_required
def classes():
    classes = services.get_data('classes')

    return render_template(
        'view/table.html',
        header='Аудитории',
        records=classes
    )
