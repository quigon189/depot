from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.require import jwt_required
from app.main import services
from app.main.forms import SpecialityForm, GroupForm, StudentForm, TeacherForm, DisciplineForm, ClassForm
import requests


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

    if specs['errors']:
        for err in specs['errors']:
            print(err)
            flash(err)

    return render_template(
        'control/list.html',
        header='Специальности',
        fields=specs['fields'],
        items=specs['items'],
        entity_type='specialties'
    )


@main_bp.route('/groups')
@jwt_required
def groups():
    groups = services.get_groups()

    return render_template(
        'control/list.html',
        header='Группы',
        fields=groups['fields'],
        items=groups['items'],
        entity_type='groups'
    )


@main_bp.route('/students')
@jwt_required
def students():
    students = services.get_students()

    return render_template(
        'control/list.html',
        header='Студенты',
        fields=students['fields'],
        items=students['items'],
        entity_type='students'
    )


@main_bp.route('/teachers')
@jwt_required
def teachers():
    teachers = services.get_teachers()

    return render_template(
        'control/list.html',
        header='Преподаватели',
        fields=teachers['fields'],
        items=teachers['items'],
        entity_type='teachers'
    )


@main_bp.route('/disciplines')
@jwt_required
def disciplines():
    disciplines = services.get_disciplines()

    return render_template(
        'control/list.html',
        header='Дисциплины',
        fields=disciplines['fields'],
        items=disciplines['items'],
        entity_type='disciplines'
    )


@main_bp.route('/classes')
@jwt_required
def classes():
    classes = services.get_classes()

    return render_template(
        'control/list.html',
        header='Аудитории',
        fields=classes['fields'],
        items=classes['items'],
        entity_type='classes'
    )


@main_bp.route('/specialties/<int:id>')
@jwt_required
def specialty_info(id):
    specialty = services.get_specialty(id)

    return render_template(
        'control/view.html',
        fields=specialty['fields'],
        item=specialty['item'],
        nested=specialty['nested']
    )


@main_bp.route('/groups/<int:id>')
@jwt_required
def group_info(id):
    group = services.get_group(id)

    return render_template(
        'control/view.html',
        fields=group['fields'],
        item=group['item'],
        nested=group['nested']
    )


@main_bp.route('/students/<int:id>')
@jwt_required
def student_info(id):
    student = services.get_student(id)

    return render_template(
        'control/view.html',
        fields=student['fields'],
        item=student['item'],
        nested=student['nested']
    )


@main_bp.route('/teachers/<int:id>')
@jwt_required
def teacher_info(id):
    teacher = services.get_teacher(id)

    return render_template(
        'control/view.html',
        fields=teacher['fields'],
        item=teacher['item'],
        nested=teacher['nested']
    )


@main_bp.route('/disciplines/<int:id>')
@jwt_required
def discipline_info(id):
    discipline = services.get_discipline(id)

    return render_template(
        'control/view.html',
        fields=discipline['fields'],
        item=discipline['item'],
        nested=discipline['nested']
    )


@main_bp.route('/classes/<int:id>')
@jwt_required
def class_info(id):
    cl = services.get_class(id)

    return render_template(
        'control/view.html',
        fields=cl['fields'],
        item=cl['item'],
        nested=cl['nested']
    )


@main_bp.route('/specialties/create', methods=['GET', 'POST'])
@jwt_required
def create_specialty():
    form = SpecialityForm()

    if form.validate_on_submit():
        response = services.send_specialty(form)
        if response.status_code == 201:
            flash(f"Специальность {form.code.data} добавленна")
        else:
            flash(
                f"Ошибка при добавлении специальности: {response.status_code}")
        return redirect(url_for('main.specialties'))

    return render_template(
        'control/form.html',
        header='Добавить специальность',
        form=form,
        entity_type='specialties'
    )


