from tkinter import *
from tkinter import ttk
import sqlite3 as sq
from datetime import datetime, timedelta
from tkinter.ttk import Combobox
from tkinter import scrolledtext, messagebox
from docx import Document
from docx.shared import Cm
from docx.shared import Pt
import os

import shutil

import pyperclip

import decoding_name
import certificate as cert

patient = {
    'name': '',
    'birth_date': '',
    'gender': '',
    'amb_cart': '',
    'patient_district': '',
    'address': ''
}


def data_base():
    with sq.connect('data_base.db') as conn:
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS врачи "
                    "(doctor_name text, district text, ped_div text, manager text, open_mark text)")
        cur.execute(f"SELECT doctor_name FROM врачи")
        doctor_data = list()
        for i in cur.fetchall():
            doctor_data.append(i[0])
        print('doctor_data:', doctor_data)
        if not doctor_data:
            cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)", ['Иванов И.И.', 1, 1, 'Петров П.П.', True])

        cur.execute(f"SELECT doctor_name, district, ped_div, manager, open_mark FROM врачи")
        flag = False
        doctor_data = cur.fetchall()
        for doctor_name, district, ped_div, manager, open_mark in doctor_data:
            if open_mark:
                flag = True
        if not flag:
            cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE 'Иванов И.И.'")
            cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)", ['Иванов И.И.', 1, 1, 'Петров П.П.', True])


def updating_patient_data_base():
    try:
        shutil.copy2(r"\\SRV2\data_base\patient_data_base.db", f"patient_data_base.db")
    except Exception as ex:
        messagebox.showinfo('Ошибка', f'Ошибка обновления базы данных!\n{ex}')
    else:
        messagebox.showinfo('Успех!', 'База данных обновлена')


def get_doctor_data():
    with sq.connect('data_base.db') as conn:
        cur = conn.cursor()

        cur.execute(f"SELECT doctor_name, district, ped_div, manager FROM врачи "
                    f"WHERE open_mark LIKE '1'")
    return cur.fetchone()


def redact_doctor():
    def save():

        doctor_name = txt_doctor_name.get()
        manager = txt_manager.get()
        district = txt_district.get()
        ped_div = txt_ped_div.get()
        if not doctor_name:
            messagebox.showinfo('Ошибка', 'Ошибка имени доктора!')
        elif not manager:
            messagebox.showinfo('Ошибка', 'Ошибка имени заведующего!')
        elif not district or not district.isdigit():
            messagebox.showinfo('Ошибка', 'Ошибка участка!\nУкажите участок числом')
        elif not ped_div or not ped_div.isdigit():
            messagebox.showinfo('Ошибка', 'Ошибка ПО\nУкажите номер ПО числом')
        else:
            new_doctor = [doctor_name, district, ped_div, manager, True]

            try:
                with sq.connect('data_base.db') as conn:
                    cur = conn.cursor()
                    cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{doctor_name}'")

                    cur.execute(f"SELECT doctor_name, district, ped_div, manager FROM врачи")
                    data = cur.fetchall()
                    for doctor_name, district, ped_div, manager in data:
                        cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{doctor_name}'")
                        cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)",
                                    [doctor_name, district, ped_div, manager, False])

                    cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)", new_doctor)
            except Exception as ex:
                messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{ex}')
            else:
                messagebox.showinfo('Успешно', 'Данные успешно сохранены!')
                combo_doc['values'] = get_doc_names()
                combo_doc.current(0)

                new_root.destroy()
                write_lbl_doc()

    old_doctor_name, old_district, old_ped_div, old_manager = get_doctor_data()

    new_root = Tk()
    new_root.title('Изменение данных')

    Label(new_root, text='ФИО доктора: ', font=('Comic Sans MS', 20)).grid(column=0, row=0)
    Label(new_root, text='ФИО заведующего: ', font=('Comic Sans MS', 20)).grid(column=0, row=1)
    Label(new_root, text='Номер участка: ', font=('Comic Sans MS', 20)).grid(column=0, row=2)
    Label(new_root, text='Номер ПО: ', font=('Comic Sans MS', 20)).grid(column=0, row=3)

    txt_doctor_name = Entry(new_root, width=30, font=('Comic Sans MS', 20))
    txt_doctor_name.insert(0, old_doctor_name)
    txt_doctor_name.grid(column=1, row=0)

    txt_manager = Entry(new_root, width=30, font=('Comic Sans MS', 20))
    txt_manager.insert(0, old_manager)
    txt_manager.grid(column=1, row=1)

    txt_district = Entry(new_root, width=5, font=('Comic Sans MS', 20))
    txt_district.insert(0, old_district)
    txt_district.grid(column=1, row=2)

    txt_ped_div = Entry(new_root, width=5, font=('Comic Sans MS', 20))
    txt_ped_div.insert(0, old_ped_div)
    txt_ped_div.grid(column=1, row=3)

    Button(new_root, text='Сохранить', command=save, font=('Comic Sans MS', 20)).grid()

    new_root.mainloop()


