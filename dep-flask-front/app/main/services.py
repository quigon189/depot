import requests

CATALOG = "http://go-catalog:8080/"


def get_data(path):
    resp = requests.get(f"{CATALOG}{path}")

    if resp.status_code == 200:
        return resp.json()
    else:
        return []


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
    return specs, fields


def get_specialty(id):
    resp = requests.get(f"{CATALOG}/specialties/{id}")
    if resp.status_code == 200:
        specialty = resp.json()
    else:
        return {}, [], []

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
    return specialty, fields, nested


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

    return groups, fields


def get_group(id):
    resp = requests.get(f"{CATALOG}/groups/{id}")
    if resp.status_code == 200:
        group = resp.json()
    else:
        return {}, [], []

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
    return group, fields, nested


def get_students():
    students = get_data('students')
    result = []
    for student in students:
        try:
            s = {}
            s["#"] = student["id"]
            s["ФИО"] = f"{student['last_name']} {student['first_name']} {student['middle_name']}"
            s["Дата рождения"] = student["birth_date"]
            s["Номер телефона"] = student["phone"]
            if 'specialty' in student['group']:
                s["Группа"] = f"{student['group']['specialty']['short_name']}-{student['group']['number']}"
            else:
                s['Группа'] = student['group']['number']
            result.append(s)
        except Exception as e:
            print(f"Error ({e}) with show student: {student}")

    return result


def get_disciplines():
    disciplines = get_data('disciplines')
    result = []
    for discipline in disciplines:
        d = {}
        d["#"] = discipline["id"]
        d["Группа"] = discipline["group"]["number"]
        d["Код"] = discipline["code"]
        d["Наименование"] = discipline["name"]
        d["Семестр"] = discipline["semester"]
        d["Нагрузка"] = f"{discipline['hours']} ч."

        result.append(d)

    return result


def get_teachers():
    teachers = get_data('teachers')
    result = []
    for teacher in teachers:
        t = {}
        t["#"] = teacher["id"]
        t["ФИО"] = f"{teacher['last_name']} {teacher['first_name']} {teacher['middle_name']}"
        t["Дата рождения"] = teacher["birth_date"]
        t["Номер телефона"] = teacher["phone"]
        if 'groups' in teacher:
            groups = []
            for group in teacher["groups"]:
                g = {}
                g["#"] = group["id"]
                g["Номер"] = group["number"]
                g["Год набора"] = group["year_formed"]
                groups.append(g)
            t["Группы"] = groups
        else:
            t["Группы"] = "-"
        result.append(t)

    return result


def get_classes():
    classes = get_data('classes')
    result = []
    for cl in classes:
        c = {}
        c["#"] = cl["id"]
        c["Номер"] = cl["number"]
        c["Наименование"] = cl["name"]
        c["Тип"] = cl["type"]
        c["Вместимость"] = f"{cl['capacity']} чел."
        c["Оснащение"] = cl["Equipment"]
        c["Заведующий"] = f"{cl['teacher']['last_name']} {cl['teacher']['first_name'][0]}. {cl['teacher']['middle_name'][0]}."

        result.append(c)
    return result
