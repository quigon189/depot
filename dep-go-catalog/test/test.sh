#! /bin/bash

port=$1

http -v POST :$port/specialties Content-Type:application/json < <(echo '[{"name":"Сетевое и системное администрирование", "code":"09.02.06", "short_name":"СА"}]')

http -v POST :$port/teachers Content-Type:application/json < <(echo '[{"first_name":"Иван", "middle_name":"Иванович", "last_name":"Иванов", "birth_date":"01.01.1990"}]')

http -v POST :$port/groups Content-Type:application/json < <(echo '[{"number":501, "year_formed":2023, "spec_id":1, "class_teacher_id":1}]')

http -v POST :$port/students Content-Type:application/json < <(echo '[{"first_name":"Студент", "middle_name":"Студентович", "last_name":"Студентов", "birth_date":"02.02.2002", "group_id":1}]')

http -v POST :$port/disciplines Content-Type:application/json < <(echo '[{"code":"ОП.10", "name":"Электротехника", "semester":1, "hours":70, "group_id":1}]')

http -v POST :$port/classes Content-Type:application/json < <(echo '[{"number":409, "name":"Операционные системы", "type":"Лаборатория", "teacher_id":1}]')
