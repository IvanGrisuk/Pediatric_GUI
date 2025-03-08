import threading

import shutil
import time

import pyperclip
import os
import random

from tkinter import *
import sqlite3 as sq
from tkinter.ttk import Combobox
from tkinter import messagebox, Label, Frame
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk

from datetime import datetime, timedelta
import calendar

from docx.enum.section import WD_ORIENT
from docx.shared import Cm
from docx.shared import Pt
from docx import Document
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from mkb_10 import mkb_10
from post_1201 import post_1201

import subprocess, platform

from database import data_base
from examination import paste_examination


from variables import all_patient, patient, app_info, user, program_version


def main_root():

    def start_action(func=None):
        def check_thread(thread_):
            if thread_.is_alive():
                animation.set(animation.get()[-1] + animation.get()[:-1])
                root.after(50, lambda: check_thread(thread))
            else:
                animation.set("")

        def run_action():
            if func:
                func()
            else:
                time.sleep(5)

        animation.set("▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░")
        thread = threading.Thread(target=run_action)
        thread.start()
        check_thread(thread)

    def edit_local_db():

        load_info_text.set("Синхронизация осмотров...")

        app_info['load_info_text'] = load_info_text
        answer = data_base(command='examination__edit_examination_loc')

        if 'Exception' in answer:
            load_info_text.set(f"{answer}")
            time.sleep(1)

        load_info_text.set("")
        crynet_systems_label.bind('<Double-Button-1>', start_edit_local_db)

    def start_edit_local_db(event=None):
        crynet_systems_label.unbind('<Double-Button-1>')
        start_action(edit_local_db)

    def paste_log_in_root():
        def select_doctor_name():
            load_info_text.set(f"Выбран доктор: {selected_doctor_name.get()}")

            if app_info['all_doctor_info'][selected_doctor_name.get()].get('password'):
                frame_pass.pack_configure(fill='both', expand=True, padx=2, pady=2)
                pass_txt.focus()
            else:
                open_main_root()
                frame_pass.pack_forget()

        def open_main_root():
            if app_info.get('frame_doc'):
                app_info['frame_doc'].destroy()
                app_info['frame_doc'] = None
            frame_pass.pack_forget()

            if not user.get('error_connection'):
                doctor_name = selected_doctor_name.get()
                user['doctor_name'] = app_info['all_doctor_info'][doctor_name].get('doctor_name')
                user['password'] = app_info['all_doctor_info'][doctor_name].get('password')
                user['doctor_district'] = app_info['all_doctor_info'][doctor_name].get('district')
                user['ped_div'] = app_info['all_doctor_info'][doctor_name].get('ped_div')
                user['manager'] = app_info['all_doctor_info'][doctor_name].get('manager')
                user['text_size'] = int(app_info['all_doctor_info'][doctor_name].get('text_size'))
                user['add_info'] = app_info['all_doctor_info'][doctor_name].get('add_info')

                user['my_saved_diagnosis'] = app_info['all_doctor_info'][doctor_name].get('my_saved_diagnosis')
                user['my_LN'] = app_info['all_doctor_info'][doctor_name].get('my_LN')
                user['my_sport_section'] = app_info['all_doctor_info'][doctor_name].get('my_sport_section')

                data_base('activate_app')
            paste_frame_main()

        def connect_to_srv_data_base():
            load_info_text.set(f"Попытка подключения к базе данных...")
            if not os.path.exists(path=f".{os.sep}data_base"):
                os.mkdir(path=f".{os.sep}data_base")
            data_base('create_db')
            last_edit_srv = data_base('last_edit_patient_db_srv')
            if last_edit_srv:
                load_info_text.set("Соединение с сервером установлено")
            else:
                load_info_text.set("Ошибка подключения к базе данных!")
            if not last_edit_srv:
                user['error_connection'] = True
            else:
                last_edit_loc = data_base('last_edit_patient_db_loc')
                if last_edit_loc != last_edit_srv:
                    load_info_text.set("Обнаружена новая версия базы данных пациентов\n"
                                       "Начинаю обновление...")
                    shutil.copy2(f"{user['app_data'].get('path_srv_data_base')}patient_data_base.db",
                                 f".{os.sep}data_base{os.sep}patient_data_base.db")
                    load_info_text.set(f"База данных пациентов обновлена")
                else:
                    load_info_text.set(f"У вас актуальная версия базы данных")
            if not all_patient:
                load_info_text.set(f"Создание базы данных пациентов")
                data_base('select_all_patient')
                load_info_text.set(f"Загрузка завершена")

            if not user.get('error_connection'):
                if not app_info.get('all_doctor_info'):
                    data_base('get_all_doctor_info')

                if app_info.get('all_doctor_info'):
                    frame_doc = Frame(log_in_root, borderwidth=1, relief="solid", padx=8, pady=10)
                    app_info['frame_doc'] = frame_doc
                    load_info_text.set("Выберите учетную запись")

                    users_sorted_pd = dict()
                    for doctor_name in sorted(app_info.get('all_doctor_info')):
                        ped_div = app_info['all_doctor_info'][doctor_name].get('ped_div')
                        if ped_div not in users_sorted_pd:
                            users_sorted_pd[ped_div] = list()
                        users_sorted_pd[ped_div].append(doctor_name)

                    row, col = 0, 0
                    for ped_div in sorted(users_sorted_pd):
                        row += 1
                        if ped_div.isdigit():
                            text = f'{ped_div}-е ПО'
                        else:
                            text = f'{ped_div}'
                        Label(frame_doc, text=text,
                              font=('Comic Sans MS', user.get('text_size')),
                              bg='white').grid(row=row, column=0, sticky='ew', columnspan=4)
                        row += 1
                        col = 0
                        for doctor_name in users_sorted_pd.get(ped_div):

                            btn = Radiobutton(master=frame_doc, text=doctor_name,
                                              font=('Comic Sans MS', user.get('text_size')),
                                              command=select_doctor_name,
                                              value=doctor_name, variable=selected_doctor_name,
                                              indicatoron=False, selectcolor='#77f1ff')
                            btn.grid(row=row, column=col, sticky='ew')
                            col += 1
                            if col == 4:
                                col = 0
                                row += 1
                    frame_doc.columnconfigure(index='all', minsize=40, weight=1)
                    frame_doc.rowconfigure(index='all', minsize=20)
                    frame_doc.pack(fill='both', expand=True, padx=2, pady=2)


                else:
                    user['error_connection'] = True

            if user.get('error_connection'):
                if user['app_data'].get('last_reg_password'):
                    if (datetime.now() - datetime.strptime(user['app_data'].get('last_reg_password'),
                                                           "%d.%m.%Y")).days > 60:
                        load_info_text.set('Срок активации истек! '
                                           '\nВведите пароль для продления 60-дневной подписки')

                        frame_pass.pack_configure(fill='both', expand=True, padx=2, pady=2)
                        app_info['check_pass_app'] = True

                    else:
                        open_main_root()
                else:
                    open_main_root()

        def is_valid__password(password):
            if app_info.get('check_pass_app'):
                if password == "profkiller_10539008":
                    text_is_correct_password.set('Пароль принят')

                    open_main_root()
                    data_base('activate_app')
                else:
                    text_is_correct_password.set('Пароль не верен!')
            else:
                if password == app_info['all_doctor_info'][selected_doctor_name.get()].get('password'):
                    text_is_correct_password.set('Пароль принят')
                    open_main_root()
                else:
                    text_is_correct_password.set('Пароль не верен!')

            return True

        if app_info.get('frame_main'):
            app_info['frame_main'].destroy()
            app_info['frame_main'] = None

        selected_doctor_name = StringVar()
        txt_password_variable = StringVar()
        text_is_correct_password = StringVar()


        log_in_root = Frame(master=root, bg="#36566d")
        app_info['log_in_root'] = log_in_root
        user['error_connection'] = False

        frame_lbl = Frame(log_in_root, padx=3, pady=3, bg="#36566d")

        frame_animation = Frame(frame_lbl, padx=3, pady=3, bg="#36566d")

        Label(frame_animation, textvariable=animation,
              anchor='ne', bg="#36566d", fg='white', compound='bottom'
              ).pack(fill='both', expand=True, padx=2, pady=2)

        Label(frame_animation, textvariable=load_info_text,
              anchor='ne', bg="#36566d", fg='white', compound='bottom'
              ).pack(fill='both', expand=True, padx=2, pady=2)

        frame_animation.pack(fill='both', expand=True, padx=2, pady=2, side='left')


        crynet_systems_label = Label(frame_lbl, image=image_crynet_systems,
                                     anchor='ne', bg="#36566d", fg='white', compound='bottom')
        crynet_systems_label.pack(fill='both', expand=True, padx=2, pady=2, side='left')
        frame_lbl.pack(fill='both', expand=True, padx=2, pady=2)
        crynet_systems_label.bind('<Double-Button-1>', start_edit_local_db)


        load_info_text.set('Запуск программы...')

        frame_pass = Frame(log_in_root, borderwidth=1, relief="solid", padx=8, pady=10)
        check_pass = (log_in_root.register(is_valid__password), "%P")

        Label(frame_pass, text='Введите пароль: ',
              font=('Comic Sans MS', 12), bg='white'
              ).pack(fill='both', expand=True, padx=2, pady=2, side='left')
        pass_txt = Entry(frame_pass, width=40,
              font=('Comic Sans MS', user.get('text_size')),
              justify="center",
              validate="all",
              textvariable=txt_password_variable,
              validatecommand=check_pass,
              show="*"
              )
        pass_txt.pack(fill='both', expand=True, padx=2, pady=2, side='left')
        # Entry(frame_pass, width=40,
        #       font=('Comic Sans MS', user.get('text_size')),
        #       justify="center",
        #       validate="all",
        #       textvariable=txt_password_variable,
        #       validatecommand=check_pass,
        #       show="*"
        #       ).pack(fill='both', expand=True, padx=2, pady=2, side='left')

        Label(frame_pass, textvariable=text_is_correct_password,
              font=('Comic Sans MS', 12), bg='white', foreground="red"
              ).pack(fill='both', expand=True, padx=2, pady=2, side='left')


        log_in_root.columnconfigure(index='all', minsize=40, weight=1)
        log_in_root.rowconfigure(index='all', minsize=20)
        log_in_root.pack(fill='both', expand=True, padx=2, pady=2)


        start_action(connect_to_srv_data_base)

    def paste_frame_main():

        def add_new_patient():
            def save():
                def check_input():
                    error_flag = False
                    for marker in local_data:
                        if marker in ("№ участка", "Фамилия", "Имя", "Отчество", "Пол", "Дата рождения",
                                      "Адрес") and not local_data.get(marker).get():
                            messagebox.showerror('Ошибка', f"Ошибка!\nНе указан пункт\n'{marker}'")
                            break
                        elif marker in ("№ амбулаторной карты", "№ участка") and local_data.get(
                                marker).get() and not local_data.get(marker).get().isdigit():
                            messagebox.showerror('Ошибка', f"Ошибка!\nУкажите пункт\n'{marker}'\nчислом")
                            break
                        elif marker == "Дата рождения":
                            try:
                                if (datetime.now() - datetime.strptime(local_data.get(marker).get(),
                                                                       "%d.%m.%Y")).days < 0:
                                    messagebox.showerror('Ошибка', f"Дата рождения не может быть больше текущей даты!")
                                    break
                            except Exception:
                                messagebox.showerror('Ошибка', f"Дата рождения должна быть в формате 'ДД.ММ.ГГГГ'")
                                break
                    else:
                        return True
                    return False

                if check_input():
                    insert_data = list()
                    for marker in ("№ участка", "№ амбулаторной карты",
                                   "Фамилия", "Имя", "Отчество", "Пол",
                                   "Дата рождения", "Адрес",
                                   "None", "None", "None"):
                        if local_data.get(marker) and local_data.get(marker).get().strip():
                            insert_data.append(local_data.get(marker).get().strip())
                        else:
                            insert_data.append("")
                    if data_base(command='save_new_patient', insert_data=insert_data):
                        messagebox.showinfo('Инфо', "Данные успешно сохранены!")
                        patient['name'] = f"{local_data.get('Фамилия').get().strip()} " \
                                          f"{local_data.get('Имя').get().strip()} " \
                                          f"{local_data.get('Отчество').get().strip()}".strip()
                        patient['birth_date'] = f"{local_data.get('Дата рождения').get().strip()}"
                        patient['gender'] = f"{local_data.get('Пол').get().strip()}"
                        patient['amb_cart'] = f"{local_data.get('№ амбулаторной карты').get().strip()}"
                        patient['patient_district'] = f"{local_data.get('№ участка').get().strip()}"
                        patient['address'] = f"{local_data.get('Адрес').get().strip()}"
                        patient['age'] = get_age_d_m_y(patient.get('birth_date'))

                        patient_info.set(f"ФИО: {patient.get('name')}\t"
                                         f"Дата рождения: {patient.get('birth_date')}    {patient['age'].get('age_txt')}\n"
                                         f"Адрес: {patient.get('address')}\n"
                                         f"№ амб: {patient.get('amb_cart')}\t"
                                         f"Участок: {patient.get('patient_district')}")

                        new_root.destroy()
                    else:
                        messagebox.showerror('Ошибка', f"Ошибка!\nОшибка сохранения двнных")

            new_root = Toplevel()
            new_root.title('Добавление нового пациента')
            root.bind("<Control-KeyPress>", keypress)
            local_data = {
                "№ амбулаторной карты": StringVar(),
                "№ участка": StringVar(),
                "Фамилия": StringVar(),
                "Имя": StringVar(),
                "Отчество": StringVar(),
                "Пол": StringVar(),
                "Дата рождения": StringVar(),
                "Адрес": StringVar(),
            }

            row = 0
            for marker in local_data:

                Label(new_root, text=marker,
                      font=('Comic Sans MS', user.get('text_size')),
                      bg="#36566d", fg='white').grid(column=0, row=row, sticky='nwse', padx=2, pady=2)
                if marker == 'Пол':
                    combo_sex = Combobox(new_root, font=('Comic Sans MS', user.get('text_size')), state="readonly",
                                         textvariable=local_data.get(marker))
                    combo_sex['values'] = ["", "мужской", "женский"]
                    combo_sex.current(0)
                    combo_sex.grid(column=1, row=row, sticky='nwse')
                else:

                    Entry(new_root, width=30, font=('Comic Sans MS', user.get('text_size')),
                          textvariable=local_data.get(marker)
                          ).grid(column=1, row=row, sticky='nwse', ipadx=2, ipady=2)
                row += 1

            Button(new_root, text='Сохранить', command=save, font=('Comic Sans MS', user.get('text_size'))).grid(
                columnspan=2, sticky='ew')

            new_root.mainloop()

        def download_ped_div():
            def start_search():
                pediatric_division = user.get('ped_div')
                download_ped_div_variable.set(f"Выгрузка справок {pediatric_division} ПО...\n"
                                              f"Обращение к базе данных...")
                download_ped_div_root.update()

                info = data_base(f"get_certificate_for_district__certificate_ped_div__{pediatric_division}")
                if not info:
                    download_ped_div_variable.set(
                        f"{download_ped_div_variable.get()} \nОшибка подключения к базе данных")
                    download_ped_div_root.update()
                else:
                    download_ped_div_variable.set(f"{download_ped_div_variable.get()} ответ получен!\n"
                                                  f"Создаю документ...")
                    download_ped_div_root.update()

                    if pediatric_division == '1':
                        document = Document()
                        table = document.add_table(rows=(len(info) + 1), cols=10)
                        table.style = 'Table Grid'
                        # widths = (Cm(1.0), Cm(1.0), Cm(2.0), Cm(3.0), Cm(2.5), Cm(1.8), Cm(3.0))
                        # for row in table.rows:
                        #     for idx, width in enumerate(widths):
                        #         row.cells[idx].width = width
                        data_table = ('№ п/п',
                                      'Дата',
                                      'ФИО лица, обратившегося за выдачей справки и (или) другого документа',
                                      'Адрес',
                                      'Документ, удостоверяющий личность',
                                      'Наименование справки и (или) другого запрашиваемого документа',
                                      'Срок исполнения',
                                      'Размер платы, взимаемый',
                                      'Дата выдачи справки и (или) другого запрашиваемого документа',
                                      'ФИО врача')
                        hdr_cells = table.rows[0].cells
                        for i in range(10):
                            hdr_cells[i].text = data_table[i]

                            rc = hdr_cells[i].paragraphs[0].runs[0]
                            rc.font.name = 'Times New Roman'
                            rc.font.size = Pt(10)
                            rc.font.bold = True

                        len_doc = len(info)
                        per_num_data = dict()
                        for per_num in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1):
                            per_num_data[round(len_doc * per_num)] = per_num
                        download_ped_div_variable.set(f"{download_ped_div_variable.get()} \n"
                                                      f"Таблица создана. Заполняю ячейки данными...")
                        download_ped_div_root.update()

                        for i in range(1, len(info) + 1):
                            if per_num_data.get(i):
                                download_ped_div_variable.set(f"{download_ped_div_variable.get()} \n"
                                                              f"Завершено на {round(per_num_data.get(i) * 100)}%")
                                download_ped_div_root.update()

                            hdr_cells = table.rows[i].cells
                            ped_div, district, num, date, name, birth_date, address, type_cert, doctor_name = info[
                                i - 1]
                            local_info = (
                                num, date, name, address, 'паспорт', type_cert, '1 день', 'бесплатно', date,
                                doctor_name)
                            for q in range(10):
                                hdr_cells[q].text = local_info[q]
                                rc = hdr_cells[q].paragraphs[0].runs[0]
                                rc.font.name = 'Times New Roman'
                                rc.font.size = Pt(9)

                    else:
                        document = Document()
                        table = document.add_table(rows=(len(info) + 1), cols=11)
                        table.style = 'Table Grid'
                        # widths = (Cm(1.0), Cm(1.0), Cm(2.0), Cm(3.0), Cm(2.5), Cm(1.8), Cm(3.0))
                        # for row in table.rows:
                        #     for idx, width in enumerate(widths):
                        #         row.cells[idx].width = width
                        data_table = ('№ п/п',
                                      'ФИО, обратившегося за выдачей справки и (или) другого документа',
                                      "Дата рождения",
                                      'Домашний адрес',
                                      'Дата подачи заявления',
                                      'Наименование справки и (или) другого запрашиваемого документа',
                                      'Срок исполнения',
                                      'Документ, удостоверяющий личность',
                                      'Размер платы, взимаемой за подачу справки и (или) другого документа',
                                      'Дата выдачи справки и (или) другого запрашиваемого документа',
                                      'ФИО врача (роспись заявителя)')
                        hdr_cells = table.rows[0].cells
                        for i in range(11):
                            hdr_cells[i].text = data_table[i]

                            rc = hdr_cells[i].paragraphs[0].runs[0]
                            rc.font.name = 'Times New Roman'
                            rc.font.size = Pt(10)
                            rc.font.bold = True
                        len_doc = len(info)
                        per_num_data = dict()
                        for per_num in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1):
                            per_num_data[round(len_doc * per_num)] = per_num
                        download_ped_div_variable.set(f"{download_ped_div_variable.get()} \n"
                                                      f"Таблица создана. Заполняю ячейки данными...")
                        download_ped_div_root.update()

                        for i in range(1, len(info) + 1):
                            if per_num_data.get(i):
                                download_ped_div_variable.set(f"{download_ped_div_variable.get()} \n"
                                                              f"Завершено на {round(per_num_data.get(i) * 100)}%")
                                download_ped_div_root.update()

                            hdr_cells = table.rows[i].cells
                            ped_div, district, num, date, name, birth_date, address, type_cert, doctor_name = info[
                                i - 1]
                            type_cert = f"пункт {type_cert}"
                            local_info = (
                                num,
                                name,
                                birth_date,
                                address,
                                date,
                                type_cert,
                                '1 день',
                                'паспорт',
                                'бесплатно',
                                date,
                                doctor_name)
                            for q in range(11):
                                hdr_cells[q].text = local_info[q]
                                rc = hdr_cells[q].paragraphs[0].runs[0]
                                rc.font.name = 'Times New Roman'
                                rc.font.size = Pt(9)

                    sections = document.sections
                    for section in sections:
                        section.orientation = WD_ORIENT.LANDSCAPE
                        section.top_margin = Cm(1.5)
                        section.bottom_margin = Cm(1.5)
                        section.left_margin = Cm(1.5)
                        section.right_margin = Cm(1.5)
                        section.page_height = Cm(21)
                        section.page_width = Cm(29.7)

                    file_name = f'.{os.sep}generated{os.sep}БРЕД_{pediatric_division}_го_ПО.docx'
                    file_name = save_document(doc=document, doc_name=file_name)
                    os.system(f"start {file_name}")
                    download_ped_div_root.destroy()

            download_ped_div_root = Toplevel()
            download_ped_div_root.title('Инфо')
            download_ped_div_variable = StringVar()
            Label(download_ped_div_root, textvariable=download_ped_div_variable,
                  font=('Comic Sans MS', user.get('text_size')),
                  bg="#36566d", fg='white').pack(fill='x', expand=True, ipady=3, ipadx=3)
            download_ped_div_variable.set("Выгрузка справок в среднем занимает около 5 минут\n"
                                          "На время формирования документа не закрывайте приложение\n"
                                          "Для начала выгрузки нажмите кнопку 'Начать поиск'")
            btn_start = Button(download_ped_div_root, text='Начать поиск', command=start_search,
                               font=('Comic Sans MS', user.get('text_size')))
            btn_start.pack(fill='x', expand=True, ipady=3, ipadx=3)

            download_ped_div_root.mainloop()

        def download_camp():
            def start_search():
                district = user.get('doctor_district')
                download_camp_variable.set(f"Выгрузка справок детского лагеря {district} участка...\n"
                                           f"Обращение к базе данных...")
                download_camp_root.update()
                info = data_base(f"get_certificate_for_district__certificate_camp__{district}")

                if not info:
                    download_camp_variable.set(f"{download_camp_variable.get()} \nОшибка подключения к базе данных")
                    download_camp_root.update()

                else:
                    download_camp_variable.set(f"{download_camp_variable.get()} ответ получен!\n"
                                               f"Создаю документ...")
                    download_camp_root.update()

                    document = Document()
                    table = document.add_table(rows=(len(info) + 1), cols=7)
                    table.style = 'Table Grid'
                    widths = (Cm(1.0), Cm(1.0), Cm(2.0), Cm(3.0), Cm(2.5), Cm(1.8), Cm(3.0))
                    for row in table.rows:
                        for idx, width in enumerate(widths):
                            row.cells[idx].width = width
                    data_table = ('Участок', '№ п/п', 'Дата выписки', 'ФИО', 'Дата рождения', 'Пол', 'Адрес')
                    hdr_cells = table.rows[0].cells
                    for i in range(7):
                        hdr_cells[i].text = data_table[i]

                        rc = hdr_cells[i].paragraphs[0].runs[0]
                        rc.font.name = 'Times New Roman'
                        rc.font.size = Pt(8)
                        rc.font.bold = True
                    len_doc = len(info)
                    per_num_data = dict()
                    for per_num in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1):
                        per_num_data[round(len_doc * per_num)] = per_num
                    download_camp_variable.set(f"{download_camp_variable.get()} \n"
                                               f"Таблица создана. Заполняю ячейки данными...")
                    download_camp_root.update()

                    for i in range(1, len(info) + 1):
                        if per_num_data.get(i):
                            download_camp_variable.set(f"{download_camp_variable.get()} \n"
                                                       f"Завершено на {round(per_num_data.get(i) * 100)}%")
                            download_camp_root.update()

                        hdr_cells = table.rows[i].cells
                        for q in range(7):
                            if info[i - 1][q]:
                                hdr_cells[q].text = info[i - 1][q]

                                rc = hdr_cells[q].paragraphs[0].runs[0]
                                rc.font.name = 'Times New Roman'
                                rc.font.size = Pt(8)

                    sections = document.sections
                    for section in sections:
                        section.top_margin = Cm(1.5)
                        section.bottom_margin = Cm(1.5)
                        section.left_margin = Cm(1.5)
                        section.right_margin = Cm(1.5)
                        section.page_height = Cm(21)
                        section.page_width = Cm(14.8)

                    file_name = f'.{os.sep}generated{os.sep}концлагерь_{district}_участка.docx'
                    file_name = save_document(doc=document, doc_name=file_name)
                    os.system(f"start {file_name}")
                    download_camp_root.destroy()

            download_camp_root = Toplevel()
            download_camp_root.title('Инфо')
            download_camp_variable = StringVar()
            Label(download_camp_root, textvariable=download_camp_variable,
                  font=('Comic Sans MS', user.get('text_size')),
                  bg="#36566d", fg='white').pack(fill='x', expand=True, ipady=3, ipadx=3)
            download_camp_variable.set("Выгрузка лагеря в среднем занимает около 5 минут\n"
                                       "На время формирования документа не закрывайте приложение\n"
                                       "Для начала выгрузки нажмите кнопку 'Начать поиск'")
            btn_start = Button(download_camp_root, text='Начать поиск', command=start_search,
                               font=('Comic Sans MS', user.get('text_size')))
            btn_start.pack(fill='x', expand=True, ipady=3, ipadx=3)

            download_camp_root.mainloop()

        def search_loop():
            search_data = {
                'found_patient_root': None,
                'found_patient_data': dict()
            }

            def select_patient():
                rowid, district, amb_cart, name_1, name_2, name_3, gender, birth_date, address, phone, vac_1, vac_2 = \
                    search_data['found_patient_data'].get(int(selected_patient.get()))
                patient['name'] = f"{name_1} {name_2} {name_3}"
                patient['birth_date'] = birth_date
                patient['gender'] = gender
                patient['amb_cart'] = amb_cart
                patient['patient_district'] = district
                patient['address'] = address
                patient['vac_1'] = vac_1
                patient['vac_2'] = vac_2
                patient['age'] = get_age_d_m_y(patient.get('birth_date'))
                patient['phone'] = phone

                patient_info.set(f"ФИО: {patient.get('name')}    "
                                 f"Дата рождения: {patient.get('birth_date')}\n"
                                 f"Адрес: {patient.get('address')}\n"
                                 f"№ амб: {patient.get('amb_cart')}    "
                                 f"Участок: {patient.get('patient_district')}    "
                                 f"Возраст: {patient['age'].get('age_txt')}\n"
                                 f"Телефон: {patient.get('phone')}")
                search_root.destroy()
                delete_txt_patient_data()

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
                    counter_patient.set('Ошибка!\n'
                                        'По введенной информации не удалось сформулировать sql запрос')


                else:
                    with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
                        cur = conn.cursor()
                        cur.execute(f"SELECT rowid, * FROM patient_data WHERE {sql_str}")
                        found_data = cur.fetchall()

                    if len(found_data) < 1:
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
                                 gender, birth_date, address, phone,
                                 vac_1, vac_2) = info

                                for mark_1, mark_2 in (
                                        (district, 'col_1'),
                                        (amb_cart, 'col_2'),
                                        (f"{name_1} {name_2} {name_3}", 'col_3')):
                                    if len(mark_1) > split_len.get(mark_2):
                                        split_len[mark_2] = len(mark_1)

                            for info in found_data:
                                (rowid, district, amb_cart,
                                 name_1, name_2, name_3,
                                 gender, birth_date, address, phone,
                                 vac_1, vac_2) = info
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

            search_root = Toplevel()
            search_root.title('Поиск пациента')
            search_root.config(bg='white')
            search_root.geometry('+0+0')

            frame_title = Frame(master=search_root, bg="#36566d")
            Label(frame_title, text='Окно данных пациента',
                  font=('Comic Sans MS', user.get('text_size')), bg="#36566d", fg='white').grid(column=0, row=0,
                                                                                                columnspan=2)

            text_patient_data = Entry(frame_title, width=100,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      textvariable=txt_patient_data_variable)
            text_patient_data.grid(column=0, row=1)
            text_patient_data.focus()
            text_patient_data.bind('<Return>', button_search_in_db)

            Button(frame_title, text='Найти', command=button_search_in_db,
                   font=('Comic Sans MS', user.get('text_size'))).grid(column=1, row=1, sticky='ew')

            counter_patient = StringVar()
            selected_patient = StringVar()
            Label(frame_title,
                  textvariable=counter_patient,
                  font=('Comic Sans MS', user.get('text_size')),
                  bg="#36566d", fg='white'
                  ).grid(column=0, row=2, columnspan=2)
            frame_title.pack(fill='both', expand=True, padx=2, pady=2)
            counter_patient.set('Поиск пациентов...')
            button_search_in_db()
            search_root.mainloop()

        def redact_doctor():
            change_doctor(command='redact')

        def add_new_doctor():
            change_doctor(command='new')

        def change_doctor(command):
            def save():
                doctor_name = txt_doctor_name.get().strip()
                manager = txt_manager.get().strip()
                district = txt_district.get().strip()
                ped_div = txt_ped_div.get().strip()
                text_size = txt_text_size.get().strip()
                password = txt_password.get()

                db_type = 'loc'
                if combo_db.get() == 'Сервер':
                    db_type = 'srv'

                if not doctor_name:
                    messagebox.showinfo('Ошибка', 'Ошибка имени доктора!')
                elif not manager:
                    messagebox.showinfo('Ошибка', 'Ошибка имени заведующего!')
                elif not district:
                    messagebox.showinfo('Ошибка', 'Ошибка участка!\nУкажите участок числом')
                elif not ped_div or ped_div not in ('1', '2', '3', 'ПРОЧЕЕ'):
                    messagebox.showinfo('Ошибка', "Ошибка ПО\nУкажите номер ПО числом или 'ПРОЧЕЕ'")
                elif not text_size or not text_size.isdigit() or (4 > int(text_size) or int(text_size) > 30):
                    messagebox.showinfo('Ошибка', 'Ошибка размера текста\n'
                                                  'Укажите размер текста числом от 5 до 30')

                else:
                    user['app_data']['path_examination_data_base'] = txt_path_db_loc.get().strip()
                    user['app_data']['path_srv_data_base'] = txt_path_db_srv.get().strip()
                    data_base(command='edit_path_db')

                    if user.get('error_connection'):
                        new_doc = [doctor_name, district, ped_div, manager, True, text_size]
                        answer, mess = data_base(command='save_new_doc',
                                                 insert_data=new_doc)
                        if answer:
                            messagebox.showinfo('Успешно', 'Данные успешно сохранены!')
                            combo_doc['values'] = data_base(command='get_doc_names_local')

                            combo_doc.current(0)

                            user['text_size'] = int(txt_text_size.get())

                            new_root.destroy()
                            data_base(command='append_local_doctor_data',
                                      insert_data=combo_doc.get())
                            write_lbl_doc()
                            update_font_main()
                            root.update()

                        else:
                            messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{mess}')

                    else:
                        for string in user.get('add_info').split('__<end!>__'):
                            if 'examination_db_place:____' in string:
                                user['add_info'] = user.get('add_info', '').replace(string,
                                                                                    f"examination_db_place:____{db_type}")
                                break
                        else:
                            user['add_info'] = f"examination_db_place:____{db_type}__<end!>__\n"
                        new_doc = [doctor_name, password, district, ped_div, manager, True, text_size,
                                   user.get('add_info')]
                        answer, mess = data_base(command='save_new_doc',
                                                 insert_data=new_doc)
                        if answer:

                            messagebox.showinfo('Успешно', 'Данные успешно сохранены!')
                            user['text_size'] = int(text_size)
                            user['password'] = password
                            user['doctor_district'] = district
                            user['ped_div'] = ped_div
                            user['manager'] = manager

                            if app_info['all_doctor_info'].get(doctor_name):
                                app_info['all_doctor_info'][doctor_name]['password'] = password
                                app_info['all_doctor_info'][doctor_name]['district'] = district
                                app_info['all_doctor_info'][doctor_name]['ped_div'] = ped_div
                                app_info['all_doctor_info'][doctor_name]['manager'] = manager
                                app_info['all_doctor_info'][doctor_name]['text_size'] = int(text_size)

                            new_root.destroy()
                            write_lbl_doc()
                            update_font_main()
                            root.update()

                        else:
                            messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{mess}')

            new_root = Toplevel()

            txt_doctor_name = Entry(new_root, width=30, font=('Comic Sans MS', user.get('text_size')))
            txt_password = Entry(new_root, width=30, font=('Comic Sans MS', user.get('text_size')))

            if command == 'new':
                new_root.title('Новая учетная запись')
                Label(new_root, text='ФИО доктора: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0,
                                                                                                          row=0)
                txt_doctor_name.grid(column=1, row=0, sticky='ew')

            else:
                new_root.title('Редактирование учетной записи')
                Label(new_root, text=f"Пользователь: {user.get('doctor_name')}",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg="#36566d", fg='white').grid(column=0, row=0, columnspan=2,
                                                     sticky='nwse', ipadx=5, ipady=5)

            Label(new_root, text='ФИО заведующего: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0,
                                                                                                          row=1)
            Label(new_root, text='Номер участка: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=2)
            Label(new_root, text='Номер ПО (1, 2, 3, ПРОЧЕЕ): ',
                  font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=3)
            Label(new_root, text='Размер текста: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=4)

            txt_manager = Entry(new_root, width=30, font=('Comic Sans MS', user.get('text_size')))
            txt_manager.grid(column=1, row=1, sticky='ew')

            txt_district = Entry(new_root, width=5, font=('Comic Sans MS', user.get('text_size')))
            txt_district.grid(column=1, row=2, sticky='ew')

            txt_ped_div = Entry(new_root, width=5, font=('Comic Sans MS', user.get('text_size')))
            txt_ped_div.grid(column=1, row=3, sticky='ew')

            txt_text_size = Entry(new_root, width=5, font=('Comic Sans MS', user.get('text_size')))
            txt_text_size.grid(column=1, row=4, sticky='ew')

            combo_db = Combobox(new_root, font=('Comic Sans MS', user.get('text_size')), state="readonly")
            combo_db['values'] = ["Сервер", "Мой компьютер"]
            combo_db.current(0)

            if not user.get('error_connection'):
                Label(new_root, text='Пароль: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=5)
                txt_password.grid(column=1, row=5, sticky='ew')

                Label(new_root, text='Место хранения осмотров: ', font=('Comic Sans MS', user.get('text_size'))).grid(
                    column=0, row=8)
                if 'examination_db_place:____loc' in user.get('add_info'):
                    combo_db.current(1)
                combo_db.grid(column=1, row=8)

            txt_path_db_loc = Entry(new_root, width=30, font=('Comic Sans MS', user.get('text_size')))

            txt_path_db_srv = Entry(new_root, width=30, font=('Comic Sans MS', user.get('text_size')))

            Label(new_root, text='path loc DB: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=6)
            txt_path_db_loc.grid(column=1, row=6, sticky='ew')
            if user['app_data'].get('path_examination_data_base'):
                txt_path_db_loc.insert(0, user['app_data'].get('path_examination_data_base', ''))

            Label(new_root, text='path srv DB: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=7)
            txt_path_db_srv.grid(column=1, row=7, sticky='ew')
            if user['app_data'].get('path_srv_data_base'):
                txt_path_db_srv.insert(0, user['app_data'].get('path_srv_data_base', ''))

            Button(new_root, text='Сохранить', command=save, font=('Comic Sans MS', user.get('text_size'))).grid(
                columnspan=2, sticky='ew')

            if command == 'redact':
                txt_doctor_name.insert(0, user.get('doctor_name'))
                txt_manager.insert(0, user.get('manager'))
                txt_district.insert(0, user.get('doctor_district'))
                txt_ped_div.insert(0, user.get('ped_div'))
                txt_text_size.insert(0, user.get('text_size'))
                txt_password.insert(0, user.get('password', ''))

            new_root.mainloop()

        def paste_txt_patient_data(event):
            if event.keycode == 86 or event.keycode == 150994966:
                txt_patient_data.delete(0, 'end')
                event.widget.event_generate('<<Paste>>')
                search_patient()

            elif event.keycode == 67 or event.keycode == 134217731:
                event.widget.event_generate('<<Copy>>')
            elif event.keycode == 88 or event.keycode == 117440536:
                event.widget.event_generate('<<Cut>>')

        def save_doctor(new_doctor_name):
            print('new_doctor_name', new_doctor_name)
            data_base(command='append_local_doctor_data', insert_data=new_doctor_name)
            data_base(command='save_doctor_local',
                      insert_data=new_doctor_name)
            write_lbl_doc()
            update_font_main()

        def search_patient(*args, **kwargs):
            patient_data = txt_patient_data_variable.get()

            if ('Фамилия, имя, отчество пациента:' in patient_data or
                    '№ амб. карты' in patient_data or
                    '№ амбулаторной карты' in patient_data):
                patient_data = decoding_name(patient_data)
                if patient_data:
                    for key in patient:
                        if patient_data.get(key):
                            patient[key] = patient_data.get(key)
                    patient['age'] = get_age_d_m_y(patient.get('birth_date'))
                    patient_info.set(f"ФИО: {patient_data.get('name')}    "
                                     f"Дата рождения: {patient_data.get('birth_date')}\n"
                                     f"Адрес: {patient_data.get('address')}\n"
                                     f"№ амб: {patient_data.get('amb_cart')}    "
                                     f"Участок: {patient_data.get('patient_district')}    "
                                     f"Возраст: {patient['age'].get('age_txt')}")
                    delete_txt_patient_data()
                    return True
                else:
                    delete_txt_patient_data()
            else:
                search_loop()

        def write_lbl_doc():

            lbl_doc_text.set(f"Учетная запись:\n"
                             f"Доктор: {user.get('doctor_name')}\n"
                             f"Зав: {user.get('manager')};    "
                             f"Участок: {user.get('doctor_district')};    "
                             f"ПО: {user.get('ped_div')}")

            if 'константинова' in user.get('doctor_name'):
                lbl_doc_text.set(f"Учетная запись:\n"
                                 f"Доктор: Яночка Константиновна\n"
                                 f"Зав: {user.get('manager')};    "
                                 f"Участок: {user.get('doctor_district')};    "
                                 f"ПО: {user.get('ped_div')}")

            root.update()

        def selected(event=None):
            save_doctor(new_doctor_name=combo_doc.get())

        def delete_txt_patient_data():
            txt_patient_data_variable.set('')

        def update_font_main():
            if app_info.get('frame_main'):
                app_info['frame_main'].destroy()
                app_info['frame_main'] = None

            paste_frame_main()

        def delete_doc_local():
            result = messagebox.askyesno(title='Удаление учетной записи',
                                         message=f"Удалить пользователя?\n"
                                                 f"{combo_doc.get()}")
            if result:
                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                    cur = conn.cursor()
                    cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{combo_doc.get()}'")

                messagebox.showinfo("Результат", "Учетная запись удалена")
                data_base('create_db')
                combo_doc['values'] = data_base(command='get_doc_names_local')
                combo_doc.current(0)
                selected()

        def change_account():
            paste_log_in_root()

        def pack_main_frame():
            # height = root.winfo_screenheight() - 200
            # width = root.winfo_screenwidth() - 100
            # print(height, width)
            # root.config(height=height, width=width)

            frame_main = Frame(master=root, bg="#36566d")
            frame_main.pack(fill='both', expand=True, padx=2, pady=2)

            app_info['frame_main'] = frame_main

            frame_title = Frame(master=frame_main, bg="#36566d", padx=2, pady=2)

            frame = Frame(master=frame_title, bg="#36566d", padx=2, pady=2)
            Label(frame, textvariable=lbl_doc_text,
                  anchor='w', bg="#36566d", fg='white', compound='bottom',
                  font=('Comic Sans MS', user.get('text_size'))
                  ).pack(fill='both', expand=True, padx=2, pady=2)

            Label(frame, textvariable=patient_info,
                  anchor='w', bg="#36566d", fg='white', compound='bottom',
                  font=('Comic Sans MS', user.get('text_size'))
                  ).pack(fill='both', expand=True, padx=2, pady=2)
            frame.pack(fill='both', expand=True, padx=2, pady=2, side='left')
            lbl_doc_text.set(f"Учетная запись: "
                             f"Доктор: {user.get('doctor_name').upper()}    "
                             f"Зав: {user.get('manager')};    "
                             f"Участок: {user.get('doctor_district')};    "
                             f"ПО: {user.get('ped_div')}")

            crynet_systems_label = Label(frame_title, image=image_crynet_systems,
                                         anchor='ne', bg="#36566d", fg='white', compound='bottom')
            crynet_systems_label.pack(fill='both', expand=True, padx=2, pady=2, side='left')
            crynet_systems_label.bind('<Double-Button-1>', start_edit_local_db)


            frame_title.pack(fill='both', padx=2, pady=2, anchor='n')

            frame_patient = Frame(master=frame_main, bg="#36566d", padx=2, pady=2)
            frame_patient_but = Frame(master=frame_patient, padx=2, pady=2)

            Label(frame_patient_but, text="Поиск пациента",
                  anchor='w',  font=('Comic Sans MS', user.get('text_size'))

                  ).pack(fill='both', expand=True, padx=2, pady=2, side='left')

            txt_patient_data = Entry(frame_patient_but, width=100,
                                     textvariable=txt_patient_data_variable,
                                     font=('Comic Sans MS', user.get('text_size')))
            txt_patient_data.pack(fill='both', expand=True, padx=2, pady=2, side='left')
            txt_patient_data.bind('<Control-KeyPress>', paste_txt_patient_data)
            txt_patient_data.bind('<Return>', search_patient)

            Button(frame_patient_but, text='X', command=delete_txt_patient_data,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2, side='left')

            Button(frame_patient_but, text='Добавить нового пациента', command=add_new_patient,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2, side='left')

            frame_patient_but.pack(fill='both', padx=2, pady=2, anchor='n')

            Label(frame_patient, textvariable=patient_info,
                  font=('Comic Sans MS', user.get('text_size'))
                  ).pack(fill='both', expand=True, padx=2, pady=2)
            frame_patient.pack(fill='both', padx=2, pady=2, anchor='n')

            frame_buttons = Frame(master=frame_main, bg="#36566d", padx=2, pady=2)

            Button(frame_buttons, text='Справка', command=fast_certificate,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            Button(frame_buttons, text='Анализы', command=analyzes_cmd,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            Button(frame_buttons, text='Вкладыши', command=blanks_cmd,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            Button(frame_buttons, text='Прививки', command=vaccination_cmd,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            Button(frame_buttons, text='Направления', command=direction_cmd,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            Button(frame_buttons, text='Мой прием', command=open_last_examination,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            Button(frame_buttons, text='Осмотры', command=examination_cmd,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            Button(frame_buttons, text='Осмотры до года', command=examination_cmd_child,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            if 'local_admin' in str(user.get('add_info', "")):
                Button(frame_buttons, text='Журнал справок', command=download_ped_div,
                       font=('Comic Sans MS', user.get('text_size'))
                       ).pack(fill='both', expand=True, padx=2, pady=2)

            Button(frame_buttons, text='Сменить пользователя', command=change_account,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)
            Button(frame_buttons, text='Редактировать данные', command=redact_doctor,
                   font=('Comic Sans MS', user.get('text_size'))
                   ).pack(fill='both', expand=True, padx=2, pady=2)

            frame_buttons.pack(fill='both', expand=True, padx=2, pady=2)



            # Label(frame_animation, textvariable=animation,
            #       anchor='ne', bg="#36566d", fg='white', compound='bottom'
            #       ).pack(fill='both', expand=True, padx=2, pady=2)
            #
            #
            # frame_lbl = Frame(log_in_root, padx=3, pady=3, bg="#36566d")
            #
            # frame_animation = Frame(frame_lbl, padx=3, pady=3, bg="#36566d")
            #
            # Label(frame_animation, textvariable=animation,
            #       anchor='ne', bg="#36566d", fg='white', compound='bottom'
            #       ).pack(fill='both', expand=True, padx=2, pady=2)
            #
            # Label(frame_animation, textvariable=load_info_text,
            #       anchor='ne', bg="#36566d", fg='white', compound='bottom'
            #       ).pack(fill='both', expand=True, padx=2, pady=2)
            #
            # frame_animation.pack(fill='both', expand=True, padx=2, pady=2, side='left')

            # frame_main_loc = Frame(master=frame_main, borderwidth=1, relief="solid", padx=8, pady=10)
            #
            #
            # combo_doc = Combobox(frame_main_loc, state="readonly")
            #
            # if user.get('error_connection'):
            #     combo_doc['values'] = data_base(command='get_doc_names_local')
            #     combo_doc.current(0)
            #     combo_doc.grid(column=0, row=1, columnspan=3)
            #     combo_doc.bind("<<ComboboxSelected>>", selected)
            #     data_base(command='append_local_doctor_data',
            #               insert_data=combo_doc.get())
            #
            #     Label(frame_main_loc, textvariable=lbl_doc_text,
            #           font=('Comic Sans MS', user.get('text_size'))
            #           ).grid(column=0, row=0, columnspan=3)
            #
            #     Button(frame_main_loc, text='Добавить доктора', command=add_new_doctor,
            #            font=('Comic Sans MS', user.get('text_size'))
            #            ).grid(column=0, row=2, sticky='ew')
            #     Button(frame_main_loc, text='Редактировать данные', command=redact_doctor,
            #            font=('Comic Sans MS', user.get('text_size'))
            #            ).grid(column=1, row=2, sticky='ew')
            #     Button(frame_main_loc, text='Удалить пользователя', command=delete_doc_local,
            #            font=('Comic Sans MS', user.get('text_size'))
            #            ).grid(column=2, row=2, sticky='ew')
            #
            #     write_lbl_doc()
            #
            # else:
            #     start_action(edit_local_db)
            #
            #     Label(frame_main_loc, textvariable=lbl_doc_text,
            #           font=('Comic Sans MS', user.get('text_size'))
            #           ).grid(column=0, row=0, columnspan=2)
            #
            #     lbl_doc_text.set(f"Учетная запись:\n"
            #                      f"Доктор: {user.get('doctor_name')}\n"
            #                      f"Зав: {user.get('manager')};    "
            #                      f"Участок: {user.get('doctor_district')};    "
            #                      f"ПО: {user.get('ped_div')}")
            #
            #
            # frame_main_loc.columnconfigure(index='all', minsize=40, weight=1)
            # frame_main_loc.rowconfigure(index='all', minsize=20)
            # frame_main_loc.pack(fill='both', expand=True, padx=2, pady=2)
            #
            # frame_main_loc = Frame(master=frame_main, borderwidth=1, relief="solid", padx=8, pady=10)
            #
            # Label(frame_main_loc, text='Окно данных пациента',
            #       font=('Comic Sans MS', user.get('text_size'))
            #       ).grid(column=0, row=2, columnspan=3, sticky='ew')
            #
            # txt_patient_data = Entry(frame_main_loc, width=40, textvariable=txt_patient_data_variable,
            #                          font=('Comic Sans MS', user.get('text_size')))
            # txt_patient_data.grid(column=0, row=3)
            # txt_patient_data.bind('<Control-KeyPress>', paste_txt_patient_data)
            # txt_patient_data.bind('<Return>', search_patient)
            # patient_info = StringVar()
            # Label(frame_main_loc, textvariable=patient_info,
            #       font=('Comic Sans MS', user.get('text_size'))
            #       ).grid(column=0, row=4, sticky='ew', columnspan=2, ipadx=3)
            #
            # Button(frame_main_loc, text='Добавить\nнового\nпациента', command=add_new_patient,
            #        font=('Comic Sans MS', user.get('text_size'))
            #        ).grid(column=2, row=3, rowspan=2, sticky='nswe')
            #
            # Button(frame_main_loc, text='X', command=delete_txt_patient_data,
            #        font=('Comic Sans MS', user.get('text_size'))
            #        ).grid(column=1, row=3, sticky='ew')
            #
            # frame_main_loc.columnconfigure(index='all', minsize=40, weight=1)
            # frame_main_loc.rowconfigure(index='all', minsize=20)
            # frame_main_loc.pack(fill='both', expand=True, padx=2, pady=2)
            #
            # frame_main_loc = Frame(master=frame_main, borderwidth=1, relief="solid", padx=8, pady=10)
            #
            # Label(frame_main_loc, text='Что хотите сделать?', anchor='center',
            #       font=('Comic Sans MS', user.get('text_size'))
            #       ).grid(column=0, row=0, columnspan=2, sticky='ew')
            #
            #
            # frame_main_loc.columnconfigure(index='all', minsize=40, weight=1)
            # frame_main_loc.rowconfigure(index='all', minsize=20)
            # frame_main_loc.pack(fill='both', expand=True, padx=2, pady=2)




        if app_info.get('log_in_root'):
            app_info['log_in_root'].destroy()
            app_info['log_in_root'] = None

        lbl_doc_text = StringVar()
        txt_patient_data_variable = StringVar()
        patient_info = StringVar()
        pack_main_frame()
        сalendar_img = ImageTk.PhotoImage(Image.open('сalendar_img.png').resize((user.get('text_size')*2, user.get('text_size')*2)))
        user['сalendar_img'] = сalendar_img

    root = Tk()
    root.title(f"Генератор справок v_{program_version}")
    root.config(bg="#36566d")
    root.geometry('+0+0')

    animation = StringVar()
    animation.set("")
    load_info_text = StringVar()
    image_crynet_systems = ImageTk.PhotoImage(Image.open('Crynet_systems.png').resize((200, 50)))

    paste_log_in_root()
    root.mainloop()

if __name__ == "__main__":
    main_root()
