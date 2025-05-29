from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from app.main.services import get_specialties, get_teachers
import io



def generate_template(entity: str, api: str) -> io.BytesIO:
    wb = Workbook()
    if wb.active:

        ws = wb.active

        if entity == 'specialties':
            ws.title = 'Специальности'

            header = ['Код', 'Название', 'Короткое обозначение']
            ws.append(header)

            ws.append(
                ['09.02.06', 'Сетевои и системное администрирование', 'СА', 'пример'])
        elif entity == 'groups':
            ws.title = 'Группы'

            header = ['Номер','Год набора', 'Специальность', 'Классный руководитель']
            ws.append(header)

            specialties = get_specialties(api)
            teachers = get_teachers(api)

            specialtiy_dv = DataValidation(
                    type='list',
                    formula1=f'=Списки!$A$2:$A${len(specialties.items)}',
                    allow_blank=True
                    )
            ws.add_data_validation(specialtiy_dv)
            specialtiy_dv.add(f'C2:C1048576')

            teacher_dv = DataValidation(
                    type='list',
                    formula1=f'=Списки!$B$2:$B${len(teachers.items)}',
                    allow_blank=True
                    )
            ws.add_data_validation(teacher_dv)
            teacher_dv.add(f'D2:D1048576')

            
            list_sheet = wb.create_sheet("Списки")
            list_sheet.append(['Специальности', 'Преподаватели'])
            for idx, spec in enumerate(specialties.items, start=2):
                cell=f'A{idx}'
                list_sheet[cell]=spec.code 
            for idx, teacher in enumerate(teachers.items, start=2):
                cell=f'B{idx}'
                list_sheet[cell]=f'{teacher.last_name} {teacher.first_name} {teacher.middle_name}'
            list_sheet.hidden = True


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
