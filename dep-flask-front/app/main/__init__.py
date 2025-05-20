from flask import Blueprint

main_bp = Blueprint("main", __name__)

from app.main.routes import index
from app.main.routes import user
from app.main.routes import specialties
from app.main.routes import groups
from app.main.routes import students
from app.main.routes import teachers
from app.main.routes import disciplines
from app.main.routes import classrooms
