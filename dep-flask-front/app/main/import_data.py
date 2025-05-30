from typing import Dict, List
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel
from app.main.services import GroupsPresenter, SpecialtiesPresenter, TeachersPresenter, get_groups, get_specialties, get_teachers, send_entity, send_specialty
import io


def add_dv(ws: Worksheet, letter1: str, letter2: str, count: int):
    dv = DataValidation(
        type='list',
        formula1=f'=Списки!${letter1}$2:${letter1}${count}',
        allow_blank=True
    )
    dv.add(f'{letter2}2:{letter2}1048576')
    ws.add_data_validation(dv)


def specialty_template(wb: Workbook):
    if wb.active:
        ws = wb.active

        ws.title = 'Специальности'

        header = ['Код', 'Название', 'Короткое обозначение']
        ws.append(header)

        ws.append(
            ['09.02.06', 'Сетевои и системное администрирование', 'СА', 'пример'])


def group_template(wb: Workbook, specialties: SpecialtiesPresenter, teachers: TeachersPresenter):
    if wb.active:
        ws = wb.active
        ws.title = 'Группы'

        header = ['Номер', 'Год набора',
                  'Специальность', 'Классный руководитель']
        ws.append(header)

        add_dv(ws, 'A', 'C', len(specialties.items)+1)
        add_dv(ws, 'B', 'D', len(teachers.items)+1)

        list_sheet = wb.create_sheet("Списки")
        list_sheet.append(['Специальности', 'Преподаватели'])
        for idx, spec in enumerate(specialties.items, start=2):
            cell = f'A{idx}'
            list_sheet[cell] = spec.code
        for idx, teacher in enumerate(teachers.items, start=2):
            cell = f'B{idx}'
            list_sheet[cell] = teacher.name
        list_sheet.hidden = True


def student_template(wb: Workbook, groups: GroupsPresenter):
    if wb.active:
        ws = wb.active

        ws.title = "Студенты"
        header = ['Фамилия', 'Имя', 'Отчество',
                  'Дата рождения', 'Номер телефона', 'Группа']
        ws.append(header)

        add_dv(ws, 'A', 'F', len(groups.items)+1)

        list_sheet = wb.create_sheet("Списки")
        list_sheet.append(['Группы'])
        for idx, group in enumerate(groups.items, start=2):
            cell = f'A{idx}'
            list_sheet[cell] = group.name
        list_sheet.hidden = True


def teacher_template(wb: Workbook):
    if wb.active:
        ws = wb.active

        ws.title = "Преподаватели"
        header = ['Фамилия', 'Имя', 'Отчество',
                  'Дата рождения', 'Номер телефона']
        ws.append(header)


def discipline_template(wb: Workbook, groups: GroupsPresenter):
    if wb.active:
        ws = wb.active

        ws.title = "Дисциплины"
        header = ['Группа', 'Код', 'Название', 'Семестр', 'Нагрузка']
        ws.append(header)

        add_dv(ws, 'A', 'A', len(groups.items)+1)

        list_sheet = wb.create_sheet("Списки")
        list_sheet.append(['Группы'])
        for idx, group in enumerate(groups.items, start=2):
            cell = f'A{idx}'
            list_sheet[cell] = group.name
        list_sheet.hidden = True


def classroom_template(wb, teachers):
    if wb.active:
        ws = wb.active

        classrooms_types = ['Кабинет', 'Лаборатория', 'Полигон']

        ws.title = "Аудитории"
        header = ['Номер', 'Название', 'Тип',
                  'Вместительность', 'Оснащение', 'Заведующий']
        ws.append(header)

        add_dv(ws, 'A', 'C', len(classrooms_types)+1)
        add_dv(ws, 'B', 'F', len(teachers.items)+1)

        list_sheet = wb.create_sheet("Списки")
        list_sheet.append(['Тип', 'Преподаватели'])
        for idx, value in enumerate(classrooms_types, start=2):
            cell = f'A{idx}'
            list_sheet[cell] = value
        for idx, teacher in enumerate(teachers.items, start=2):
            cell = f'B{idx}'
            list_sheet[cell] = teacher.name
        list_sheet.hidden = True


def generate_template(entity: str, api: str) -> io.BytesIO:
    wb = Workbook()

    if entity == 'specialties':
        specialty_template(wb)
    elif entity == 'groups':
        group_template(
            wb,
            get_specialties(api),
            get_teachers(api)
        )
    elif entity == 'students':
        student_template(
            wb,
            get_groups(api)
        )
    elif entity == 'teachers':
        teacher_template(wb)
    elif entity == 'disciplines':
        discipline_template(
            wb,
            get_groups(api)
        )
    elif entity == 'classes':
        classroom_template(
            wb,
            get_teachers(api)
        )

    ws = wb.worksheets[0]

    for col in ws.columns:
        max_lenght = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_lenght:
                    max_lenght = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_lenght + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


class ImportResults(BaseModel):
    success: int
    errors: List[str]
    total: int


entity_map = {
    'specialties': {
        'Код': 'code',
        'Название': 'name',
        'Короткое обозначение': 'short_name'
    }
}


def import_excel(api: str, entity: str, file_stream):
    results = ImportResults(success=0, errors=[], total=0)
    wb = load_workbook(filename=file_stream)
    data_to_send = []
    if wb.active:
        ws = wb.active

        headers = [cell.value for cell in ws[1]]

        for row in ws.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue

            results.total += 1
            row_data = dict(zip(headers, row))

            data = {}
            for header in row_data.keys():
                h = entity_map[entity][header]
                data[h] = row_data[header]

            data_to_send.append(data)

    return send_entity(
        f'{api}/{entity}',
        data_to_send,
        "Специальности импортированны"
    )
