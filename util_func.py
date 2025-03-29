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
from variables import all_patient, patient, app_info, user, program_version


def save_document(doc: Document, doc_name: str):
    if not os.path.exists(path=f".{os.sep}generated"):
        os.mkdir(path=f".{os.sep}generated")

    try:
        doc.save(doc_name)
    except Exception:
        counter = 1
        doc_name = doc_name.replace('.docx', '') + f"_{counter}.docx"
        while True:
            try:
                doc.save(doc_name)
            except Exception:
                counter += 1
                if counter == 100:
                    messagebox.showerror('Ошибка', "Невозможно создать документ")
                    return False
                doc_name = '_'.join(doc_name.replace('.docx', '').split('_')[:-1]) + f"_{counter}.docx"
            else:
                return doc_name

    else:
        return doc_name


def run_document(doc_name):
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', doc_name))
    elif platform.system() == 'Windows':  # Windows
        subprocess.call(('start', "", doc_name), shell=True)
    else:  # linux variants
        subprocess.call(('xdg-open', doc_name))


def get_age_d_m_y(birth_date, today=datetime.today()):
    patient_age = {
        "day": 0,
        "month": 0,
        "year": 0}

    birthday = ''
    for i in birth_date:
        if i.isdigit():
            birthday += i
        else:
            birthday += '.'
    birthday = birthday.split('.')
    date_form = "%d.%m.%Y"
    if len(birthday[-1]) == 2:
        date_form = "%d.%m.%y"

    birthday = datetime.strptime('.'.join(birthday), date_form)

    age = today.year - birthday.year
    if (today.month < birthday.month) or (today.month == birthday.month and today.day < birthday.day):
        age -= 1
    patient_age["year"] = age

    if today.month >= birthday.month:
        age = today.month - birthday.month
    else:
        age = 12 - birthday.month + today.month

    if today.day < birthday.day:
        age -= 1
    if age == 12:
        age = 0
    if age == -1:
        age = 11
    patient_age["month"] = age

    if today.day >= birthday.day:
        age = today.day - birthday.day
    else:
        new = datetime(today.year, today.month, 1) - timedelta(days=1)
        if birthday.day > new.day:
            birthday = new
        age = (today - datetime(new.year, new.month, birthday.day)).days

    patient_age["day"] = age

    age_txt = f""
    if patient_age.get('year') in (2, 3, 4):
        age_txt += f" {patient_age.get('year')} года"
    elif patient_age.get('year') == 1:
        age_txt += f" {patient_age.get('year')} год"
    elif patient_age.get('year') > 1:
        age_txt += f" {patient_age.get('year')} лет"

    age_txt += f" {patient_age.get('month')} мес. "
    if patient_age.get('year') == 0:
        age_txt += f"{patient_age.get('day')} д."
    patient_age['age_txt'] = age_txt
    return patient_age


def patient_anthro(marker_age_y='после года', marker_age=None, height=None, weight=None):
    if not marker_age:
        age = get_age_d_m_y(patient.get('birth_date'))
        if marker_age_y == 'после года':
            marker_age = age.get('year')
            if marker_age > 17:
                marker_age = 17
        else:
            marker_age = age.get('month')
            if age.get('year') > 0:
                marker_age = 12

    marker_gender = 'женский'
    if patient.get('gender').lower().startswith('м'):
        marker_gender = 'мужской'

    anthro_height = anthropometry[marker_age_y][marker_gender]['height'].get(marker_age)
    anthro_weight = anthropometry[marker_age_y][marker_gender]['weight'].get(marker_age)


    patient_physical_anthro = ""

    if height and weight:
        if anthro_height and anthro_weight:

            index_height, index_weight = 7, 7

            for a_height in anthro_height:
                if height < a_height:
                    index_height = anthro_height.index(a_height)
                    break

            for a_weight in anthro_weight:
                if weight <= a_weight:
                    index_weight = anthro_weight.index(a_weight)
                    break

            if index_height == 0:
                anthro = 'Низкое '
            elif index_height <= 2:
                anthro = 'Ниже среднего '
            elif index_height <= 4:
                anthro = 'Среднее '
            elif index_height <= 6:
                anthro = 'Выше среднего '
            elif index_height == 7:
                anthro = 'Высокое '

            if abs(index_weight - index_height) <= 1:
                anthro += 'гармоничное'
            else:
                if abs(index_weight - index_height) < 3:
                    anthro += 'дисгармоничное'
                else:
                    anthro += 'резко дисгармоничное'

                if not 2 < index_height < 5 and not 2 < index_weight < 5:
                    anthro += ' по росту и по весу'
                elif not 2 < index_height < 5:
                    anthro += ' по росту'
                elif not 2 < index_weight < 5:
                    anthro += ' по весу'

            patient_physical_anthro = anthro

    if weight:
        if anthro_weight:
            index_weight = 7
            for a_weight in anthro_weight:
                if weight <= a_weight:
                    index_weight = anthro_weight.index(a_weight)
                    break

            if index_weight == 0:
                anthro = f'Вес резко ниже нормы ({anthro_weight[0]} - {anthro_weight[-1]})'
            elif index_weight <= 2:
                anthro = 'Вес ниже среднего '
            elif index_weight <= 4:
                anthro = 'Вес в норме '
            elif index_weight <= 6:
                anthro = 'Вес выше среднего '
            elif index_weight == 7:
                anthro = f'Вес резко выше нормы ({anthro_weight[0]} - {anthro_weight[-1]})'

            patient_physical_anthro = f"{anthro} -- {patient_physical_anthro}"

    if height:
        if anthro_height:
            index_height = 7
            for a_height in anthro_height:
                if height < a_height:
                    index_height = anthro_height.index(a_height)
                    break

            if index_height == 0:
                anthro = f'Рост резко ниже нормы ({anthro_height[0]} - {anthro_height[-1]})'
            elif index_height <= 2:
                anthro = 'Рост ниже среднего '
            elif index_height <= 4:
                anthro = 'Рост в норме '
            elif index_height <= 6:
                anthro = 'Рост выше среднего '
            elif index_height == 7:
                anthro = f'Рост резко выше нормы ({anthro_height[0]} - {anthro_height[-1]})'

            patient_physical_anthro = f"{anthro} -- {patient_physical_anthro}"

    if not patient_physical_anthro:
        patient_physical_anthro = "Физическое развитие: нет данных"
    return patient_physical_anthro


