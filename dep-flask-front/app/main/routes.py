from flask import redirect, render_template, url_for
from app.main import main_bp
from app.require import jwt_required


@main_bp.route('/index')
@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/user')
@jwt_required
def user():
    return redirect(url_for('main.index'))


@main_bp.route('/specializations')
@jwt_required
def specializations():
    specs = [
        {
            "#": "1",
            "Код": "27.02.03",
            "Название": "Автоматика и телемеханика на транспорте"
        },
        {
            "#": "2",
            "Код": "09.02.06",
            "Название": "Сетевое и системное администрирование"
        },
    ]

    return render_template(
        'view/table.html',
        header='Специализации',
        records=specs
    )


@main_bp.route('/groups')
@jwt_required
def groups():
    records = [
        {
            "#": "1",
            "Группа": "Ш-200",
            "Специальность": "Автоматика"
        },
        {
            "#": "2",
            "Группа": "СДМ-699",
            "Специальность": "Строительные машины"
        },
    ]

    return render_template(
        'view/table.html',
        header='Группы',
        records=records
    )


@main_bp.route('/students')
@jwt_required
def students():
    records = [
        {
            "#": "1",
            "Группа": "Ш-200",
            "Специальность": "Автоматика"
        },
        {
            "#": "2",
            "Группа": "СДМ-699",
            "Специальность": "Строительные машины"
        },
    ]

    return render_template(
        'view/table.html',
        header='Студенты',
        records=records
    )


@main_bp.route('/disciplines')
@jwt_required
def disciplines():
    records = [
        {
            "#": "1",
            "Группа": "Ш-200",
            "Специальность": "Автоматика"
        },
        {
            "#": "2",
            "Группа": "СДМ-699",
            "Специальность": "Строительные машины"
        },
    ]

    return render_template(
        'view/table.html',
        header='Дисциплины',
        records=records
    )


@main_bp.route('/teachers')
@jwt_required
def teachers():
    records = [
        {
            "#": "1",
            "Группа": "Ш-200",
            "Специальность": "Автоматика"
        },
        {
            "#": "2",
            "Группа": "СДМ-699",
            "Специальность": "Строительные машины"
        },
    ]

    return render_template(
        'view/table.html',
        header='Преподаватели',
        records=records
    )


@main_bp.route('/audience')
@jwt_required
def audience():
    records = [
        {
            "#": "1",
            "Группа": "Ш-200",
            "Специальность": "Автоматика"
        },
        {
            "#": "2",
            "Группа": "СДМ-699",
            "Специальность": "Строительные машины"
        },
    ]

    return render_template(
        'view/table.html',
        header='Аудитории',
        records=records
    )
