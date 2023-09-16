from tkinter import *
from tkinter import ttk
import sqlite3 as sq
from tkinter.ttk import Combobox
from tkinter import scrolledtext, messagebox
import os


def decoding_name(patient_data):
    user = {
        'name': None,
        'birth_date': None,
        'gender': None,
        'amb_cart': None,
        'patient_district': None,
        'address': None
    }
    if ('Фамилия, имя, отчество пациента:' in patient_data or
            '№ амб. карты' in patient_data or
            '№ амбулаторной карты' in patient_data):
        text = patient_data
        try:
            if 'Фамилия, имя, отчество пациента:' in text:
                info = text.split()
                counter = 0
                for i in info:
                    counter += 1

                    if i == 'пациента:':
                        user['name'] = f'{info[counter]} {info[counter + 1]}'
                        if '№' not in info[counter + 2]:
                            user['name'] += f' {info[counter + 2]}'
                    elif i == 'рождения:':
                        user['birth_date'] = info[counter]
                    elif i == 'Пол:':
                        if info[counter] == 'Жен.':
                            user['gender'] = 'женский'
                        elif info[counter] == 'Муж.':
                            user['gender'] = 'мужской'
                    elif i == 'карты:':
                        user['amb_cart'] = info[counter]
                    elif i == 'Участок:':
                        user['patient_district'] = ''
                        district = info[counter]
                        for q in district:
                            if q.isdigit():
                                user['patient_district'] += q
                    elif i == 'Адрес:':
                        address = ''
                        for q in info[counter:]:
                            if ':' in q:
                                break
                            address += q + ' '
                        user['address'] = address

            elif '№ амб. карты' in text:
                for i in text.split('\n'):
                    if i.split()[0].isdigit():
                        if len(i.split('  ')) == 8:
                            info = i.split('  ')

                            user['amb_cart'] = info[0]
                            user['name'] = info[1]
                            user['birth_date'] = info[2]
                            user['address'] = info[4]
                            user['patient_district'] = ''
                            district = info[3]
                            for q in district:
                                if q.isdigit():
                                    user['patient_district'] += q
                            if len(info[1].split()) == 3:
                                if info[1][-1] == 'ч':
                                    user['gender'] = 'мужской'
                                elif info[1][-1] == 'а':
                                    user['gender'] = 'женский'
                                else:
                                    user['gender'] = 'мужской/женский'
                            else:
                                user['gender'] = 'мужской/женский'
                            break
                        else:
                            info = i.split()
                            user['amb_cart'] = info.pop(0)
                            user['name'] = ''
                            for i in range(3):
                                if info[0].isalpha():
                                    user['name'] += f'{info[0]} '
                                    info.pop(0)
                            user['birth_date'] = info.pop(0)
                            user['patient_district'] = ''
                            district = info.pop(0)
                            for q in district:
                                if q.isdigit():
                                    user['patient_district'] += q
                            user['address'] = ''
                            for i in info[info.index('г'):]:
                                if len(i) == 10 and '.' in i:
                                    break
                                else:
                                    user['address'] += f'{i} '
                            if len(user.get('name').split()) == 3:
                                if user.get('name').split()[2][-1] == 'ч':
                                    user['gender'] = 'мужской'
                                elif user.get('name').split()[2][-1] == 'а':
                                    user['gender'] = 'женский'
                                else:
                                    user['gender'] = 'мужской/женский'
                            else:
                                user['gender'] = 'мужской/женский'

                            break

            elif '№ амбулаторной карты' in text:

                for i in text.split('\n'):
                    if i.split()[0].isdigit():

                        info = i.split()
                        user['amb_cart'] = info.pop(0)
                        user['name'] = ''
                        for _ in range(3):
                            if info[0].isalpha() or info[0] not in ('Ж', 'М'):
                                user['name'] += f'{info[0]} '
                                info.pop(0)

                        gender = info.pop(0)
                        if gender == 'М':
                            user['gender'] = 'мужской'
                        elif gender == 'Ж':
                            user['gender'] = 'женский'
                        else:
                            user['gender'] = 'мужской/женский'

                        user['birth_date'] = info.pop(0)

                        user['patient_district'] = ''
                        district = info.pop(0)
                        for q in district:
                            if q.isdigit():
                                user['patient_district'] += q

                        user['address'] = 'г. '
                        for i in info[info.index('Минск'):]:
                            if i.isdigit():
                                user['address'] += f'{i} - '
                            else:
                                user['address'] += f'{i} '
                        else:
                            user['address'] = user['address'][:-2]

                        break

            if not user.get('gender'):
                user['gender'] = 'мужской/женский'
            for key, value in user.items():
                print(key, value)

                if not value:
                    if key != 'gender':
                        print(f'1) Exception! decoding_name: \ntext:{text}\n', user.get('amb_cart'),
                              user.get('district'),
                              user.get('name'), user.get('birth_date'), user.get('gender'), user.get('address'))

                        raise ValueError

        except (IndexError, ValueError):
            print(f'2) Exception! decoding_name: \ntext:{text}\n', user.get('amb_cart'), user.get('district'),
                  user.get('name'), user.get('birth_date'), user.get('gender'), user.get('address'))
            messagebox.showinfo('Ошибка', 'Ошибка имени! \nВведите шапку полностью!')

        else:
            return user

    else:
        search_loop(patient_data)


