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
    id: int


class Specialty(BaseEntity):
    code: str = Field(..., pattern=r'\d{2}\.\d{2}\.\d{2}')
    name: str = Field(..., max_length=200, examples=[
                      "Системное и сетевое администрирование"])
    short_name: str = Field(..., max_length=8, examples=["СА"])

    groups: Optional[List["Group"]] = None

    @property
    def view_name(self):
        return f"{self.code} {self.name}"

    @property
    def groups_count(self) -> int:
        if self.groups:
            return len(self.groups)
        return 0


class Teacher(BaseEntity):
    first_name: str = Field(..., examples=['Иван'])
    middle_name: str = Field(..., examples=['Иванович'])
    last_name: str = Field(..., examples=['Иванов'])
    birth_date: BirthDate
    phone: Optional[Phone]

    groups: Optional[List["Group"]] = None
    classes: Optional[List["Classroom"]] = None

    @property
    def name(self) -> str:
        return "{} {} {}".format(
            self.last_name,
            self.first_name,
            self.middle_name
        )


class Student(BaseEntity):
    first_name: str = Field(..., examples=['Иван'])
    middle_name: str = Field(..., examples=['Иванович'])
    last_name: str = Field(..., examples=['Иванов'])
    birth_date: BirthDate
    phone: Optional[Phone]

    group_id: int
    group: Optional["Group"] = None

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
    number: int = Field(..., gt=0)
    year_formed: int

    spec_id: int
    specialty: Optional[Specialty] = None

    class_teacher_id: int
    class_teacher: Optional[Teacher] = None

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
    code: str
    name: str
    semester: int = Field(..., gt=0, le=8)
    hours: int = Field(..., gt=0)

    group_id: int
    group: Optional[Group] = None

    @property
    def view_name(self) -> str:
        return f"{self.code}.{self.name}"

    @property
    def group_name(self) -> str:
        if self.group:
            return self.group.name
        return "-"


class Classroom(BaseEntity):
    number: int = Field(..., gt=0)
    name: str = Field(..., examples=['Операционные системы'])
    type: Literal['Кабинет', 'Лаборатория', 'Полигон']
    capacity: int
    equipment: str

    teacher_id: int
    teacher: Optional[Teacher] = None

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
