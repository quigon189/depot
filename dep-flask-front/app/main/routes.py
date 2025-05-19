from flask import flash, redirect, render_template, url_for
from app.main import main_bp
from app.require import jwt_required
from app.main import services
from app.main.forms import SpecialityForm, GroupForm, StudentForm, TeacherForm
from app.main.forms import DisciplineForm, ClassForm


CATALOG = "http://go-catalog:8080"


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
    specialties = services.get_specialties(CATALOG)

    for err in specialties.errors:
        flash(err)

    return render_template('control/list.html', presenter=specialties)


@main_bp.route('/groups')
@jwt_required
def groups():
    groups = services.get_groups(CATALOG)

    for error in groups.errors:
        flash(error)

    return render_template('control/list.html', presenter=groups)


@main_bp.route('/students')
@jwt_required
def students():
    students = services.get_students(CATALOG)

    for error in students.errors:
        flash(error)

    return render_template('control/list.html', presenter=students)


@main_bp.route('/teachers')
@jwt_required
def teachers():
    teachers = services.get_teachers(CATALOG)

    for error in teachers.errors:
        flash(error)

    return render_template('control/list.html', presenter=teachers)


@main_bp.route('/disciplines')
@jwt_required
def disciplines():
    disciplines = services.get_disciplines(CATALOG)

    for error in disciplines.errors:
        flash(error)

    return render_template('control/list.html', presenter=disciplines)


@main_bp.route('/classes')
@jwt_required
def classes():
    classes = services.get_classes(CATALOG)

    for error in classes.errors:
        flash(error)

    return render_template('control/list.html', presenter=classes)


@main_bp.route('/specialties/<int:id>')
@jwt_required
def specialty_info(id):
    specialty = services.get_specialty(CATALOG, id)

    for error in specialty.errors:
        flash(error)

    return render_template(
        'control/view.html',
        presenter=specialty,
        nested=[specialty.get_nested(services.GroupsPresenter, 'groups')]
    )


@main_bp.route('/groups/<int:id>')
@jwt_required
def group_info(id):
    group = services.get_group(CATALOG, id)

    for error in group.errors:
        flash(error)

    return render_template(
        'control/view.html',
        presenter=group,
        nested=[
            group.get_nested(services.StudentsPresenter, 'students'),
            group.get_nested(services.DisciplinesPresenter, 'disciplines')
        ]
    )


@main_bp.route('/students/<int:id>')
@jwt_required
def student_info(id):
    student = services.get_student(CATALOG, id)

    for error in student.errors:
        flash(error)

    return render_template(
        'control/view.html',
        presenter=student,
        nested=[]
    )


@main_bp.route('/teachers/<int:id>')
@jwt_required
def teacher_info(id):
    teacher = services.get_teacher(CATALOG, id)

    return render_template(
        'control/view.html',
        presenter=teacher,
        nested=[
            teacher.get_nested(services.GroupsPresenter, 'groups'),
            teacher.get_nested(services.ClassesPresenter, 'classes'),
        ]
    )


@main_bp.route('/disciplines/<int:id>')
@jwt_required
def discipline_info(id):
    discipline = services.get_discipline(CATALOG, id)

    for error in discipline.errors:
        flash(error)

    return render_template(
        'control/view.html',
        presenter=discipline,
        nested=[]
    )


@main_bp.route('/classes/<int:id>')
@jwt_required
def class_info(id):
    cl = services.get_class(CATALOG, id)

    for error in cl.errors:
        flash(error)

    return render_template(
        'control/view.html',
        presenter=cl,
        nested=[]
    )