@main_bp.route('/groups/create', methods=['GET', 'POST'])
@jwt_required
def create_group():
    form = GroupForm()

    specialties = services.get_specialties()['items']
    teachers = services.get_teachers()['items']

    form.spec_id.choices = [
        (s["id"], f"{s['code']} {s['name']}") for s in specialties
    ]
    form.class_teacher_id.choices = [
        (t['id'], f"{t['last_name']} {t['first_name'][0]}. {t['middle_name'][0]}.") for t in teachers
    ]

    if form.validate_on_submit():
        response = services.send_group(form)
        if response.status_code == 201:
            flash(f"Группа {form.number.data} добавленна")
        else:
            flash(
                f"Ошибка добавления группы: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.groups'))

    return render_template(
        'control/form.html',
        header='Добавить группу',
        form=form,
        entity_type='groups'
    )


@main_bp.route('/students/create', methods=['GET', 'POST'])
@jwt_required
def create_student():
    form = StudentForm()

    groups = services.get_groups()['items']

    form.group_id.choices = [
        (g["id"], f"{g['name']}") for g in groups
    ]

    if form.validate_on_submit():
        response = services.send_student(form)
        if response.status_code == 201:
            flash(f"Студент {form.last_name.data} добавленн")
        else:
            flask(
                f"Ошибка при добавлении: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.students'))

    return render_template(
        'control/form.html',
        header='Добавить студента',
        form=form,
        entity_type='students'
    )


@main_bp.route('/teachers/create', methods=['GET', 'POST'])
@jwt_required
def create_teacher():
    form = TeacherForm()

    if form.validate_on_submit():
        response = services.send_teacher(form)
        if response.status_code == 201:
            flash(f"Преподаватель {form.last_name.data} добавлен")
        else:
            flask(
                f"Ошибка при добавлении: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.teachers'))

    return render_template(
        'control/form.html',
        header='Добавить преподавателя',
        form=form,
        entity_type='teachers'
    )


@main_bp.route('/disciplines/create', methods=['GET', 'POST'])
@jwt_required
def create_discipline():
    form = DisciplineForm()

    groups = services.get_groups()['items']

    form.group_id.choices = [
        (g['id'], g['name']) for g in groups
    ]

    if form.validate_on_submit():
        response = services.send_discipline(form)
        if response.status_code == 201:
            flash(f"Дисциплина {form.name.data} добавленна")
        else:
            flash(
                f"Ошибка при добавлении: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.disciplines'))

    return render_template(
        'control/form.html',
        header='Добавить дисциплину',
        form=form,
        entity_type='disciplines'
    )


@main_bp.route('/classes/create', methods=['GET', 'POST'])
@jwt_required
def create_class():
    form = ClassForm()

    teachers = services.get_teachers()['items']

    form.teacher_id.choices = [
        (t['id'], t['name']) for t in teachers
    ]
    form.type.choices = [
        ('Кабинет', 'Кабинет'),
        ('Лаборатория', 'Лаборатория'),
        ('Полигон', 'Полигон')
    ]

    if form.validate_on_submit():
        response = services.send_class(form)
        if response.status_code == 201:
            flash(f"Аудитория {form.number.data} добавленна")
        else:
            flash(
                f"Ошибка при добавлении: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.classes'))

    return render_template(
        'control/form.html',
        header='Добавить аудиторию',
        form=form,
        entity_type='classes'
    )


@main_bp.route('/specialties/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_specialty(id):
    form = SpecialityForm()

    if form.validate_on_submit():
        spec = {
            'id': id,
            'code': form.code.data,
            'name': form.name.data,
            'short_name': form.short_name.data
        }
        response = services.update_entity(spec, 'specialties')
        if response.status_code == 200:
            flash(f"Специальность {spec['code']} {spec['name']} обновленна")
        else:
            flash(
                f"Ошибка обновления: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.specialties'))

    specialty = services.get_specialty(id)['item']

    form.code.data = specialty['code']
    form.name.data = specialty['name']
    form.short_name.data = specialty['short_name']

    return render_template(
        'control/form.html',
        header='Изменить специальность',
        form=form,
        entity_type='specialties',
    )


@main_bp.route('/groups/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_group(id):
    form = GroupForm()

    specialties = services.get_specialties()['items']
    teachers = services.get_teachers()['items']

    form.spec_id.choices = [
        (s["id"], f"{s['code']} {s['name']}") for s in specialties
    ]
    form.class_teacher_id.choices = [
        (t['id'], f"{t['last_name']} {t['first_name'][0]}. {t['middle_name'][0]}.") for t in teachers
    ]

    if form.validate_on_submit():
        g = {
            'id': id,
            'number': int(form.number.data) if form.number.data else 0,
            'year_formed': int(form.year_formed.data) if form.year_formed.data else 0,
            'spec_id': int(form.spec_id.data),
            'class_teacher_id': int(form.class_teacher_id.data)
        }
        response = services.update_entity(g, 'groups')
        if response.status_code == 200:
            flash(f"Группа {g['number']} обновлена")
        else:
            flash(
                f"Ошибка обновления: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.groups'))

    group = services.get_group(id)['item']

    form.number.data = group['number']
    form.year_formed.data = group['year_formed']
    form.spec_id.data = str(group['spec_id'])
    form.class_teacher_id.data = str(group['class_teacher_id'])

    return render_template(
        'control/form.html',
        header='Изменить группу',
        form=form,
        entity_type='groups',
    )


@main_bp.route('/students/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_student(id):
    form = StudentForm()

    groups = services.get_groups()['items']
    form.group_id.choices = [(g['id'], g['name']) for g in groups]

    if form.validate_on_submit():
        s = {
            'id': id,
            'last_name': form.last_name.data,
            'first_name': form.first_name.data,
            'middle_name': form.middle_name.data,
            'birth_date': form.birth_date.data,
            'phone': form.phone.data,
            'group_id': int(form.group_id.data)
        }
        response = services.update_entity(s, 'students')
        if response.status_code == 200:
            flash(
                f"Студент {s['last_name']} {s['first_name'][0]}. {s['middle_name'][0]}. обновлен")
        else:
            flash(
                f"Ошибка обновления: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.students'))

    student = services.get_student(id)['item']

    form.last_name.data = student['last_name']
    form.first_name.data = student['first_name']
    form.middle_name.data = student['middle_name']
    form.birth_date.data = student['birth_date']
    form.phone.data = student['phone']
    form.group_id.data = str(student['group_id'])

    return render_template(
        'control/form.html',
        header='Изменить студента',
        form=form,
        entity_type='students',
    )


@main_bp.route('/teachers/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_teacher(id):
    form = TeacherForm()

    if form.validate_on_submit():
        t = {
            'id': id,
            'last_name': form.last_name.data,
            'first_name': form.first_name.data,
            'middle_name': form.middle_name.data,
            'birth_date': form.birth_date.data,
            'phone': form.phone.data,
        }
        response = services.update_entity(t, 'teachers')
        if response.status_code == 200:
            flash(
                f"Преподаватель {t['last_name']} {t['first_name'][0]}. {t['middle_name'][0]}. обновлен")
        else:
            flash(
                f"Ошибка обновления: код {response.status_code} ошибка {response.json()}")
        return redirect(url_for('main.teachers'))

    teacher = services.get_teacher(id)['item']

    form.last_name.data = teacher['last_name']
    form.first_name.data = teacher['first_name']
    form.middle_name.data = teacher['middle_name']
    form.birth_date.data = teacher['birth_date']
    form.phone.data = teacher['phone']

    return render_template(
        'control/form.html',
        header='Изменить преподавателя',
        form=form,
        entity_type='teachers',
    )


@main_bp.route('/disciplines/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_discipline(id):
    form = DisciplineForm()

    groups = services.get_groups()['items']

    form.group_id.choices = [(g['id'], g['name']) for g in groups]

    if form.validate_on_submit():
        d = {
            'id': id,
            'code': form.code.data,
            'name': form.name.data,
            'semester': int(form.semester.data) if form.semester.data else 0,
            'hours': int(form.hours.data) if form.hours.data else 0,
            'group_id': int(form.group_id.data)
        }

        response = services.update_entity(d, 'disciplines')
        if response.status_code == 200:
            flash(f"Дисциплина {d['name']} обновленa")
        else:
            flash(f"Ошибка обновления: код {response.status_code}")
        return redirect(url_for('main.disciplines'))

    discipline = services.get_discipline(id)['item']

    form.code.data = discipline['code']
    form.name.data = discipline['name']
    form.semester.data = discipline['semester']
    form.hours.data = discipline['hours']
    form.group_id.data = str(discipline['group_id'])

    return render_template(
        'control/form.html',
        header='Изменить дисциплину',
        form=form,
        entity_type='disciplines',
    )


@main_bp.route('/classes/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_class(id):
    form = ClassForm()

    teachers = services.get_teachers()['items']

    form.teacher_id.choices = [(t['id'], t['name']) for t in teachers]
    form.type.choices = [
            ('Кабинет', 'Кабинет'),
            ('Лаборатория', 'Лаборатория'),
            ('Полигон', 'Полигон'),
            ]

    if form.validate_on_submit():
        c = {
            'id': id,
            'number': form.number.data,
            'name': form.name.data,
            'type': form.type.data,
            'capacity': int(form.capacity.data) if form.capacity.data else 0,
            'equipment': form.equipment.data,
            'teacher_id': int(form.teacher_id.data)
        }

        response = services.update_entity(c, 'classes')
        if response.status_code == 200:
            flash(f"Аудитория {c['number']} обновленa")
        else:
            flash(f"Ошибка обновления: код {response.status_code}")
        return redirect(url_for('main.classes'))

    cl = services.get_class(id)['item']

    form.number.data = cl['number']
    form.name.data = cl['name']
    form.type.data = cl['type']
    form.capacity.data = cl['capacity']
    form.teacher_id.data = str(cl['teacher_id'])

    return render_template(
        'control/form.html',
        header='Изменить аудиторию',
        form=form,
        entity_type='classes',
    )


@main_bp.route('/specialties/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_specialty(id):
    specialty = services.get_specialty(id)['item']
    response = services.delete_entity(specialty, 'specialties')
    if response.status_code == 200:
        flash(f"Специальность \"{specialty['name']}\" удалена")
    else:
        flash(f"Ошибка удаления: код {response.status_code}")
    return redirect(url_for('main.specialties'))


@main_bp.route('/groups/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_group(id):
    group = services.get_group(id)['item']
    response = services.delete_entity(group, 'groups')
    if response.status_code == 200:
        flash(f"Группа \"{group['name']}\" удалена")
    else:
        flash(f"Ошибка удаления: код {response.status_code}")
    return redirect(url_for('main.groups'))


@main_bp.route('/students/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_student(id):
    student = services.get_student(id)['item']
    response = services.delete_entity(student, 'students')
    if response.status_code == 200:
        flash(f"Студент \"{student['name']}\" удален(а)")
    else:
        flash(f"Ошибка удаления: код {response.status_code}")
    return redirect(url_for('main.students'))


@main_bp.route('/teachers/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_teacher(id):
    teacher = services.get_teacher(id)['item']
    response = services.delete_entity(teacher, 'teachers')
    if response.status_code == 200:
        flash(f"Преподаватель \"{teacher['name']}\" удален(а)")
    else:
        flash(f"Ошибка удаления: код {response.status_code}")
    return redirect(url_for('main.teachers'))


@main_bp.route('/disciplines/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_discipline(id):
    discipline = services.get_discipline(id)['item']
    response = services.delete_entity(discipline, 'disciplines')
    if response.status_code == 200:
        flash(f"Дисциплина \"{discipline['name']}\" удалена")
    else:
        flash(f"Ошибка удаления: код {response.status_code}")
    return redirect(url_for('main.disciplines'))


@main_bp.route('/classes/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_class(id):
    cl = services.get_class(id)['item']
    response = services.delete_entity(cl, 'classes')
    if response.status_code == 200:
        flash(f"Аудитория \"{cl['name']}\" удалена")
    else:
        flash(f"Ошибка удаления: код {response.status_code}")
    return redirect(url_for('main.classes'))
