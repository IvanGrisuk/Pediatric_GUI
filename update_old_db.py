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
    'path_DB': ''
}

def select_last_patient_info():
    with sq.connect(files.get('path_DB')) as connect:
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

    add_info_marker = None
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
    with open(path, 'rb') as f:
        for line in f:
            line = line.decode()


            num, amb, name, birth_date, add_info = None, None, None, None, None,
            if len(line.split('__<!>__')) == 5:
                num, amb, name, birth_date, add_info = line.split('__<!>__')
                num = ' '.join(num.strip().split())
                amb = ' '.join(amb.strip().split())
                name = ' '.join(name.strip().split())
                birth_date = ' '.join(birth_date.strip().split())
                add_info = ' '.join(add_info.strip().split())

            if num and not amb and not name and not birth_date and not add_info:
                loc_data['district'] = num.replace('-й участок', '')
                continue
            if num and amb and name and birth_date:
                if len(name.split()) == 3:
                    loc_data['Фамилия'], loc_data['Имя'], loc_data['Отчество'] = name.split()
                elif len(name.split()) == 2:
                    loc_data['Фамилия'], loc_data['Имя'] = name.split()
                else:
                    loc_data['Фамилия'] = name


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
                    loc_data['Домашний адрес'] = add_info[:add_info.index('(')]
                    loc_data['Домашний телефон'] = add_info[add_info.index('('):]
                else:
                    loc_data['Домашний адрес'] = add_info


            marker_2 = f"{loc_data.get('Фамилия')}_{loc_data.get('Имя')}_{loc_data.get('Отчество')}_{loc_data.get('Дата рождения')}"
            if all_patients_data.get(marker_2):
                all_patients_data.pop(marker_2)
            if not all_patients_data.get(amb):
                all_patients_data[amb] = dict()

            for marker in loc_data:
                all_patients_data[amb][marker] = loc_data.get(marker)
                if marker != 'district':
                    loc_data[marker] = ''