def add_new_doctor():
    def save():
        doctor_name = txt_doctor_name.get()
        manager = txt_manager.get()
        district = txt_district.get()
        ped_div = txt_ped_div.get()
        if not doctor_name:
            messagebox.showinfo('Ошибка', 'Ошибка имени доктора!')
        elif not manager:
            messagebox.showinfo('Ошибка', 'Ошибка имени заведующего!')
        elif not district or not district.isdigit():
            messagebox.showinfo('Ошибка', 'Ошибка участка!\nУкажите участок числом')
        elif not ped_div or not ped_div.isdigit():
            messagebox.showinfo('Ошибка', 'Ошибка ПО\nУкажите номер ПО числом')
        else:
            new_doctor = [doctor_name, district, ped_div, manager, True]

            try:
                with sq.connect('data_base.db') as conn:
                    cur = conn.cursor()

                    cur.execute(f"SELECT doctor_name, district, ped_div, manager FROM врачи")
                    data = cur.fetchall()
                    for doctor_name, district, ped_div, manager in data:
                        cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{doctor_name}'")
                        cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)",
                                    [doctor_name, district, ped_div, manager, False])

                    cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)", new_doctor)
            except Exception as ex:
                messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{ex}')
            else:
                messagebox.showinfo('Успешно', 'Данные успешно сохранены!')
                combo_doc['values'] = get_doc_names()
                combo_doc.current(0)

                new_root.destroy()
                write_lbl_doc()

    new_root = Tk()
    new_root.title('Новая учетная запись')

    Label(new_root, text='ФИО доктора: ', font=('Comic Sans MS', 20)).grid(column=0, row=0)
    Label(new_root, text='ФИО заведующего: ', font=('Comic Sans MS', 20)).grid(column=0, row=1)
    Label(new_root, text='Номер участка: ', font=('Comic Sans MS', 20)).grid(column=0, row=2)
    Label(new_root, text='Номер ПО: ', font=('Comic Sans MS', 20)).grid(column=0, row=3)

    txt_doctor_name = Entry(new_root, width=30, font=('Comic Sans MS', 20))
    txt_doctor_name.grid(column=1, row=0)

    txt_manager = Entry(new_root, width=30, font=('Comic Sans MS', 20))
    txt_manager.grid(column=1, row=1)

    txt_district = Entry(new_root, width=5, font=('Comic Sans MS', 20))
    txt_district.grid(column=1, row=2)

    txt_ped_div = Entry(new_root, width=5, font=('Comic Sans MS', 20))
    txt_ped_div.grid(column=1, row=3)

    Button(new_root, text='Сохранить', command=save, font=('Comic Sans MS', 20)).grid()

    new_root.mainloop()


def get_doc_names():
    with sq.connect('data_base.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT doctor_name, open_mark FROM врачи")
        data = cur.fetchall()
    all_doctors = list()
    for doctor_name, mark in data:
        if mark == '1':
            all_doctors.insert(0, doctor_name)
        else:
            all_doctors.append(doctor_name)

    return all_doctors


def certificate():
    with sq.connect('data_base.db') as conn:
        cur = conn.cursor()

        cur.execute(f"SELECT doctor_name, district, ped_div, manager FROM врачи "
                    f"WHERE doctor_name LIKE '{combo_doc.get()}'")
        data = cur.fetchone()
        print('data', data)
        doctor_name, district, ped_div, manager = data

    data = {
        "patient": {
            'name': patient.get('name'),
            'birth_date': patient.get('birth_date'),
            'gender': patient.get('gender'),
            'amb_cart': patient.get('amb_cart'),
            'patient_district': patient.get('patient_district'),
            'address': patient.get('address')},
        "doctor": {
            'doctor_name': doctor_name,
            'manager': manager,
            'ped_div': ped_div,
            'doctor_district': district}
    }
    cert.append_info(data)

    pass


def analyzes():
    pass


def blanks():
    pass


def save_doctor(new_doctor_name):
    with sq.connect('data_base.db') as conn:
        cur = conn.cursor()

        cur.execute(f"SELECT doctor_name, district, ped_div, manager FROM врачи")
        data = cur.fetchall()

        for doctor_name, district, ped_div, manager in data:
            cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{doctor_name}'")
            if doctor_name == new_doctor_name:
                cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)",
                            [doctor_name, district, ped_div, manager, True])
            else:
                cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)",
                            [doctor_name, district, ped_div, manager, False])
    write_lbl_doc()


