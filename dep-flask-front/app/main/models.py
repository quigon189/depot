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

    @property
    def name(self) -> str:
        return "{} {} {}".format(
            self.last_name,
            self.first_name,
            self.middle_name
        )


class Group(BaseModel):
    id: int
    number: int = Field(..., gt=0)
    year_formed: int

    spec_id: int

    class_teacher_id: int

    @property
    def name(self) -> str:
        return f"{self.number}"


class GroupWithSpecialty(Group):
    specialty: Specialty

    @property
    def name(self) -> str:
        if self.specialty:
            return f"{self.specialty.short_name}-{self.number}"
        return f"{self.number}"

    @property
    def specialty_name(self) -> str:
        return "{} {}".format(
            self.specialty.code,
            self.specialty.name
        )


class GroupWithTeacher(GroupWithSpecialty):
    class_teacher: Teacher

    @property
    def class_teacher_name(self) -> str:
        return "{} {}. {}.".format(
            self.class_teacher.last_name,
            self.class_teacher.first_name[0],
            self.class_teacher.middle_name[0]
        )


class Student(BaseModel):
    id: int
    first_name: str = Field(..., examples=['Иван'])
    middle_name: str = Field(..., examples=['Иванович'])
    last_name: str = Field(..., examples=['Иванов'])
    birth_date: str
    phone: str

    group_id: int

    @property
    def name(self) -> str:
        return "{} {} {}".format(
            self.last_name,
            self.first_name,
            self.middle_name
        )


class StudentWithGroup(Student):
    group: GroupWithSpecialty

    @property
    def group_name(self) -> str:
        return self.group.name


class Discipline(BaseModel):
    id: int
    code: str
    name: str
    semester: int = Field(..., gt=0, le=10)
    hours: int = Field(..., gt=0)

    group_id: int
    group: GroupWithSpecialty

    @property
    def view_name(self) -> str:
        return f"{self.code}.{self.name}"

    @property
    def group_name(self) -> str:
        return self.group.name


class Classroom(BaseModel):
    id: int
    number: int = Field(..., gt=0)
    name: str = Field(..., examples=['Операционные системы'])
    type: Literal['Кабинет', 'Лаборатория', 'Полигон']
    capacity: int
    equipment: str

    teacher_id: int
    teacher: Teacher

    @property
    def class_teacher_name(self) -> str:
        return "{} {}. {}.".format(
            self.teacher.last_name,
            self.teacher.first_name[0],
            self.teacher.middle_name[0]
        )


class SpecialtyWithGroups(Specialty):
    groups: List[Group] = []

    @property
    def groups_count(self) -> int:
        return len(self.groups)


class GroupWithStudents(GroupWithTeacher):
    students: List[Student] = []

    @property
    def students_count(self) -> int:
        return len(self.students) if self.students else 0


class TeacherWitGroups(Teacher):
    groups: List[GroupWithSpecialty] = []