def create_vaccination_db(path):
    def append_info():

        if all_data.get('Фамилия, имя, отчество'):
            user_id = all_data.get('Карта профилактических прививок №').strip()
            user_data = f"Карта профилактических прививок № {user_id}\n" \
                        f"ФИО: {all_data.get('Фамилия, имя, отчество')}\t" \
                        f"Дата рождения: {all_data.get('Дата рождения')}\n" \
                        f"Домашний адрес: {all_data.get('Домашний адрес')}"
            vaccination = ''

            for tab_name in all_tabs:
                vaccination += f'{tab_name}\n'
                for q in all_data[tab_name]:
                    if len(q) == 0:
                        continue
                    else:
                        flag = False
                        for d in q:
                            if d in (' ', ''):
                                pass
                            else:
                                flag = True
                        if flag:
                            vaccination += f"{'__'.join(q)}\n"

            vaccination = vaccination.strip()
            conflict_flag = False

            if all_patients_data.get(user_id):
                check_name = (f"{all_patients_data.get(user_id, dict()).get('Фамилия', '')}"
                              f"{all_patients_data.get(user_id, dict()).get('Имя', '')}"
                              f"{all_patients_data.get(user_id, dict()).get('Отчество', '')}")
                if check_name:
                    for marker in all_data.get('Фамилия, имя, отчество').split():
                        if marker not in check_name:
                            if marker.lower().replace('ё', "е") not in check_name.lower().replace('ё', "е"):

                                with open('conflict_log.txt', 'a') as conflict_log:
                                    conflict_log_txt = (f"\nCONFLICT create_vaccination_db "
                                                       f"{datetime.strftime(datetime.now(), '%d.%m.%y  %H:%M:%S')}\n"
                                                       f"check_name: {check_name}\n"
                                                       f"ФИО_vac: {all_data.get('Фамилия, имя, отчество')} "
                                                       f"{user_id}\n"
                                                       f"DB_check_name: {all_patients_data.get(user_id)}\n")
                                    messagebox_txt = (f"Пропустить? \nБаза данных:\n"
                                                      f"ФИО: {all_patients_data.get(user_id, dict()).get('Фамилия', '')}"
                                                      f" {all_patients_data.get(user_id, dict()).get('Имя', '')}"
                                                      f" {all_patients_data.get(user_id, dict()).get('Отчество', '')} "
                                                      f"Дата рождения: {all_patients_data.get(user_id, dict()).get('Дата рождения')}\n"
                                                      f"Домашний адрес: {all_patients_data.get(user_id, dict()).get('Домашний адрес')}\n\n"
                                                      f"VACC_DATA:\n"
                                                      f"{user_data}")


                                    conflict_flag = messagebox.askyesno('CONFLICT',
                                                                 messagebox_txt)


                                    conflict_log.write(conflict_log_txt)
                                    print(conflict_log_txt)


            if not conflict_flag:
                if not all_patients_data.get(user_id):

                    all_patients_data[user_id] = dict()
                    all_patients_data[user_id]['№ амбулаторной карты'] = user_id

                if not all_patients_data[user_id].get('Фамилия'):
                    name = all_data.get('Фамилия, имя, отчество')
                    if len(name.split()) == 3:
                        all_patients_data[user_id]['Фамилия'], all_patients_data[user_id]['Имя'], all_patients_data[user_id]['Отчество'] = name.split()
                    elif len(name.split()) == 2:
                        all_patients_data[user_id]['Фамилия'], all_patients_data[user_id]['Имя'] = name.split()
                    else:
                        all_patients_data[user_id]['Фамилия'] = name

                    if all_patients_data[user_id].get('Отчество'):
                        if all_patients_data[user_id]['Отчество'][-1] == 'а':
                            all_patients_data[user_id]['Пол'] = 'женский'
                        elif all_patients_data[user_id]['Отчество'][-1] == 'ч':
                            all_patients_data[user_id]['Пол'] = 'мужской'
                        else:
                            all_patients_data[user_id]['Пол'] = 'мужской/женский'
                    else:
                        all_patients_data[user_id]['Пол'] = 'мужской/женский'

                    all_patients_data[user_id]['Дата рождения'] = all_data.get('Дата рождения')
                    all_patients_data[user_id]['Домашний адрес'] = all_data.get('Домашний адрес')

                marker_2 = f"{all_patients_data[user_id].get('Фамилия')}_{all_patients_data[user_id].get('Имя')}_{all_patients_data[user_id].get('Отчество')}_{all_patients_data[user_id].get('Дата рождения')}"
                if all_patients_data.get(marker_2):
                    all_patients_data.pop(marker_2)


                all_patients_data[user_id]['user_data'] = user_data
                all_patients_data[user_id]['vaccination'] = vaccination


        all_flag['flag'] = ''
        all_tabs.clear()


    all_tabs = list()
    all_flag = {
        'flag': ''
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

    with open(path, 'rb') as file:

        for line in file:
            line = line.decode()
            res = list()
            for mark in line.split('__<!>__'):
                mark = ' '.join(mark.strip().split())
                if mark:
                    res.append(mark)
            if not res:
                continue

            if res[0].startswith('Приложение 1'):
                append_info()
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


                continue


            if 'Карта профилактических прививок №' in res:
                all_flag['flag'] = 'Карта профилактических прививок №'
                continue

            if all_flag.get('flag') == 'Карта профилактических прививок №':
                all_data['Карта профилактических прививок №'] = res[0]
                all_flag['flag'] = ''

            if res[0].startswith('Фамилия, '):
                all_data['Фамилия, имя, отчество'] = res[-1]
                continue

            if 'Дата рождения' in res:
                all_data['Дата рождения'] = res[-1]
                continue

            if 'Домашний адрес' in res:
                all_data['Домашний адрес'] = ' '.join(res[-1].split())

                continue

            if res[0].startswith('Прививки против') or res[0].startswith('Реакция'):
                all_flag['flag'] = res[0]
                if not all_data.get(res[0]):
                    all_tabs.append(res[0])
                    all_data[res[0]] = list()

                continue

            if res[0] == 'Возраст приви- ваемого':
                continue

            if all_flag.get('flag').startswith('Прививки против') or all_flag.get('flag').startswith('Реакция'):
                vac_mark = all_flag.get('flag')
                info = line.split('__<!>__')
                all_data[vac_mark].append([
                    ' '.join(info[0].strip().split()),
                    ' '.join(info[1].strip().split()),
                    ' '.join(info[5].strip().split()),
                    ' '.join(info[7].strip().split()),
                    ' '.join(info[12].strip().split()),
                    ' '.join(info[15].strip().split()),
                    ' '.join(info[18].strip().split()),
                    ' '.join(info[20].strip().split()),
                    ' '.join(info[22].strip().split())
                ])


        else:
            if all_data.get('Фамилия, имя, отчество'):
                append_info()


def search_in_dir(path):
    def check_file(file_name):
        if '.csv' in file_name:
            with open(f'{file_name}', 'rb') as f:
                for line in f:
                    line_str = line.decode()

                    if 'Карта профилактических прививок' in line_str:
                        files['vaccination_file_list'].append(f"{file_name}")
                        break
                else:
                    files['card_file_list'].append(f"{file_name}")

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

    with sq.connect(files.get('path_DB')) as connect:
        cur = connect.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS patient_data ("
                    "district TEXT, "
                    "amb_cart TEXT, "
                    "Фамилия TEXT, "
                    "Имя TEXT, "
                    "Отчество TEXT, "
                    "Пол TEXT, "
                    "Дата_рождения TEXT, "
                    "Домашний_адрес TEXT, "
                    "Домашний_телефон TEXT, "
                    "Прививки_шапка TEXT, "
                    "Прививки TEXT)")

        cur.execute(f"DELETE FROM patient_data")
        for data in local_patient_data:
            cur.execute(f"INSERT INTO patient_data VALUES({'?, ' * 10}?)", data)

        cur.execute(f'''CREATE TABLE IF NOT EXISTS last_edit (last_edit TEXT)''')
        cur.execute(f"DELETE FROM last_edit")
        now = datetime.strftime(datetime.now(), "%d.%m.%y__%H:%M")
        cur.execute(f"INSERT INTO last_edit VALUES ('{now}')")
    return len(local_patient_data)


def create_main_root():
    def select_path():
        filepath = filedialog.askopenfilenames()
        if not filepath:
            return
        files['card_file_list'].clear()
        files['vaccination_file_list'].clear()
        for path in filepath:
            path = os.path.abspath(path)
            search_in_dir(path)
        txt = ''
        for marker in ('card_file_list', 'vaccination_file_list'):
            txt += marker + '\n'
            for path in files.get(marker):
                txt += f"'{path.split(os.sep)[-1]}'; "
        search_path.set(txt.strip())


    def select_db_path():
        filepath = filedialog.askopenfilename()
        if filepath:
            files['path_DB'] = os.path.abspath(filepath)
            db_path.set(os.path.abspath(filepath))

    def update():
        if not files.get('path_DB'):
            return
        log_info.set('select_last_patient_info')
        root.update()
        select_last_patient_info()
        for file in files.get('card_file_list'):
            log_info.set(f"{log_info.get()}\ncard_file -- {file}")
            root.update()
            create_card_file_db(file)
        for file in files.get('vaccination_file_list'):
            log_info.set(f"{log_info.get()}\nvaccination -- {file}")
            root.update()
            create_vaccination_db(file)
        log_info.set(f"{log_info.get()}\nwrite_in_db")
        root.update()
        write_in_db()

        log_info.set(f"{log_info.get()}\nFINISH")




    root = Tk()
    root.title(f"Обновление базы данных")
    root.config(bg="#36566d")
    root.geometry('+0+0')
    db_path = StringVar()
    search_path = StringVar()
    log_info = StringVar()


    frame = Frame(root)
    Button(master=frame,
           text="Выбрать БД",
           font=('Comic Sans MS', 10),
           command=select_db_path
           ).pack(fill='both', expand=True, padx=20, pady=10, side='left')
    Label(frame, textvariable=db_path,
          font=('Comic Sans MS', 10),
          bg="#36566d", fg='white', anchor='nw', justify='left'
          ).pack(fill='x', expand=True, padx=2, pady=4, side='left')
    frame.pack(fill='both', expand=True)

    frame = Frame(root)
    Button(master=frame,
           text="Выбрать файлы",
           font=('Comic Sans MS', 10),
           command=select_path
           ).pack(fill='both', expand=True, padx=20, pady=10, side='left')
    Label(frame, textvariable=search_path,
          font=('Comic Sans MS', 10),
          bg="#36566d", fg='white', anchor='nw', justify='left', wraplength=700
          ).pack(fill='x', expand=True, padx=2, pady=4, side='left')
    frame.pack(fill='both', expand=True)

    Button(master=root,
           text="Обновить",
           font=('Comic Sans MS', 10),
           command=update
           ).pack(fill='both', expand=True, padx=40, pady=10)

    Label(root, textvariable=log_info,
          font=('Comic Sans MS', 10),
          bg="#36566d", fg='white', anchor='nw', justify='left'
          ).pack(fill='x', expand=True, padx=2, pady=4, )

    root.mainloop()


if __name__ == '__main__':
    create_main_root()
