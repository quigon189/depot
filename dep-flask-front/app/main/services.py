import requests

CATALOG = "http://go-catalog:8080/"


def get_specialties():
    resp = requests.get(f"{CATALOG}/specialties/all")
    if resp.status_code == 200:
        specs = resp.json()
    else:
        specs = []

    for spec in specs:
        if 'groups' in spec:
            spec['groups_count'] = len(spec['groups'])
        else:
            spec['groups_count'] = 0

    fields = [
        {'key': 'code', 'label': 'Код', 'link': True},
        {'key': 'name', 'label': 'Наименование'},
        {'key': 'short_name', 'label': 'Короткое обозначение'},
        {'key': 'groups_count', 'label': 'Количество групп'}
    ]
    return {
        'items': specs,
        'fields': fields
    }


def get_specialty(id):
    resp = requests.get(f"{CATALOG}/specialties/{id}")
    if resp.status_code == 200:
        specialty = resp.json()
    else:
        return {'item': {}, 'fields': [], 'nested': []}

    fields = [
        {'key': 'code', 'label': 'Код'},
        {'key': 'name', 'label': 'Наименование'},
        {'key': 'short_name', 'label': 'Короткое обозначение'}
    ]

    if not ('groups' in specialty):
        specialty['groups'] = []

    for group in specialty['groups']:
        group['name'] = f'{specialty["short_name"]}-{group["number"]}'
        group['class_teacher'] = f'{group["class_teacher"]["last_name"]} {group["class_teacher"]["first_name"][0]}. {group["class_teacher"]["middle_name"][0]}.'
        if 'students' in group:
            group['students_count'] = len(group['students'])
        else:
            group['students_count'] = 0

    nested = [
        {
            'label': 'Группы',
            'type': 'groups',
            'fields': [
                {'key': 'name', 'label': 'Номер', 'link': True},
                {'key': 'year_formed', 'label': 'Год набора'},
                {'key': 'class_teacher', 'label': 'Классный руководитель'},
                {'key': 'students_count', 'label': 'Количество студентов'}
            ],
            'items': specialty['groups'],
        }
    ]
    return {
        'item': specialty,
        'fields': fields,
        'nested': nested
    }


def get_groups():
    resp = requests.get(f'{CATALOG}/groups/all')
    if resp.status_code == 200:
        groups = resp.json()
    else:
        groups = []

    for group in groups:
        if 'specialty' in group:
            group['name'] = f"{group['specialty']['short_name']}-{group['number']}"
        else:
            group['name'] = group['number']
        group["class_teacher"] = f"{group['class_teacher']['last_name']} {group['class_teacher']['first_name'][0]}. {group['class_teacher']['middle_name'][0]}."
        if 'students' in group:
            group['students_count'] = len(group['students'])
        else:
            group['students_count'] = 0
        if 'specialty' in group:
            group['specialty'] = f"{group['specialty']['code']} {group['specialty']['name']}"
        else:
            group['specialty'] = "-"

    fields = [
        {'key': 'name', 'label': 'Наименование', 'link': True},
        {'key': 'specialty', 'label': 'Специальность'},
        {'key': 'year_formed', 'label': 'Год набора'},
        {'key': 'class_teacher', 'label': 'Классный руководитель'},
        {'key': 'students_count', 'label': 'Количество студентов'}
    ]

    return {
        'items': groups,
        'fields': fields
    }


def get_group(id):
    resp = requests.get(f"{CATALOG}/groups/{id}")
    if resp.status_code == 200:
        group = resp.json()
    else:
        return {'item': {}, 'fields': [], 'nested': []}

    group['name'] = f"{group['specialty']['short_name']}-{group['number']}"
    group["class_teacher"] = f"{group['class_teacher']['last_name']} {group['class_teacher']['first_name']} {group['class_teacher']['middle_name']}"
    group['specialty'] = f"{group['specialty']['code']} {group['specialty']['name']}"

    fields = [
        {'key': 'specialty', 'label': 'Специальность'},
        {'key': 'year_formed', 'label': 'Год набора'},
        {'key': 'class_teacher', 'label': 'Классный руководитель'}
    ]

    if not ('students' in group):
        group['students'] = []

    for student in group['students']:
        student['name'] = f'{student["last_name"]} {student["first_name"]} {student["middle_name"]}'

    nested = [
        {
            'label': 'Студенты',
            'type': 'students',
            'fields': [
                {'key': 'name', 'label': 'ФИО', 'link': True},
                {'key': 'birth_date', 'label': 'День рождения'},
                {'key': 'phone', 'label': 'Номер телефона'},
            ],
            'items': group['students']
        }
    ]
    return {
        'item': group,
        'fields': fields,
        'nested': nested
    }


