from typing import Annotated, Literal, List, Optional, Union
from pydantic import BaseModel, Field

Entity = Union['Specialty', 'Group', 'Student',
               'Teacher', 'Discipline', 'Classroom', 'BaseEntity']

BirthDate = Annotated[
    str,
    Field(..., pattern=r'^[0-9]{4}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1])$')
]

Phone = Annotated[
    str,
    Field(..., pattern=r'^(\+\d\(\d{3}\)\d{3}-\d{2}-\d{2})?$')
]


class BaseEntity(BaseModel):
    id: Optional[int] = Field(None, title='ID')


class Specialty(BaseEntity):
    code: str = Field(..., pattern=r'\d{2}\.\d{2}\.\d{2}', title='Код')
    name: str = Field(..., max_length=200, title='Название', examples=[
                      "Системное и сетевое администрирование"])
    short_name: str = Field(..., max_length=8,
                            title='Короткое обозначение', examples=["СА"])

    groups: Optional[List["Group"]] = None

    @property
    def view_name(self):
        return f"{self.code} {self.name}"

    @property
    def groups_count(self) -> int:
        if self.groups:
            return len(self.groups)
        return 0

    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'short_name': self.short_name
        }


class Teacher(BaseEntity):
    first_name: str = Field(..., title='Имя', examples=['Иван'])
    middle_name: str = Field(..., title='Отчество', examples=['Иванович'])
    last_name: str = Field(..., title='Фамилия', examples=['Иванов'])
    birth_date: BirthDate = Field(..., title='День рождения')
    phone: Optional[Phone] = Field(..., title='Номер телефона')

    groups: Optional[List["Group"]] = None
    classes: Optional[List["Classroom"]] = None

    @property
    def name(self) -> str:
        return "{} {} {}".format(
            self.last_name,
            self.first_name,
            self.middle_name
        )

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'phone': self.phone
        }


class Student(BaseEntity):
    first_name: str = Field(..., title='Имя', examples=['Иван'])
    middle_name: str = Field(..., title='Отчество', examples=['Иванович'])
    last_name: str = Field(..., title='Фамилия', examples=['Иванов'])
    birth_date: BirthDate = Field(..., title='День рождения')
    phone: Optional[Phone] = Field(..., title='Номер телефона')

    group_id: int
    group: Optional["Group"] = Field(None, title='Группа')

    @property
    def name(self) -> str:
        return "{} {} {}".format(
            self.last_name,
            self.first_name,
            self.middle_name
        )

    @property
    def group_name(self) -> str:
        if self.group:
            return self.group.name
        return "-"


class Group(BaseEntity):
    number: int = Field(..., gt=0, title='Номер')
    year_formed: int = Field(..., title='Год набора')

    spec_id: int
    specialty: Optional[Specialty] = Field(None, title='Специальность')

    class_teacher_id: int
    class_teacher: Optional[Teacher] = Field(
        None, title='Классный руководитель')

    students: Optional[List[Student]] = None
    disciplines: Optional[List["Discipline"]] = None

    @property
    def name(self) -> str:
        if self.specialty:
            return f"{self.specialty.short_name}-{self.number}"
        return f"{self.number}"

    @property
    def specialty_name(self) -> str:
        if self.specialty:
            return "{} {}".format(
                self.specialty.code,
                self.specialty.name
            )
        return "-"

    @property
    def class_teacher_name(self) -> str:
        if self.class_teacher:
            return "{} {}. {}.".format(
                self.class_teacher.last_name,
                self.class_teacher.first_name[0],
                self.class_teacher.middle_name[0]
            )
        return "-"

    @property
    def students_count(self) -> int:
        return len(self.students) if self.students else 0


class Discipline(BaseEntity):
    code: str = Field(..., title='Код')
    name: str = Field(..., title='Название')
    semester: int = Field(..., gt=0, le=8, title='Семестр')
    hours: int = Field(..., gt=0, title='Максимальная нагрузка')

    group_id: int
    group: Optional[Group] = Field(None, title='Группа')

    @property
    def view_name(self) -> str:
        return f"{self.code}.{self.name}"

    @property
    def group_name(self) -> str:
        if self.group:
            return self.group.name
        return "-"


class Classroom(BaseEntity):
    number: int = Field(..., gt=0, title='Номер')
    name: str = Field(..., title='Название', examples=['Операционные системы'])
    type: Literal['Кабинет', 'Лаборатория',
                  'Полигон'] = Field(..., title='Тип')
    capacity: int = Field(..., title='Вместительность')
    equipment: str = Field(..., title='Оснащение')

    teacher_id: int
    teacher: Optional[Teacher] = Field(None, title='Преподаватель')

    @property
    def class_teacher_name(self) -> str:
        if self.teacher:
            return "{} {}. {}.".format(
                self.teacher.last_name,
                self.teacher.first_name[0],
                self.teacher.middle_name[0]
            )
        return "-"


Specialty.model_rebuild()
Group.model_rebuild()
Student.model_rebuild()
Teacher.model_rebuild()
Discipline.model_rebuild()
Classroom.model_rebuild()
