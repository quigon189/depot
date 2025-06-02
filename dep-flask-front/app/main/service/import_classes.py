import io
from typing import Dict, List, Optional, Type, TypeVar

from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from pydantic import BaseModel

from app.main.models import Classroom, Discipline, Group, Specialty, Student, Teacher
from app.main.services import get_groups, get_specialties, get_teachers


T = TypeVar('T', bound=BaseModel)


class ExcelImporter:
    """
    Общий клас экспорта из Excel файла
    Так же нужен для создания шаблонов Excel файлов
    """

    def __init__(self, model: Type[T], template_properties: List[str], dependensies: Optional[Dict[str, List[tuple]]] = None):
        self.model = model
        self.dependensies = dependensies or {}
        self.template_properties = template_properties
        schema = model.model_json_schema()
        m = schema['$ref'].split('/')[-1]
        self.schema = schema['$defs'][m]

    def generate_template(self) -> io.BytesIO:
        wb = Workbook()
        ws = wb.active or wb.worksheets[0]

        ws.title = self.schema.get('title', 'Data')

        fields = self._get_fields()

        headers = []
        for field_info in fields:
            if field_info['name'] in self.template_properties:
                headers.append(field_info['header'])

        ws.append(headers)

        if self.dependensies:
            list_sheet = wb.create_sheet('Списки')
            i = 1
            for d_name, dependence in self.dependensies.items():
                letter = get_column_letter(i)
                list_sheet[f'{letter}1'] = d_name
                list_sheet[f'{get_column_letter(i+1)}1'] = f'{d_name}_id'
                for idx, (value, id) in enumerate(dependence, start=2):
                    list_sheet[f'{letter}{idx}'] = value
                    list_sheet[f'{get_column_letter(i+1)}{idx}'] = id

                dv = DataValidation(
                    type='list',
                    formula1=f'=Списки!${letter}$2:${letter}${len(dependence)+1}',
                    allow_blank=True
                )
                letter_dep = 'A'
                for idx, header in enumerate(headers):
                    for field_info in fields:
                        if field_info['name'] == d_name and field_info['header'] == header:
                            letter_dep = get_column_letter(idx + 1)

                dv.add(f'{letter_dep}2:{letter_dep}1048576')
                ws.add_data_validation(dv)
                i += 2

        for col in ws.columns:
            column = col[0].column_letter
            adjusted_width = 22 * 1.2
            ws.column_dimensions[column].width = adjusted_width

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer

    def import_data(self, file_path: str, skip_rows: int = 1) -> List[T]:
        try:
            wb = load_workbook(filename=file_path, read_only=True)
            ws = wb.active or wb.worksheets[0]

            header_row = list(ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]

        except Exception as e:
            pass

    def _get_fields(self) -> List[Dict]:
        fields = []

        for field_name, field_info in self.schema['properties'].items():
            fields.append({
                'name': field_name,
                'header': field_info.get('title', field_name.replace('_', ' ').upper()),
                'type': field_info.get('type', 'string'),
                'required': field_name in self.schema.get('required', [])
            })

        return fields


def generate_template(entity: str, api: str) -> Optional[io.BytesIO]:

    if entity == 'specialties':
        return ExcelImporter(
            model=Specialty,
            template_properties=['code', 'name', 'short_name']
        ).generate_template()

    elif entity == 'groups':
        return ExcelImporter(
            model=Group,
            template_properties=['number', 'year_formed',
                                 'specialty', 'class_teacher'],
            dependensies={
                'specialty': [(s.code, s.id) for s in get_specialties(api).items],
                'class_teacher': [(t.name, t.id) for t in get_teachers(api).items]
            }

        ).generate_template()

    elif entity == 'students':
        return ExcelImporter(
            model=Student,
            template_properties=['last_name', 'first_name', 'middle_name',
                                 'group', 'birth_date', 'phone'],
            dependensies={
                'group': [(g.name, g.id) for g in get_groups(api).items]
            }
        ).generate_template()

    elif entity == 'teachers':
        return ExcelImporter(
            model=Teacher,
            template_properties=['last_name', 'first_name', 'middle_name',
                                 'birth_date', 'phone'],
        ).generate_template()

    elif entity == 'disciplines':
        return ExcelImporter(
            model=Discipline,
            template_properties=['code', 'name', 'semester', 'hours', 'group'],
            dependensies={
                'group': [(g.name, g.id) for g in get_groups(api).items]
                }
        ).generate_template()

    elif entity == 'classes':
        return ExcelImporter(
            model=Classroom,
            template_properties=['number', 'name', 'type', 'capacity', 'equipment', 'teacher'],
            dependensies={
                'type': [('Кабинет', 'Кабинет'), ('Лаборатория', 'Лаборатория'), ('Полигон', 'Полигон')],
                'teacher': [(t.name, t.id) for t in get_teachers(api).items]
                }
        ).generate_template()
