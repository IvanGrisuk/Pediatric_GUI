import os
from tkinter import *
import sqlite3 as sq
from tkinter import messagebox, Label, Frame


from variables import patient, app_info, user
from util_func import paste_new_frame, get_age_d_m_y


def search_patient():
    search_data = {
        'found_patient_root': None,
        'found_patient_data': dict()
    }


    def select_patient():
        patient.clear()
        with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT "
                        f"district, amb_cart, Surname, Name, Patronymic, "
                        f"gender, birth_date, address, phone, vacc_title, vacc_data, passport, "
                        f"weight, height, vision, chickenpox, allergy, injury, "
                        f"posture, health_group, fiz_group, diet, diagnosis, add_info "
                        f"FROM patient_data "
                        f"WHERE rowid LIKE '{selected_patient.get()}'")
            found_data = cur.fetchone()
            (patient["district"],
            patient["amb_cart"],
            patient["Surname"],
            patient["Name"],
            patient["Patronymic"],
            patient["gender"],
            patient["birth_date"],
            patient["address"],
            patient["phone"],
            patient["vacc_title"],
            patient["vacc_data"],
            patient["passport"],
            patient["weight"],
            patient["height"],
            patient["vision"],
            patient["chickenpox"],
            patient["allergy"],
            patient["injury"],
            patient["posture"],
            patient["health_group"],
            patient["fiz_group"],
            patient["diet"],
            patient["diagnosis"],
            patient["add_info"]) = found_data


        for key in patient:
            if patient.get(key) == '':
                patient[key] = "Нет данных"

        patient['name'] = f"{patient.get('Surname')} {patient.get('Name')} {patient.get('Patronymic')}"
        patient['age'] = get_age_d_m_y(patient.get('birth_date'))
        patient_info_text = app_info['title_frame'].get('patient_info_text')

        patient_info_text.set(
            f"Пациент: {patient.get('name')}    "
            f"Дата рождения: {patient.get('birth_date')}    "
            f"Возраст: {patient['age'].get('age_txt')}\n"
            
            f"Адрес: {patient.get('address')}    "
            f"Телефон: {patient.get('phone')}    "
            f"№ амб: {patient.get('amb_cart')}    "
            f"Участок: {patient.get('district')}    "
            f"Паспорт: {patient.get('passport', 'Нет данных')}")
        search_root.destroy()

    def button_search_in_db(event=None):
        if search_data.get('found_patient_root'):
            search_data['found_patient_root'].destroy()
        search_root.update()

        word_list = ["qwertyuiopasdfghjkl;'zxcvbnm,.", "йцукенгшщзфывапролджэячсмитьбю"]
        patient_data = txt_patient_data_variable.get()
        name = list()

        for i in patient_data.split():
            if i[0] in word_list[0]:
                name_0 = ''
                for q in i.lower():
                    if q in word_list[0]:
                        name_0 += word_list[1][word_list[0].index(q)]
                    else:
                        name_0 += q
                name.append(name_0.capitalize())
            else:
                name.append(i.capitalize())

        sql_str = ''
        if patient_data.isdigit():
            sql_str += f"amb_cart LIKE '{patient_data}%'"
        else:
            for i in patient_data:
                if i.isdigit():
                    sql_str += "address LIKE '"
                    for q in name:
                        sql_str += f"%{q}"
                    sql_str += "%'"
                    break
            else:

                if len(name) == 1:
                    sql_str += f"Surname LIKE '{name[0]}%'"
                elif len(name) == 2:
                    sql_str += f"Surname LIKE '{name[0]}%' AND Name LIKE '{name[1]}%'"
                elif len(name) == 3:
                    sql_str += f"Surname LIKE '{name[0]}%' AND Name LIKE '{name[1]}%' AND Patronymic LIKE '{name[2]}%'"

                elif len(patient_data.split()) > 3:
                    messagebox.showinfo('Ошибка', 'Неверный формат ввода!\n'
                                                  'Ожидалось максимум 3 блока данных\n'
                                                  f'Получено: <b>{len(patient_data.split())}</b> блоков\n'
                                                  f'Измените запрос')

        if not sql_str:
            counter_patient.set('Ошибка!\n'
                                'По введенной информации не удалось сформулировать sql запрос')


        else:
            with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
                cur = conn.cursor()
                cur.execute(f"SELECT "
                            f"rowid, district, amb_cart, Surname, Name, Patronymic, "
                            f"gender, birth_date, address, phone "
                            f"FROM patient_data WHERE {sql_str}")
                found_data = cur.fetchall()

            if len(found_data) < 1:
                counter_patient.set("Найдено пациентов: 0")
                counter_patient.set("По введенной информации не удалось найти пациента")
                # messagebox.showinfo('Ошибка', 'По введенной информации не удалось найти пациента')

            else:
                search_data['found_patient_data'].clear()
                if len(found_data) == 1:
                    search_data['found_patient_data'][found_data[0][0]] = found_data[0]
                    selected_patient.set(found_data[0][0])
                    select_patient()

                else:

                    frame_search = Frame(master=search_root, bg="#36566d")
                    search_data['found_patient_root'] = frame_search
                    counter_patient.set(f"Найдено пациентов: {len(found_data)}")
                    split_len = {
                        'col_1': 0,
                        'col_2': 0,
                        'col_3': 0,
                        'col_4': 0}
                    for info in found_data:
                        (rowid, district, amb_cart,
                         name_1, name_2, name_3,
                         gender, birth_date, address, phone) = info

                        for mark_1, mark_2 in (
                                (district, 'col_1'),
                                (amb_cart, 'col_2'),
                                (f"{name_1} {name_2} {name_3}", 'col_3')):
                            if len(mark_1) > split_len.get(mark_2):
                                split_len[mark_2] = len(mark_1)

                    for info in found_data:
                        (rowid, district, amb_cart,
                         name_1, name_2, name_3,
                         gender, birth_date, address, phone) = info
                        search_data['found_patient_data'][rowid] = info

                        text = f"Участок: {district};" + ' ' * (split_len.get('col_1') - len(district))
                        text += f"\t№ амб: {amb_cart};" + ' ' * (split_len.get('col_2') - len(amb_cart))
                        text += f"\tФИО: {name_1.capitalize()} {name_2.capitalize()} {name_3.capitalize()}" \
                                + ' ' * (split_len.get('col_3') - len(f"{name_1} {name_2} {name_3}"))
                        text += f"  \t{birth_date};  "
                        text += f"  \tАдрес: {address}"

                        Radiobutton(master=frame_search, text=text,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    compound='left',
                                    command=select_patient,
                                    value=rowid, variable=selected_patient,
                                    indicatoron=False, selectcolor='#77f1ff',
                                    anchor='w'
                                    ).pack(fill='both', expand=True, padx=2, pady=2, anchor='w')
                    frame_search.columnconfigure(index='all', minsize=40, weight=1)
                    frame_search.rowconfigure(index='all', minsize=20)
                    frame_search.pack(fill='both', expand=True, padx=2, pady=2)

    txt_patient_data_variable = StringVar()
    canvas_frame = app_info['scrolled_frame'].get('scrolled_frame')

    search_root = Frame(master=canvas_frame, bg="#36566d")

    frame_title = Frame(master=search_root, bg="#36566d")
    Label(frame_title, text='Поиск пациентов',
          font=('Comic Sans MS', user.get('text_size')), bg="#36566d", fg='white'
          ).pack(fill='both', expand=True, padx=2, side='left')

    text_patient_data = Entry(frame_title, width=100,
                              font=('Comic Sans MS', user.get('text_size')),
                              textvariable=txt_patient_data_variable)
    text_patient_data.pack(fill='both', expand=True, padx=2, side='left')
    text_patient_data.focus()
    text_patient_data.bind('<Return>', button_search_in_db)

    Button(frame_title, text='Найти', command=button_search_in_db,
           font=('Comic Sans MS', user.get('text_size'))
           ).pack(fill='both', expand=True, padx=2, side='left')

    counter_patient = StringVar()
    selected_patient = StringVar()
    Label(frame_title,
          textvariable=counter_patient,
          font=('Comic Sans MS', user.get('text_size')),
          bg="#36566d", fg='white'
          ).pack(fill='both', expand=True, padx=2, side='left')
    frame_title.pack(fill='both', expand=True, padx=2, pady=2)
    counter_patient.set('')
    paste_new_frame(search_root)
