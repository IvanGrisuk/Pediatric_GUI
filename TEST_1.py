import os
import random
from datetime import datetime, timedelta
from tkinter.scrolledtext import ScrolledText

import tkinter as tk
from tkinter import *

all_diagnosis = {
    'ОРИ': {
        "complaints": {'температура до': ['38.5'],
                       'кашель': ['сухой'],
                       'боль': ['в горле'],
                       'насморк': ['сопли прозрачные']},
        "examination": {'Общее состояние': ['удовлетворительное'],
                        "Температура": ['36.6'],
                        'Кожные покровы': ['влажные', 'чистые'],
                        'Сыпь': ['нет'],
                        'Слизистая глотки': ['гиперемирована', 'зернистая'],
                        'Нёбные миндалины': ['увеличены', '1ст.', "налетов нет"],
                        'Носовое дыхание': ['затруднено', 'из носа', 'слизистое отделяемое'],
                        'Периферические лимфоузлы': ['увеличены', 'шейные', 'подчелюстные', "эластичные",
                                                     "безболезненные", "при пальпации"],
                        'Легкие': ["ЧД", 'дыхание', 'везикулярное', "проводится во все отделы", "хрипов нет"],
                        'Сердце': ["ЧСС", 'тоны сердца', 'ясные', 'ритмичные', "границы в пределах возрастной нормы"],
                        'Живот': ['мягкий', 'безболезненный', "доступен глубокой пальпации",
                                  "Печень у края реберной дуги", "селезенка не пальпируется"],
                        'Мочеиспускание': ['регулярное', 'безболезненное'],
                        'Стул': ['оформленный', 'коричневый', 'без патологических примесей'],
                        'Прочее': ['Менингеальные симптомы', 'Аппендикулярные симптомы', "отрицательные"]},
        "prescription": {"Рекомендации": ["домашний режим", "Парацетамол", "Ибупрофен", "питьевой режим",
                                          "полоскать горло", "орошать горло", "промывать нос"]}
    },
    'ФРК': {
        "complaints": {'боль': ['в животе']},
        "examination": {'Общее состояние': ['удовлетворительное'],
                        "Температура": ['36.6'],
                        'Кожные покровы': ['влажные', 'чистые'],
                        'Сыпь': ['нет'],
                        'Слизистая глотки': ['гиперемирована', 'зернистая'],
                        'Нёбные миндалины': ['увеличены', '1ст.'],
                        'Носовое дыхание': ['свободное'],
                        'Периферические лимфоузлы': ['в норме'],
                        'Легкие': ["ЧД", 'дыхание', 'везикулярное', "проводится во все отделы", "хрипов нет"],
                        'Сердце': ["ЧСС", 'тоны сердца', 'ясные', 'ритмичные', "границы в пределах возрастной нормы"],
                        'Живот': ['мягкий', 'болезненный', "в эпигастральной обл", "доступен глубокой пальпации",
                                  "Печень у края реберной дуги", "селезенка не пальпируется"],
                        'Мочеиспускание': ['регулярное', 'безболезненное'],
                        'Прочее': ['Аппендикулярные симптомы', "Перитониальные симптомы", "Пузырные симптомы",
                                   "отрицательные"]},
        "prescription": {"Рекомендации": ["домашний режим", "Парацетамол", "Ибупрофен", "питьевой режим",
                                          "диета", "Смекта"]}
    },
    'Ветряная оспа': {
        "complaints": {'температура до': ['37.5'],
                       'сыпь': True},
        "examination": {'Общее состояние': ['удовлетворительное'],
                        "Температура": ['36.6'],
                        'Кожные покровы': ['влажные', 'чистые'],
                        'Сыпь': ['везикулярная'],
                        'Слизистая глотки': ['гиперемирована', 'зернистая'],
                        'Нёбные миндалины': ['увеличены', '1ст.'],
                        'Носовое дыхание': ['свободное'],
                        'Периферические лимфоузлы': ['увеличены', 'шейные', 'подчелюстные', "эластичные",
                                                     "безболезненные", "при пальпации"],
                        'Легкие': ["ЧД", 'дыхание', 'везикулярное', "проводится во все отделы", "хрипов нет"],
                        'Сердце': ["ЧСС", 'тоны сердца', 'ясные', 'ритмичные', "границы в пределах возрастной нормы"],
                        'Живот': ['мягкий', 'безболезненный', "доступен глубокой пальпации",
                                  "Печень у края реберной дуги", "селезенка не пальпируется"],
                        'Мочеиспускание': ['регулярное', 'безболезненное'],
                        'Стул': ['оформленный', 'коричневый', 'без патологических примесей'],
                        'Прочее': ['Менингеальные симптомы', "отрицательные"]},
        "prescription": {"Рекомендации": ["домашний режим", "Парацетамол", "питьевой режим",
                                          "обработка элементов раствором 'Каламин'",
                                          "карантин 5 дней с момента появления последнего элемента"]}
    },
    'Здоров': {
        "complaints": {'нет': True},
        "examination": {'Общее состояние': ['удовлетворительное'],
                        "Температура": ['36.6'],
                        'Кожные покровы': ['влажные', 'чистые'],
                        'Сыпь': ['нет'],
                        'Слизистая глотки': ['без изменений'],
                        'Нёбные миндалины': ['увеличены', '1ст.'],
                        'Носовое дыхание': ['свободное'],
                        'Периферические лимфоузлы': ['не увеличены', 'эластичные', "безболезненные", "при пальпации"],
                        'Легкие': ["ЧД", 'дыхание', 'везикулярное', "проводится во все отделы", "хрипов нет"],
                        'Сердце': ["ЧСС", 'тоны сердца', 'ясные', 'ритмичные', "границы в пределах возрастной нормы"],
                        'Живот': ['мягкий', 'безболезненный', "доступен глубокой пальпации",
                                  "Печень у края реберной дуги", "селезенка не пальпируется"],
                        'Мочеиспускание': ['регулярное', 'безболезненное'],
                        'Стул': ['оформленный', 'коричневый', 'без патологических примесей'],

                        'Прочее': ['Менингеальные симптомы', 'Аппендикулярные симптомы', "отрицательные"]},
        "prescription": {"Рекомендации": []}
    },

}

