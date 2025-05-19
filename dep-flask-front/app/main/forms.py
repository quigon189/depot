from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired

from app.main import services


class SpecialityForm(FlaskForm):
    code = StringField("Код специальности", validators=[DataRequired()])
    name = StringField("Наименование", validators=[DataRequired()])
    short_name = StringField("Короткое обозначение", validators=[DataRequired()])


class GroupForm(FlaskForm):
    number = IntegerField("Номер группы")
    year_formed = IntegerField("Год набора")

    spec_id = SelectField("Специальность")
    class_teacher_id = SelectField("Классный руководитель")

    def with_choices(self, api: str) -> "GroupForm":
        specialties = services.get_specialties(api).items
        teachers = services.get_teachers(api).items
        self.spec_id.choices = [(s.id, s.view_name) for s in specialties]
        self.class_teacher_id.choices = [(t.id, t.name) for t in teachers]
        return self


class StudentForm(FlaskForm):
    last_name = StringField("Фамилия", validators=[DataRequired()])
    first_name = StringField("Имя")
    middle_name = StringField("Отчество")
    birth_date = StringField("Дата рождения")
    phone = StringField("Номер телефона")

    group_id = SelectField("Группа")

    def with_choices(self, api: str) -> 'StudentForm':
        groups = services.get_groups(api).items
        self.group_id.choices = [(g.id, g.name) for g in groups]
        return self


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

    def with_choices(self, api: str) -> 'DisciplineForm':
        groups = services.get_groups(api).items
        self.group_id.choices = [(g.id, g.name) for g in groups]
        return self


class ClassForm(FlaskForm):
    number = IntegerField("Номер")
    name = StringField("Название")
    type = SelectField(
        "Тип",
        choices=[
            ('Кабинет', 'Кабинет'),
            ('Лаборатория', 'Лаборатория'),
            ('Полигон', 'Полигон')
        ]
    )
    capacity = IntegerField("Вместительность (чел.)")
    equipment = TextAreaField("Оснащение")

    teacher_id = SelectField("Заведующий")

    def with_choices(self, api: str) -> 'ClassForm':
        teachers = services.get_teachers(api).items
        self.teacher_id.choices = [(t.id, t.name) for t in teachers]
        return self
