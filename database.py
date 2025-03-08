import os
import sqlite3 as sq
from datetime import datetime

from variables import all_patient, patient, app_info, user


def data_base(command,
              insert_data=None,
              delete_data=None):
    if command == 'create_db':
        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()

            cur.execute("CREATE TABLE IF NOT EXISTS врачи "
                        "(doctor_name text, district text, ped_div text, "
                        "manager text, open_mark text, text_size text)")
            cur.execute("CREATE TABLE IF NOT EXISTS examination "
                        "(date_time text, doctor_name text, status text, "
                        "LN_type text, patient_info text, examination_text text, "
                        "examination_key text, add_info text)")
            cur.execute("CREATE TABLE IF NOT EXISTS my_saved_diagnosis "
                        "(doctor_name text, diagnosis text, examination_key text)")
            cur.execute("CREATE TABLE IF NOT EXISTS my_LN "
                        "(doctor_name text, ln_type text, ln_num text)")
            cur.execute("CREATE TABLE IF NOT EXISTS my_sport_section "
                        "(doctor_name text, sport_section text)")
            cur.execute("CREATE TABLE IF NOT EXISTS app_data "
                        "(path_examination_data_base text, path_srv_data_base text, "
                        "app_password text, last_reg_password text)")
            cur.execute('''CREATE TABLE IF NOT EXISTS statistic_DOC_db (
            date TEXT, time TEXT, user_id TEXT, info TEXT, district TEXT)''')

            user['app_data'] = dict()
            for mark in ('path_examination_data_base', 'path_srv_data_base', 'app_password', 'last_reg_password'):
                cur.execute(f"SELECT {mark} FROM app_data")
                app_data = cur.fetchone()
                if isinstance(app_data, tuple):
                    user['app_data'][mark] = app_data[0]
                else:
                    user['app_data'][mark] = None
            cur.execute(f"SELECT doctor_name FROM врачи")
            doctor_data = list()
            for i in cur.fetchall():
                doctor_data.append(i[0])
            if not doctor_data:
                cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)",
                            ['Иванов И.И.', 1, 1, 'Петров П.П.', True, 20])

            cur.execute(f"SELECT doctor_name, district, ped_div, manager, open_mark FROM врачи")
            flag = False
            doctor_data = cur.fetchall()
            for doctor_name, district, ped_div, manager, open_mark in doctor_data:
                if open_mark:
                    flag = True
            if not flag:
                cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE 'Иванов И.И.'")
                cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)",
                            ['Иванов И.И.', 1, 1, 'Петров П.П.', True, 20])

    elif command == 'edit_path_db':
        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE from app_data")
            cur.execute("INSERT INTO app_data VALUES (?, ?, ?, ?)",
                        [user['app_data'].get('path_examination_data_base'),
                         user['app_data'].get('path_srv_data_base'),
                         user['app_data'].get('app_password'),
                         user['app_data'].get('last_reg_password')])

    elif command == 'save_new_patient':
        try:
            path = f".{os.sep}data_base{os.sep}patient_data_base.db"

            with sq.connect(f"{path}") as conn:
                cur = conn.cursor()
                cur.execute(f"INSERT INTO patient_data VALUES({'?, ' * (len(insert_data) - 1)}?)", insert_data)

            if user['app_data'].get('path_srv_data_base') and not user.get('error_connection'):
                path = f"{user['app_data'].get('path_srv_data_base')}patient_data_base.db"
                with sq.connect(f"{path}") as conn:
                    cur = conn.cursor()
                    cur.execute(f"INSERT INTO patient_data VALUES({'?, ' * (len(insert_data) - 1)}?)", insert_data)
            return True
        except Exception:
            return False

    elif command == 'activate_app':
        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE from app_data")
            cur.execute("INSERT INTO app_data VALUES (?, ?, ?, ?)",
                        [user['app_data'].get('path_examination_data_base'),
                         user['app_data'].get('path_srv_data_base'),
                         user['app_data'].get('app_password'),
                         datetime.now().strftime("%d.%m.%Y")])

    elif command == 'create_SRV_db':
        try:
            with sq.connect(f"{user['app_data'].get('path_srv_data_base')}examination_data_base.db") as conn:
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS examination "
                            "(date_time text, doctor_name text, status text, "
                            "LN_type text, patient_info text, examination_text text, "
                            "examination_key text, add_info text)")

            with sq.connect(f"{user['app_data'].get('path_srv_data_base')}application_data_base.db") as conn:
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS врачи "
                            "(doctor_name text, password text, district text, ped_div text, "
                            "manager text, open_mark text, text_size text, add_info text)")
                cur.execute("CREATE TABLE IF NOT EXISTS my_saved_diagnosis "
                            "(doctor_name text, diagnosis text, examination_key text)")
                cur.execute("CREATE TABLE IF NOT EXISTS my_LN "
                            "(doctor_name text, ln_type text, ln_num text)")
                cur.execute("CREATE TABLE IF NOT EXISTS my_sport_section "
                            "(doctor_name text, sport_section text)")
        except Exception:
            pass

    elif command == 'last_edit_patient_db_srv':
        try:
            with sq.connect(f"{user['app_data'].get('path_srv_data_base')}patient_data_base.db") as conn:
                cur = conn.cursor()
                cur.execute(f"SELECT last_edit FROM last_edit")
                last_edit_srv = cur.fetchall()[0]

            return last_edit_srv

        except Exception:
            return False

    elif command == 'last_edit_patient_db_loc':
        with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT last_edit FROM last_edit")
            last_edit_loc = cur.fetchall()[0]
        return last_edit_loc

    elif command == 'select_all_patient':
        with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM patient_data")
            found_data = cur.fetchall()
            for patient_data in found_data:
                district, amb_num, name_1, name_2, name_3, gender, birth_date, address, phone, vac_1, vac_2 = \
                    patient_data
                all_patient[f"{amb_num}_{name_1}_{name_2}_{name_3}_{birth_date}"] = {
                    'district': district,
                    'amb_num': amb_num,
                    'name_1': name_1,
                    'name_2': name_2,
                    'name_3': name_3,
                    'gender': gender,
                    'birth_date': birth_date,
                    'address': address,
                    'phone': phone,
                    'vac_1': vac_1,
                    'vac_2': vac_2,

                }

    elif command == 'get_all_doctor_info':
        user['my_saved_diagnosis'] = list()
        user['my_LN'] = list()
        user['my_sport_section'] = list()

        try:
            local_data = dict()
            with sq.connect(f"{user['app_data'].get('path_srv_data_base')}application_data_base.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM врачи")
                all_doctor_info = cur.fetchall()
                for marker in ('my_saved_diagnosis', 'my_LN', 'my_sport_section'):
                    cur.execute(f"SELECT * FROM {marker}")
                    local_data[marker] = cur.fetchall()

            for doctor_name, password, district, ped_div, manager, open_mark, text_size, add_info in all_doctor_info:
                app_info['all_doctor_info'][doctor_name] = {
                    'doctor_name': doctor_name,
                    'password': password,
                    'district': district,
                    'ped_div': ped_div,
                    'manager': manager,
                    'open_mark': open_mark,
                    'text_size': text_size,
                    'add_info': add_info,
                    'my_saved_diagnosis': list(),
                    'my_LN': list(),
                    'my_sport_section': list()}

            for marker in ('my_saved_diagnosis', 'my_LN', 'my_sport_section'):
                for info in local_data.get(marker):
                    doctor_name = info[0]
                    if doctor_name in app_info.get('all_doctor_info'):
                        app_info['all_doctor_info'][doctor_name][marker].append(info[1:])

                        # print(app_info['all_doctor_info'][doctor_name].get(marker))

        except Exception:
            return False

    elif command.startswith('get_certificate_for_district'):
        _, type_table, marker = command.split('__')
        try:
            with sq.connect(f"{user['app_data'].get('path_srv_data_base')}data_base.db") as conn:
                cur = conn.cursor()
                cur.execute(f"CREATE TABLE IF NOT EXISTS certificate_camp__{datetime.now().year} ("
                            "district TEXT, num TEXT, date TEXT, "
                            "name TEXT, birth_date TEXT, gender TEXT, address TEXT)")
                cur.execute(f"CREATE TABLE IF NOT EXISTS certificate_ped_div__{datetime.now().year} ("
                            "ped_div TEXT, district TEXT, num TEXT, date TEXT, "
                            "name TEXT, birth_date TEXT, address TEXT, type_cert TEXT, doctor_name TEXT)")

                found_data = list()
                for year in range(2023, datetime.now().year + 1):
                    if type_table == f"certificate_ped_div":
                        cur.execute(f"SELECT *"
                                    f" FROM {type_table}__{year} WHERE ped_div LIKE '{marker}';")
                    elif type_table == 'certificate_camp':
                        cur.execute(f"SELECT *"
                                    f" FROM {type_table}__{year} WHERE district LIKE '{marker}';")

                    for info in cur.fetchall():
                        if info:
                            found_data.append(info)
            return found_data
        except Exception:
            return False

    elif command == 'save_new_diagnosis':
        try:
            try:
                with sq.connect(f"{user['app_data'].get('path_srv_data_base')}application_data_base.db",
                                timeout=10.0) as connect:
                    cursor = connect.cursor()
                    cursor.execute(f"INSERT INTO my_saved_diagnosis "
                                   f"VALUES(?, ?, ?)", insert_data)
            except Exception:
                pass
            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                cursor = connect.cursor()
                cursor.execute(f"INSERT INTO my_saved_diagnosis "
                               f"VALUES(?, ?, ?)", insert_data)

            user['my_saved_diagnosis'].append(insert_data[1:])



        except Exception:
            return False
        else:
            return True

    elif command == 'save_new_hobby':
        try:
            try:
                with sq.connect(database=f"{user['app_data'].get('path_srv_data_base')}application_data_base.db",
                                timeout=10.0) as connect:
                    cursor = connect.cursor()
                    cursor.execute("INSERT INTO my_sport_section VALUES(?, ?)",
                                   insert_data)
            except Exception:
                pass

            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                cursor = connect.cursor()
                cursor.execute("INSERT INTO my_sport_section VALUES(?, ?)",
                               insert_data)
            user['my_sport_section'].append(tuple(insert_data[1:]))

        except Exception as ex:
            print(ex)
            return False
        else:
            return True

    elif command == 'delete_sport_section':
        try:
            try:
                with sq.connect(database=f"{user['app_data'].get('path_srv_data_base')}application_data_base.db",
                                timeout=10.0) as connect:
                    cursor = connect.cursor()
                    cursor.execute(f"DELETE FROM my_sport_section "
                                   f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                                   f"AND sport_section LIKE '{delete_data}'")
            except Exception:
                pass

            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                cursor = connect.cursor()
                cursor.execute(f"DELETE FROM my_sport_section "
                               f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                               f"AND sport_section LIKE '{delete_data}'")
            for info in user.get('my_sport_section'):
                if delete_data in info:
                    user['my_sport_section'].remove(info)

        except Exception as ex:
            return False
        else:
            return True

    elif command == 'save_doctor_local':
        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()

            cur.execute(f"SELECT doctor_name, district, ped_div, manager, text_size FROM врачи")
            found_data = cur.fetchall()
            cur.execute(f"DELETE FROM врачи")

            for doctor_name, district, ped_div, manager, text_size in found_data:
                if doctor_name == insert_data:
                    cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)",
                                [doctor_name, district, ped_div, manager, True, text_size])
                else:
                    cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)",
                                [doctor_name, district, ped_div, manager, False, text_size])

    elif command == 'append_local_doctor_data':
        print(insert_data)
        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()

            cur.execute(f"SELECT doctor_name, district, ped_div, manager, text_size FROM врачи "
                        f"WHERE doctor_name LIKE '{insert_data}'")

            doctor_name, district, ped_div, manager, text_size = cur.fetchone()
            user['text_size'] = int(text_size)
            user['doctor_name'] = doctor_name
            user['doctor_district'] = district
            user['ped_div'] = ped_div
            user['manager'] = manager

            for marker in ('my_saved_diagnosis', 'my_LN', 'my_sport_section'):
                cur.execute(f"SELECT * FROM {marker} "
                            f"WHERE doctor_name LIKE '{doctor_name}'")
                user[marker] = list()
                found_data = cur.fetchall()
                if found_data:
                    for i in found_data:
                        user[marker].append(i[1:])

    elif command == 'save_certificate_single_window':
        try:

            with sq.connect(f"{user['app_data'].get('path_srv_data_base')}data_base.db") as conn:
                cur = conn.cursor()

                cur.execute(f"CREATE TABLE IF NOT EXISTS certificate_single_window__{datetime.now().year} ("
                            "ped_div TEXT, district TEXT, num INTEGER, date TEXT, "
                            "name TEXT, birth_date TEXT, address TEXT, type_cert TEXT, doctor_name TEXT, add_info TEXT)")

                cur.execute(f"SELECT MAX(num)"
                            f" FROM certificate_single_window__{datetime.now().year}")

                number = cur.fetchone()[0]
                if not number:
                    number = 0
                number += 1
                insert_data[2] = number
                cur.execute(f"INSERT INTO certificate_single_window__{datetime.now().year} VALUES({'?, ' * 9}?)",
                            insert_data)
                return number

                # if type_table == 'certificate_ped_div':
                #     cur.execute(f"SELECT num"
                #                 f" FROM {type_table}__{datetime.now().year} WHERE ped_div LIKE '{district_pd}';")
                # elif type_table == 'certificate_camp':
                #     cur.execute(f"SELECT num FROM {type_table}__{datetime.now().year} WHERE district LIKE '{district_pd}';")
                #
                # numbers = list()
                # for num in cur.fetchall():
                #     if isinstance(num, tuple) and len(num) > 0:
                #         num = num[0]
                #     if num.isdigit():
                #         numbers.append(int(num))
                # if len(numbers) == 0:
                #     numbers.append(0)
                #
                # number = max(numbers) + 1
                # if type_table == 'certificate_ped_div':
                #     data_cert[2] = number
                #     cur.execute(f"INSERT INTO certificate_ped_div__{datetime.now().year} VALUES({'?, ' * 8}?)", insert_data)
                #
                # elif type_table == 'certificate_camp':
                #     data_cert[1] = number
                #     cur.execute(f"INSERT INTO certificate_camp__{datetime.now().year} VALUES({'?, ' * 6}?)", data_cert)
        except Exception as ex:
            print(ex)
            return '__________'

    elif command == 'statistic_write':
        date_now, time_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S").split()
        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT INTO statistic_DOC_db VALUES('{date_now}', '{time_now}', 'приложение', "
                        f"'{insert_data}', '{user.get('doctor_name')}')")

    elif command == 'get_doc_names_local':
        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT doctor_name, open_mark FROM врачи")
            all_doctors = list()
            for doctor_name, mark in cur.fetchall():
                if mark == '1':
                    all_doctors.insert(0, doctor_name)
                else:
                    all_doctors.append(doctor_name)

        return all_doctors

    elif command == 'get_doctor_data_local':
        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()

            cur.execute(f"SELECT doctor_name, district, ped_div, manager, text_size FROM врачи "
                        f"WHERE open_mark LIKE '1'")
        return cur.fetchone()

    elif command == 'save_new_doc':
        try:
            if user.get('error_connection'):
                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                    cur = conn.cursor()
                    # cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{doctor_name}'")

                    cur.execute(f"SELECT doctor_name, district, ped_div, manager, text_size FROM врачи")
                    all_doc = cur.fetchall()
                    cur.execute(f"DELETE FROM врачи")

                    for doctor_name, district, ped_div, manager, text_size in all_doc:
                        if doctor_name != insert_data[0]:
                            cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)",
                                        [doctor_name, district, ped_div, manager, False, text_size])

                    cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)", insert_data)
            else:
                with sq.connect(f"{user['app_data'].get('path_srv_data_base')}application_data_base.db") as conn:
                    cur = conn.cursor()
                    cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{insert_data[0]}'")
                    cur.execute(f"INSERT INTO врачи VALUES({'?, ' * (len(insert_data) - 1)}?)", insert_data)

        except Exception as ex:
            return False, ex
        else:
            return True, True

    elif command == 'certificate__upload_last_data':
        path = f".{os.sep}data_base{os.sep}"
        if user['app_data'].get('path_examination_data_base'):
            path = user['app_data'].get('path_examination_data_base')
        path_examination = f"{path}data_base.db"

        found_info = {
            'select_past_examination': None}

        with sq.connect(f"{path_examination}") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT date_time, examination_key "
                        f"FROM examination "
                        f"WHERE patient_info LIKE "
                        f"'{patient.get('name').strip()}__{patient.get('birth_date').strip()}' "
                        f"AND status NOT LIKE 'deleted' "
                        f"AND add_info LIKE 'certificate'")
            found_info['select_past_examination'] = cur.fetchall()
        return found_info

    elif command.startswith('examination'):
        try:
            path = f".{os.sep}data_base{os.sep}"
            if user['app_data'].get('path_examination_data_base'):
                path = user['app_data'].get('path_examination_data_base')
            path_examination = f"{path}data_base.db"

            if command == 'examination__delete':
                with sq.connect(f"{path_examination}") as connect:
                    cursor = connect.cursor()
                    cursor.execute(f"UPDATE examination SET status = 'deleted' WHERE rowid LIKE '{insert_data}'")

                    # cursor.execute(f"DELETE FROM examination WHERE rowid LIKE '{insert_data}'")

            elif command == 'examination__upload_last_data':
                found_info = {
                    'select_past_examination': None,
                    'get_last_doc_LN': None}

                with sq.connect(f"{path_examination}") as conn:
                    cur = conn.cursor()

                    cur.execute(f"SELECT rowid, date_time, doctor_name, status, LN_type, patient_info, "
                                f"examination_text, examination_key "
                                f"FROM examination "
                                f"WHERE patient_info LIKE "
                                f"'{patient.get('name')}%{patient.get('birth_date')}' "
                                f"AND status NOT LIKE 'deleted'")

                    found_info['select_past_examination'] = cur.fetchall()

                    cur.execute(f"SELECT LN_type FROM examination "
                                f"WHERE doctor_name LIKE '{user.get('doctor_name')}'")
                    found_info['get_last_doc_LN'] = cur.fetchall()

                return found_info

            elif command == 'examination__save':
                with sq.connect(f"{path_examination}") as conn:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO examination VALUES(?, ?, ?, ?, ?, ?, ?, ?)", insert_data)

            elif command == 'examination__delete_my_diagnosis':
                try:
                    with sq.connect(f"{user['app_data'].get('path_srv_data_base')}application_data_base.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"DELETE FROM my_saved_diagnosis WHERE doctor_name LIKE "
                                       f"'{user.get('doctor_name')}' AND diagnosis LIKE '{delete_data}'")
                except Exception:
                    pass

                with sq.connect(f"{path}data_base.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute(f"DELETE FROM my_saved_diagnosis WHERE doctor_name LIKE "
                                   f"'{user.get('doctor_name')}' AND diagnosis LIKE '{delete_data}'")
                for diagnosis_data in user.get('my_saved_diagnosis'):
                    if diagnosis_data[0] == delete_data:
                        user['my_saved_diagnosis'].remove(diagnosis_data)

            elif command == 'examination__edit_doctor_LN':
                try:
                    with sq.connect(f"{user['app_data'].get('path_srv_data_base')}application_data_base.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"DELETE FROM my_LN "
                                       f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                                       f"AND ln_type LIKE '{insert_data[0]}'")

                        cursor.execute("INSERT INTO my_LN VALUES(?, ?, ?)",
                                       [user.get('doctor_name'), insert_data[0], insert_data[1]])
                except Exception:
                    pass

                with sq.connect(f"{path}data_base.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute(f"DELETE FROM my_LN "
                                   f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                                   f"AND ln_type LIKE '{insert_data[0]}'")

                    cursor.execute("INSERT INTO my_LN VALUES(?, ?, ?)",
                                   [user.get('doctor_name'), insert_data[0], insert_data[1]])
                if not user.get('my_LN'):
                    user['my_LN'] = list()
                for i in user.get('my_LN'):
                    if insert_data[0] == i[0]:
                        user['my_LN'].remove(i)
                user['my_LN'].append(insert_data)

            elif command == 'examination__edit_examination_loc':
                load_info_text = app_info.get('load_info_text')

                local_data = {
                    'examination_loc': list(),
                    'examination_srv': list(),
                    'found_data_statistic': list(),
                    'sorted_examination_loc': {
                        'deleted': set(),
                        'srv': set(),
                        'loc': set(),
                        'loc_list': list()},
                    'sorted_examination_srv': list(),
                    'loc': f"{path}data_base.db",
                    'srv': f"{user['app_data'].get('path_srv_data_base')}examination_data_base.db"
                }
                load_info_text.set("Извлечение локальных осмотров... ")

                with sq.connect(database=f"{local_data.get('loc')}") as conn:
                    cur = conn.cursor()
                    cur.execute(f"SELECT date_time, doctor_name, status, LN_type, patient_info, "
                                f"examination_text, examination_key, add_info "
                                f"FROM examination")
                    local_data[f"examination_loc"] = cur.fetchall()

                load_info_text.set("Синхронизация...")

                for examination in local_data.get("examination_loc"):
                    (date_time, doctor_name, status, LN_type,
                     patient_info, examination_text,
                     examination_key, add_info) = examination
                    if len(date_time.split(':')) == 2:
                        date_time += ":00"

                    if status in ('loc', 'srv', 'deleted'):
                        local_data["sorted_examination_loc"][status].add(
                            f"{date_time}___{doctor_name}___{patient_info}")
                        if status == 'loc':
                            local_data["sorted_examination_loc"][f"{status}_list"].append(
                                (date_time, doctor_name, 'srv', LN_type,
                                 patient_info, examination_text,
                                 examination_key, add_info))

                load_info_text.set("Изменение локальной БД")

                for path_mark in ('srv', 'loc'):
                    try:
                        with sq.connect(database=f"{local_data.get(path_mark)}") as conn:
                            cur = conn.cursor()

                            if path_mark == 'srv':
                                load_info_text.set("Ожидание ответа сервера... ")

                                if 'examination_db_place:____srv' in user.get('add_info'):
                                    cur.execute(f"SELECT date_time, doctor_name, status, LN_type, patient_info, "
                                                f"examination_text, examination_key, add_info "
                                                f"FROM examination")
                                    local_data[f"examination_{path_mark}"] = cur.fetchall()

                                cur.executemany("INSERT INTO examination VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                                local_data["sorted_examination_loc"].get(f"loc_list"))

                                for examination in local_data["sorted_examination_loc"].get(f"deleted"):
                                    date_time, doctor_name, patient_info = examination.split('___')
                                    cur.execute(f"DELETE from examination "
                                                f"WHERE date_time LIKE '{date_time}' "
                                                f"AND doctor_name LIKE '{doctor_name}' "
                                                f"AND patient_info LIKE '{patient_info}' ")
                                load_info_text.set("ОК")

                            elif path_mark == 'loc':
                                load_info_text.set("Локальные... ")

                                cur.execute("DELETE from examination WHERE status LIKE 'deleted'")
                                cur.execute(f"UPDATE examination SET status = 'srv'")
                                load_info_text.set("ОК")



                    except Exception as ex:
                        return f"Exception edit_local_db\n{ex}"

                load_info_text.set("Запись на сервер... ")

                if 'examination_db_place:____srv' in user.get('add_info'):
                    for examination in local_data.get("examination_srv"):
                        (date_time, doctor_name, status, LN_type,
                         patient_info, examination_text,
                         examination_key, add_info) = examination
                        if len(date_time.split(':')) == 2:
                            date_time += ":00"

                        key = f"{date_time}___{doctor_name}___{patient_info}"

                        if not (key in local_data["sorted_examination_loc"].get('srv') or
                                key in local_data["sorted_examination_loc"].get('deleted')):
                            local_data['sorted_examination_srv'].append(
                                (date_time, doctor_name, 'srv', LN_type,
                                 patient_info, examination_text,
                                 examination_key, add_info))

                    if local_data.get('sorted_examination_srv'):
                        with sq.connect(database=f"{local_data.get('loc')}") as conn:
                            cur = conn.cursor()
                            cur.executemany("INSERT INTO examination VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                            local_data.get(f"sorted_examination_srv"))

                load_info_text.set("Запись статистики... ")

                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                    cur = conn.cursor()
                    cur.execute(f"SELECT * FROM statistic_DOC_db")
                    found_data_statistic = cur.fetchall()

                if found_data_statistic:

                    try:
                        with sq.connect(f"{user['app_data'].get('path_srv_data_base')}data_base.db") as conn:
                            cur = conn.cursor()
                            cur.executemany("INSERT INTO statistic_DOC_db VALUES(?, ?, ?, ?, ?)",
                                            found_data_statistic)

                    except Exception as ex:

                        return f"Exception edit_local_db\n{ex}"
                    else:
                        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                            cur = conn.cursor()
                            cur.execute(f"DELETE FROM statistic_DOC_db")

                load_info_text.set("ОК")

                answer = f"Данные синхронизированы!\n\n" \
                         f"Выгружено осмотров на сервер: {len(local_data['sorted_examination_loc'].get('loc'))}\n" \
                         f"Удалено осмотров: {len(local_data['sorted_examination_loc'].get('deleted'))}\n" \
                         f"Всего осмотров в базе данных: " \
                         f"{len(local_data['sorted_examination_loc'].get('loc')) + len(local_data['sorted_examination_loc'].get('srv'))}\n" \
                         f"Загружено осмотров: {len(local_data.get('sorted_examination_srv'))}\n" \
                         f"Обновлено статистики: {len(found_data_statistic)}\n" \
                         f"Данные синхронизированы"

                load_info_text.set(answer)
                load_info_text.set('')

            # else:
            #
            #     if command == 'examination__delete':
            #         with sq.connect(f"{user['app_data'].get('path_srv_data_base')}examination_data_base.db") as connect:
            #             cursor = connect.cursor()
            #             cursor.execute(f"DELETE FROM examination WHERE rowid LIKE '{insert_data}'")
            #
            # elif command == 'examination__select_past_examination':
            #     try:
            #         with sq.connect(
            #                 database=f"{user['app_data'].get('path_srv_data_base')}examination_data_base.db",
            #                 timeout=10.0) as conn:
            #             cur = conn.cursor()
            #
            #             cur.execute(f"SELECT rowid, date_time, doctor_name, LN_type, patient_info, "
            #                         f"examination_text, examination_key "
            #                         f"FROM examination "
            #                         f"WHERE patient_info LIKE "
            #                         f"'{patient.get('name')}%{patient.get('birth_date')}'")
            #
            #             return 'srv', cur.fetchall()
            #     except Exception:
            #         with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            #             cur = conn.cursor()
            #
            #             cur.execute(f"SELECT rowid, date_time, doctor_name, LN_type, patient_info, "
            #                         f"examination_text, examination_key "
            #                         f"FROM examination "
            #                         f"WHERE patient_info LIKE "
            #                         f"'{patient.get('name')}%{patient.get('birth_date')}'")
            #
            #             return 'loc', cur.fetchall()

            #     elif command == 'examination__save':
            #         with sq.connect(f"{user['app_data'].get('path_srv_data_base')}examination_data_base.db") as conn:
            #             cur = conn.cursor()
            #             cur.execute("INSERT INTO examination VALUES(?, ?, ?, ?, ?, ?, ?, ?)", insert_data)
            #
            #     elif command == 'examination__delete_my_diagnosis':
            #         with sq.connect(f"{user['app_data'].get('path_srv_data_base')}application_data_base.db") as connect:
            #             cursor = connect.cursor()
            #             cursor.execute(f"DELETE FROM my_saved_diagnosis WHERE doctor_name LIKE "
            #                            f"'{user.get('doctor_name')}' AND diagnosis LIKE '{delete_data}'")
            #
            #
            #     elif command == 'examination__get_last_patient_ln':
            #         answer = dict()
            #         with sq.connect(f"{user['app_data'].get('path_srv_data_base')}examination_data_base.db") as conn:
            #             cur = conn.cursor()
            #             for type_ln in ("Справка ВН", "Лист ВН"):
            #                 cur.execute(f"SELECT date_time, LN_type FROM examination "
            #                             f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
            #                             f"AND patient_info LIKE "
            #                             f"'{patient.get('name')}%{patient.get('birth_date')}' "
            #                             f"AND LN_type LIKE '{type_ln}%'")
            #
            #                 answer[type_ln] = cur.fetchall()
            #         return answer
            #
            #     elif command == 'examination__edit_doctor_LN':
            #         with sq.connect(f"{user['app_data'].get('path_srv_data_base')}application_data_base.db") as connect:
            #             cursor = connect.cursor()
            #             cursor.execute(f"DELETE FROM my_LN "
            #                            f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
            #                            f"AND ln_type LIKE '{insert_data[0]}'")
            #
            #             cursor.execute("INSERT INTO my_LN VALUES(?, ?, ?)",
            #                            [user.get('doctor_name'), insert_data[0], insert_data[1]])
            #
            #             if not user.get('my_LN'):
            #                 user['my_LN'] = list()
            #             for i in user.get('my_LN'):
            #                 if insert_data[0] == i[0]:
            #                     user['my_LN'].remove(i)
            #             user['my_LN'].append(insert_data)
            #
            #
            #
            #
            #     elif command == 'examination__get_last_doc_LN':
            #         with sq.connect(f"{user['app_data'].get('path_srv_data_base')}examination_data_base.db") as conn:
            #             cur = conn.cursor()
            #             cur.execute(f"SELECT LN_type FROM examination "
            #                         f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
            #                         f"AND LN_type LIKE '{insert_data}%'")
            #             found_info_past = cur.fetchall()
            #         return found_info_past
            #
            #     elif command == 'examination__get_last_anthro_data':
            #         with sq.connect(f"{user['app_data'].get('path_srv_data_base')}examination_data_base.db") as conn:
            #             cur = conn.cursor()
            #
            #             cur.execute(f"SELECT date_time, examination_key FROM examination "
            #                         f"WHERE examination_key LIKE "
            #                         f"'{insert_data}' "
            #                         f"AND patient_info LIKE "
            #                         f"'{patient.get('name')}%{patient.get('birth_date')}'")
            #
            #             found_info = cur.fetchall()
            #         return found_info

        except Exception as ex:
            return False, ex
        else:
            return True, True

    elif command == 'last_examination':

        path = f".{os.sep}data_base{os.sep}"
        if user['app_data'].get('path_examination_data_base'):
            path = user['app_data'].get('path_examination_data_base')
        path_examination = f"{path}data_base.db"

        found_info = dict()

        with sq.connect(f"{path_examination}") as conn:
            cur = conn.cursor()

            for date in insert_data:
                cur.execute(f"SELECT date_time, status, patient_info, "
                            f"examination_text, examination_key "
                            f"FROM examination "
                            f"WHERE status NOT LIKE 'deleted' "
                            f"AND date_time LIKE '{date}%'"
                            f"AND doctor_name LIKE '{user.get('doctor_name')}'")
                found_info[date] = cur.fetchall()

        return found_info