all_data_diagnosis = {
    "diagnosis": ("Предварительный диагноз", 'ОРИ', 'ФРК', "Ветряная оспа", "Здоров"),
    "place": ("Место осмотра", 'на дому', 'в поликлинике'),
    'complaints': ("Жалобы", "нет", "рвота", "сыпь",
                   ("температура до", '37', '37.5', '38', '38.5', '39', '39.5', '40', '40.5'),
                   ("кашель", "сухой", "влажный", "приступообразный", "лающий"),
                   ("боль", "головная", "в ушах", "в горле", "в глазах", "в груди", "в мышцах", "в животе"),
                   ("насморк", "сопли зеленые", "сопли прозрачные"),
                   ("диарея: стул", "зеленый", "коричневый", "обесцвеченный", "желтый", "с кровью", "с слизью")),
    "examination": ("Осмотр",
                    ("Температура", "36.6", '37', '37.5', '38', '38.5', '39', '39.5', '40', '40.5'),
                    ("Общее состояние", "удовлетворительное", "средней тяжести", "тяжелое"),
                    ("Кожные покровы", "влажные", "сухие", "чистые"),
                    ("Сыпь", "нет", "пятнистая", "папулезная", "пустулезная", "везикулярная", "мелкоточечная",
                     "геморрагическая",
                     "на", "лице", "шее", "туловище", "руках", "кистях", "стопах", "ногах", "в паховой области",
                     "в складках кожи", "по всему телу"),
                    ("Слизистая глотки", "без изменений", "гиперемирована", "зернистая"),
                    ("Нёбные миндалины", "без изменений", "увеличены", "1ст.", "2ст.", "3ст.",
                     "налетов нет", "обложены налетом", "белого цвета", "серого цвета"),
                    ("Носовое дыхание", "свободное", "затруднено", "из носа",
                     "слизистое отделяемое", "гнойное отделяемое"),
                    ("Периферические лимфоузлы", "не увеличены", "увеличены", "подчелюстные", "шейные", "надключичные",
                     "подмышечные", "паховые", "справа", "слева", "с обеих сторон", "плотные", "эластичные",
                     "болезненные", "безболезненные", "при пальпации"),
                    ("Легкие", "ЧД", "дыхание", "везикулярное", "пуэрильное", "жесткое", "ослабленное",
                     "проводится во все отделы", "хрипов нет",
                     "хрипы", "сухие", "влажные", "проводные", "свистящие"),
                    ("Сердце", "ЧСС", "тоны сердца", "ясные", "приглушены", "ритмичные",
                     "границы в пределах возрастной нормы", "систолический шум"),
                    ("Живот", "мягкий", "безболезненный", "доступен глубокой пальпации", "твердый", "болезненный",
                     "в эпигастральной обл", "в мезогастральной обл", "в гипогастральной обл", "справа", "слева",
                     "Печень у края реберной дуги", "селезенка не пальпируется"),
                    ("Мочеиспускание", "регулярное", "безболезненное", "диурез снижен", "боль при мочеиспускании"),
                    ("Стул", "оформленный", "послабленный", "разжиженный", "кашицеобразный",
                     "коричневый", "зеленый", "обесцвеченный", "желтый", "без патологических примесей",
                     "с кровью", "с слизью", "регулярный", "частый", "редкий"),
                    ("Отоскопия", "не проводилась", "без патологии", "справа", "слева", "с обеих сторон",
                     "отит", "катаральный", "гнойный", "экссудативный", "наружный диффузный"),
                    ("Прочее", "Менингеальные симптомы", "Аппендикулярные симптомы",
                     "Перитониальные симптомы", "Пузырные симптомы",
                     "отрицательные", "положительные", "сомнительные")),
    "prescription": ("Назначения", ("Анализы", "ОАК", "ОАМ", "Глюкоза", "Копрограмма", "я/глист"),
                     ("Рекомендации", "домашний режим", "Парацетамол", "Ибупрофен", "питьевой режим",
                      "полоскать горло", "орошать горло", "промывать нос",
                      "диета", "Смекта"),

                     ("Антибиотик Амоксициллин",
                      "Форма", "сусп. 125/5", "сусп. 250/5", "таб. 250", "таб. 500", "таб. 1000",
                      "Дозировка", "50 мг/кг/сут", "75 мг/кг/сут", "90 мг/кг/сут"),

                     ("Антибиотик Амоксициллин + клавулановая кислота",
                      "Форма", "сусп. 125/31.25/5", "сусп. 200/28.5/5",
                      "сусп. 250/62.5/5", "сусп. 400/57/5", "сусп. 600/42.9/5",
                      "таб. 250/125", "таб. 500/125", "таб. 875/125",
                      "Дозировка", "50 мг/кг/сут", "75 мг/кг/сут", "90 мг/кг/сут"),

                     ("Антибиотик Цефуроксим",
                      "Форма", "сусп. 125/5", "таб. 125", "таб. 250",
                      "Дозировка", "20 мг/кг/сут", "30 мг/кг/сут")
                     )
}