def get_students():
    resp = requests.get(f'{CATALOG}/students/all')
    if resp.status_code == 200:
        students = resp.json()
    else:
        students = []

    for student in students:
        student['name'] = f"{student['last_name']} {student['first_name']} {student['middle_name']}"
        student['group_number'] = f"{student['group']['specialty']['short_name']}-{student['group']['number']}"

    fields = [
        {'key': 'name', 'label': 'ФИО', 'link': True},
        {'key': 'group_number', 'label': 'Номер группы'},
        {'key': 'birth_date', 'label': 'Дата рождения'},
        {'key': 'phone', 'label': 'Номер телефона'}
    ]

    return {
        'items': students,
        'fields': fields
    }


def get_student(id):
    resp = requests.get(f"{CATALOG}/students/{id}")
    if resp.status_code == 200:
        student = resp.json()
    else:
        return {'item': {}, 'fields': [], 'nested': []}

    student['name'] = f"{student['last_name']} {student['first_name']} {student['middle_name']}"
    student['group_number'] = f"{student['group']['specialty']['short_name']}-{student['group']['number']}"

    fields = [
        {'key': 'group_number', 'label': 'Группа'},
        {'key': 'birth_date', 'label': 'Дата рождения'},
        {'key': 'phone', 'label': 'Номер телефона'}
    ]

    return {
        'item': student,
        'fields': fields,
        'nested': []
    }


def get_teachers():
    resp = requests.get(f"{CATALOG}/teachers/all")
    if resp.status_code == 200:
        teachers = resp.json()
    else:
        teachers = []

    for teacher in teachers:
        teacher['name'] = f"{teacher['last_name']} {teacher['first_name']} {teacher['middle_name']}"

    fields = [
        {'key': 'name', 'label': 'ФИО', 'link': True},
        {'key': 'birth_date', 'label': 'Дата рождения'},
        {'key': 'phone', 'label': 'Номер телефона'}
    ]

    return {
        'items': teachers,
        'fields': fields
    }


def get_teacher(id):
    resp = requests.get(f"{CATALOG}/teachers/{id}")
    if resp.status_code == 200:
        teacher = resp.json()
    else:
        return {'item': {}, 'fields': [], 'nested': []}

    teacher['name'] = f"{teacher['last_name']} {teacher['first_name']} {teacher['middle_name']}"

    fields = [
        {'key': 'birth_date', 'label': 'Дата рождения'},
        {'key': 'phone', 'label': 'Номер телефона'}
    ]

    if not ('groups' in teacher):
        teacher['groups'] = []

    for group in teacher['groups']:
        group['name'] = f"{group['specialty']['short_name']}-{group['number']}"

    nested = [
        {
            'label': 'Группы',
            'type': 'groups',
            'fields': [
                {'key': 'name', 'label': 'Наименование', 'link': True},
                {'key': 'year_formed', 'label': 'Год набора'},
            ],
            'items': teacher['groups']
        }
    ]

    return {
        'item': teacher,
        'fields': fields,
        'nested': nested
    }


def get_disciplines():
    resp = requests.get(f'{CATALOG}/disciplines/all')
    if resp.status_code == 200:
        disciplines = resp.json()
    else:
        disciplines = []

    for disc in disciplines:
        disc['name'] = f'{disc["code"]}.{disc["name"]}'
        disc['group_number'] = f"{disc['group']['specialty']['short_name']}-{disc['group']['number']}"
        disc['hours'] = f"{disc['hours']} ч."

    fields = [
        {'key': 'name', 'label': 'Наименование', 'link': True},
        {'key': 'group_number', 'label': 'Номер группы'},
        {'key': 'semester', 'label': 'Семестр'},
        {'key': 'hours', 'label': 'Нагрузка'},
    ]

    return {
        'items': disciplines,
        'fields': fields
    }


def get_discipline(id):
    resp = requests.get(f"{CATALOG}/disciplines/{id}")
    if resp.status_code == 200:
        discipline = resp.json()
    else:
        return {'item': {}, 'fields': [], 'nested': []}

    discipline['name'] = f"{discipline['code']}.{discipline['name']}"
    discipline['group_number'] = f"{discipline['group']['specialty']['short_name']}-{discipline['group']['number']}"

    fields = [
        {'key': 'group_number', 'label': 'Номер группы'},
        {'key': 'semester', 'label': 'Семестр'},
        {'key': 'hours', 'label': 'Нагрузка'}
    ]

    nested = []

    return {
        'item': discipline,
        'fields': fields,
        'nested': nested
    }


