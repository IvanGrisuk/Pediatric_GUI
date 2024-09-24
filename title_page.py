import os
import re
import sqlite3 as sq
from datetime import datetime

from docx.enum.section import WD_ORIENT
from docx.shared import Cm
from docx.shared import Pt
from docx import Document
from docxtpl import DocxTemplate
from docxcompose.composer import Composer



all_patients_data = dict()
all_patients_data_amb_cart = dict()


def create_card_file_db(path):
    def append_info():
        conflict_flag = False
        for flag_ in all_flag:
            all_flag[flag_] = False
        all_flag['№ g/g'] = True

        if all_data.get('Фамилия') and all_data.get('Фамилия') != 'Фамилия':
            all_data['Фамилия'], all_data['Имя'], all_data['Отчество'] = \
                (all_data.get('Фамилия').strip(),
                 all_data.get('Имя').strip(),
                 all_data.get('Отчество').strip())

            if all_data.get('Отчество'):
                if all_data['Отчество'][-1] == 'а':
                    all_data['Пол'] = 'женский'
                elif all_data['Отчество'][-1] == 'ч':
                    all_data['Пол'] = 'мужской'
                else:
                    all_data['Пол'] = '______'
            else:
                all_data['Пол'] = '______'

            info = all_data.get('№ амбулаторной карты')

            if not all_patients_data.get(info):
                all_patients_data[info] = dict()
            else:
                print(f"CONFLICT!\n"
                      f"{all_patients_data.get(info)}\n"
                      f"{all_data}\n\n")

            if conflict_flag:
                all_patients_data[info].clear()

            for marker in all_data:
                all_patients_data[info][marker] = all_data.get(marker)

        for data in all_data:
            if data == 'district':
                continue
            else:
                all_data[data] = ''
        if not conflict_flag:
            return True
        return False

    pattern = r'<[^>]*>'

    all_flag = {

        '№ g/g': False,
        '№ амбулаторной карты': False,
        'Фамилия': False,
        'Имя': False,
        'Отчество': False,
        'Дата рождения': False,
        'Домашний адрес': False,
        '_': False
    }

    all_data = {
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

    counter_string = 0
    counter_error = 0
    counter_patients = 0

    with open(path, 'rb') as f:
        for line in f:
            counter_string += 1

            line_str = ' '.join(line.decode('windows-1251').replace('&nbsp;', ' ').replace('<br>', '').split())
            if '<tr height=' in line_str:

                res = 'new tab'
            else:
                res = re.sub(pattern, '', line_str)

            if len(res) != 0:

                if res == 'new tab':
                    if append_info():
                        counter_patients += 1
                    else:
                        counter_error += 1

                    continue

                if all_flag['№ g/g']:
                    if ('участок' in res
                            or '0-Минск' in res
                            or 'Личный педиатр' in res
                            or 'Минская обл' in res):
                        all_data['district'] = res.replace('-й участок', '')
                        continue
                    else:
                        all_flag['№ g/g'] = False
                        all_flag['№ амбулаторной карты'] = True
                        continue

                flags = ('№ амбулаторной карты',
                         'Фамилия', 'Имя', 'Отчество',
                         'Дата рождения', 'Домашний адрес', '_')

                for flag in flags:
                    if all_flag[flag]:
                        if res.isalpha():
                            all_data[flag] = res.capitalize()
                        elif flag == 'Домашний адрес':
                            if '(' in res:
                                all_data['Домашний адрес'] = res[:res.index('(')]
                                all_data['Домашний телефон'] = res[res.index('('):]
                            else:
                                all_data[flag] = res
                        else:
                            all_data[flag] = res
                        all_flag[flag] = False
                        all_flag[flags[flags.index(flag) + 1]] = True
                        break

        else:
            if all_data.get('Фамилия'):
                if append_info():
                    counter_patients += 1
                else:
                    counter_error += 1

    print(f"Файл {path}  успешно записан\n"
          f"Количество строк: {counter_string}\n"
          f"Количество пациентов: {counter_patients}\n"
          f"Количество ошибок: {counter_error}")


def create_child_card_file_db(path):
    def append_info():
        conflict_flag = False
        for flag_ in all_flag:
            all_flag[flag_] = False
        all_flag['№ g/g'] = True

        if all_data.get('ФИО') and all_data.get('№ амбулаторной карты'):

            info = f"{all_data.get('№ амбулаторной карты')}"

            if not all_patients_data.get(info):
                conflict_flag = True
            else:
                for marker in ('Фамилия', 'Имя', 'Отчество'):
                    if all_patients_data[info].get(marker) not in all_data.get('ФИО'):
                        print(f"CONFLICT!\n"
                              f"{all_patients_data.get(info)}\n"
                              f"{all_data}\n\n")
                        break

                for marker in ('Домашний адрес', 'Домашний телефон', 'Учеба'):
                    all_patients_data[info][marker] = all_data.get(marker)

        for data in all_data:
            all_data[data] = ''
        if not conflict_flag:
            return True
        return False

    pattern = r'<[^>]*>'

    all_flag = {

        '№ g/g': False,
        '№ амбулаторной карты': False,
        'ФИО': False,
        'Дата рождения': False,
        'Домашний адрес': False,
        'Домашний телефон': False,
        'Учеба': False,
        '_': False,
        '__': False,
        '___': False
    }

    all_data = {
        '№ амбулаторной карты': '',
        'ФИО': '',
        'Дата рождения': '',
        'Домашний адрес': '',
        'Домашний телефон': '',
        'Учеба': ''
    }

    counter_string = 0
    counter_error = 0
    counter_patients = 0

    with open(path, 'rb') as f:
        for line in f:
            counter_string += 1

            line_str = ' '.join(line.decode('windows-1251').replace('&nbsp;', ' ').replace('<br>', '').split())
            if '<tr height=' in line_str:
                res = 'new tab'
            else:
                res = re.sub(pattern, '', line_str)

            if len(res) != 0:

                if res == 'new tab':
                    if append_info():
                        counter_patients += 1
                    else:
                        counter_error += 1
                    continue

                if all_flag['№ g/g']:
                    all_flag['№ g/g'] = False
                    all_flag['№ амбулаторной карты'] = True
                    continue

                flags = ('№ амбулаторной карты',
                         'ФИО', 'Дата рождения', 'Домашний адрес', 'Домашний телефон', 'Учеба',
                         '_', '__', '___')

                for flag in flags:
                    if all_flag[flag]:
                        all_data[flag] = res
                        all_flag[flag] = False
                        all_flag[flags[flags.index(flag) + 1]] = True
                        break

        else:
            if all_data.get('Фамилия'):
                if append_info():
                    counter_patients += 1
                else:
                    counter_error += 1

    print(f"Файл {path}  успешно записан\n"
          f"Количество строк: {counter_string}\n"
          f"Количество пациентов: {counter_patients}\n"
          f"Количество ошибок: {counter_error}")


def create_doc():
    all_data = dict()
    for amb_card in all_patients_data:
        district = all_patients_data[amb_card].get('district')
        if not all_data.get(district):
            all_data[district] = dict()
        birth_date = all_patients_data[amb_card].get('Дата рождения').split('.')[-1]
        if not all_data[district].get(birth_date):
            all_data[district][birth_date] = list()
        all_data[district][birth_date].append(all_patients_data.get(amb_card))

    path = f".{os.sep}картотека"
    if not os.path.exists(path=f".{os.sep}картотека"):
        os.mkdir(path)

    for district in all_data:
        path = f".{os.sep}картотека{os.sep}{district.replace('.', '').replace(' ', '_')}"
        if not os.path.exists(path):
            os.mkdir(path)
        print(district)
        for year in all_data.get(district):
            print(year)
            master = Document(f".{os.sep}картотека{os.sep}Титульник.docx")
            composer = Composer(master)

            for patient_data in sorted(all_data[district].get(year), key=lambda i: i.get('Фамилия')):
                render_data = dict()

                for mark_1, mark_2 in (('district', 'district'),
                                       ('name_1', 'Фамилия'),
                                       ('name_2', 'Имя'),
                                       ('name_3', 'Отчество'),
                                       ('gender', 'Пол'),
                                       ('birth_date', 'Дата рождения'),
                                       ('address', 'Домашний адрес'),
                                       ('phone', 'Домашний телефон'),
                                       ('date_1', 'Взят на учет'),
                                       ('aducation', 'Учеба'),
                                       ('amb_cart', '№ амбулаторной карты')
                                       ):
                    render_data[mark_1] = patient_data.get(mark_2, '__________')
                    # name_4 = ''
                    # for sym in patient_data.get('Фамилия', ' '):
                      #     name_4 += f"{sym}\n"
                    # if len(name_4) > 28:
                    #     name_4 = name_4[:28] + '...'
                    # else:
                    #     name_4 = name_4[:-1]
                    # render_data['name_4'] = name_4
                    # render_data['b_date'] = patient_data.get('Дата рождения', '_____').split('.')[-1]

                # master.add_page_break()
                doc = DocxTemplate(f".{os.sep}картотека{os.sep}Титульник.docx")
                doc.render(render_data)
                composer.append(doc)
            doc_name = f"{path}{os.sep}{year}.docx"
            composer.save(doc_name)


create_card_file_db(path=f'.{os.sep}картотека{os.sep}Картотека пациентов.html')
create_child_card_file_db(path=f'.{os.sep}картотека{os.sep}Картотека детского населения.html')
create_doc()
