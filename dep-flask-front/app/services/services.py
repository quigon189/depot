import requests

CATALOG = "http://go-catalog:8080/"

specialties_headers = {
    "id": "#",
    "code": "Код специальности",
    "name": "Наименование",
    "short_name": "Обозначение"
}

students_headers = {
    "id": "#",
    "last_name": "Фамилия",
    "first_name": "Имя",
    "middle_name": "Отчество",

}


def get_data(path):
    req = requests.get(f"{CATALOG}{path}/all")

    try:
        result = req.json()
    except Exception as e:
        print(e)
        return []

    return result


def get_specialties():
    specs = get_data('specialties')

    result = []
    for spec in specs:
        row = {}
        for header in specialties_headers:
            row[specialties_headers[header]] = spec[header]
        result.append(row)

    return result


def get_groups():
    groups = get_data('groups')

    result = []
    for group in groups:
        try:
            row = {}
            row["#"] = group["id"]
            row["Наименование"] = f"{group['specialty']['short_name']}-{group['number']}"
            row["Год набора"] = group["year_formed"]
            if 'class_teacher' in group:
                row["Классный руководитель"] = f"{group['class_teacher']['last_name']} {group['class_teacher']['first_name']} {group['class_teacher']['middle_name']}"
            else:
                row["Классный руководитель"] = "не назначен"
            result.append(row)

        except Exception as e:
            print(e)

    return result
