from flask_wtf import FlaskForm
from wtforms import StringField


class CreateSpecialityForm(FlaskForm):
    code = StringField("Код специальности")
    name = StringField("Наименование")
    short_name = StringField("Короткое обозначение")