def paste_main_calendar(txt_variable, main_title=''):

    if app_info['roots'].get('calendar_root'):
        app_info['roots']['calendar_root'].destroy()

    calendar_root = Toplevel()
    app_info['roots']['calendar_root'] = calendar_root
    calendar_root.title(f'Календарь {main_title}')
    calendar_root.config(bg='white')

    selected_day = StringVar()
    actual_data = dict()
    destroy_elements = dict()

    now = datetime.now()
    actual_data['year'] = now.year
    actual_data['month'] = now.month

    def prev_month():
        curr = datetime(actual_data.get('year'), actual_data.get('month'), 1)
        new = curr - timedelta(days=1)
        actual_data['year'] = int(new.year)
        actual_data['month'] = int(new.month)
        create_calendar()

    def next_month():
        curr = datetime(actual_data.get('year'), actual_data.get('month'), 1)
        new = curr + timedelta(days=31)
        actual_data['year'] = int(new.year)
        actual_data['month'] = int(new.month)
        create_calendar()

    def select_day():
        app_info['roots']['calendar_root'] = None
        day = selected_day.get()
        edit_day = list()
        for i in day.split('.'):
            if len(i) == 1:
                i = f"0{i}"
            edit_day.append(i)
        answer = '.'.join(edit_day)
        if txt_variable:
            txt_variable.set(answer)

        calendar_root.destroy()

    frame_month_year = Frame(calendar_root, relief="solid", padx=1, pady=1)

    frame_month_year.columnconfigure(index='all', minsize=40, weight=1)
    frame_month_year.rowconfigure(index='all', minsize=20)
    frame_month_year.pack(fill='both', expand=True)

    def create_calendar():
        if destroy_elements.get('loc_calendar_frame'):
            loc_calendar_frame = destroy_elements.get('loc_calendar_frame')
            loc_calendar_frame.destroy()

        loc_calendar_frame = Frame(calendar_root, relief="solid", padx=1, pady=1)
        destroy_elements['loc_calendar_frame'] = loc_calendar_frame

        for calendar_mark in ('prev', 'curr', 'next'):
            row, col = 0, 0

            frame_days = Frame(loc_calendar_frame, relief="ridge", borderwidth=0.5, padx=1, pady=1)
            if calendar_mark == 'prev':
                but_prev_month = Button(frame_days, text='<', command=prev_month,
                                        font=('Comic Sans MS', user.get('text_size')))
                but_prev_month.grid(row=row, column=0, sticky='ew', columnspan=7)


            elif calendar_mark == 'next':
                but_next_month = Button(frame_days, text='>', command=next_month,
                                        font=('Comic Sans MS', user.get('text_size')))
                but_next_month.grid(row=row, column=0, sticky='ew', columnspan=7)


            else:
                btn = Radiobutton(frame_days, text="Сегодня",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=datetime.now().strftime("%d.%m.%Y"),
                                  variable=selected_day, command=select_day,
                                  indicatoron=False, selectcolor='#77f1ff')
                btn.grid(row=row, column=0, sticky='ew', columnspan=7)

            if calendar_mark == 'prev':
                curr = datetime(actual_data.get('year'), actual_data.get('month'), 1)
                new = curr - timedelta(days=1)
                year = int(new.year)
                month = int(new.month)

            elif calendar_mark == 'next':
                curr = datetime(actual_data.get('year'), actual_data.get('month'), 1)
                new = curr + timedelta(days=31)
                year = int(new.year)
                month = int(new.month)

            else:
                year = actual_data.get('year')
                month = actual_data.get('month')

            month_name = {
                'January': 'Январь',
                'February': 'Февраль',
                'March': 'Март',
                'April': 'Апрель',
                'May': 'Май',
                'June': 'Июнь',
                'July': 'Июль',
                'August': 'Август',
                'September': 'Сентябрь',
                'October': 'Октябрь',
                'November': 'Ноябрь',
                'December': 'Декабрь'
            }

            row += 1
            lbl_month_year = Label(frame_days,
                                   text=f"{month_name.get(calendar.month_name[month])}",
                                   font=('Comic Sans MS', user.get('text_size')),
                                   bg='white')
            lbl_month_year.grid(column=0, row=row, sticky='ew', columnspan=7)

            if calendar_mark == 'curr':
                lbl_month_year['text'] = f"{month_name.get(calendar.month_name[month])} {str(year)}"

            # Second row - Week Days
            column = 0
            row += 1
            for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
                lbl = Label(frame_days, text=day,
                            relief="solid", borderwidth=0.5,
                            font=('Comic Sans MS', user.get('text_size')), bg='white')
                lbl.grid(column=column, row=row, sticky='ew', padx=2, pady=2)
                column += 1

            row += 1
            column = 0

            my_calendar = calendar.monthcalendar(year, month)
            for week in my_calendar:
                row += 1
                col = 0
                for day in week:
                    if day == 0:
                        col += 1
                    else:
                        # day = str(day)
                        # day = str(day)
                        # if len(day) == 1:
                        #     day = f"0{day}"
                        # if len(str(month)) == 1:
                        #     month = f"0{month}"
                        btn_value = ''

                        btn = Radiobutton(frame_days, text=day,
                                          font=('Comic Sans MS', user.get('text_size')),
                                          value=f"{day}.{month}.{year}", variable=selected_day,
                                          command=select_day,
                                          indicatoron=False, selectcolor='#77f1ff')
                        btn.grid(row=row, column=col, sticky='ew')
                        col += 1

                        if datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y").weekday() in (5, 6):
                            btn['bg'] = '#b4ffff'
                        if datetime.now().year == year and datetime.now().month == month and datetime.now().day == int(
                                day):
                            btn['bg'] = '#ff7b81'

            frame_days.columnconfigure(index='all', minsize=40, weight=1)
            frame_days.rowconfigure(index='all', minsize=20)
            frame_days.pack(fill='both', expand=True, side='left')

        loc_calendar_frame.columnconfigure(index='all', minsize=40, weight=1)
        loc_calendar_frame.rowconfigure(index='all', minsize=20)
        loc_calendar_frame.pack(fill='both', expand=True, side='left')

    create_calendar()