@main_bp.route('/specialties/create', methods=['GET', 'POST'])
@jwt_required
def create_specialty():
    form = SpecialityForm()

    if form.validate_on_submit():
        flash(services.send_specialty(CATALOG, form))
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
    form = GroupForm().with_choices(CATALOG)

    if form.validate_on_submit():
        flash(services.send_group(CATALOG, form))
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
    form = StudentForm().with_choices(CATALOG)

    if form.validate_on_submit():
        flash(services.send_student(CATALOG, form))
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
        flash(services.send_teacher(CATALOG, form))
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
    form = DisciplineForm().with_choices(CATALOG)

    if form.validate_on_submit():
        flash(services.send_discipline(CATALOG, form))
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
    form = ClassForm().with_choices(CATALOG)

    if form.validate_on_submit():
        flash(services.send_class(CATALOG, form))
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
        flash(services.update_specialty(CATALOG, id, form))
        return redirect(url_for('main.specialties'))

    specialty = services.get_specialty(CATALOG, id).items[0]

    form.code.data = specialty.code
    form.name.data = specialty.name
    form.short_name.data = specialty.short_name

    return render_template(
        'control/form.html',
        header='Изменить специальность',
        form=form,
        entity_type='specialties',
    )


@main_bp.route('/groups/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_group(id):
    form = GroupForm().with_choices(CATALOG)

    if form.validate_on_submit():
        flash(services.update_group(CATALOG, id, form))
        return redirect(url_for('main.groups'))

    group = services.get_group(CATALOG, id).items[0]

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


@main_bp.route('/students/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_student(id):
    form = StudentForm().with_choices(CATALOG)

    if form.validate_on_submit():
        flash(services.update_student(CATALOG, id, form))
        return redirect(url_for('main.students'))

    student = services.get_student(CATALOG, id).items[0]

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


@main_bp.route('/teachers/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_teacher(id):
    form = TeacherForm()

    if form.validate_on_submit():
        flash(services.update_teacher(CATALOG, id, form))
        return redirect(url_for('main.teachers'))

    teacher = services.get_teacher(CATALOG, id).items[0]

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


@main_bp.route('/disciplines/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_discipline(id):
    form = DisciplineForm().with_choices(CATALOG)
    if form.validate_on_submit():
        flash(services.update_discipline(CATALOG, id, form))
        return redirect(url_for('main.disciplines'))

    discipline = services.get_discipline(CATALOG, id).items[0]

    form.code.data = discipline.code
    form.name.data = discipline.name
    form.semester.data = discipline.semester
    form.hours.data = discipline.hours
    form.group_id.data = str(discipline.group_id)

    return render_template(
        'control/form.html',
        header='Изменить дисциплину',
        form=form,
        entity_type='disciplines',
    )


@main_bp.route('/classes/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_class(id):
    form = ClassForm().with_choices(CATALOG)
    if form.validate_on_submit():
        flash(services.update_classroom(CATALOG, id, form))
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


@main_bp.route('/specialties/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_specialty(id):
    specialty = services.get_specialty(CATALOG, id).items[0]
    flash(services.delete_entity(
        CATALOG,
        specialty,
        'specialties',
        f'Удаленна специальность: {specialty.view_name}'
    ))
    return redirect(url_for('main.specialties'))


@main_bp.route('/groups/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_group(id):
    group = services.get_group(CATALOG, id).items[0]
    flash(services.delete_entity(
        CATALOG,
        group,
        'groups',
        f'Удалена группа: {group.name}'
    ))
    return redirect(url_for('main.groups'))


@main_bp.route('/students/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_student(id):
    student = services.get_student(CATALOG, id).items[0]
    flash(services.delete_entity(
        CATALOG,
        student,
        'students',
        f'Удален студент: {student.name}'
    ))
    return redirect(url_for('main.students'))


@main_bp.route('/teachers/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_teacher(id):
    teacher = services.get_teacher(CATALOG, id).items[0]
    flash(services.delete_entity(
        CATALOG,
        teacher,
        'teachers',
        f'Удален преподаватель: {teacher.name}'
    ))
    return redirect(url_for('main.teachers'))


@main_bp.route('/disciplines/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_discipline(id):
    discipline = services.get_discipline(CATALOG, id).items[0]
    flash(services.delete_entity(
        CATALOG,
        discipline,
        'disciplines',
        f'удалена дисциплина: {discipline.name}'
    ))
    return redirect(url_for('main.disciplines'))


@main_bp.route('/classes/<int:id>/delete', methods=['POST'])
@jwt_required
def delete_class(id):
    classroom = services.get_class(CATALOG, id).items[0]
    flash(services.delete_entity(
        CATALOG,
        classroom,
        'classes',
        f'Удалена аудитория: {classroom.name}'
        ))
    return redirect(url_for('main.classes'))