def search_loop(patient_info):

    def search_in_db(patient_data):
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

            with sq.connect(r"\\SRV2\data_base\patient_data_base.db") as conn:
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

            if len(found_data) < 1:
                counter_patient_text.set("По введенной информации не удалось найти пациента")
                # messagebox.showinfo('Ошибка', 'По введенной информации не удалось найти пациента')

            else:
                counter_patient_text.set(f"{len(found_data)}")

                if len(found_data) > 10:
                    for num in range(10):
                        lbl = Label(search_root, text=f"{found_data[num][0]}", font=('Comic Sans MS', 20))
                        lbl.grid()

                else:
                    for patient in patient_data:
                        lbl = Label(search_root, text=f"{patient[0]}", font=('Comic Sans MS', 20))
                        lbl.grid()

    search_root = Tk()
    search_root.title('Поиск пациента')
    search_root.config(bg='white')
    counter_patient_text = StringVar()
    counter_patient = Label(search_root, textvariable=counter_patient_text, font=('Comic Sans MS', 16), width=20, height=1)
    counter_patient.grid()

    Label(search_root, text='Окно данных пациента', font=('Comic Sans MS', 20)).grid(column=0, row=0, rowspan=3)

    txt_patient_data = Entry(search_root, width=30, font=('Comic Sans MS', 20))

    txt_patient_data.grid(column=0, row=1, rowspan=2)
    txt_patient_data.insert(0, patient_info)
    txt_patient_data.focus()

    Button(search_root, text='Найти', command=search_in_db, font=('Comic Sans MS', 20)).grid(column=2, row=1)

    search_root.mainloop()


# def show_patient(message: types.Message, state: FSMContext):
#     with state.proxy() as data:
#         found_data = data.get('decoding_name', dict()).get('found_data', [])
#
#     for info in found_data:
#         rowid, district, amb_cart, name_1, name_2, name_3, gender, birth_date, address, phone = info
#
#         text = f"Участок: {district};   " \
#                f"№ амб карты: {amb_cart}\n" \
#                f"ФИО: {name_1.capitalize()} {name_2.capitalize()} {name_3.capitalize()}\n" \
#                f"Пол: {gender};    " \
#                f"Дата рождения: {birth_date}\n" \
#                f"Адрес: {address}\n" \
#                f"Дополнительная информация (телефон): {phone}"
#         inline_kb = InlineKeyboardMarkup(row_width=1)
#         inline_kb.add(InlineKeyboardButton(text='Выбрать пациента',
#                                            callback_data=f'decoding_name__{rowid}__select_patient'))
#         await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=inline_kb)
#     else:
#         inline_kb = InlineKeyboardMarkup(row_width=1)
#         inline_kb.add(
#             InlineKeyboardButton(text='Изменить поисковый запрос',
#                                  callback_data='decoding_name__start_search'))
#         inline_kb.add(InlineKeyboardButton(text='Главное меню', callback_data='exit_in_main__decoding_name'))
#         await bot.send_message(message.chat.id, text=f' _ _ _ _ _ _ Конец выборки _ _ _ _ _ _ ',
#                                reply_markup=inline_kb)