def paste_new_frame(frame):

    scrolled_frame = app_info['scrolled_frame'].get('scrolled_frame')
    canvas = app_info['scrolled_frame'].get('canvas')

    if app_info['scrolled_frame'].get('selected_frame'):
        app_info['scrolled_frame']['selected_frame'].pack_forget()

    app_info['scrolled_frame']['selected_frame'] = frame


    # certificate_main_root.update_idletasks()
    frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

    scrolled_frame.configure(height=frame.winfo_height())
    region = canvas.bbox(tk.ALL)
    canvas.configure(scrollregion=region)
    canvas.create_window((0, 0), window=scrolled_frame, anchor="nw",
                         width=canvas.winfo_width())
    canvas.yview_moveto(0)
    # certificate_main_root.update()


# text = """​№
# п/п
# ​Показатель
# ​Результат
# исследования
# ​1
# ​ Эритроциты (RBC), 10^12/л
#     мужчины,   женщины
# ​5,02 ​
# ​2
# ​ Гемоглобин (Hb), г/л
#     мужчины,   женщины
# ​139 ​
# ​3	​ Гематокрит (HCT)	​421 ​
# ​4	​ Средний объем эритроцита (MCV), фл	​84 ​
# ​5	​ Среднее содержание гемоглобина в эритроците (MCH), пг	​27,7 ​
# ​6	​ Средняя концентрация гемоглобина в эритроците (MCHC), г/дл 	​330 ​
# ​7	​ Анизоцитоз эритроцитов (RDW), %	​13,1 ​
# ​8	​ Ретикулоциты	​​
# ​9	​ Тромбоциты (PLT), 10^9/л	​323 ​
# ​10	​ Лейкоциты (WBC), 10^9/л	​8,2 ​
# ​11	​ Базофилы, %	​​
# ​12	​ Базофилы, 10^9/л	​​
# ​13	​ Эозинофилы, %	​​
# ​14	​ Эозинофилы, 10^9/л	​​
# ​15	​ Нейтрофилы:	​​
# ​	​  миелоциты, %	​​
# ​	​  юные, %	​​
# ​	​  палочкоядерные, %	​​
# ​	  сегментоядерные, %	​59,4 ​
# ​16
# ​ Пельгеровская аномалия нейтрофилов
# ​​
# ​17	​ Лимфоциты, %	​33,9 ​
# ​18	​ Лимфоциты, 10^9/л	​​
# ​19
# ​ Реактивные лимфоциты, %
# ​​
# ​20	​ Моноциты, %	​6,7 ​
# ​21	​ Моноциты, 10^9/л	​​
# ​22
# ​ Плазматическая клетка, %
# ​​
# ​23
# ​ Скорость оседания эритроцитов (СОЭ), мм/час
#     мужчины,   женщины
# ​8 ​
# ​24	 ​Свертываемость начало
#  Свертываемость конец	​ мин  сек
#
# ​ мин  сек​​​​"""
#
# text = text.replace(text.split('Эритроциты')[0], '')
# markers = (("​ Эритроциты (RBC), 10^12/л\n    мужчины,   женщины\n​", "Эритроциты (RBC), 10^12/л"),
#            ("​2	\n​ Гемоглобин (Hb), г/л\n    мужчины,   женщины\n​", "Гемоглобин (Hb), г/л"),
#            ("​3	​ Гематокрит (HCT)	​", "Гематокрит (HCT)"),
#            ("​4	​ Средний объем эритроцита (MCV), фл	​", "MCV, фл"),
#            ("​5	​ Среднее содержание гемоглобина в эритроците (MCH), пг	​", "MCH, пг"),
#            ("​6	​ Средняя концентрация гемоглобина в эритроците (MCHC), г/дл 	​", "MCHC, г/дл"),
#            ("​7	​ Анизоцитоз эритроцитов (RDW), %	​", "RDW, %"),
#            ("​8	​ Ретикулоциты	​", "Ретикулоциты"),
#            ("​9	​ Тромбоциты (PLT), 10^9/л	​", "Тромбоциты (PLT), 10^9/л"),
#            ("​10	​ Лейкоциты (WBC), 10^9/л	​", "Лейкоциты (WBC), 10^9/л"),
#            ("​11	​ Базофилы, %	​", "Базофилы, %"),
#            ("​12	​ Базофилы, 10^9/л	​​", "Базофилы, 10^9/л"),
#            ("​13	​ Эозинофилы, %	​​", "Эозинофилы, %"),
#            ("​14	​ Эозинофилы, 10^9/л	​​", "Эозинофилы, 10^9/л"),
#            ("​15	​ Нейтрофилы:	​​", ""),
#            ("​	​  миелоциты, %	​​", ""),
#            ("​	​  юные, %	​​", ""),
#            ("​	​  палочкоядерные, %	​​", ""),
#            ("​	  сегментоядерные, %	​59,4 ​", ""),
#            ("​16\n​ Пельгеровская аномалия нейтрофилов\n​​", ""),
#            ("​17	​ Лимфоциты, %	​", ""),
#            ("​18	​ Лимфоциты, 10^9/л	​​", ""),
#            ("​19\n​ Реактивные лимфоциты, %\n​​", ""),
#            ("​20	​ Моноциты, %	​6,7 ​", ""),
#            ("​21	​ Моноциты, 10^9/л	​​", ""),
#            ("​22\n​ Плазматическая клетка, %\n​​", ""),
#            ("​23	\n​ Скорость оседания эритроцитов (СОЭ), мм/час\n    мужчины,   женщины\n​", ""),
#            ("", ""),
#            ("", ""),
#            ("", ""),
#            ("", ""),
#
#            )
#
#
# """
#
# 33,9 ​
#
#
#
#
#
# 8 ​
# ​24	 ​Свертываемость начало
#  Свертываемость конец	​ мин  сек
#
# """
# for string in text.split('\n'):
#     if 'мужчины,   женщины' in string:
#         continue
#     print(string)
