from openpyxl import Workbook
import io


def generate_template(entity: str) -> io.BytesIO:
    wb = Workbook()
    if wb.active:

        ws = wb.active

        if entity == 'specialties':
            ws.title = 'Специальности'

            header = ['Код', 'Название', 'Короткое обозначение']
            ws.append(header)

            ws.append(
                ['09.02.06', 'Сетевои и системное администрирование', 'СА', 'пример'])

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
