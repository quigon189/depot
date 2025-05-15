from typing import Dict, List, Optional
from pydantic import BaseModel
import requests
from app.main.models import SpecialtyWithGroups, GroupWithStudents
from app.main.models import StudentWithGroup, Teacher, Discipline
from app.main.models import Classroom

CATALOG = "http://go-catalog:8080/"


class Presenter:
    """Базовый класс представленний сущностей для отображения в шаблонах"""

    def __init__(self, model_type: type, api_path: str):
        self.type = model_type
        self.items: List[BaseModel] = []
        self.nested: List[Presenter] = []
        self.errors: List[str] = []
        self.fields: List[Dict] = []
        self.label: str = "Заголовок"
        self.entity: str = "index"
        if api_path:
            get_entity(self, api_path)

    def set_entity(self, entity: str):
        self.entity = entity

    def set_header(self, label: str):
        self.label = label

    def set_fields(self, fields: List[Dict]):
        self.fields = fields

    def add_item(self, item: BaseModel):
        self.items.append(item)

    def add_nested_items(self, p):
        self.nested.append(p)

    def add_error(self, error: str):
        self.errors.append(error)


def get_entity(presenter: Presenter, api_path: str):
    resp = requests.get(api_path)
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, list):
            for item in data:
                try:
                    presenter.add_item(presenter.type(**item))
                except ValueError as e:
                    print(f"Ошибка валидации {e}")
                    presenter.add_error(f"Ошибка валидации {e}")
        elif isinstance(data, dict):
            try:
                presenter.add_item(presenter.type(**data))
            except ValueError as e:
                print(f"Ошибка валидации {e}")
                presenter.add_error(f"Ошибка валидации {e}")
    else:
        print(f"Ошибка запроса к API. Код ответа {resp.status_code}")
        presenter.add_error(
            f"Ошибка запроса к API. Код ответа {resp.status_code}")


def get_entity_from_entity(presenter_in: Presenter, presenter_out: Presenter):
    item = presenter_in.items[0].model_dump()
    for i in item[presenter_out.entity]:
        presenter_out.add_item(i)


def get_specialties(api_url: str) -> Presenter:
    specs = Presenter(SpecialtyWithGroups, f"{api_url}/specialties/all")
    specs.set_header("Специальности")
    specs.set_entity("specialties")
    specs.set_fields(
        [
            {'key': 'code', 'label': 'Код', 'link': True},
            {'key': 'name', 'label': 'Наименование'},
            {'key': 'short_name', 'label': 'Короткое обозначение'},
            {'key': 'groups_count', 'label': 'Количество групп'}
        ]
    )
    return specs


def get_specialty(api_url: str, id: int) -> Presenter:
    specialties = Presenter(StudentWithGroup, f'{api_url}/specialties/{id}')
    specialties.set_fields([
        {'key': 'code', 'label': 'Код'},
        {'key': 'name', 'label': 'Наименование'},
        {'key': 'short_name', 'label': 'Короткое обозначение'}
    ])

    return specialties


def get_groups(api_url: str) -> Presenter:
    groups = Presenter(GroupWithStudents, f'{api_url}/groups/all')
    groups.set_header('Группы')
    groups.set_entity('groups')
    groups.set_fields([
        {'key': 'name', 'label': 'Наименование', 'link': True},
        {'key': 'specialty_name', 'label': 'Специальность'},
        {'key': 'year_formed', 'label': 'Год набора'},
        {'key': 'class_teacher_name', 'label': 'Классный руководитель'},
        {'key': 'students_count', 'label': 'Количество студентов'}
    ])

    return groups


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


def get_students(api_url: str) -> Presenter:
    students = Presenter(StudentWithGroup, f'{api_url}/students/all')
    students.set_header('Студенты')
    students.set_entity('students')
    students.set_fields([
        {'key': 'name', 'label': 'ФИО', 'link': True},
        {'key': 'group_name', 'label': 'Номер группы'},
        {'key': 'birth_date', 'label': 'Дата рождения'},
        {'key': 'phone', 'label': 'Номер телефона'}
    ])

    return students


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


def get_teachers(api_url: str) -> Presenter:
    teachers = Presenter(Teacher, f'{api_url}/teachers/all')
    teachers.set_header('Преподаватели')
    teachers.set_entity('teachers')
    teachers.set_fields([
        {'key': 'name', 'label': 'ФИО', 'link': True},
        {'key': 'birth_date', 'label': 'Дата рождения'},
        {'key': 'phone', 'label': 'Номер телефона'}
    ])
    return teachers


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


def get_disciplines(api_url: str) -> Presenter:
    disciplines = Presenter(Discipline, f"{api_url}/disciplines/all")
    disciplines.set_header('Дисциплины')
    disciplines.set_entity('disciplines')
    disciplines.set_fields([
        {'key': 'view_name', 'label': 'Наименование', 'link': True},
        {'key': 'group_name', 'label': 'Номер группы'},
        {'key': 'semester', 'label': 'Семестр'},
        {'key': 'hours', 'label': 'Нагрузка'},
    ])

    return disciplines


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


def get_classes(api_url: str) -> Presenter:
    classes = Presenter(Classroom, f"{api_url}/classes/all")
    classes.set_header('Аудитории')
    classes.set_entity('classes')
    classes.set_fields([
        {'key': 'number', 'label': 'Номер', 'link': True},
        {'key': 'name', 'label': 'Наименование'},
        {'key': 'class_teacher_name', 'label': 'Заведующий'},
        {'key': 'capacity', 'label': 'Вместительность'},
        {'key': 'equipment', 'label': 'Оснащение'},
    ])

    return classes


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