def search_loop():
    patient_found_data = list()

    def select_patient(event):
        print(event.widget)
        num = ''
        for i in str(event.widget):
            if i.isdigit():
                num += i
        rowid, district, amb_cart, name_1, name_2, name_3, gender, birth_date, address, phone = \
            patient_found_data[int(num) - 3]
        patient['name'] = f"{name_1} {name_2} {name_3}"
        patient['birth_date'] = birth_date
        patient['gender'] = gender
        patient['amb_cart'] = amb_cart
        patient['patient_district'] = district
        patient['address'] = address

        patient_info['text'] = f"ФИО: {patient.get('name')}\t" \
                               f"Дата рождения: {patient.get('birth_date')}\n" \
                               f"Адрес: {patient.get('address')}\n" \
                               f"№ амб: {patient.get('amb_cart')}\t" \
                               f"Участок: {patient.get('patient_district')}"
        search_root.destroy()

    def button_search_in_db(*args, **kwargs):
        delete_txt_patient_data()
        txt_patient_data.insert(index=0,
                                string=text_patient_data.get())
        search_root.destroy()
        search_loop()

    def search_in_db():
        delete_txt_patient_data()
        txt_patient_data.insert(0, text_patient_data.get())

        patient_data = text_patient_data.get()
        name = list()
        for i in patient_data.split():
            name.append(i.capitalize())
        sql_str = ''
        if patient_data.isdigit():
            sql_str += f"amb_cart LIKE '{patient_data}%'"
        else:
            for i in patient_data:
                if i.isdigit():
                    sql_str += "Домашний_адрес LIKE '"
                    for q in name:
                        sql_str += f"%{q}"
                    sql_str += "%'"
                    break
            else:

                if len(name) == 1:
                    sql_str += f"Фамилия LIKE '{name[0]}%'"
                elif len(name) == 2:
                    sql_str += f"Фамилия LIKE '{name[0]}%' AND Имя LIKE '{name[1]}%'"
                elif len(name) == 3:
                    sql_str += f"Фамилия LIKE '{name[0]}%' AND Имя LIKE '{name[1]}%' AND Отчество LIKE '{name[2]}%'"

                elif len(patient_data.split()) > 3:
                    messagebox.showinfo('Ошибка', 'Неверный формат ввода!\n'
                                                  'Ожидалось максимум 3 блока данных\n'
                                                  f'Получено: <b>{len(patient_data.split())}</b> блоков\n'
                                                  f'Измените запрос')

        if not sql_str:
            messagebox.showinfo('Ошибка', 'По введенной информации не удалось сформулировать sql запрос')

        else:
            print("sql_str", sql_str)

            with sq.connect(r"patient_data_base.db") as conn:
                cur = conn.cursor()
                cur.execute(f"SELECT rowid, "
                            f"district, "
                            f"amb_cart, "
                            f"Фамилия, "
                            f"Имя, "
                            f"Отчество, "
                            f"Пол, "
                            f"Дата_рождения, "
                            f"Домашний_адрес, "
                            f"Домашний_телефон "
                            f"FROM patient_data WHERE {sql_str}")
                found_data = cur.fetchall()
            print(found_data)

            if len(found_data) < 1:
                counter_patient['text'] = "По введенной информации не удалось найти пациента"
                # messagebox.showinfo('Ошибка', 'По введенной информации не удалось найти пациента')

            else:
                counter_patient['text'] = f"Найдено пациентов: {len(found_data)}"

                if len(found_data) > 15:
                    count_patient = 15
                else:
                    count_patient = len(found_data)

                patient_found_data.clear()
                for num in range(count_patient):
                    rowid, district, amb_cart, name_1, name_2, name_3, gender, birth_date, address, phone = \
                        found_data[num]

                    text = f"Участок: {district};\t" \
                           f"№ амб: {amb_cart}\t" \
                           f"ФИО: {name_1.capitalize()} {name_2.capitalize()} {name_3.capitalize()}\t" \
                           f"{birth_date}\t" \
                           f"Адрес: {address}"
                    lbl_0 = Label(search_root, text=text, font=('Comic Sans MS', 15), border=1, compound='left',
                                  bg='#bbfffe', relief='ridge')
                    lbl_0.grid(columnspan=3, sticky='w', padx=2, pady=2, ipadx=2, ipady=2)
                    lbl_0.bind('<Double-Button-1>', select_patient)
                    patient_found_data.append(found_data[num])

    search_root = Tk()
    search_root.title('Поиск пациента')
    search_root.config(bg='white')
    counter_patient = Label(search_root, text='', font=('Comic Sans MS', 16), bg='white')
    counter_patient.grid(column=0, row=2, columnspan=3)

    Label(search_root, text='Окно данных пациента', font=('Comic Sans MS', 20), bg='white').grid(column=0, row=0,
                                                                                                 columnspan=3)
    text_patient_data = Entry(search_root, width=30, font=('Comic Sans MS', 20))
    text_patient_data.grid(column=0, row=1, columnspan=2)
    text_patient_data.insert(0, txt_patient_data.get())
    text_patient_data.focus()
    text_patient_data.bind('<Return>', button_search_in_db)

    Button(search_root, text='Найти', command=button_search_in_db, font=('Comic Sans MS', 20)).grid(column=2, row=1)
    search_in_db()
    search_root.mainloop()


