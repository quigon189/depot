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

    fields = [
        {'key': 'code', 'lable': 'Код', 'link': True},
        {'key': 'name', 'lable': 'Наименование'},
        {'key': 'short_name', 'lable': 'Короткое обозначение'},
        {'key': 'groups_count', 'lable': 'Количество групп'}
    ]

    return render_template(
        'control/list.html',
        header='Специализации',
        fields=fields,
        items=specs,
        entity_type='specialties'
    )


@main_bp.route('/specialties/<int:id>')
@jwt_required
def specialty_info(id):
    specialty = services.get_specialty(id)
    return render_template(
        'vies'
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
    students = services.get_students()

    return render_template(
        'view/table.html',
        header='Студенты',
        records=students
    )


@main_bp.route('/disciplines')
@jwt_required
def disciplines():
    disciplines = services.get_disciplines()

    return render_template(
        'view/table.html',
        header='Дисциплины',
        records=disciplines
    )


@main_bp.route('/teachers')
@jwt_required
def teachers():
    teachers = services.get_teachers()

    return render_template(
        'view/table.html',
        header='Преподаватели',
        records=teachers
    )


@main_bp.route('/classes')
@jwt_required
def classes():
    classes = services.get_classes()

    return render_template(
        'view/table.html',
        header='Аудитории',
        records=classes
    )
