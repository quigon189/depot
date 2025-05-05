import requests

CATALOG = "http://go-catalog:8080/"


def get_data(path):
    req = requests.get(f"{CATALOG}{path}")

    if req.status_code == 200:
        return req.json()
    else:
        return []

def get_specialties():
    specs = get_data('specialties/all')
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
    req = requests.get(f"{CATALOG}/specialties/{id}")
    if req.status_code == 200:
        specialty = req.json()
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


def get_specialties_old():
    specs = get_data('specialties')
    result = []
    for spec in specs:
        try:
            row = {}
            row["#"] = spec["id"]
            row["Код специальности"] = spec["code"]
            row["Наименование специальности"] = spec["name"]
            row["Короткое обозначение"] = spec["short_name"]
            if "groups" in spec:
                groups = []
                for group in spec["groups"]:
                    g = {}
                    g["#"] = group["id"]
                    g["Наименование"] = f"{spec['short_name']}-{group['number']}"
                    g["Год набора"] = group['year_formed']
                    if 'class_teacher' in group:
                        g["Классный руководитель"] = f"{group['class_teacher']['last_name']} {group['class_teacher']['first_name'][0]}. {group['class_teacher']['middle_name'][0]}."
                    else:
                        g["Классный руководитель"] = "не назначен"
                    groups.append(g)
                row["Группы"] = groups
            else:
                row["Группы"] = "Отсутствуют"
            result.append(row)
        except Exception as e:
            print(f"Error ({e}) show spec: {spec}")

    return result


def get_groups():
    groups = get_data('groups')
    result = []
    for group in groups:
        try:
            row = {}
            row["#"] = group["id"]
            row["Наименование"] = f"{group['specialty']['short_name']}-{group['number']}"
            row["Год набора"] = group["year_formed"]
            if 'class_teacher' in group:
                row["Классный руководитель"] = f"{group['class_teacher']['last_name']} {group['class_teacher']['first_name']} {group['class_teacher']['middle_name']}"
            else:
                row["Классный руководитель"] = "не назначен"
            if 'students' in group:
                students = []
                for student in group['students']:
                    s = {}
                    s["#"] = student["id"]
                    s["ФИО"] = f"{student['last_name']} {student['first_name']} {student['middle_name']}"
                    s["Дата рождения"] = student["birth_date"]
                    s["Номер телефона"] = student["phone"]
                    students.append(s)

                row["Студенты"] = students
            else:
                row["Студенты"] = "-"
            result.append(row)

        except Exception as e:
            print(f"Error ({e}) match group: {group} ")

    return result


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