def paste_txt_patient_data(*args, **kwargs):
    text_patient_data = pyperclip.paste()
    txt_patient_data.delete(0, last=END)
    txt_patient_data.insert(index=0,
                            string=text_patient_data)


def search_patient(*args, **kwargs):
    patient_data = txt_patient_data.get()

    if ('Фамилия, имя, отчество пациента:' in patient_data or
            '№ амб. карты' in patient_data or
            '№ амбулаторной карты' in patient_data):
        patient_data = decoding_name.decoding_name(patient_data)
        for key in patient:
            if patient_data.get(key):
                patient[key] = patient_data.get(key)
        patient_info['text'] = f"ФИО: {patient_data.get('name')}\t" \
                               f"Дата рождения: {patient_data.get('birth_date')}\n" \
                               f"Адрес: {patient_data.get('address')}\n" \
                               f"№ амб: {patient_data.get('amb_cart')}\t" \
                               f"Участок: {patient_data.get('patient_district')}"
        print("patient_data", patient_data)
        return True
    else:
        search_loop()


def write_lbl_doc():
    info_doc = get_doctor_data()
    lbl_doc['text'] = f'Учетная запись:\n' \
                      f'Доктор: {info_doc[0]}\n' \
                      f'Зав: {info_doc[3]};    ' \
                      f'Участок: {info_doc[1]};    ' \
                      f'ПО: {info_doc[2]}'


def selected(_):
    save_doctor(new_doctor_name=combo_doc.get())


def delete_txt_patient_data():
    txt_patient_data.delete(0, last=END)


data_base()
root = Tk()
root.title('Временная замена БОТа')
root.config(bg='white')

frame = Frame(borderwidth=1, relief="solid", padx=8, pady=10)

lbl_doc = Label(frame, text=f'', font=('Comic Sans MS', 16))
write_lbl_doc()
lbl_doc.grid(column=0, row=0, columnspan=3)

combo_doc = Combobox(frame, font=('Comic Sans MS', 20), state="readonly")
combo_doc['values'] = get_doc_names()
combo_doc.current(0)
combo_doc.grid(column=0, row=1, columnspan=3)
combo_doc.bind("<<ComboboxSelected>>", selected)

Button(frame, text='Добавить доктора', command=add_new_doctor, font=('Comic Sans MS', 20)).grid(column=0, row=2)
Button(frame, text='Редактировать', command=redact_doctor, font=('Comic Sans MS', 20)).grid(column=2, row=2)

frame.grid(padx=5, pady=5)


frame = Frame(borderwidth=1, relief="solid", padx=8, pady=10)

Label(frame, text='Окно данных пациента', font=('Comic Sans MS', 20)).grid(column=0, row=2, columnspan=3)

txt_patient_data = Entry(frame, width=15, font=('Comic Sans MS', 20))
txt_patient_data.grid(column=0, row=3)
txt_patient_data.bind('<Control-v>', paste_txt_patient_data)
txt_patient_data.bind('<Return>', search_patient)

patient_info = Label(frame, text='', font=('Comic Sans MS', 10))
patient_info.grid(column=0, row=4)

Button(frame, text='Поиск', command=search_patient, font=('Comic Sans MS', 20)).grid(column=1, row=3)
Button(frame, text='Обновить БД', command=updating_patient_data_base, font=('Comic Sans MS', 20)).grid(column=1, row=4)
Button(frame, text='Удалить', command=delete_txt_patient_data, font=('Comic Sans MS', 20)).grid(column=2, row=3)
Button(frame, text='Вставить', command=paste_txt_patient_data, font=('Comic Sans MS', 20)).grid(column=2, row=4)

frame.grid(padx=5, pady=5)

frame = Frame(borderwidth=1, relief="solid", padx=8, pady=10)

Label(frame, text='Что хотите сделать?', font=('Comic Sans MS', 20), anchor='center').grid(column=0, row=0,
                                                                                           columnspan=3, sticky='ew')

Button(frame, text='Справка', command=certificate, font=('Comic Sans MS', 20)).grid(column=0, row=1)
Button(frame, text='Анализы', command=analyzes, font=('Comic Sans MS', 20)).grid(column=1, row=1)
Button(frame, text='Вкладыши', command=blanks, font=('Comic Sans MS', 20)).grid(column=2, row=1)

frame.grid(padx=5, pady=5)

root.mainloop()

# >>> import subprocess
# >>> subprocess.Popen('C:\\Windows\\System32\\calc.exe')
