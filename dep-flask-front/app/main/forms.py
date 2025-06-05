from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired

from app.main.service.view_services import get_groups, get_specialties, get_teachers


class SpecialityForm(FlaskForm):
    code = StringField(
        "Код специальности",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r'\d{2}\.\d{2}\.\d{2}',
            'placeholder': '__.__.__',
            'title': ' 99.99.99 (три группы по 2 цифры, разделенные точками)',
            'required': True,
        }
    )
    name = StringField(
        "Наименование",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True}
    )
    short_name = StringField(
        "Короткое обозначение",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True}
    )


class GroupForm(FlaskForm):
    number = IntegerField(
        "Номер группы",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True}
    )
    year_formed = IntegerField(
        "Год набора",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True}
    )

    spec_id = SelectField(
        "Специальность",
        validators=[DataRequired()],
        render_kw={'class': 'form-select', 'required': True}
    )
    class_teacher_id = SelectField(
        "Классный руководитель",
        validators=[DataRequired()],
        render_kw={'class': 'form-select', 'required': True}
    )

    def with_choices(self, api: str) -> "GroupForm":
        specialties = get_specialties(api).items
        teachers = get_teachers(api).items
        self.spec_id.choices = [(s.id, s.view_name) for s in specialties]
        self.class_teacher_id.choices = [(t.id, t.name) for t in teachers]
        return self


class StudentForm(FlaskForm):
    last_name = StringField(
        "Фамилия",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r"^[А-ЯЁ]('[А-ЯЁ])?[а-яё]+(-[А-ЯЁ]('[А-ЯЁ])?[а-яё]+)?$",
            'title': 'Фамилия с большой буквы, например: Иванов, Мамин-Сибиряк, О\'Конор',
            'required': True
        }
    )
    first_name = StringField(
        "Имя",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$',
            'title': 'Имя с большой буквы, например: Иван, Петр-Олег',
            'required': True
        }
    )
    middle_name = StringField(
        "Отчество",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r'^[А-ЯЁ][а-яё]+((-[А-ЯЁ][а-яё]+)|(\s[а-яё]+))?$',
            'title': 'Отчество с большой буквы, например: Иванович, Яков-Петрович',
            'required': True
        }
    )
    birth_date = StringField(
        "Дата рождения",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'type': 'date',
            'pattern': r"^[0-9]{4}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1])$",
            'required': True
        }
    )
    phone = StringField(
        "Номер телефона",
        render_kw={
            'class': 'form-control',
            'pattern': r'^\+\d\(\d{3}\)\d{3}-\d{2}-\d{2}$',
            'placeholder': '+7(999)999-99-99',
            'title': '+7(999)999-99-99',
        }
    )

    group_id = SelectField(
        "Группа",
        validators=[DataRequired()],
        render_kw={'class': 'form-select', 'required': True}
    )

    def with_choices(self, api: str) -> 'StudentForm':
        groups = get_groups(api).items
        self.group_id.choices = [(g.id, g.name) for g in groups]
        return self


class TeacherForm(FlaskForm):
    last_name = StringField(
        "Фамилия",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r"^[А-ЯЁ]('[А-ЯЁ])?[а-яё]+(-[А-ЯЁ]('[А-ЯЁ])?[а-яё]+)?$",
            'title': 'Фамилия с большой буквы, например: Иванов, Мамин-Сибиряк, О\'Конор',
            'required': True
        }
    )
    first_name = StringField(
        "Имя",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$',
            'title': 'Имя с большой буквы, например: Иван, Петр-Олег',
            'required': True
        }
    )
    middle_name = StringField(
        "Отчество",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r'^[А-ЯЁ][а-яё]+((-[А-ЯЁ][а-яё]+)|(\s[а-яё]+))?$',
            'title': 'Отчество с большой буквы, например: Иванович, Яков-Петрович',
            'required': True
        }

    )
    birth_date = StringField(
        "Дата рождения",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'type': 'date',
            'pattern': r"^[0-9]{4}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1])",
            'title': 'ГГГГ-ММ-ДД',
            'required': True
        }
    )
    phone = StringField(
        "Номер телефона",
        render_kw={
            'class': 'form-control',
            'pattern': r'^\+\d\(\d{3}\)\d{3}-\d{2}-\d{2}$',
            'placeholder': '+7(999)999-99-99',
            'title': '+7(999)999-99-99',
        }
    )


class DisciplineForm(FlaskForm):
    group_id = SelectField(
        "Группа",
        validators=[DataRequired()],
        render_kw={'class': 'form-select', 'required': True}
    )

    code = StringField(
        "Код",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r'^[А-Я]+[\.А-Я\d]*$',
            'title': 'Большие буквы, цифры, точка. Например: ОПЦ.01',
            'required': True
        }
    )
    name = StringField(
        "Название",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True}
    )
    semester = IntegerField(
        "Семестр",
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'pattern': r'[1-8]',
            'title': 'Цифра от 1 до 8',
            'required': True
        }
    )
    hours = IntegerField(
        "Нагрузка (ч.)",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True}
    )

    def with_choices(self, api: str) -> 'DisciplineForm':
        groups = get_groups(api).items
        self.group_id.choices = [(g.id, g.name) for g in groups]
        return self


class ClassForm(FlaskForm):
    number = IntegerField(
        "Номер",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True}
    )
    name = StringField(
        "Название",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True}
    )
    type = SelectField(
        "Тип",
        validators=[DataRequired()],
        render_kw={'class': 'form-control', 'required': True},
        choices=[
            ('Кабинет', 'Кабинет'),
            ('Лаборатория', 'Лаборатория'),
            ('Полигон', 'Полигон')
        ]
    )
    capacity = IntegerField(
        "Вместительность (чел.)",
        render_kw={'class': 'form-control'}
    )
    equipment = TextAreaField(
        "Оснащение",
        render_kw={'class': 'form-control'}
    )

    teacher_id = SelectField(
        "Заведующий",
        validators=[DataRequired()],
        render_kw={'class': 'form-select', 'required': True}
    )

    def with_choices(self, api: str) -> 'ClassForm':
        teachers = get_teachers(api).items
        self.teacher_id.choices = [(t.id, t.name) for t in teachers]
        return self


class ImportForm(FlaskForm):
    entity = SelectField(
        "Выберете модель для импорта",
        validators=[DataRequired()],
        choices=[
            ('specialties', 'Специальности'),
            ('groups', 'Группы'),
            ('students', 'Студенты'),
            ('teachers', 'Преподаватели'),
            ('disciplines', 'Дисциплины'),
            ('classes', 'Аудитории'),
        ],
        render_kw={'class': 'form-select', 'required': True}
    )

    file = FileField(
        "Выберите excel файл",
        validators=[
            FileRequired(),
            FileAllowed(['xlsx'], 'Поддерживается только формат xlsx')
        ],
        render_kw={'class': 'form-control', 'required': True}
    )
