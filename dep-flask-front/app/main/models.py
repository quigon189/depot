from typing import Literal, List
from pydantic import BaseModel, Field


class Specialty(BaseModel):
    id: int
    code: str = Field(..., min_length=8, max_length=8, examples=["09.02.06"])
    name: str = Field(..., max_length=200, examples=[
                      "Системное и сетевое администрирование"])
    short_name: str = Field(..., max_length=8, examples=["СА"])


class Teacher(BaseModel):
    id: int
    first_name: str = Field(..., examples=['Иван'])
    middle_name: str = Field(..., examples=['Иванович'])
    last_name: str = Field(..., examples=['Иванов'])
    birth_date: str
    phone: str


class Group(BaseModel):
    id: int
    number: int = Field(..., gt=0)
    year_formed: int

    spec_id: int

    class_teacher_id: int
    class_teacher: Teacher


class GroupWithSpecialty(Group):
    specialty: Specialty


class Student(BaseModel):
    id: int
    first_name: str = Field(..., examples=['Иван'])
    middle_name: str = Field(..., examples=['Иванович'])
    last_name: str = Field(..., examples=['Иванов'])
    birth_date: str
    phone: str

    group_id: int
    group: GroupWithSpecialty


class Discipline(BaseModel):
    id: int
    code: str
    name: str
    semester: int = Field(..., gt=0, le=10)
    hours: int = Field(..., gt=0)

    group_id: int
    group: GroupWithSpecialty


class Classroom(BaseModel):
    id: int
    number: int = Field(..., gt=0)
    name: str = Field(..., examples=['Операционные системы'])
    type: Literal['Кабинет', 'Лаборатория', 'Полигон']
    capacity: int
    equipment: str

    teacher_id: int
    teacher: Teacher


class SpecialtyWithGroups(Specialty):
    groups: List[Group] = []

    @property
    def groups_count(self) -> int:
        return len(self.groups)


class TeacherWitGroups(Teacher):
    groups: List[Group] = []
