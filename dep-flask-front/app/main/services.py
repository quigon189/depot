from typing import List, Type
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

    def get_nested(self, cls: Type['Presenter'], attribute: str) -> 'Presenter':
        nested = cls()
        nested_items = getattr(self.items[0], attribute)
        if nested_items:
            for item in nested_items:
                nested.add_item(item)
        return nested

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


def get_group(api_url: str, id: int) -> GroupsPresenter:
    api = f"{api_url}/groups/{id}"
    return GroupsPresenter().get_items(api)


def get_student(api_url: str, id: int) -> StudentsPresenter:
    api = f"{api_url}/students/{id}"
    return StudentsPresenter().get_items(api)


def get_teacher(api_url: str, id: int) -> TeachersPresenter:
    api = f"{api_url}/teachers/{id}"
    return TeachersPresenter().get_items(api)


def get_discipline(api_url: str, id: int):
    api = f"{api_url}/disciplines/{id}"
    return DisciplinesPresenter().get_items(api)


def get_class(api_url: str, id: str):
    api = f"{api_url}/classes/{id}"
    return ClassesPresenter().get_items(api)


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
