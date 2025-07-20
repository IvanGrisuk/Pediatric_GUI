import os
import re
import sqlite3 as sq

from tkinter import *
from tkinter import messagebox, Label, Frame, filedialog

from datetime import datetime, timedelta

all_patients_data = dict()
files = {
    'card_file_list': list(),
    'vaccination_file_list': list(),
}


def select_last_patient_info():
    with sq.connect(f'{os.sep}{os.sep}192.168.19.1{os.sep}database{os.sep}patient_data_base.db') as connect:
        cur = connect.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS patient_data (
                    district TEXT,
                    amb_cart TEXT,
                    Фамилия TEXT,
                    Имя TEXT,
                    Отчество TEXT,
                    Пол TEXT,
                    Дата_рождения TEXT,
                    Домашний_адрес TEXT,
                    Домашний_телефон TEXT,
                    Прививки_шапка TEXT,
                    Прививки TEXT)''')

        cur.execute(f"SELECT * "
                    f"FROM patient_data")
        found_data = cur.fetchall()

    for info in found_data:
        (district, amb_cart,
         name_1, name_2, name_3, gender,
         birth_date, address, phone, vac_1, vac_2) = info
        (district, amb_cart, name_1, name_2, name_3, gender, birth_date) = \
            (district.strip(),
             amb_cart.strip(),
             name_1.strip().replace(' ', ''),
             name_2.strip().replace(' ', ''),
             name_3.strip().replace(' ', ''),
             gender.strip(),
             birth_date.strip())

        data = {
            'district': district,
            '№ амбулаторной карты': amb_cart,
            'Фамилия': name_1,
            'Имя': name_2,
            'Отчество': name_3,
            'Пол': gender,
            'Дата рождения': birth_date,
            'Домашний адрес': address,
            'Домашний телефон': phone,
            'user_data': vac_1,
            'vaccination': vac_2}

        if amb_cart:
            all_patients_data[f"{amb_cart}"] = data
        else:
            all_patients_data[f"{name_1}_{name_2}_{name_3}_{birth_date}"] = data


def create_card_file_db(path):

    district = None
    add_info_marker = None

    with open(path, 'rb') as f:
        for line in f:
            loc_data = {
                'district': '',
                '№ амбулаторной карты': '',
                'Фамилия': '',
                'Имя': '',
                'Отчество': '',
                'Пол': '',
                'Дата рождения': '',
                'Домашний адрес': '',
                'Домашний телефон': ''
            }

            num, amb, name, birth_date, add_info = None, None, None, None, None,
            if len(line.split('__<!>__')) == 5:
                num, amb, name, birth_date, add_info = line.split('__<!>__')
            if num and not amb and not name and not birth_date and not add_info:
                district = num.replace('-й участок', '')
                continue
            if num and amb and name and birth_date and district:
                if len(name.split()) == 3:
                    loc_data['Фамилия'], loc_data['Имя'], loc_data['Отчество'] = name.split()
                elif len(name.split()) == 2:
                    loc_data['Фамилия'], loc_data['Имя'] = name.split()
                elif len(name.split()) == 1:
                    loc_data['Фамилия'] = name.split()

                if loc_data.get('Отчество'):
                    if loc_data['Отчество'][-1] == 'а':
                        loc_data['Пол'] = 'женский'
                    elif loc_data['Отчество'][-1] == 'ч':
                        loc_data['Пол'] = 'мужской'
                    else:
                        loc_data['Пол'] = 'мужской/женский'
                else:
                    loc_data['Пол'] = 'мужской/женский'

                loc_data['№ амбулаторной карты'] = amb
                loc_data['Дата рождения'] = birth_date

                if '(' in add_info:
                    loc_data['Домашний адрес'] = line[:line.index('(')]
                    loc_data['Домашний телефон'] = line[line.index('('):]

            marker_2 = f"{loc_data.get('Фамилия')}_{loc_data.get('Имя')}_{loc_data.get('Отчество')}_{loc_data.get('Дата рождения')}"
            if all_patients_data.get(marker_2):
                all_patients_data.pop(marker_2)
            if not all_patients_data.get(amb):
                all_patients_data[amb] = dict()

            for marker in loc_data:
                all_patients_data[amb][marker] = loc_data.get(marker)


def create_vaccination_db(path):
    def append_info():
        for flag in all_flag:
            all_flag[flag] = False
        all_flag['start'] = True

        if all_data.get('Фамилия, имя, отчество'):
            user_id = all_data.get('Карта профилактических прививок №').strip()
            user_data = f"Карта профилактических прививок № {user_id}\n" \
                        f"ФИО: {all_data.get('Фамилия, имя, отчество')}\t" \
                        f"Дата рождения: {all_data.get('Дата рождения')}\n" \
                        f"Домашний адрес: {all_data.get('Домашний адрес')}"
            vaccination = ''

            for i in all_tabs:
                vaccination += f'{i}\n'
                for q in all_data[i]:
                    if len(q) == 0:
                        continue
                    else:
                        flag = False
                        for d in q:
                            if d == ' ':
                                pass
                            else:
                                flag = True
                        if flag:
                            vaccination += f"{'__'.join(q)}\n"

            vaccination = vaccination.strip()

            info = all_patients_data_amb_cart.get(user_id)

            conflict_flag = False
            if info:
                for marker in all_data.get('Фамилия, имя, отчество').split():
                    if marker not in info:
                        if marker.lower().replace('ё', "е") not in info.lower().replace('ё', "е"):
                            with open('conflict_log.txt', 'a') as conflict_log:
                                conflict_log.write(f"\nCONFLICT create_vaccination_db "
                                                   f"{datetime.strftime(datetime.now(), '%d.%m.%y  %H:%M')}\n"
                                                   f"info: {info}\n"
                                                   f"ФИО_vac: {all_data.get('Фамилия, имя, отчество')} "
                                                   f"{user_id}\n"
                                                   f"DB_info: {all_patients_data.get(info)}\n\n")

                            conflict_flag = True
            else:
                info = f"{all_data.get('Фамилия, имя, отчество')}_{all_data.get('Дата рождения')}"
            if not conflict_flag:
                if not all_patients_data.get(info):
                    all_patients_data[info] = dict()
                    all_patients_data[info]['№ амбулаторной карты'] = user_id

                all_patients_data[info]['user_data'] = user_data
                all_patients_data[info]['vaccination'] = vaccination
                return True
            return False

    pattern = r'<[^>]*>'
    info_drop = [
        "Возраст приви- ваемого",
        "Дата проведения прививки",
        "Тип иммуни- зации",
        "Наименование препарата",
        "Страна изготовитель препарата",
        "Доза препа- рата",
        "Серия",
        "Реакция на прививку",
        "Медицинский отвод"
    ]

    all_tabs = (
        'Прививки против туберкулёза',
        'Прививки против гепатита В',
        'Прививки против кори, эпидемического паротита и краснухи',
        'Прививки против полиомиелита',
        'Прививки против дифтерии, коклюша, столбняка',
        'Прививки против других инфекций'
    )
    all_flag = {
        'start': False,
        'Карта профилактических прививок №': False,
        'Фамилия, имя, отчество': False,
        'Дата рождения': False,
        'Домашний адрес': False,
        'Прививки против туберкулёза': False,
        'Прививки против гепатита В': False,
        'Прививки против кори, эпидемического паротита и краснухи': False,
        'Прививки против полиомиелита': False,
        'Прививки против дифтерии, коклюша, столбняка': False,
        'Прививки против других инфекций': False
    }

    all_data = {
        'Карта профилактических прививок №': '',
        'Фамилия, имя, отчество': '',
        'Дата рождения': '',
        'Домашний адрес': '',
        'Прививки против туберкулёза': [],
        'Прививки против гепатита В': [],
        'Прививки против кори, эпидемического паротита и краснухи': [],
        'Прививки против полиомиелита': [],
        'Прививки против дифтерии, коклюша, столбняка': [],
        'Прививки против других инфекций': []
    }

    counter_string = 0
    counter_error = 0
    counter_patients = 0
    with open(path, 'rb') as file:

        for line in file:
            counter_string += 1

            line_str = ' '.join(line.decode('windows-1251').replace('&nbsp;', ' ').replace('<br>', ' ').split())
            if '<tr height=' in line_str:

                res = 'new tab'

            else:
                res = re.sub(pattern, '', line_str)

            if len(res) != 0:

                if 'Учреждение здравоохранения "19-я городская детская поликлиника' in res:
                    if append_info():
                        counter_patients += 1
                    else:
                        counter_error += 1

                    all_data = {
                        'Карта профилактических прививок №': '',
                        'Фамилия, имя, отчество': '',
                        'Дата рождения': '',
                        'Домашний адрес': '',
                        'Прививки против туберкулёза': [],
                        'Прививки против гепатита В': [],
                        'Прививки против кори, эпидемического паротита и краснухи': [],
                        'Прививки против полиомиелита': [],
                        'Прививки против дифтерии, коклюша, столбняка': [],
                        'Прививки против других инфекций': []}

                if all_flag['start']:

                    if 'Карта профилактических прививок №' in res:
                        all_flag['Карта профилактических прививок №'] = True
                        continue
                    if all_flag['Карта профилактических прививок №']:
                        all_data['Карта профилактических прививок №'] = res
                        all_flag['Карта профилактических прививок №'] = False

                    if 'Фамилия, имя, отчество' in res:
                        all_flag['Фамилия, имя, отчество'] = True
                        continue
                    if all_flag['Фамилия, имя, отчество']:
                        all_data['Фамилия, имя, отчество'] = res
                        all_flag['Фамилия, имя, отчество'] = False

                    if 'Дата рождения' in res:
                        all_flag['Дата рождения'] = True
                        continue
                    if all_flag['Дата рождения']:
                        all_data['Дата рождения'] = res
                        all_flag['Дата рождения'] = False

                    if 'Домашний адрес' in res:
                        all_flag['Домашний адрес'] = True
                        continue
                    if all_flag['Домашний адрес']:
                        all_data['Домашний адрес'] = res
                        all_flag['Домашний адрес'] = False

                    for i in all_tabs:
                        if i in res:
                            for q in all_flag:
                                if q != 'start':
                                    all_flag[q] = False
                            all_flag[i] = True
                            all_data[i].append([])
                            continue

                        elif all_flag[i]:
                            if res not in info_drop and res not in all_tabs:
                                if res == 'new tab':
                                    if len(all_data[i][-1]) < 9:
                                        all_data[i].pop()
                                    all_data[i].append([])
                                else:
                                    all_data[i][-1].append(res)

        else:
            if all_data.get('Фамилия, имя, отчество'):
                if append_info():
                    counter_patients += 1
                else:
                    counter_error += 1
    path = path.replace(f'.{os.sep}Archive{os.sep}Загрузка_обновлений_БД{os.sep}', '')
    await edit_message_text(message=message,
                            text=f"База данных прививок \n{path}\n участка успешно обновлена\n"
                                 f"Количество строк: {counter_string}\n"
                                 f"Количество пациентов: {counter_patients}\n"
                                 f"Количество ошибок: {counter_error}")


def search_in_dir(path):
    def check_file(file_name):
        if '.csv' in file_name:
            with open(f'{path}{file_name}', 'rb') as f:
                for line in f:
                    line_str = ' '.join(
                        line.decode('windows-1251').replace('&nbsp;', ' ').replace('<br>', ' ').split())

                    if 'Картотека пациентов' in line_str:
                        files['card_file_list'].append(f"{path}{file_name}")
                        break

                    elif 'Карта профилактических прививок' in line_str:
                        files['vaccination_file_list'].append(f"{path}{file_name}")
                        break

    files['card_file_list'].clear()
    files['vaccination_file_list'].clear()

    if os.path.isdir(path):

        for file in sorted(os.listdir(path)):
            if os.path.isdir(f'{path}{file}'):
                search_in_dir(path=f'{path}{file}{os.sep}')
            else:
                check_file(f'{path}{file}')
    else:
        check_file(path)


def write_in_db():
    local_patient_data = list()
    for patient_name in all_patients_data:
        local_data = list()
        for marker in ('district',
                       '№ амбулаторной карты',
                       'Фамилия',
                       'Имя',
                       'Отчество',
                       'Пол',
                       'Дата рождения',
                       'Домашний адрес',
                       'Домашний телефон',
                       'user_data',
                       'vaccination'):
            local_data.append(all_patients_data[patient_name].get(marker, ''))
        local_patient_data.append(local_data)

    with sq.connect(f'{os.sep}{os.sep}192.168.19.1{os.sep}database{os.sep}patient_data_base.db') as connect:
        cur = connect.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS patient_data (
                    district TEXT,
                    amb_cart TEXT,
                    Фамилия TEXT,
                    Имя TEXT,
                    Отчество TEXT,
                    Пол TEXT,
                    Дата_рождения TEXT,
                    Домашний_адрес TEXT,
                    Домашний_телефон TEXT,
                    Прививки_шапка TEXT,
                    Прививки TEXT)''')

        cur.execute(f"DELETE FROM patient_data")
        cur.executemany(f"INSERT INTO patient_data VALUES({'?, ' * 10}?)", local_patient_data)

        cur.execute(f'''CREATE TABLE IF NOT EXISTS last_edit (last_edit TEXT)''')
        cur.execute(f"DELETE FROM last_edit")
        now = datetime.strftime(datetime.now(), "%d.%m.%y__%H:%M")
        cur.execute(f"INSERT INTO last_edit VALUES ('{now}')")
    return len(local_patient_data)


def create_main_root():
    def select_path():
        filepath = filedialog.askopenfilenames()
        if filepath:
            print(datetime.strftime(datetime.now(), "%d.%m.%y__%H:%M:%S"), filepath)

    root = Tk()
    root.title(f"Обновление базы данных")
    root.config(bg="#36566d")
    root.geometry('+0+0')

    Button(master=root,
           text="Выбрать файлы",
           font=('Comic Sans MS', 12),
           command=select_path
           ).pack(fill='both', expand=True, padx=40, pady=10)
    root.mainloop()


if __name__ == '__main__':
    create_main_root()
