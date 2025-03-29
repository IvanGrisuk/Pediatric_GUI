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
        if mess == 'loc':
            messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{mess}')
        elif mess == 'loc':
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
    def save():

        new_patient = {
            'district': district.get(),
            'amb_cart': amb_cart.get(),
            'Surname': Surname.get(),
            'Name': Name.get(),
            'Patronymic': Patronymic.get(),
            'gender': gender.get(),
            'birth_date': birth_date.get(),
            'phone': phone.get(),
            'passport': passport.get(),

        }

        answer, mess = data_base(command='redact_patient',
                                 insert_data=new_patient)
        if mess == 'loc':
            messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{mess}')
        elif mess == 'loc':
            messagebox.showinfo('Ошибка', f'Ошибка подключения к серверу:\n{mess}')
        else:
            messagebox.showinfo('Успешно', 'Данные успешно сохранены!')

            # user['password'] = password.get()
            # user['doctor_district'] = district.get()
            # user['ped_div'] = ped_div.get()
            # user['manager'] = manager.get()
            #
            # new_root.destroy()
            # if app_info.get('frame_main'):
            #     app_info['frame_main'].destroy()
            #     app_info['frame_main'] = None
            #     frame_main_func = app_info.get('frame_main_func')
            #     frame_main_func()

    canvas_frame = app_info['scrolled_frame'].get('scrolled_frame')
    new_root = Frame(master=canvas_frame, bg="#36566d")

    Label(new_root, text=f"Редактирование данных пациента",
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
        ('Фамилия', Surname, 'Surname'),
        ('Имя', Name, 'Name'),
        ('Отчество', Patronymic, 'Patronymic'),
        ('Пол', gender, 'gender'),
        ('Дата рождения', birth_date, 'birth_date'),
        ('Адрес', address, 'address'),
        ('Телефон', phone, 'phone'),
        ('Паспорт', passport, 'passport'),
    )
    row = 1
    for txt, var, key in loc_data:
        var.set(patient.get(key))

        Label(new_root, text=txt,
              font=('Comic Sans MS', user.get('text_size'))
              ).grid(column=0, row=row, sticky='ew', pady=1)
        if txt == 'Пол':
            combo = Combobox(new_root,
                             font=('Comic Sans MS', user.get('text_size')),
                             state="readonly", textvariable=var,
                             values=['мужской', 'женский',]
                     )
            combo.grid(column=1, row=row, sticky='ew')
            # if patient.get(key) == 'мужской':
            #     print('if')
            #     combo.current(0)
            # elif patient.get(key) == 'женский':
            #     combo.current(1)
            # else:
            #     combo.configure(background='red')

        else:
            Entry(new_root, width=30, textvariable=var,
                  font=('Comic Sans MS', user.get('text_size'))
                  ).grid(column=1, row=row, sticky='ew', pady=1)
        row += 1
    Button(new_root, text='Сохранить', command=save, font=('Comic Sans MS', user.get('text_size'))
           ).grid(columnspan=2, sticky='ew')

    paste_new_frame(new_root)
