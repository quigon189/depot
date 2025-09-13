from typing import List, Tuple, Type, Any
from app.main.models import BaseEntity, Specialty, Group, Student, Entity
from app.main.models import Teacher, Discipline, Classroom


import requests


class Presenter:
    """Базовый класс представленний сущностей для отображения в шаблонах"""

    def __init__(self):
        self.type: Type[Entity]
        self.items: List[Any] = []
        self.errors: List[str] = []

    def add_item(self, item: Entity):
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


def send_entity(url: str, data: List, text: str):
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        return text, 'success'

    return "Ошибка при добавлении: код {} текст {}".format(
        response.status_code,
        response.json()
    ), 'danger'


def send_specialty(api_url: str, form: 'SpecialityForm'):
    return send_entity(
        f"{api_url}/specialties",
        [{
            'code': form.code.data,
            'name': form.name.data,
            'short_name': form.short_name.data
        }],
        "Добавлена специальность: {} {}".format(
            form.code.data,
            form.name.data
        )
    )


def send_group(api_url: str, form: 'GroupForm') -> Tuple[str, str]:
    return send_entity(
        f"{api_url}/groups",
        [{
            'number': form.number.data,
            'year_formed': form.year_formed.data,
            'spec_id': int(form.spec_id.data),
            'class_teacher_id': int(form.class_teacher_id.data)
        }],
        f"Добавлена группа: {form.number.data}"
    )


def send_student(api_url: str, form: 'StudentForm') -> Tuple[str, str]:
    return send_entity(
        f"{api_url}/students",
        [{
            'last_name': form.last_name.data,
            'first_name': form.first_name.data,
            'middle_name': form.middle_name.data,
            'birth_date': form.birth_date.data,
            'phone': form.phone.data,
            'group_id': int(form.group_id.data)
        }],
        "Добавлен студент {} {}. {}.".format(
            form.last_name.data,
            form.first_name.data[0] if form.first_name.data else "",
            form.middle_name.data[0] if form.middle_name.data else ""
        )
    )


def send_teacher(api_url: str, form: 'TeacherForm') -> Tuple[str, str]:
    return send_entity(
        f"{api_url}/teachers",

        [{
            'last_name': form.last_name.data,
            'first_name': form.first_name.data,
            'middle_name': form.middle_name.data,
            'birth_date': form.birth_date.data,
            'phone': form.phone.data,
        }],
        "Добавлен преподаватель {} {}. {}.".format(
            form.last_name.data,
            form.first_name.data[0] if form.first_name.data else "",
            form.middle_name.data[0] if form.middle_name.data else ""
        )
    )


def send_discipline(api_url: str, form: 'DisciplineForm') -> Tuple[str,str]:
    return send_entity(
        f"{api_url}/disciplines",
        [{
            'code': form.code.data,
            'name': form.name.data,
            'semester': form.semester.data,
            'hours': form.hours.data,
            'group_id': int(form.group_id.data)
        }],
        "Добавлена дисциплина:\n{}.{}".format(
            form.code.data,
            form.name.data
        )
    )


def send_class(api_url: str, form: 'ClassForm') -> Tuple[str, str]:
    return send_entity(
        f"{api_url}/classes",
        [{
            'number': form.number.data,
            'name': form.name.data,
            'type': form.type.data,
            'capacity': form.capacity.data,
            'equipment': form.equipment.data,
            'teacher_id': int(form.teacher_id.data)
        }],
        "Добавлена аудитория:\n{} {}".format(
            form.number.data,
            form.name.data
        )
    )


def update_entity(url: str, entity: BaseEntity, text: str) -> Tuple[str, str]:
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.put(url, json=entity.model_dump(), headers=headers)
    if response.status_code == 200:
        return text, 'success'
    else:
        return "Ошибка обновления: код {} ошибка {}".format(
            response.status_code,
            response.json()
        ), 'danger'


def update_specialty(api_url: str, id: int, form: 'SpecialityForm') -> Tuple[str, str]:
    try:
        specialty = Specialty(
            id=id,
            code=form.code.data,
            name=form.name.data,
            short_name=form.short_name.data
        )
    except ValueError as e:
        return f"Ошибка валидации данных: {e}", 'danger'

    return update_entity(
        f"{api_url}/specialties",
        specialty,
        f"Обнавлена специальность:\n{specialty.view_name}"
    )


def update_group(api_url: str, id: int, form: 'GroupForm') -> Tuple[str, str]:
    try:
        group = Group(
            id=id,
            number=form.number.data,
            year_formed=form.year_formed.data,
            spec_id=form.spec_id.data,
            class_teacher_id=form.class_teacher_id.data
        )
    except ValueError as e:
        return f"Ошибка валидации данных: {e}", 'danger'

    return update_entity(
        f"{api_url}/groups",
        group,
        f"Обнавлена группа:\n{group.name}"
    )


def update_student(api_url: str, id: int, form: 'StudentForm') -> Tuple[str, str]:
    try:
        student = Student(
            id=id,
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            last_name=form.last_name.data,
            birth_date=form.birth_date.data,
            phone=form.phone.data,
            group_id=form.group_id.data
        )
    except ValueError as e:
        return f"Ошибка валидации данных: {e}", 'danger'

    return update_entity(
        f"{api_url}/students",
        student,
        f"Обнавлен студент:\n{student.name}"
    )


def update_teacher(api_url: str, id: int, form: 'TeacherForm') -> Tuple[str, str]:
    try:
        teacher = Teacher(
            id=id,
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            last_name=form.last_name.data,
            birth_date=form.birth_date.data,
            phone=form.phone.data,
        )
    except ValueError as e:
        return f"Ошибка валидации данных: {e}", 'danger'

    return update_entity(
        f"{api_url}/teachers",
        teacher,
        f"Обнавлен преподаватель:\n{teacher.name}"
    )


def update_discipline(api_url: str, id: int, form: 'DisciplineForm') -> Tuple[str, str]:
    try:
        discipline = Discipline(
            id=id,
            code=form.code.data,
            name=form.name.data,
            semester=form.semester.data,
            hours=form.hours.data,
            group_id=form.group_id.data
        )
    except ValueError as e:
        return f"Ошибка валидации данных: {e}", 'danger'

    return update_entity(
        f"{api_url}/disciplines",
        discipline,
        f"Обнавлена дисциплина:\n{discipline.name}"
    )


def update_classroom(api_url: str, id: int, form: 'ClassForm') -> Tuple[str, str]:
    try:
        classroom = Classroom(
            id=id,
            number=form.number.data,
            name=form.name.data,
            type=form.type.data,
            capacity=form.capacity.data,
            equipment=form.equipment.data,
            teacher_id=form.teacher_id.data
        )
    except ValueError as e:
        return f"Ошибка валидации данных: {e}", 'danger'

    return update_entity(
        f"{api_url}/classes",
        classroom,
        f"Обнавлена аудитория:\n{classroom.name}"
    )


def delete_entity(api_url: str, entity: BaseEntity, entity_type, text: str) -> tuple:
    url = f"{api_url}/{entity_type}/{entity.id}"

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return text, 'success'
    else:
        return f"Ошибка удаления: код {response.status_code}", 'danger'
