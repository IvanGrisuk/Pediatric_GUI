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

from . import decoding_name


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
        for doc_name, mark in doctor_data:
            if mark:
                flag = True
        if not flag:
            cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE 'Иванов И.И.'")
            cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?)", ['Иванов И.И.', 1, 1, 'Петров П.П.', True])


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
            messagebox.showinfo('Ошибка', 'Ошибка ПО!\nУкажите номер ПО числом')
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
                new_root.destroy()

    new_root = Tk()
    new_root.title('Изменение данных')

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
        cur.execute(f"SELECT doctor_name, mark FROM врачи")
        data = cur.fetchall()
        all_doctors = list()
        for doctor_name, mark in data:
            if mark:
                all_doctors.insert(0, doctor_name)
            else:
                all_doctors.append(doctor_name)
        return all_doctors


def certificate():
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


def main_loop():
    def is_valid(patient_data):
        patient_data = decoding_name.decoding_name(patient_data)

    def selected(_):
        save_doctor(new_doctor_name=combo_doc.get())

    def delete_txt_patient_data():
        txt_patient_data.delete(0, last='END')

    data_base()
    root = Tk()
    root.title('Временная замена БОТа')
    root.config(bg='white')

    lbl = Label(root, text='Учетная запись:', font=('Comic Sans MS', 16), width=20, height=1)
    lbl.grid()
    combo_doc = Combobox(root, font=('Comic Sans MS', 20), state="readonly")
    combo_doc['values'] = get_doc_names()
    combo_doc.current(0)
    combo_doc.grid()
    combo_doc.bind("<<ComboboxSelected>>", selected)

    btn = Button(root, text='Добавить доктора', command=add_new_doctor, font=('Comic Sans MS', 20))
    btn.grid()

    Label(root, text='Окно данных пациента', font=('Comic Sans MS', 20)).grid()
    txt_patient_data = Entry(root, width=30, font=('Comic Sans MS', 20))
    txt_patient_data.grid()

    check = (root.register(is_valid), "%P")

    errmsg = StringVar()

    phone_entry = ttk.Entry(validate="key", validatecommand=check)
    phone_entry.pack(padx=5, pady=5, anchor=NW)

    error_label = ttk.Label(foreground="red", textvariable=errmsg, wraplength=250)
    error_label.pack(padx=5, pady=5, anchor=NW)

    Button(root, text='Изменить', command=delete_txt_patient_data, font=('Comic Sans MS', 20)).grid()

    Label(root, text='Что хотите сделать?', font=('Comic Sans MS', 20)).grid()

    Button(root, text='Справка', command=certificate, font=('Comic Sans MS', 20)).grid()
    Button(root, text='Анализы', command=analyzes, font=('Comic Sans MS', 20)).grid()
    Button(root, text='Вкладыши', command=blanks, font=('Comic Sans MS', 20)).grid()

    root.mainloop()


if __name__ == "__main__":
    main_loop()

# >>> import subprocess
# >>> subprocess.Popen('C:\\Windows\\System32\\calc.exe')