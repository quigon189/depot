import requests

CATALOG = "http://go-catalog:8080/"


def get_specialties():
    resp = requests.get(f"{CATALOG}/specialties/all")
    if resp.status_code == 200:
        specs = resp.json()
    else:
        specs = []

    for spec in specs:
        spec['groups_count'] = len(spec['groups'])

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
        group['name'] = f"{group['specialty']['short_name']}-{group['number']}"
        group["class_teacher"] = f"{group['class_teacher']['last_name']} {group['class_teacher']['first_name'][0]}. {group['class_teacher']['middle_name'][0]}."
        if 'students' in group:
            group['students_count'] = len(group['students'])
        else:
            group['students_count'] = 0
        group['specialty'] = f"{group['specialty']['code']} {group['specialty']['name']}"

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
        student['group_number'] = student['group']['number']

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
    student['group_number'] = student['group']['number']

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
        group['name'] = group['number']

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
        disc['group_number'] = disc['group']['number']
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
    discipline['group_number'] = discipline['group']['number']

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
        {'key': 'Equipment', 'label': 'Оснащение'},
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

    fields = [
        {'key': 'class_teacher', 'label': 'Заведующий'},
        {'key': 'type', 'label': 'Тип'},
        {'key': 'capacity', 'label': 'Вместимтельность'},
        {'key': 'Equipment', 'label': 'Оснащение'}
    ]

    nested = []

    return {
        'item': cl,
        'fields': fields,
        'nested': nested
    }
