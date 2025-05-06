#! /bin/bash

port=$1

http -v POST :$port/specialties Content-Type:application/json < <(echo '[{"name":"Сетевое и системное администрирование", "code":"09.02.06", "short_name":"СА"},{"name":"Автоматика и телемеханика на транспорте (ж/д транспорте)", "code":"27.02.03", "short_name":"Ш"},{"name":"Эксплуатация подвижного состава (вагоны)", "code":"23.02.04", "short_name":"В"}]')

http -v POST :$port/teachers Content-Type:application/json < <(echo '[{"first_name":"Иван", "middle_name":"Иванович", "last_name":"Иванов", "birth_date":"01.01.1990"}, {"first_name":"Преподаватель", "middle_name":"Преподавателевич", "last_name":"Преподавателев", "birth_date":"02.02.1992"}, {"first_name":"Руководитель", "middle_name":"Иванович", "last_name":"Классный", "birth_date":"03.03.1993"}]')

http -v POST :$port/groups Content-Type:application/json < <(echo '[{"number":501, "year_formed":2023, "spec_id":1, "class_teacher_id":1}, {"number":502, "year_formed":2023, "spec_id":1, "class_teacher_id":2}, {"number":206, "year_formed":2023, "spec_id":2, "class_teacher_id":3}, {"number":102, "year_formed":2024, "spec_id":3, "class_teacher_id":1}]')

http -v POST :$port/students Content-Type:application/json < <(echo '[{"first_name":"Студент", "middle_name":"Студентович", "last_name":"Студентов", "birth_date":"02.02.2002", "group_id":1}, {"first_name":"Студент2", "middle_name":"Студентович", "last_name":"Студ", "birth_date":"03.02.2002", "group_id":1}, {"first_name":"Студ", "middle_name":"Студентович", "last_name":"Петров", "birth_date":"04.02.2002", "group_id":2}, {"first_name":"Жека", "middle_name":"Студентович", "last_name":"Двоишников", "birth_date":"05.02.2002", "group_id":2}, {"first_name":"Один", "middle_name":"Ещу", "last_name":"Студент", "birth_date":"06.02.2002", "group_id":3}]')

http -v POST :$port/disciplines Content-Type:application/json < <(echo '[{"code":"ОП.10", "name":"Электротехника", "semester":1, "hours":70, "group_id":1}]')

http -v POST :$port/classes Content-Type:application/json < <(echo '[{"number":409, "name":"Операционные системы", "type":"Лаборатория", "teacher_id":1}]')
