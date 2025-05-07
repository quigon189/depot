from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField


class SpecialityForm(FlaskForm):
    code = StringField("Код специальности")
    name = StringField("Наименование")
    short_name = StringField("Короткое обозначение")


class GroupForm(FlaskForm):
    number = IntegerField("Номер группы")
    year_formed = IntegerField("Год набора")

    spec_id = SelectField("Специальность")
    class_teacher_id = SelectField("Классный руководитель")


class StudentForm(FlaskForm):
    last_name = StringField("Фамилия")
    first_name = StringField("Имя")
    middle_name = StringField("Отчество")
    birth_date = StringField("Дата рождения")
    phone = StringField("Номер телефона")

    group_id = SelectField("Группа")


class TeacherForm(FlaskForm):
    last_name = StringField("Фамилия")
    first_name = StringField("Имя")
    middle_name = StringField("Отчество")
    birth_date = StringField("Дата рождения")
    phone = StringField("Номер телефона")


class DisciplineForm(FlaskForm):
    group_id = SelectField("Группа")

    code = StringField("Код")
    name = StringField("Название")
    semester = IntegerField("Семестр")
    hours = IntegerField("Нагрузка (ч.)")


class ClassForm(FlaskForm):
    number = IntegerField("Номер")
    name = StringField("Название")
    type = SelectField("Тип")
    capacity = IntegerField("Вместительность (чел.)")
    equipment = TextAreaField("Оснащение")

    teacher_id = SelectField("Заведующий")