def get_classes():
    resp = requests.get(f"{CATALOG}/classes/all")
    if resp.status_code == 200:
        classes = resp.json()
    else:
        classes = []

    for c in classes:
        c['class_teacher'] = f"{c['teacher']['last_name']} {c['teacher']['first_name'][0]}. {c['teacher']['middle_name'][0]}."

    fields = [
        {'key': 'number', 'label': 'Номер', 'link': True},
        {'key': 'name', 'label': 'Наименование'},
        {'key': 'class_teacher', 'label': 'Заведующий'},
        {'key': 'capacity', 'label': 'Вместительность'},
        {'key': 'equipment', 'label': 'Оснащение'},
    ]

    return {
        'items': classes,
        'fields': fields
    }


def get_class(id):
    resp = requests.get(f"{CATALOG}/classes/{id}")
    if resp.status_code == 200:
        cl = resp.json()
    else:
        return {'item': {}, 'fields': [], 'nested': []}

    cl['name'] = f"{cl['number']} \"{cl['name']}\""
    cl['class_teacher'] = f"{cl['teacher']['last_name']} {cl['teacher']['first_name'][0]}. {cl['teacher']['middle_name'][0]}."

    fields = [
        {'key': 'class_teacher', 'label': 'Заведующий'},
        {'key': 'type', 'label': 'Тип'},
        {'key': 'capacity', 'label': 'Вместимтельность'},
        {'key': 'equipment', 'label': 'Оснащение'}
    ]

    nested = []

    return {
        'item': cl,
        'fields': fields,
        'nested': nested
    }


def send_specialty(form):
    url = f"{CATALOG}/specialties"

    specialty = {
        'code': form.code.data,
        'name': form.name.data,
        'short_name': form.short_name.data
    }

    headers = {
        'Content-Type': 'application/json',
    }

    return requests.post(url, json=[specialty], headers=headers)


def send_group(form):
    url = f"{CATALOG}/groups"

    group = {
        'number': int(form.number.data),
        'year_formed': int(form.year_formed.data),
        'spec_id': int(form.spec_id.data),
        'class_teacher_id': int(form.class_teacher_id.data)
    }

    headers = {
        'Content-Type': 'application/json'
    }

    return requests.post(url, json=[group], headers=headers)


def send_student(form):
    url = f"{CATALOG}/students"

    student = {
        'last_name': form.last_name.data,
        'first_name': form.first_name.data,
        'middle_name': form.middle_name.data,
        'birth_date': form.birth_date.data,
        'phone': form.phone.data,
        'group_id': int(form.group_id.data)
    }

    headers = {
        'Content-Type': 'application/json'
    }

    return requests.post(url, json=[student], headers=headers)


def send_teacher(form):
    url = f"{CATALOG}/teachers"

    teacher = {
        'last_name': form.last_name.data,
        'first_name': form.first_name.data,
        'middle_name': form.middle_name.data,
        'birth_date': form.birth_date.data,
        'phone': form.phone.data,
    }

    headers = {
        'Content-Type': 'application/json'
    }

    return requests.post(url, json=[teacher], headers=headers)


def send_discipline(form):
    url = f"{CATALOG}/disciplines"

    disciplines = {
        'code': form.code.data,
        'name': form.name.data,
        'semester': int(form.semester.data),
        'hours': int(form.hours.data),
        'group_id': int(form.group_id.data)
    }

    headers = {
        'Content-Type': 'application/json'
    }

    return requests.post(url, json=[disciplines], headers=headers)


def send_class(form):
    url = f"{CATALOG}/classes"

    cl = {
        'number': int(form.number.data),
        'name': form.name.data,
        'type': form.type.data,
        'capacity': int(form.capacity.data),
        'equipment': form.equipment.data,
        'teacher_id': int(form.teacher_id.data)
    }

    headers = {
        'Content-Type': 'application/json'
    }

    return requests.post(url, json=[cl], headers=headers)


def update_entity(entity, entity_type):
    url = f"{CATALOG}/{entity_type}"

    headers = {
        'Content-Type': 'application/json'
    }

    return requests.put(url, json=entity, headers=headers)


def delete_entity(entity, entity_type):
    url = f"{CATALOG}/{entity_type}/{entity['id']}"

    headers = {
        'Content-Type': 'application/json'
    }

    return requests.delete(url, headers=headers)
