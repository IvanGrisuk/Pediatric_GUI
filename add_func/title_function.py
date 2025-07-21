import os
from tkinter import *
import sqlite3 as sq
from tkinter import messagebox, Label, Frame
from tkinter.ttk import Combobox


from variables import patient, app_info, user
from util_func import paste_new_frame, get_age_d_m_y
from database import data_base


def redact_doctor():
    def save():

        user['app_data']['path_srv_data_base'] = path_db_srv.get().strip()
        user['text_size'] = int(text_size.get())

        data_base(command='edit_path_db')

        new_doc = [user.get('doctor_name'),
                   user.get('doctor_id'),
                   password.get(),
                   district.get(),
                   ped_div.get(),
                   manager.get(),
                   user.get('admin_status'),
                   specialities.get(),
                   user.get('add_info')]
        answer, mess = data_base(command='save_new_doc',
                                 insert_data=new_doc)
        if answer == 'loc':
            messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{mess}')
        elif answer == 'srv':
            messagebox.showinfo('Ошибка', f'Ошибка подключения к серверу:\n{mess}')
        else:
            messagebox.showinfo('Успешно', 'Данные успешно сохранены!')

            user['password'] = password.get()
            user['doctor_district'] = district.get()
            user['ped_div'] = ped_div.get()
            user['manager'] = manager.get()

            new_root.destroy()
            if app_info.get('frame_main'):
                app_info['frame_main'].destroy()
                app_info['frame_main'] = None
                frame_main_func = app_info.get('frame_main_func')
                frame_main_func()

    canvas_frame = app_info['scrolled_frame'].get('scrolled_frame')

    new_root = Frame(master=canvas_frame, bg="#36566d")

    Label(new_root, text=f"Редактирование учетной записи: {user.get('doctor_name')}",
          font=('Comic Sans MS', user.get('text_size')),
          bg="#36566d", fg='white').grid(column=0, row=0, columnspan=2,
                                         sticky='nsew', ipadx=5, ipady=5)

    doctor_name = user.get('doctor_name')
    manager = StringVar()
    district = StringVar()
    ped_div = StringVar()
    text_size = StringVar()
    password = StringVar()
    path_db_srv = StringVar()
    specialities = StringVar()

    manager.set(user.get('manager'))
    district.set(user.get('doctor_district'))
    ped_div.set(user.get('ped_div'))
    text_size.set(user.get('text_size'))
    password.set(user.get('password', ''))
    specialities.set(user.get('specialities'))
    path_db_srv.set(user['app_data'].get('path_srv_data_base', ''))

    Label(new_root, text='ФИО заведующего: ',
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=0, row=1, sticky='ew')
    Entry(new_root, width=30, textvariable=manager,
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=1, row=1, sticky='ew')

    Label(new_root, text='Номер участка: ',
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=0, row=2, sticky='ew')
    Entry(new_root, width=30, textvariable=district,
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=1, row=2, sticky='ew')

    Label(new_root, text='Номер ПО: ',
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=0, row=3, sticky='ew')
    Combobox(new_root,
             font=('Comic Sans MS', user.get('text_size')),
             state="readonly", textvariable=ped_div, values=['1', '2', '3', 'ПРОЧЕЕ']
             ).grid(column=1, row=3, sticky='ew')

    Label(new_root, text='Пароль: ',
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=0, row=4, sticky='ew')
    Entry(new_root, width=30, textvariable=password,
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=1, row=4, sticky='ew')

    Label(new_root, text='Специальность: ',
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=0, row=5, sticky='ew')
    Entry(new_root, width=30, textvariable=specialities,
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=1, row=5, sticky='ew')

    Label(new_root, text=f"Настройки приложения",
          font=('Comic Sans MS', user.get('text_size')),
          bg="#36566d", fg='white'
          ).grid(column=0, row=6, columnspan=2,
                 sticky='nsew', ipadx=5, ipady=5)

    Label(new_root, text='Размер текста: ',
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=0, row=7, sticky='ew')
    Combobox(new_root,
             font=('Comic Sans MS', user.get('text_size')),
             state="readonly", textvariable=text_size,
             values=['6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
             ).grid(column=1, row=7, sticky='ew')

    Label(new_root, text='path srv DB: ',
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=0, row=8, sticky='ew')
    Entry(new_root, width=30, textvariable=path_db_srv,
          font=('Comic Sans MS', user.get('text_size'))
          ).grid(column=1, row=8, sticky='ew')

    Button(new_root, text='Сохранить', command=save, font=('Comic Sans MS', user.get('text_size'))).grid(
        columnspan=2, sticky='ew')

    paste_new_frame(new_root)

def redact_patient():
    add_new_patient(redact_marker=True)

def add_new_patient(redact_marker=False):
    def save():
        new_patient = dict()
        for txt, var, mark in (('Участок', district, 'district'),
                               ('№ Амб карты', amb_cart, 'amb_cart'),
                               ('Фамилия *', Surname, 'Surname'),
                               ('Имя *', Name, 'Name'),
                               ('Отчество *', Patronymic, 'Patronymic'),
                               ('Пол *', gender, 'gender'),
                               ('Дата рождения *', birth_date, 'birth_date'),
                               ('Адрес *', address, 'address'),
                               ('Телефон', phone, 'phone'),
                               ('Паспорт', passport, 'passport')):
            if '*' in txt and var.get().strip() == '':
                messagebox.showinfo('Ошибка', f'Не указан параметр:\n{txt}')
                return


            new_patient[mark] = var.get().strip()
        try:
            get_age_d_m_y(birth_date.get())
        except ValueError:
            messagebox.showinfo('Ошибка', f'Некорректно указан параметр даты рождения!\n'
                                          f'Введите дату рождения в формате ДД.ММ.ГГГГ')


        new_patient['redact_marker'] = redact_marker
        answer, mess = data_base(command='redact_patient',
                                 insert_data=new_patient)
        if answer == 'loc':
            messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{mess}')
        elif answer == 'srv':
            messagebox.showinfo('Ошибка', f'Ошибка подключения к серверу:\n{mess}')
        else:
            for mark in new_patient:
                patient[mark] = new_patient.get(mark)
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
            messagebox.showinfo('Успешно', 'Данные успешно сохранены!')
            new_root.destroy()

    canvas_frame = app_info['scrolled_frame'].get('scrolled_frame')
    new_root = Frame(master=canvas_frame, bg="#36566d")

    if redact_marker:
        Label(new_root, text=f"Редактирование данных пациента",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').grid(column=0, row=0, columnspan=2,
                                             sticky='nsew', ipadx=5, ipady=5)
    else:
        Label(new_root, text=f"Добавление нового пациента",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').grid(column=0, row=0, columnspan=2,
                                             sticky='nsew', ipadx=5, ipady=5)


    district = StringVar()
    amb_cart = StringVar()
    Surname = StringVar()
    Name = StringVar()
    Patronymic = StringVar()
    gender = StringVar()
    birth_date = StringVar()
    address = StringVar()
    phone = StringVar()
    passport = StringVar()

    loc_data = (
        ('Участок', district, 'district'),
        ('№ Амб карты', amb_cart, 'amb_cart'),
        ('Фамилия *', Surname, 'Surname'),
        ('Имя *', Name, 'Name'),
        ('Отчество *', Patronymic, 'Patronymic'),
        ('Пол *', gender, 'gender'),
        ('Дата рождения *', birth_date, 'birth_date'),
        ('Адрес *', address, 'address'),
        ('Телефон', phone, 'phone'),
        ('Паспорт', passport, 'passport'),
    )
    row = 1
    for txt, var, key in loc_data:
        if redact_marker:
            var.set(patient.get(key))

        Label(new_root, text=txt,
              font=('Comic Sans MS', user.get('text_size'))
              ).grid(column=0, row=row, sticky='ew', pady=1)
        if txt == 'Пол *':
            combo = Combobox(new_root,
                             font=('Comic Sans MS', user.get('text_size')),
                             state="readonly", textvariable=var,
                             values=['мужской', 'женский', ]
                             )
            combo.grid(column=1, row=row, sticky='ew')

        else:
            Entry(new_root, width=30, textvariable=var,
                  font=('Comic Sans MS', user.get('text_size'))
                  ).grid(column=1, row=row, sticky='ew', pady=1)
        row += 1
    Button(new_root, text='Сохранить', command=save, font=('Comic Sans MS', user.get('text_size'))
           ).grid(columnspan=2, sticky='ew')

    paste_new_frame(new_root)

