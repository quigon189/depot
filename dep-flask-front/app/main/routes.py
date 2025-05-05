from flask import flash, redirect, render_template, url_for, request
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
    specs, fields = services.get_specialties()

    return render_template(
        'control/list.html',
        header='Специальности',
        fields=fields,
        items=specs,
        entity_type='specialties'
    )


@main_bp.route('/specialties/<int:id>')
@jwt_required
def specialty_info(id):
    specialty, fields, nested = services.get_specialty(id)

    return render_template(
        'control/view.html',
        fields=fields,
        item=specialty,
        nested=nested
    )


@main_bp.route('/specialties/create', methods=['GET', 'POST'])
@jwt_required
def create_specialty():
    if request.method == 'POST':
        flash("Добавляем специальность")
        return redirect(url_for('main.specialties'))
    fields = [
            {'label': 'Код', 'type': 'text', 'name': 'code', 'value': '', 'required': 'required'},
            {'label': 'Наименование', 'type': 'text', 'name': 'name', 'value': '', 'required': 'required'},
            {'label': 'Короткое обозначение', 'type': 'text', 'name': 'short_name', 'value': '', 'required': 'required'},
            ]
    return render_template(
        'control/form.html',
        header = 'Создать специальность',
        fields = fields,
        entity_type = 'specialties'
    )


@main_bp.route('/specialties/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_specialty(id):
    if request.method == 'POST':
        flash("Изменения внесены")
        return redirect(url_for('main.specialties'))

    specialty, f, n = services.get_specialty(id)
    fields = [
            {'label': 'Код', 'type': 'text', 'name': 'code', 'value': specialty["code"], 'required': 'required'},
            {'label': 'Наименование', 'type': 'text', 'name': 'name', 'value': specialty["name"], 'required': 'required'},
            {'label': 'Короткое обозначение', 'type': 'text', 'name': 'short_name', 'value': specialty["short_name"], 'required': 'required'}
        ]
    return render_template(
        'control/form.html',
        header = 'Изменить специальность',
        fields = fields,
        entity_type = 'specialties',
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