patient = {
    'name': 'Яко Нат',
    'birth_date': '11.11.2011',
    'gender': 'ж',
    'amb_cart': '1111',
    'patient_district': '1',
    'address': 'Славин'
}

user = {'text_size': 10,
        'doctor_name': '',
        'manager': '',
        'ped_div': '',
        'doctor_district': ''}

render_data = dict()

data = dict()


def get_age(birth_date):
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
    birthday = '.'.join(birthday)
    birthday = datetime.strptime(birthday, date_form)

    today = datetime.today()
    age = today.year - birthday.year

    if (today.month < birthday.month) or (today.month == birthday.month and today.day < birthday.day):
        age -= 1

    return age


def examination_cmd():
    destroy_elements = dict()
    data['examination'] = dict()

    selected_place = StringVar()
    selected_diagnosis = StringVar()

    examination_root = Frame(borderwidth=1)

    def paste_hr_br():
        age = get_age(patient.get('birth_date'))
        indicators = {
            '0-3': {
                'br': (22, 28),
                'hr': (80, 100),
                'bp': (90, 100, 60, 70)},
            '3-6': {
                'br': (20, 28),
                'hr': (80, 100),
                'bp': (96, 110, 60, 70)},
            '6-12': {
                'br': (18, 22),
                'hr': (70, 90),
                'bp': (100, 110, 60, 75)},
            '>12': {
                'br': (18, 22),
                'hr': (70, 80),
                'bp': (110, 120, 70, 78)},
        }

        if age <= 3:
            indicator = indicators['0-3']
        elif age <= 6:
            indicator = indicators['3-6']
        elif age <= 12:
            indicator = indicators['6-12']
        else:
            indicator = indicators['>12']

        render_data['br'] = random.randrange(start=indicator['br'][0], stop=indicator['br'][1], step=2)
        render_data['hr'] = random.randrange(start=indicator['hr'][0], stop=indicator['hr'][1], step=2)

    def paste_frame_diagnosis():
        frame_diagnosis = Frame(frame_1, borderwidth=1, relief="solid")
        label_diagnosis = Label(master=frame_diagnosis, text=f"{all_data_diagnosis.get('diagnosis')[0]}",
                                font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_diagnosis.pack(fill='both', expand=True)
        frame_diagnosis_1 = Frame(frame_diagnosis, borderwidth=1)

        def select_diagnosis():
            data['examination']['diagnosis'] = selected_diagnosis.get()
            # label_diagnosis['text'] = f"{all_data_diagnosis.get('diagnosis')[0]}: {selected_diagnosis.get()}"
            # frame_diagnosis_1.destroy()
            #
            # frame_diagnosis.columnconfigure(index='all', minsize=40, weight=1)
            # frame_diagnosis.rowconfigure(index='all', minsize=20)
            for el in destroy_elements.get('examination'):
                el.destroy()
            destroy_elements['examination'].clear()
            for mark_ in data['examination'].get('complaints_but'):
                data['examination']['complaints_but'].get(mark_).set(0)
            for mark_ in data['examination'].get('examination_but'):
                data['examination']['examination_but'].get(mark_).set(0)
            for mark_ in data['examination'].get('prescription_but'):
                data['examination']['prescription_but'].get(mark_).set(0)

            for complaints_but in all_diagnosis.get(selected_diagnosis.get()).get("complaints"):
                complaints_list = all_diagnosis.get(selected_diagnosis.get()).get("complaints").get(complaints_but)
                if isinstance(complaints_list, list):
                    for complaints in complaints_list:
                        if f"{complaints_but}_{complaints}" in data['examination'].get('complaints_but'):
                            data['examination']['complaints_but'][f"{complaints_but}_{complaints}"].set(1)
                else:
                    if complaints_but in data['examination'].get('complaints_but'):
                        data['examination']['complaints_but'][complaints_but].set(1)

            select_complaints()

            for examination_but in all_diagnosis.get(selected_diagnosis.get()).get("examination"):
                examination_list = all_diagnosis.get(selected_diagnosis.get()).get("examination").get(examination_but)
                if isinstance(examination_list, list):
                    for examination in examination_list:
                        if f"{examination_but}_{examination}" in data['examination'].get('examination_but'):
                            data['examination']['examination_but'][f"{examination_but}_{examination}"].set(1)
                else:
                    if examination_but in data['examination'].get('examination_but'):
                        data['examination']['examination_but'][examination_but].set(1)

            select_examination()

            txt_prescription.delete(1.0, 'end')
            text = 'Рекомендации: '
            for prescription_but in all_diagnosis.get(selected_diagnosis.get()).get("prescription"):
                prescription_list = all_diagnosis.get(selected_diagnosis.get()).get("prescription").get(
                    prescription_but)
                if isinstance(prescription_list, list):
                    for prescription in prescription_list:
                        if f"{prescription_but}_{prescription}" in data['examination'].get('prescription_but'):
                            data['examination']['prescription_but'][f"{prescription_but}_{prescription}"].set(1)
                        else:
                            text += f"{prescription}, "
                else:
                    if prescription_but in data['examination'].get('prescription_but'):
                        data['examination']['prescription_but'][prescription_but].set(1)

            if text != 'Рекомендации: ':
                txt_prescription.insert(1.0, text)

            select_prescription()

            paste_examination_kb()

            frame_diagnosis.update()

        row, col = 0, 0
        for mark in all_data_diagnosis.get('diagnosis')[1:]:
            btn = Radiobutton(frame_diagnosis_1, text=mark,
                              font=('Comic Sans MS', user.get('text_size')),
                              value=mark, variable=selected_diagnosis, command=select_diagnosis,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=row, column=col, sticky='ew')
            col += 1

        frame_diagnosis_1.columnconfigure(index='all', minsize=40, weight=1)
        frame_diagnosis_1.rowconfigure(index='all', minsize=20)
        frame_diagnosis_1.pack(fill='both', expand=True)

        frame_diagnosis.columnconfigure(index='all', minsize=40, weight=1)
        frame_diagnosis.rowconfigure(index='all', minsize=20)
        frame_diagnosis.grid(row=0, column=0, sticky='ew')

    def paste_frame_place():
        frame_place = Frame(frame_1, borderwidth=1, relief="solid")
        label_place = Label(master=frame_place, text=f"{all_data_diagnosis.get('place')[0]}",
                            font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_place.pack(fill='both', expand=True)
        frame_place_1 = Frame(frame_place, borderwidth=1)

        def select_place():
            data['examination']['place'] = selected_place.get()
            label_place['text'] = f"{all_data_diagnosis.get('place')[0]}: {selected_place.get()}"
            frame_place_1.destroy()

            frame_place.columnconfigure(index='all', minsize=40, weight=1)
            frame_place.rowconfigure(index='all', minsize=20)

            frame_place.update()

        row, col = 0, 0
        for mark in all_data_diagnosis.get('place')[1:]:
            btn = Radiobutton(frame_place_1, text=mark,
                              font=('Comic Sans MS', user.get('text_size')),
                              value=mark, variable=selected_place, command=select_place,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=row, column=col, sticky='ew')
            col += 1

        frame_place_1.columnconfigure(index='all', minsize=40, weight=1)
        frame_place_1.rowconfigure(index='all', minsize=20)
        frame_place_1.pack(fill='both', expand=True)

        frame_place.columnconfigure(index='all', minsize=40, weight=1)
        frame_place.rowconfigure(index='all', minsize=20)
        frame_place.grid(row=0, column=1, sticky='ew')

    def paste_frame_1():
        paste_frame_diagnosis()
        paste_frame_place()

        frame_1.columnconfigure(index='all', minsize=40, weight=1)
        frame_1.rowconfigure(index='all', minsize=20)
        frame_1.pack(fill='both', expand=True)

    frame_1 = Frame(examination_root, borderwidth=1, relief="solid")
    paste_frame_1()

    def paste_frame_complaints():

        label_complaints = Label(master=frame_complaints_main, text=f"{all_data_diagnosis.get('complaints')[0]}",
                                 font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_complaints.grid(row=0, column=0, sticky='ew')

        txt_complaints.grid(column=0, row=1, sticky='ew', columnspan=2)
        data['examination']['complaints_but'] = dict()

        for mark in all_data_diagnosis.get('complaints')[1:]:
            if isinstance(mark, tuple):
                for mark_2 in mark[1:]:
                    data['examination']['complaints_but'][f"{mark[0]}_{mark_2}"] = IntVar()
            else:
                data['examination']['complaints_but'][mark] = IntVar()

        def change_complaints_kb_status():
            if data['examination'].get('open_complaints_kb'):
                for el in destroy_elements.get('complaints'):
                    el.destroy()
                data['examination']['open_complaints_kb'] = False
                destroy_elements['complaints'].clear()
                change_complaints_kb_button['text'] = 'открыть клавиатуру жалоб'
                txt_complaints['height'] = 2
                frame_complaints_main.grid(row=0, column=0, sticky='ew', columnspan=3)
                data['examination']['complaints_buttons'].clear()

            else:
                destroy_elements['complaints'].clear()
                change_complaints_kb_button['text'] = 'скрыть клавиатуру жалоб'
                paste_complaints_kb()
                txt_complaints['height'] = 6
                frame_complaints_main.grid(row=0, column=0, sticky='ew', columnspan=1)

        change_complaints_kb_button = Button(frame_complaints_main, text='скрыть клавиатуру жалоб',
                                             command=change_complaints_kb_status,
                                             font=('Comic Sans MS', user.get('text_size')))
        change_complaints_kb_button.grid(column=1, row=0, sticky='ew')

        frame_complaints_main.columnconfigure(index='all', minsize=10, weight=1)
        frame_complaints_main.rowconfigure(index='all', minsize=10)
        # frame_complaints_main.pack(fill='both', expand=True, side=tk.LEFT)
        frame_complaints_main.grid(row=0, column=0, sticky='ew')

        def paste_complaints_kb():

            data['examination']['open_complaints_kb'] = True
            destroy_elements['complaints'] = list()
            data['examination']['complaints_buttons'] = dict()

            frame_complaints_1 = Frame(frame_complaints)
            frame_loc = Frame(frame_complaints_1)

            destroy_elements['complaints'].append(frame_complaints_1)

            row, col = 0, 0
            for mark in all_data_diagnosis.get('complaints')[1:]:
                if isinstance(mark, tuple):
                    pass
                else:
                    btn = Checkbutton(frame_loc, text=mark,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      onvalue=1, offvalue=0,
                                      variable=data['examination']['complaints_but'].get(mark),
                                      command=select_complaints,
                                      indicatoron=False, selectcolor='#77f1ff')
                    btn.grid(row=1, column=col, sticky='ew')
                    data['examination']['complaints_buttons'][mark] = btn

                    col += 1
            frame_loc.columnconfigure(index='all', minsize=10, weight=1)
            frame_loc.rowconfigure(index='all', minsize=10)
            frame_loc.pack(fill='both', expand=True)

            for mark in all_data_diagnosis.get('complaints')[1:]:
                if isinstance(mark, tuple):
                    row, col = 0, 0
                    frame_loc = Frame(frame_complaints_1)
                    destroy_elements['complaints'].append(frame_loc)

                    label_complaints_loc = Label(master=frame_loc, text=f"{mark[0]}",
                                                 font=('Comic Sans MS', user.get('text_size')), bg='white')
                    label_complaints_loc.grid(row=row, column=col, sticky='ew')
                    col += 1
                    for mark_2 in mark[1:]:
                        btn = Checkbutton(frame_loc, text=mark_2,
                                          font=('Comic Sans MS', user.get('text_size')),
                                          onvalue=1, offvalue=0,
                                          variable=data['examination']['complaints_but'].get(f"{mark[0]}_{mark_2}"),
                                          command=select_complaints,
                                          indicatoron=False, selectcolor='#77f1ff')
                        btn.grid(row=row, column=col, sticky='ew')
                        data['examination']['complaints_buttons'][f"{mark[0]}_{mark_2}"] = btn

                        col += 1
                    frame_loc.columnconfigure(index='all', minsize=10, weight=1)
                    frame_loc.rowconfigure(index='all', minsize=10)
                    frame_loc.pack(fill='both', expand=True)

            frame_complaints_1.columnconfigure(index='all', minsize=10, weight=1)
            frame_complaints_1.rowconfigure(index='all', minsize=10)
            # frame_complaints_1.pack(fill='both', expand=True).grid(row=0, column=0, sticky='ew')
            frame_complaints_1.grid(row=0, column=1, sticky='ew', columnspan=2)

        paste_complaints_kb()
        frame_complaints.columnconfigure(index='all', minsize=40, weight=1)
        frame_complaints.rowconfigure(index='all', minsize=20)
        frame_complaints.pack(fill='both', expand=True, padx=2, pady=2)

    def select_complaints():
        text = ''
        for mark in data['examination'].get('complaints_but'):
            if data['examination']['complaints_but'].get(mark).get() == 1:
                if mark == 'нет':
                    text = 'нет'
                    for mark_ in data['examination'].get('complaints_but'):
                        data['examination']['complaints_but'].get(mark_).set(0)
                    break
                else:
                    if '_' not in mark:
                        text += f"{mark}, "
                    else:
                        mark_1, mark_2 = mark.split('_')
                        if mark_1 == 'температура до':
                            if 'температура до' not in text:
                                text += f"температура до {mark_2}, "
                            else:
                                text = text[:-2]
                                text += f" - {mark_2}, "

                        else:
                            if mark_1 not in text:
                                if mark_1 == 'диарея: стул':
                                    text += f"{mark_1} {mark_2}, "
                                else:
                                    text += f"{mark_1}: {mark_2}, "
                            else:
                                text += f"{mark_2}, "

        txt_complaints.delete(1.0, 'end')
        if text != 'нет':
            text = text[:-2] + '.'
        txt_complaints.insert(1.0, text)

        if data['examination'].get('open_complaints_kb'):
            for but in data['examination'].get('complaints_buttons'):
                if data['examination']['complaints_but'].get(but).get() == 1:
                    data['examination']['complaints_buttons'][but]['bg'] = '#77f1ff'
                else:
                    data['examination']['complaints_buttons'][but]['bg'] = '#cdcdcd'

    frame_complaints = Frame(examination_root, relief="solid", padx=1, pady=1)
    frame_complaints_main = Frame(frame_complaints, padx=1, pady=1)
    txt_complaints = ScrolledText(frame_complaints_main, width=15, height=6,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  wrap="word")

    paste_frame_complaints()

    def paste_frame_examination():

        label_examination = Label(master=frame_examination_main, text=f"{all_data_diagnosis.get('examination')[0]}",
                                  font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_examination.grid(row=0, column=0, sticky='ew')

        txt_examination.grid(column=0, row=1, sticky='ew', columnspan=2)

        data['examination']['examination_but'] = dict()
        for mark_ in all_data_diagnosis.get('examination')[1:]:
            if isinstance(mark_, tuple):
                for mark_2_ in mark_[1:]:
                    data['examination']['examination_but'][f"{mark_[0]}_{mark_2_}"] = IntVar()

        def change_examination_kb_status():
            if data['examination'].get('open_examination_kb'):
                for el in destroy_elements.get('examination'):
                    el.destroy()
                data['examination']['open_examination_kb'] = False
                destroy_elements['examination'].clear()
                change_examination_kb_button['text'] = 'открыть клавиатуру осмотра'
                txt_examination['height'] = 5
                txt_examination['width'] = 70

            else:
                destroy_elements['examination'].clear()
                change_examination_kb_button['text'] = 'скрыть клавиатуру осмотра'
                paste_examination_kb()
                txt_examination['height'] = 20
                txt_examination['width'] = 20

        change_examination_kb_button = Button(frame_examination_main, text='скрыть клавиатуру осмотра',
                                              command=change_examination_kb_status,
                                              font=('Comic Sans MS', user.get('text_size')))
        change_examination_kb_button.grid(column=1, row=0, sticky='ew')

        frame_examination_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_examination_main.rowconfigure(index='all', minsize=20)
        frame_examination_main.pack(fill='both', expand=True, side=tk.LEFT)

        paste_examination_kb()
        frame_examination.columnconfigure(index='all', minsize=40, weight=1)
        frame_examination.rowconfigure(index='all', minsize=20)
        frame_examination.pack(fill='both', expand=True, padx=2, pady=2)

    def select_examination_frame(event):
        num = f"{event.widget}".split('.!')[-2].replace('frame', '')
        if not num:
            num = '1'
        data['examination']['examination_frame'] = data['examination'].get('examination_frame_list')[int(num) - 1]
        for el in destroy_elements.get('examination'):
            el.destroy()
        destroy_elements['examination'].clear()

        paste_examination_kb()

    def select_examination():
        text = ''
        if not render_data.get('hr'):
            paste_hr_br()
        for mark in data['examination'].get('examination_but'):
            if data['examination']['examination_but'].get(mark).get() == 1:
                mark_1, mark_2 = mark.split('_')
                if mark_1 == 'Легкие' and mark_2 == 'ЧД':
                    mark_2 = f"ЧД {render_data.get('br', '')}/мин."
                elif mark_1 == 'Сердце' and mark_2 == 'ЧСС':
                    mark_2 = f"ЧСС {render_data.get('hr', '')}/мин."

                if mark_1 == 'Прочее':
                    text += f"{mark_2}, "

                else:
                    if mark_1 not in text:
                        if text:
                            text = text[:-2] + '. '
                        text += f"{mark_1}: {mark_2}, "
                    else:
                        text += f"{mark_2}, "

        txt_examination.delete(1.0, 'end')
        text = text[:-2] + '.'
        txt_examination.insert(1.0, text)

    def paste_examination_kb():
        data['examination']['open_examination_kb'] = True
        destroy_elements['examination'] = list()
        data['examination']['examination_frame_list'] = list()
        data['examination']['examination_buttons'] = dict()

        txt_examination['height'] = 20
        txt_examination['width'] = 20

        frame_examination_kb = Frame(frame_examination, borderwidth=1)

        destroy_elements['examination'].append(frame_examination_kb)

        for mark in all_data_diagnosis.get('examination')[1:]:
            if isinstance(mark, tuple):
                data['examination']['examination_frame_list'].append(mark[0])

                frame_loc = Frame(frame_examination_kb, borderwidth=1)

                if mark[0] != data['examination'].get('examination_frame', ''):

                    text = f"{mark[0]}: "
                    if selected_diagnosis.get():
                        if all_diagnosis.get(selected_diagnosis.get()).get('examination').get(mark[0]):
                            for i in all_diagnosis.get(selected_diagnosis.get()).get('examination').get(mark[0]):
                                text += f"{i}, "
                    text = text[:-2]

                    lbl_0 = Label(frame_loc, text=text,
                                  font=('Comic Sans MS', user.get('text_size')), border=1, compound='left',
                                  bg='#f0fffe', relief='ridge')
                    lbl_0.pack(fill='both', expand=True)
                    lbl_0.bind('<Button-1>', select_examination_frame)

                else:

                    row, col = 0, 0

                    label_examination_loc = Label(master=frame_loc, text=f"{mark[0]}",
                                                  font=('Comic Sans MS', user.get('text_size')), bg='white')
                    label_examination_loc.grid(row=row, column=col, sticky='ew')
                    col += 1
                    for mark_2 in mark[1:]:

                        btn = Checkbutton(frame_loc, text=mark_2,
                                          font=('Comic Sans MS', user.get('text_size')),
                                          onvalue=1, offvalue=0,
                                          variable=data['examination']['examination_but'].get(f"{mark[0]}_{mark_2}"),
                                          command=select_examination,
                                          indicatoron=False, selectcolor='#77f1ff')
                        btn.grid(row=row, column=col, sticky='ew')
                        if data['examination']['examination_but'].get(f"{mark[0]}_{mark_2}").get() == 1:
                            btn['bg'] = '#77f1ff'

                        col += 1
                        if col == 5:
                            col = 0
                            row += 1
                frame_loc.columnconfigure(index='all', minsize=40, weight=1)
                frame_loc.rowconfigure(index='all', minsize=20)
                frame_loc.pack(fill='both', expand=True)

            else:
                pass

        frame_examination_kb.columnconfigure(index='all', minsize=40, weight=1)
        frame_examination_kb.rowconfigure(index='all', minsize=20)
        frame_examination_kb.pack(fill='both', expand=True, padx=2, pady=2)

    frame_examination = Frame(examination_root, borderwidth=1, relief="solid")
    frame_examination_main = Frame(frame_examination, borderwidth=1)
    txt_examination = ScrolledText(frame_examination_main, width=20, height=20,
                                   font=('Comic Sans MS', user.get('text_size')),
                                   wrap="word")

    paste_frame_examination()

    frame_diagnosis_txt = Frame(examination_root, borderwidth=1, relief="solid")
    txt_diagnosis = ScrolledText(frame_diagnosis_txt, width=70, height=3,
                                 font=('Comic Sans MS', user.get('text_size')),
                                 wrap="word")
    txt_diagnosis.pack(fill='both', expand=True)
    txt_diagnosis.insert(1.0, 'Диагноз: ')
    frame_diagnosis_txt.pack(fill='both', expand=True)

    def paste_frame_prescription():
        label_prescription = Label(master=frame_prescription_main, text=f"{all_data_diagnosis.get('prescription')[0]}",
                                   font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_prescription.grid(row=0, column=0, sticky='ew')

        txt_prescription.grid(column=0, row=1, sticky='ew', columnspan=2)

        data['examination']['prescription_but'] = dict()
        for mark_ in all_data_diagnosis.get('prescription')[1:]:
            if isinstance(mark_, tuple):
                for mark_2_ in mark_[1:]:
                    data['examination']['prescription_but'][f"{mark_[0]}_{mark_2_}"] = IntVar()

        def change_prescription_kb_status():
            if data['examination'].get('open_prescription_kb'):
                for el in destroy_elements.get('prescription'):
                    el.destroy()
                data['examination']['open_prescription_kb'] = False
                destroy_elements['prescription'].clear()
                change_prescription_kb_button['text'] = 'открыть клавиатуру рекомендаций'
                txt_prescription['height'] = 3
                txt_prescription['width'] = 70

            else:
                destroy_elements['prescription'].clear()
                change_prescription_kb_button['text'] = 'скрыть клавиатуру рекомендаций'
                paste_prescription_kb()
                txt_prescription['height'] = 5
                txt_prescription['width'] = 20

        change_prescription_kb_button = Button(frame_prescription_main, text='скрыть клавиатуру рекомендаций',
                                               command=change_prescription_kb_status,
                                               font=('Comic Sans MS', user.get('text_size')))
        change_prescription_kb_button.grid(column=1, row=0, sticky='ew')

        frame_prescription_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription_main.rowconfigure(index='all', minsize=20)
        frame_prescription_main.pack(fill='both', expand=True, side=tk.LEFT)

        paste_prescription_kb()
        frame_prescription.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription.rowconfigure(index='all', minsize=20)
        frame_prescription.pack(fill='both', expand=True, padx=2, pady=2)

    def select_prescription_frame(event):
        num = f"{event.widget}".split('.!')[-2].replace('frame', '')
        if not num:
            num = '1'
        data['examination']['prescription_frame'] = data['examination'].get('prescription_frame_list')[int(num) - 1]
        for el in destroy_elements.get('prescription'):
            el.destroy()
        destroy_elements['prescription'].clear()

        paste_prescription_kb()

    def select_prescription():

        text = txt_prescription.get(1.0, 'end')[:-1]
        for mark in data['examination'].get('prescription_but'):
            mark_1, mark_2 = mark.split('_')
            if mark_2 == "Парацетамол":
                mark_2 = "Парацетамол 15 мг/кг"
            if mark_2 == "Ибупрофен":
                mark_2 = "Ибупрофен 10 мг/кг"

            if data['examination']['prescription_but'].get(mark).get() == 1:
                if mark_2 not in text:
                    if text and text[-1] in ('.', ','):
                        text += ' '
                    if mark_1 not in text:

                        if text and text[-2:] == ', ':
                            text = text[:-2] + '. '
                        text += f"{mark_1}: {mark_2}, "
                    else:
                        if text[-2:] == '. ':
                            text = text[:-2] + ', '

                        text += f"{mark_2}, "
            else:
                if 'Антибиотик' in mark:
                    pass
                else:
                    if f"{mark_2}, " in text:
                        text = text.replace(f"{mark_2}, ", '')
                    elif f", {mark_2}" in text:
                        text = text.replace(f", {mark_2}", '')

                    elif f"{mark_2}" in text:
                        text = text.replace(f"{mark_2}", ' ')

        txt_prescription.delete(1.0, 'end')
        if text[-2:] == ', ':
            text = text[:-2] + '.'
        text = text.replace(' .', '')
        txt_prescription.insert(1.0, text)

    def paste_prescription_kb():
        txt_prescription['height'] = 5
        txt_prescription['width'] = 20

        data['examination']['open_prescription_kb'] = True
        destroy_elements['prescription'] = list()
        data['examination']['prescription_frame_list'] = list()
        data['examination']['prescription_buttons'] = dict()

        frame_prescription_kb = Frame(frame_prescription, borderwidth=1)

        destroy_elements['prescription'].append(frame_prescription_kb)

        for mark in all_data_diagnosis.get('prescription')[1:]:
            if isinstance(mark, tuple):
                data['examination']['prescription_frame_list'].append(mark[0])

                frame_loc = Frame(frame_prescription_kb, borderwidth=1)

                if mark[0] != data['examination'].get('prescription_frame', ''):

                    text = f"{mark[0]}: "
                    if selected_diagnosis.get():
                        if all_diagnosis.get(selected_diagnosis.get()).get('prescription').get(mark[0]):
                            for i in all_diagnosis.get(selected_diagnosis.get()).get('prescription').get(mark[0]):
                                text += f"{i}, "
                    text = text[:-2]

                    lbl_0 = Label(frame_loc, text=text,
                                  font=('Comic Sans MS', user.get('text_size')), border=1, compound='left',
                                  bg='#f0fffe', relief='ridge')
                    lbl_0.pack(fill='both', expand=True)
                    lbl_0.bind('<Button-1>', select_prescription_frame)

                else:

                    row, col = 0, 0

                    label_prescription_loc = Label(master=frame_loc, text=f"{mark[0]}",
                                                   font=('Comic Sans MS', user.get('text_size')), bg='white')
                    label_prescription_loc.grid(row=row, column=col, sticky='ew')
                    col += 1
                    for mark_2 in mark[1:]:
                        if mark_2 in ('Форма', 'Дозировка'):
                            row += 1
                            col = 0

                            label_prescription_loc = Label(master=frame_loc, text=f"{mark_2}",
                                                           font=('Comic Sans MS', user.get('text_size')), bg='white')
                            label_prescription_loc.grid(row=row, column=col, sticky='ew')
                            col += 1
                        else:

                            btn = Checkbutton(frame_loc, text=mark_2,
                                              font=('Comic Sans MS', user.get('text_size')),
                                              onvalue=1, offvalue=0,
                                              variable=data['examination']['prescription_but'].get(
                                                  f"{mark[0]}_{mark_2}"),
                                              command=select_prescription,
                                              indicatoron=False, selectcolor='#77f1ff')
                            btn.grid(row=row, column=col, sticky='ew')
                            if data['examination']['prescription_but'].get(f"{mark[0]}_{mark_2}").get() == 1:
                                btn['bg'] = '#77f1ff'
                            col += 1
                            if col == 6:
                                col = 0
                                row += 1

                frame_loc.columnconfigure(index='all', minsize=40, weight=1)
                frame_loc.rowconfigure(index='all', minsize=20)
                frame_loc.pack(fill='both', expand=True)

            else:
                pass

        frame_prescription_kb.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription_kb.rowconfigure(index='all', minsize=20)
        frame_prescription_kb.pack(fill='both', expand=True, padx=2, pady=2)

    frame_prescription = Frame(examination_root, relief="solid", padx=1, pady=1)
    frame_prescription_main = Frame(frame_prescription, padx=1, pady=1)
    txt_prescription = ScrolledText(frame_prescription_main, width=15, height=4,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    wrap="word")

    paste_frame_prescription()

    def create_examination_doc():
        date_now, time_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S").split()
        render_data['patient_info'] = f"Дата: {date_now}\t Время: {time_now}\n" \
                                      f"ФИО: {patient.get('name')}\tдата рождения: {patient.get('birth_date')}\t" \
                                      f"{patient.get('patient_district')}-й уч\nМесто осмотра: {selected_place.get()}"
        render_data['complaints'] = f"{txt_complaints.get(1.0, 'end')}\n"
        render_data['examination'] = f" {txt_examination.get(1.0, 'end')}"
        render_data['diagnosis'] = f"{txt_diagnosis.get(1.0, 'end')}"
        render_data['prescription'] = f"{txt_prescription.get(1.0, 'end')}"

        print(render_data)
        # doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}осмотр_педиатра.docx")
        # doc.render(render_data)
        # doc_name = f".{os.sep}generated{os.sep}{data['patient'].get('name').split()[0]}_осмотр.docx"
        # doc.save(doc_name)
        # os.system(f"start {doc_name}")

    button_create_examination_doc = Button(examination_root, text='Создать документ', command=create_examination_doc)
    button_create_examination_doc.pack(fill='both', expand=True, padx=2, pady=2)

    examination_root.columnconfigure(index='all', minsize=40, weight=1)
    examination_root.rowconfigure(index='all', minsize=20)

    return examination_root




class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.scroll_x = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(self, width=300, height=100,
                                xscrollcommand=self.scroll_x.set,
                                yscrollcommand=self.scroll_y.set)
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)

        self.frame = tk.Frame(self.canvas)
        self.btn = tk.Button(self.frame, text="Загрузить изображение",
                             command=self.load_image)
        self.btn.pack()

        self.canvas.create_window((0, 0), window=self.frame,
                                  anchor=tk.N + tk.W)

        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.scroll_x.grid(row=1, column=0, sticky="we")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def resize(self, event):
        region = self.canvas.bbox(tk.ALL)
        self.canvas.configure(scrollregion=region)

    def load_image(self):
        self.btn.destroy()
        # self.frame_1 = examination_cmd()
        # self.frame_1.pack()

        self.image = tk.PhotoImage(file="python.gif")
        tk.Label(self.frame, image=self.image).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()

