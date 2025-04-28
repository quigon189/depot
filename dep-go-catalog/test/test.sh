#! /bin/bash

http -v :8082/specialties code=09.02.06 name="Систмное администрирование" short_name=SA

http -v :8082/teachers first_name=Иван middle_name=Иванов last_name=Иванович birth_date=01.01.1992

http -v :8082/groups number:=501 year_formed:=2023 spec_id:=1 class_teacher_id:=1

