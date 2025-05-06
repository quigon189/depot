from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.require import jwt_required
from app.main import services
from app.main.forms import CreateSpecialityForm


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
    form = CreateSpecialityForm()

    if form.validate_on_submit():
        flash("Добавляем специальность")
        return redirect(url_for('main.specialties'))

    return render_template(
        'control/form.html',
        header='Создать специальность',
        form=form,
        entity_type='specialties'
    )


@main_bp.route('/specialties/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_specialty(id):
    form = CreateSpecialityForm()

    if form.validate_on_submit():
        flash("Изменения внесены")
        return redirect(url_for('main.specialties'))

    specialty, _, _ = services.get_specialty(id)
    form.code.data = specialty['code']
    form.name.data = specialty['name']
    form.short_name.data = specialty['short_name']

    return render_template(
        'control/form.html',
        header='Изменить специальность',
        form=form,
        entity_type='specialties',
    )


@main_bp.route('/specialties/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_specialty(id):
    flash(f"Специальность {id} удалена")
    return redirect(url_for('main.specialties'))


@main_bp.route('/groups')
@jwt_required
def groups():
    groups, fields = services.get_groups()

    return render_template(
        'control/list.html',
        header='Специальности',
        fields=fields,
        items=groups,
        entity_type='groups'
    )


@main_bp.route('/groups/<int:id>')
@jwt_required
def group_info(id):
    group, fields, nested = services.get_group(id)

    return render_template(
        'control/view.html',
        fields=fields,
        item=group,
        nested=nested
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
