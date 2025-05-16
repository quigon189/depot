from typing import List
from pydantic import BaseModel
import requests
from app.main.models import BaseEntity, Specialty, Group, Student
from app.main.models import Teacher, Discipline, Classroom


CATALOG = "http://go-catalog:8080/"


class Presenter:
    """Базовый класс представленний сущностей для отображения в шаблонах"""

    def __init__(self):
        self.type: type
        self.items: List[BaseEntity] = []
        self.errors: List[str] = []

    def add_item(self, item: BaseEntity):
        self.items.append(item)

    def add_error(self, error: str):
        self.errors.append(error)

    def get_items(self, api_path: str):
        resp = requests.get(api_path)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                for item in data:
                    try:
                        self.add_item(self.type(**item))
                    except ValueError as e:
                        print(f"Ошибка валидации {e}")
                        self.add_error(f"Ошибка валидации {e}")
            elif isinstance(data, dict):
                try:
                    self.add_item(self.type(**data))
                except ValueError as e:
                    print(f"Ошибка валидации {e}")
                    self.add_error(f"Ошибка валидации {e}")
        else:
            print(f"Ошибка запроса к API. Код ответа {resp.status_code}")
            self.add_error(
                f"Ошибка запроса к API. Код ответа {resp.status_code}")

        return self


class PresenterField:

    def __init__(self, key: str, label: str, link: bool = False):
        self.key = key
        self.label = label
        self.link = link


class SpecialtiesPresenter(Presenter):
    type = Specialty
    label: str = "Специальности"
    entity: str = "specialties"
    fields: List[PresenterField] = [
        PresenterField('code', 'Код', True),
        PresenterField('name', 'Наименование'),
        PresenterField('short_name', 'Короткое обозначение'),
        PresenterField('groups_count', 'Количество групп')
    ]

    def get_groups(self) -> "GroupsPresenter":
        groups = GroupsPresenter()
        if self.items[0].groups:
            for g in self.items[0].groups:
                groups.add_item(g)
        return groups


class GroupsPresenter(Presenter):
    type = Group
    label: str = "Группы"
    entity: str = "groups"
    fields: List[PresenterField] = [
        PresenterField('name', 'Наименование', True),
        PresenterField('specialty_name', 'Специальность'),
        PresenterField('year_formed', 'Год набора'),
        PresenterField('class_teacher_name', 'Классный руководитель'),
        PresenterField('students_count', 'Количество студентов')
    ]

    def get_students(self) -> "StudentsPresenter":
        students = StudentsPresenter()
        if self.items[0].students:
            for s in self.items[0].students:
                students.add_item(s)
        return students

    def get_disciplines(self) -> "DisciplinesPresenter":
        disciplines = DisciplinesPresenter()
        if self.items[0].disciplines:
            for d in self.items[0].disciplines:
                disciplines.add_item(d)
        return disciplines


class StudentsPresenter(Presenter):
    type = Student
    label: str = "Студенты"
    entity: str = "students"
    fields: List[PresenterField] = [
        PresenterField('name', 'ФИО', True),
        PresenterField('group_name', 'Группа'),
        PresenterField('birth_date', 'Дата рождения'),
        PresenterField('phone', 'Номер телефона'),
    ]


class TeachersPresenter(Presenter):
    type = Teacher
    label: str = "Преподаватели"
    entity: str = "teachers"
    fields: List[PresenterField] = [
        PresenterField('name', 'ФИО', True),
        PresenterField('birth_date', 'Дата рождения'),
        PresenterField('phone', 'Номер телефона'),
    ]


class DisciplinesPresenter(Presenter):
    type = Discipline
    label: str = "Дисциплины"
    entity: str = "disciplines"
    fields: List[PresenterField] = [
        PresenterField('view_name', 'Название', True),
        PresenterField('group_name', 'Группа'),
        PresenterField('semester', 'Семестер'),
        PresenterField('hours', 'Нагрузка'),
    ]


class ClassesPresenter(Presenter):
    type = Classroom
    label: str = "Аудитории"
    entity: str = "classes"
    fields: List[PresenterField] = [
            PresenterField('number', 'Номер', True),
            PresenterField('name', 'Название'),
            PresenterField('class_teacher_name', 'Заведующий'),
            PresenterField('capacity', 'Вместительность'),
            PresenterField('equipment', 'Оснащение'),
            ]


def get_specialties(api_url: str) -> SpecialtiesPresenter:
    api = f"{api_url}/specialties/all"
    return SpecialtiesPresenter().get_items(api)


def get_groups(api_url: str) -> GroupsPresenter:
    api = f"{api_url}/groups/all"
    return GroupsPresenter().get_items(api)


def get_students(api_url: str) -> StudentsPresenter:
    api = f"{api_url}/students/all"
    return StudentsPresenter().get_items(api)


def get_teachers(api_url: str) -> TeachersPresenter:
    api = f'{api_url}/teachers/all'
    return TeachersPresenter().get_items(api)


def get_disciplines(api_url: str) -> DisciplinesPresenter:
    api = f"{api_url}/disciplines/all"
    return DisciplinesPresenter().get_items(api)


def get_classes(api_url: str) -> ClassesPresenter:
    api = f"{api_url}/classes/all"
    return ClassesPresenter().get_items(api)


def get_specialty(api_url: str, id: int) -> SpecialtiesPresenter:
    api = f"{api_url}/specialties/{id}"
    return SpecialtiesPresenter().get_items(api)


def get_group(api_url: str, id: int):
    api = f"{api_url}/groups/{id}"
    return GroupsPresenter().get_items(api)


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
