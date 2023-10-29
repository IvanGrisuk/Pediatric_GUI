import shutil
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

all_data_certificate = {
    'sport_section': ('баскетболом', 'волейболом', 'вольной борьбой', 'гандболом', 'греблей', "гимнастикой", 'каратэ',
                      'легкой атлетикой', 'музыкой', 'плаванием в бассейне', 'спортивной гимнастикой', 'танцами',
                      'теннисом', 'тхэквондо', "ушу", 'фигурным катанием', 'фигурным катанием', 'футболом', 'хоккеем',
                      'шахматами', 'шашками', '+ СОРЕВНОВАНИЯ'),
    "health": {
        "group": ("1", "2", "3", "4"),
        "physical": ("Основная", "Подготовительная", "СМГ", "ЛФК"),
        "regime": ("общий", "ортопедический", "зрительный", "щадящий", "охранительный"),
        "diet": ("А", "Б", "Д", "М", 'П', 'ПП', 'Ц'),
        "desk": ("по росту", "1", "2", "3", "средний ряд")
    },
    "diagnosis": (("<< КАРДИОЛОГИЯ >>", "САС:", "ООО", "ДХЛЖ", "НК0", "НБПНПГ", "ФСШ", "ВПС:", "ДМЖП", "ДМПП",
                   "НРС:", "умеренная", "выраженная", "тахикардия", "брадикардия", "укорочение инт. PQ"),
                  ("<< ЛОГОПЕДИЯ >>", "ОНР", "ФНР", "ФФНР", "ЗРР", "стертая дизартрия",
                   "ур.р.р.", "1", "2", "3"),
                  ("<< ОФТАЛЬМОЛОГИЯ >>", "Спазм аккомодации", "Миопия", "Гиперметропия",
                   "слабой степени", "средней степени", "тяжелой степени",
                   "миопический", "гиперметропический", "OD", "OS", "OU", "ast", "с ast"),
                  ("<< ОРТОПЕДИЯ >>", "Нарушение осанки", "Сколиотическая осанка", "Плоскостопие", "ПВУС",
                   "ИС:", "левосторонняя", "правосторонняя", "кифотическая", "грудная", "поясничная",
                   "грудо-поясничная", "деформация позвоночника", "остаточная дисплазия ТБС",
                   "ГПС", "1 ст.", "2 ст.", "3 ст."),
                  ("<< ЛОР >>", "ГА", "ГНМ", "хр. тонзиллит", "искривление носовой перегородки", "1ст", "2ст", "3ст"),
                  ("<< ПРОЧЕЕ >>", "рецидивирующие заболевания ВДП", "Атопический дерматит", "Кариес",
                   "угроза", "БРА", "хр. гастрит", "СДН", "ВСД", "нефроптоз", "справа", "слева",
                   "аллергический ринит", "анемия", "легкой ст.", "средней ст.", "тяжелой ст.",
                   "субклинич. гипотиреоз", "ИМТ", "ДМТ", "СД")),

    'place': ('Средняя школа (гимназия)',
              'Детское Дошкольное Учреждение',
              'Колледж (техникум)',
              'На кружки и секции',
              'В стационар',
              'По месту требования'),

    'type': ('По выздоровлении',
             'Годовой медосмотр',
             'На кружки и секции',
             'ЦКРОиР',
             'Оформление в ДДУ / СШ / ВУЗ',
             'Об отсутствии контактов',
             'В детский лагерь',
             'О нуждаемости в сан-кур лечении',
             "Может работать по специальности...",
             'Об усыновлении (удочерении)',
             "Бесплатное питание",
             "Об обслуживании в поликлинике"),

    "all_info": {

        "По выздоровлении": {
            "additional_medical_information": "| Осмотрен на чесотку, педикулез, микроспорию |",
            "recommendation": "Освобождение от занятий физкультурой и плаванием \nв бассейне на семь дней",
            "validity_period": "5 дней"},

        "Годовой медосмотр": {
            "additional_medical_information": "Рост _____ см; Вес _____ кг; Vis OD/OS = __________; АД ________\n"
                                              "| Осмотрен на чесотку, педикулез, микроспорию |",
            "diagnosis": "Группа здоровья: _ ; Группа по физкультуре: _ ;",
            "recommendation": "Режим _; Стол _;",
            "date_of_issue": "now"},

        "На кружки и секции": {
            "place_of_requirement": "Для занятия ",
            "diagnosis": "Не имеется медицинских противопоказаний, "
                         "включенных в перечень медицинских противопоказаний для занятия ",
            "date_of_issue": "now",
            "validity_period": "1 год"},

        "Бесплатное питание": {
            "place_of_requirement": "Управление социальной защиты Первомайского района",
            "additional_medical_information": "Ребенок находится на искусственном вскармливании. "
                                              "Получает питание по возрасту",
            "diagnosis": "Соматически здоров",
            "recommendation": "Рекомендован рацион питания ребенку в соответствии с возрастом и примерным месячным "
                              "набором продуктов питания согласно приложения №1 к постановлению Министерства труда "
                              "и социальной защиты РБ и МЗРБ от 13.03.2012 № 37/20",
            "date_of_issue": "now",
            "validity_period": "6 месяцев"},

        "ЦКРОиР": {
            "place_of_requirement": "Для логопедической комиссии (ЦКРОиР)",
            "additional_medical_information": "Ребенок от _____ беременности, _____ родов. \n"
                                              "Течение беременности: без особенностей\n"
                                              "При рождении: вес ________ гр, рост _______ см, Апгар _______ \n"
                                              "К году: зубов ______ , рост ______ см, вес _______ гр\n"
                                              "Держать голову в ______ мес, ползать ______ мес, сидеть ______ мес,\n"
                                              " стоять ____ мес,  ходить _____ мес, говорить _____ мес, "
                                              "первый зуб _____ мес\n"
                                              "Невролог – ____________________________________________________ \n"
                                              "Окулист – _____________________________________________________ \n"
                                              "ЛОР – _________________________________________________________ \n"
                                              "Логопед – _____________________________________________________ ",
            "diagnosis": f"{'_' * 55}",
            "date_of_issue": "now",
            "validity_period": "1 год"},

        "Оформление в ДДУ / СШ / ВУЗ": {
            "additional_medical_information": "Рост _____ см; Вес _____ кг; Vis OD/OS = __________; АД ________\n"
                                              "| Осмотрен на чесотку, педикулез, микроспорию |\n"
                                              "Данные о профилактических прививках прилагаются",
            "diagnosis": f"Группа здоровья: _ ; Группа по физкультуре: _ ;",
            "recommendation": "Режим _; Стол _;",
            "date_of_issue": "now",
            "validity_period": "1 год"},

        "Об отсутствии контактов": {
            "additional_medical_information": "В контакте с инфекционными больными в течение 35 дней не был\n"
                                              "| Осмотрен на чесотку, педикулез, микроспорию |",
            "diagnosis": "На момент осмотра соматически здоров",
            "recommendation": "Может находиться в детском коллективе",
            "date_of_issue": "now",
            "validity_period": "5 дней"},

        "О нуждаемости в сан-кур лечении": {
            "place_of_requirement": "О нуждаемости в санаторно-курортном лечении",
            "date_of_issue": "now",
            "validity_period": "1 год"},

        "В детский лагерь": {
            "place_of_requirement": "В лагерь",
            "additional_medical_information": "Рост _____ см; Вес _____ кг; АД ________\n"
                                              "| Осмотрен на чесотку, педикулез, микроспорию |\n"
                                              "В контакте с инфекционными больными в течение 35 дней не был\n"
                                              "Данные о профилактических прививках прилагаются",
            "diagnosis": f"diagnosis\nГруппа здоровья: _ ; Группа по физкультуре: _ ;\n"
                         "На момент осмотра соматически здоров",
            "recommendation": "Режим _; Стол _;",
            "date_of_issue": "now",
            "validity_period": "5 дней"},

        "Может работать по специальности...": {
            "place_of_requirement": "Проведение обязательного предварительного / внеочередного медицинского осмотра",
            "diagnosis": "Годен к работе по специальности: ",
            "date_of_issue": "now",
            "validity_period": "До следующего обязательного периодического медицинского осмотра"},

        "Об обслуживании в поликлинике": {
            "place_of_requirement": "По месту требования",
            "diagnosis": "Ребенок обслуживается в УЗ '19-я городская детская поликлиника с ___________'",
            "date_of_issue": "now",
            "validity_period": "1 год"},

        "Об усыновлении (удочерении)": {
            "place_of_requirement": "По месту требования",
            "past_illnesses": "При рождении: Рост ______ см; Вес ______ кг; Апгар ________ ; \n"
                              "Семейно-генеалогический анамнез: (отягощен / не отягощен / нет данных)\n",
            "additional_medical_information": "Рост _____ см; Вес _____ кг;\n"
                                              "Осмотры специалистов:\n"
                                              f"Педиатр: дата {'_' * 10} д/з: _________________________________\n"
                                              f"хирург: дата {'_' * 10} д/з: __________________________________\n"
                                              f"офтальмолог: дата {'_' * 10} д/з: _____________________________\n"
                                              f"оториноларинголог: дата {'_' * 10} д/з: _______________________\n"
                                              f"стоматолог: дата {'_' * 10} д/з: ______________________________\n"
                                              f"невролог: дата {'_' * 10} д/з: ________________________________\n"
                                              f"психиатр-нарколог: дата {'_' * 10} д/з: _______________________\n"
                                              f"логопед: дата {'_' * 10} д/з: _________________________________\n"
                                              f"Лабораторные анализы:\n"
                                              f"общий анализ крови: дата {'_' * 10} закл-е: __________________\n"
                                              f"общий анализ мочи: дата {'_' * 10} закл-е: ____________________\n"
                                              f"анализ крови на ВИЧ: дата {'_' * 10} закл-е: __________________\n"
                                              f"Hbs-Ag: дата {'_' * 10} закл-е: _______________________________\n"
                                              f"RW: дата {'_' * 10} закл-е: ___________________________________\n"
                                              "Данные о профилактических прививках прилагаются",
            "diagnosis": f"diagnosis\n"
                         f"Физическое развитие (выше- ниже-) среднее, (дис-) гармоничное\n"
                         f"НПР - соответствует возрасту",
            "date_of_issue": "now",
            "validity_period": "1 год"
        }
    }}

all_blanks_anal = {
    'blood': ['Общие анализы крови:',
              'ОАК',
              'ОАК + ФОРМУЛА',
              'ОАК + СВЕРТЫВАЕМОСТЬ',
              "АЛЛЕРГОПАНЕЛЬ",
              "ИММУНОГРАММА",
              'ГЛЮКОЗА',
              'ГЛЮКОЗА ПОД НАГРУЗКОЙ'],
    'blood-inf': ['Анализы крови на инфекции:',
                  'КРОВЬ на инфекции',
                  'ВИЧ',
                  'ГЕПАТИТ',
                  'СИФИЛИС',
                  'ВИЧ экспресс',
                  'ГЕПАТИТ контакты'
                  ],
    'urine': ['Анализы мочи:',
              'ОАМ',
              'НЕЧИПОРЕНКО',
              'ЗИМНИЦКИЙ'],
    'copro': ['Копрограммы:',
              'КОПРОГРАММА',
              'СКРЫТАЯ КРОВЬ',
              'ГЛИСТЫ',
              "ДИСБАКТЕРИОЗ",
              "КАЛЬПРОТЕКТИН"],
    'swab': ['Мазки:',
             'ЭОЗИНОФИЛЫ',
             'МАЗОК НА ФЛОРУ',
             'МАЗОК НА КОВИД'
             ],
    'add': ['Сочетания анализов:',
            'ОАК + ОАМ',
            'ОАК + ОАМ + ГЛЮКОЗА',
            'ОАК + ОАМ + КОПРОГРАММА',
            'ОАК + ОАМ + ЭОЗИНОФИЛЫ',
            'ОАК + ОАМ + ГЛИСТЫ',
            'ОАК + ОАМ + ГЛИСТЫ + ГЛЮКОЗА'
            ]

}

blanks = ('Диспансеризация',
          "Информирование_законного_представителя",
          "Тест_аутизма_у_детей",
          "Анкета_по_слуху",
          "Анкета_ПАВ")

all_blanks_direction = {
    'hospital': (' - - - РНПЦ: - - - ',
                 'РНПЦ ДХ',
                 'РНПЦ НиН',
                 'РНПЦ Мать и дитя',
                 'РНПЦ ТиО',
                 'РНПЦ ЛОР',
                 ' - - - Стационары: - - - ',
                 '1-я ГКБ',
                 '2-я ГДКБ',
                 '3-я ГДКБ',
                 '3-я ГКБ',
                 '4-я ГДКБ',
                 '6-я ГКБ',
                 'ДИКБ',
                 'МГЦМР',
                 'ГККВД',
                 ' - - - Поликлиники: - - - ',
                 '19-я ГДП',
                 '1-я ГДП',
                 '8-я ГП',
                 '11-я ГДП',
                 '17-я ГДП'
                 ),

    'doctor': ('Аллерголога',
               'Гастроэнтеролога',
               'Гематолога',
               'Генетика',
               'Гемангиолога',
               'Гинеколога',
               "Дерматолога",
               'Кардиохирурга',
               'Кардиолога',
               'Невролога',
               'Нейрохирурга',
               'Нефролога',
               'Ортопеда',
               'Оториноларинголога',
               'Офтальмолога',
               'Педиатра',
               'Реабилитолога'
               'Травматолога',
               'Уролога',
               'Хирурга'
               )

}

address_hospital = {'РНПЦ ДХ': 'пр. Независимости 64',
                    'РНПЦ НиН': 'ул. Франциска Скорины 24',
                    'РНПЦ Мать и дитя': 'ул. Орловская, 66',
                    'РНПЦ ТиО': 'ул. Кижеватова 60/4',
                    'РНПЦ ЛОР': 'ул. Сухая 8',
                    '1-я ГКБ': 'пр. Независимости 64',
                    '2-я ГДКБ': 'ул. Нарочанская 17',
                    '3-я ГДКБ': 'улица Кижеватова 60/1',
                    '4-я ГДКБ': 'улица Шишкина 24',
                    '6-я ГКБ': 'Уральская улица 5',
                    'ДИКБ': 'улица Якубовского 53',
                    '19-я ГДП': 'пр. Независимости 119',
                    '1-я ГДП': 'ул. Золотая горка 17',
                    '8-я ГП': 'ул. Никифорова 3',
                    '11-я ГДП': 'ул. Никифорова 5',
                    'МГЦМР': 'ул. Володарского 1',
                    "17-я ГДП": "ул. Кольцова, 53/1",
                    "ГККВД": "ул. Смолячкова, 1"}

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
                        'Носовое дыхание': ['затруднено', 'из носа -', 'слизистое отделяемое'],
                        'Периферические лимфоузлы': ['увеличены', 'шейные', 'подчелюстные', "эластичные",
                                                     "безболезненные", "при пальпации"],
                        'Легкие': ["ЧД", "дыхание -", 'везикулярное', "проводится во все отделы", "хрипов нет"],
                        'Сердце': ["ЧСС", 'тоны сердца', 'ясные', 'ритмичные', "границы в пределах возрастной нормы"],
                        'Живот': ['мягкий', 'безболезненный', "доступен глубокой пальпации",
                                  "Печень у края реберной дуги", "селезенка не пальпируется"],
                        'Мочеиспускание': ['регулярное', 'безболезненное'],
                        'Стул': ['оформленный', 'коричневый', 'без патологических примесей'],
                        'Дополнительно': ['Менингеальные симптомы', "отрицательные"]},
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
                        'Легкие': ["ЧД", "дыхание -", 'везикулярное', "проводится во все отделы", "хрипов нет"],
                        'Сердце': ["ЧСС", 'тоны сердца', 'ясные', 'ритмичные', "границы в пределах возрастной нормы"],
                        'Живот': ['мягкий', 'болезненный -', "в эпигастральной обл", "доступен глубокой пальпации",
                                  "Печень у края реберной дуги", "селезенка не пальпируется"],
                        'Мочеиспускание': ['регулярное', 'безболезненное'],
                        'Дополнительно': ['Аппендикулярные симптомы', "Перитониальные симптомы", "Пузырные симптомы",
                                          "отрицательные"]},
        "prescription": {"Рекомендации": ["домашний режим", "Парацетамол", "Ибупрофен", "питьевой режим",
                                          "диета", "Смекта", "Пробиотик"]}
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
                        'Легкие': ["ЧД", "дыхание -", 'везикулярное', "проводится во все отделы", "хрипов нет"],
                        'Сердце': ["ЧСС", 'тоны сердца', 'ясные', 'ритмичные', "границы в пределах возрастной нормы"],
                        'Живот': ['мягкий', 'безболезненный', "доступен глубокой пальпации",
                                  "Печень у края реберной дуги", "селезенка не пальпируется"],
                        'Мочеиспускание': ['регулярное', 'безболезненное'],
                        'Стул': ['оформленный', 'коричневый', 'без патологических примесей'],
                        'Дополнительно': ['Менингеальные симптомы', "отрицательные"]},
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
                        'Легкие': ["ЧД", "дыхание -", 'везикулярное', "проводится во все отделы", "хрипов нет"],
                        'Сердце': ["ЧСС", 'тоны сердца', 'ясные', 'ритмичные', "границы в пределах возрастной нормы"],
                        'Живот': ['мягкий', 'безболезненный', "доступен глубокой пальпации",
                                  "Печень у края реберной дуги", "селезенка не пальпируется"],
                        'Мочеиспускание': ['регулярное', 'безболезненное'],
                        'Стул': ['оформленный', 'коричневый', 'без патологических примесей']},
        "prescription": {"Рекомендации": []}
    },

}

all_data_diagnosis = {
    'diagnosis_ori': ('ринит', "синусит", "отит", "вирусная экзантема",
                      'фарингит', 'ринофaрингит', "ларингит", "тонзиллит",
                      'трахеит', 'бронхит', 'пневмония',
                      "кишечный с-м", "абдоминальный с-м",
                      "продолжает болеть", "улучшение", 'реконвалесцент'),
    'diagnosis_ФРК': ("продолжает болеть", "улучшение", 'реконвалесцент'),
    'diagnosis_Ветрянка': ("продолжает болеть", "улучшение", 'реконвалесцент'),
    'diagnosis_Здоров': ("соматически здоров", 'реконвалесцент', "ОРИ", "ФРК", "Ветряной оспы"),

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
                     "на лице", "на шее", "на туловище", "на руках", "на кистях", "на стопах", "на ногах",
                     "в паховой области", "в складках кожи", "по всему телу"),
                    ("Слизистая глотки", "без изменений", "гиперемирована", "зернистая"),
                    ("Нёбные миндалины", "без изменений", "увеличены", "1ст.", "2ст.", "3ст.",
                     "налетов нет", "обложены налетом", "белого цвета", "серого цвета"),
                    ("Носовое дыхание", "свободное", "затруднено", "из носа -",
                     "слизистое отделяемое", "гнойное отделяемое"),
                    ("Периферические лимфоузлы", "не увеличены", "увеличены", "подчелюстные", "шейные", "надключичные",
                     "подмышечные", "паховые", "справа", "слева", "с обеих сторон", "плотные", "эластичные",
                     "болезненные", "безболезненные", "при пальпации"),
                    ("Легкие", "ЧД", "дыхание -", "везикулярное", "пуэрильное", "жесткое", "ослабленное",
                     "проводится во все отделы", "хрипов нет",
                     "хрипы -", "сухие", "влажные", "проводные", "свистящие"),
                    ("Сердце", "ЧСС", "тоны сердца -", "ясные", "приглушены", "ритмичные",
                     "границы в пределах возрастной нормы", "систолический шум"),
                    ("Живот", "мягкий", "безболезненный", "доступен глубокой пальпации", "твердый", "болезненный -",
                     "в эпигастральной обл", "в мезогастральной обл", "в гипогастральной обл", "справа", "слева",
                     "Печень у края реберной дуги", "селезенка не пальпируется"),
                    ("Мочеиспускание", "регулярное", "безболезненное", "диурез снижен", "боль при мочеиспускании"),
                    ("Стул", "оформленный", "послабленный", "разжиженный", "кашицеобразный",
                     "коричневый", "зеленый", "обесцвеченный", "желтый", "без патологических примесей",
                     "с кровью", "с слизью", "регулярный", "частый", "редкий"),
                    ("Отоскопия", "не проводилась", "без патологии", "справа -", "слева -", "с обеих сторон -",
                     "серная пробка", "отит", "катаральный", "гнойный", "экссудативный", "наружный диффузный"),
                    ("Дополнительно", "Менингеальные симптомы", "Аппендикулярные симптомы",
                     "Перитониальные симптомы", "Пузырные симптомы",
                     "отрицательные", "положительные", "сомнительные")),
    "prescription": ("Назначения", ("Анализы", "ОАК", "ОАМ", "Глюкоза", "Копрограмма", "я/глист"),
                     ("Рекомендации", "домашний режим", "Парацетамол", "Ибупрофен", "питьевой режим",
                      "полоскать горло", "орошать горло", "промывать нос",
                      "диета", "Смекта", "Пробиотик", "АЦЦ"),

                     ("Антибиотик Амоксициллин",
                      "Форма", "сусп. 125/5", "сусп. 250/5", "таб. 250", "таб. 500", "таб. 1000",
                      "Дозировка", "50 мг/кг/сут", "75 мг/кг/сут", "90 мг/кг/сут",
                      "Кратность", "1 р/сут", "2 р/сут", "3 р/сут"),

                     ("Антибиотик Амоксициллин + клавулановая кислота",
                      "Форма", "сусп. 125/31.25/5", "сусп. 200/28.5/5",
                      "сусп. 250/62.5/5", "сусп. 400/57/5", "сусп. 600/42.9/5",
                      "таб. 250/125", "таб. 500/125", "таб. 875/125",
                      "Дозировка", "50 мг/кг/сут", "75 мг/кг/сут", "90 мг/кг/сут",
                      "Кратность", "1 р/сут", "2 р/сут", "3 р/сут"),

                     ("Антибиотик Цефуроксим",
                      "Форма", "сусп. 125/5", "таб. 125", "таб. 250", "таб. 500",
                      "Дозировка", "20 мг/кг/сут", "30 мг/кг/сут",
                      "Кратность", "1 р/сут", "2 р/сут", "3 р/сут"),

                     ("Антибиотик Кларитромицин",
                      "Форма", "сусп. 125/5", "сусп. 250/5", "таб. 250", "таб. 500",
                      "Дозировка", "15 мг/кг/сут",
                      "Кратность", "1 р/сут", "2 р/сут", "3 р/сут"),

                     ("Антибиотик Азитромицин",
                      "Форма", "сусп. 200/5", "таб. 125", "таб. 250", "таб. 500",
                      "Дозировка", "10 мг/кг/сут",
                      "Кратность", "1 р/сут", "2 р/сут", "3 р/сут")
                     )
}

render_data = dict()

data = dict()

patient = {
    'name': '',
    'birth_date': '',
    'gender': '',
    'amb_cart': '',
    'patient_district': '',
    'address': ''
}

user = {'text_size': 10,
        'doctor_name': '',
        'manager': '',
        'ped_div': '',
        'doctor_district': ''}


class ScrolledRoot(tk.Toplevel):
    def __init__(self, marker=None, func=None):
        super().__init__()
        self.scroll_x = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL, width=user.get('text_size', 10) * 3)

        self.canvas = tk.Canvas(self, height=self.winfo_screenheight() - 100,
                                xscrollcommand=self.scroll_x.set,
                                yscrollcommand=self.scroll_y.set)
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)

        self.bind("<Control-KeyPress>", keypress)

        self.canvas_frame = Frame(self.canvas, borderwidth=1)
        if marker == 'paste_examination_cmd_main':
            paste_examination_cmd_main(self, self.canvas_frame)
        if marker == 'past_examination':
            func(self.canvas_frame)
        if marker == 'delete_diagnosis_root':
            func(self.canvas_frame)

        self.canvas_frame.columnconfigure(index='all', minsize=40, weight=1)
        self.canvas_frame.rowconfigure(index='all', minsize=20)

        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        self.canvas.grid(row=0, column=0, sticky="nswe")
        self.scroll_x.grid(row=1, column=0, sticky="we")
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        self.canvas['width'] = int(self.canvas_frame.winfo_geometry().split('x')[0])
        self.canvas.bind("<Enter>", self.on_binds)
        self.canvas.bind("<Leave>", self.off_binds)

    def resize(self, event):
        region = self.canvas.bbox(tk.ALL)
        self.canvas.configure(scrollregion=region)
        self.minsize(width=int(self.canvas_frame.winfo_width()), height=self.canvas.winfo_screenheight() - 100)

        self.canvas['width'] = int(self.canvas_frame.winfo_width())

    def on_binds(self, event):
        self.idbind = self.bind_all("<MouseWheel>", self.on_mousewheel)

    def off_binds(self, event=None):
        self.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        if os.name == 'posix':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def paste_examination_cmd_main(root_examination: Toplevel, examination_root: Frame):
    destroy_elements = dict()
    data['examination'] = dict()
    data['examination']['all_kb_status'] = 'open'

    selected_place = StringVar()
    selected_diagnosis = StringVar()
    selected_type_ln = StringVar()
    err_msd_weight = StringVar()
    selected_examination_frame = StringVar()
    selected_prescription_frame = StringVar()
    age = get_age(patient.get('birth_date'))

    def paste_past_examination():
        def past_examination(past_examination_frame: Frame):
            def selected_past_but():
                selected_past_but_info = ''
                for but_info in past_examination_data.get('buttons'):
                    if past_examination_data['buttons'].get(but_info).get() == 1:
                        selected_past_but_info = but_info
                        past_examination_data['buttons'][but_info].set(0)
                if selected_past_but_info:
                    rowid_, command = selected_past_but_info.split('__')
                    if command == 'Удалить осмотр':
                        try:
                            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                                cursor = connect.cursor()
                                cursor.execute(f"DELETE FROM examination WHERE rowid LIKE '{rowid_}'")
                        except Exception as ex:
                            messagebox.showerror('Ошибка', f"Ошибка удаления записи: \n{ex}")
                        else:
                            past_examination_data['destroy_elements'].get(rowid_).destroy()

                    if command == 'Загрузить в текущий':
                        for but_marker in ('complaints', 'examination', 'prescription'):
                            for mark_ in data['examination'].get(f'{but_marker}_but'):
                                data['examination'][f'{but_marker}_but'].get(mark_).set(0)

                        for selected_marker in past_examination_data['found_info'].get(rowid_).split('__<end!>__\n'):
                            if 'selected_diagnosis_get:____' in selected_marker:
                                selected_diagnosis.set(selected_marker.split(':____')[-1])
                            else:
                                for but_marker in ('complaints', 'examination', 'prescription', 'diagnosis', 'weight'):
                                    if f"{but_marker}:____" in selected_marker:
                                        all_buttons = selected_marker.replace(f"{but_marker}:____", '').split("__")
                                        for button in all_buttons:
                                            if button in data['examination'].get(f'{but_marker}_but'):
                                                data['examination'][f'{but_marker}_but'].get(button).set(1)

                                    elif f"{but_marker}_text:____" in selected_marker:
                                        text_inserted = selected_marker.replace(f"{but_marker}_text:____", '')

                                        if but_marker == 'complaints':
                                            txt_complaints.delete(1.0, 'end')
                                            txt_complaints.insert(1.0, text_inserted)
                                        if but_marker == 'examination':
                                            txt_examination.delete(1.0, 'end')
                                            txt_examination.insert(1.0, text_inserted)
                                        if but_marker == 'diagnosis':
                                            txt_diagnosis.delete(1.0, 'end')
                                            txt_diagnosis.insert(1.0, text_inserted)
                                        if but_marker == 'prescription':
                                            txt_prescription.delete(1.0, 'end')
                                            txt_prescription.insert(1.0, text_inserted)
                                        if but_marker == 'weight':
                                            txt_weight.delete(0, 'end')
                                            txt_weight.insert(0, text_inserted)

                        past_examination_root.destroy()
                        examination_root.update()
                        edit_examination_kb_text()

            past_examination_data = dict()
            past_examination_data['buttons'] = dict()
            past_examination_data['found_info'] = dict()
            past_examination_data['destroy_elements'] = dict()

            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                cur = conn.cursor()

                cur.execute(f"SELECT rowid, date_time, doctor_name, LN_type, patient_info, "
                            f"examination_text, examination_key "
                            f"FROM examination "
                            f"WHERE patient_info LIKE "
                            f"'{patient.get('name')}__{patient.get('birth_date')}'")

                found_info = cur.fetchall()
            if not found_info:
                Label(master=past_examination_frame, text="История о прошлых осмотрах пациента пуста",
                      font=('Comic Sans MS', user.get('text_size')), bg='white').pack(fill='both', expand=True)
            else:
                found_info = sorted(found_info,
                                    key=lambda i: (datetime.now() -
                                                   datetime.strptime(f"{i[1]}", "%d.%m.%Y %H:%M")).seconds)

                for info in found_info:
                    local_frame = Frame(past_examination_frame, borderwidth=1, relief="solid", padx=3, pady=3)
                    rowid, date_time, doctor_name, ln_type, patient_info_, examination_text, examination_key = info

                    past_examination_data['destroy_elements'][f"{rowid}"] = local_frame

                    past_examination_data['found_info'][f"{rowid}"] = examination_key
                    past_exam_text = f"Время редактирования: {date_time}\n"
                    counter = 0
                    for text in examination_text.split(" "):
                        counter += len(text)
                        if '\n' in text:
                            counter = 0
                        if counter >= 100:
                            past_exam_text += '\n'
                            counter = 0

                        past_exam_text += text + ' '
                    past_exam_text += f"\nЛН: {ln_type}\nВрач: {doctor_name}".replace('_', ' ')
                    Label(master=local_frame, width=100,
                          text=past_exam_text,
                          justify='left',
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').pack(fill='both', expand=True, side="top")

                    for mark in ('Удалить осмотр', 'Загрузить в текущий'):
                        past_examination_data['buttons'][f"{rowid}__{mark}"] = IntVar()

                        Checkbutton(local_frame, text=mark,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    onvalue=1, offvalue=0,
                                    variable=past_examination_data['buttons'].get(f"{rowid}__{mark}"),
                                    command=selected_past_but,
                                    indicatoron=False,
                                    selectcolor='#77f1ff').pack(fill='both', expand=True, side="left")

                    local_frame.columnconfigure(index='all', minsize=40, weight=1)
                    local_frame.rowconfigure(index='all', minsize=20)
                    local_frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

        past_examination_root = ScrolledRoot(marker='past_examination', func=past_examination)
        past_examination_root.title(f"Осмотры пациента "
                                    f"{patient.get('name').split()[0]} "
                                    f"{patient.get('name').split()[1]} "
                                    f"{patient.get('birth_date')}")
        past_examination_root.geometry('+0+0')
        past_examination_root.mainloop()

    def change_all_kb_status():

        if data['examination'].get('all_kb_status') == 'open':
            for marker in ('complaints', 'examination', 'prescription'):
                if data['examination'].get(f'open_{marker}_kb') != 'closed':
                    if marker == 'complaints':
                        change_complaints_kb_status()
                    elif marker == 'examination':
                        change_examination_kb_status()
                    elif marker == 'prescription':
                        change_prescription_kb_status()
            data['examination']['all_kb_status'] = 'closed'
            button_change_all_kb_status['text'] = 'Открыть\nвсе\nклавиатуры'

        elif data['examination'].get('all_kb_status') == 'closed':
            for marker in ('complaints', 'examination', 'prescription'):
                if not data['examination'].get(f'open_{marker}_kb') == 'open':
                    if marker == 'complaints':
                        change_complaints_kb_status()
                    elif marker == 'examination':
                        change_examination_kb_status()
                    elif marker == 'prescription':
                        change_prescription_kb_status()
            data['examination']['all_kb_status'] = 'open'
            button_change_all_kb_status['text'] = 'Скрыть\nвсе\nклавиатуры'

        root_examination.update()

    def create_examination_doc(doc_size):

        type_ln = selected_type_ln.get()
        if type_ln in ('Лист ВН', 'Справка ВН') and not txt_ln_num.get():
            messagebox.showerror('Ошибка!', 'Не указан номер документа ВН!')
            txt_ln_num.focus()
        elif not selected_place.get():
            messagebox.showerror('Ошибка!', 'Не указано место осмотра!')
            frame_1.focus()
        else:
            render_data.clear()

            date_time_str = txt_date_time.get().strip()
            if date_time_str:
                render_data['date_time'] = f"Дата осмотра: {date_time_str}\n"
            else:
                render_data['date_time'] = ""

            render_data['patient_info'] = f"ФИО: {patient.get('name')}\t" \
                                          f"дата рождения: {patient.get('birth_date')}\t" \
                                          f"{patient.get('patient_district')}-й уч\n" \
                                          f"Место осмотра: {selected_place.get()}"
            if selected_place.get() == 'в поликлинике':
                render_data['patient_info'] = f"{render_data.get('patient_info')}\tна приеме с {combo_company.get()}"
            render_data['complaints'] = f"{txt_complaints.get(1.0, 'end').strip()}"
            render_data['examination'] = f" {txt_examination.get(1.0, 'end').strip()}"
            render_data['diagnosis'] = f"{txt_diagnosis.get(1.0, 'end').strip()}"
            render_data['prescription'] = f"{txt_prescription.get(1.0, 'end').strip()}"

            add_info = ''
            if type_ln == 'Уход обеспечен':
                add_info += "Уход обеспечен\n"
            elif type_ln in ('Лист ВН', 'Справка ВН'):
                if data['examination'].get('ln_closed'):
                    if type_ln == 'Лист ВН':
                        add_info += f"{type_ln} № {txt_ln_num.get()} закрыт к труду\n"
                    else:
                        add_info += f"{type_ln} № {txt_ln_num.get()} закрыта к труду\n"
                else:
                    add_info += f"{type_ln} № {txt_ln_num.get()} c {txt_ln_from.get()} по {txt_ln_until.get()}\n"
            if txt_second_examination.get():
                add_info += f"Повторный осмотр: {txt_second_examination.get()}\n"
            add_info += f"Врач-педиатр: {user.get('doctor_name')}"
            render_data['add_info'] = add_info

            active_but = ""
            if selected_diagnosis.get():
                active_but += f"selected_diagnosis_get:____{selected_diagnosis.get()}__<end!>__\n"
            for mark in ('complaints', 'examination', 'prescription'):
                active_but += f'{mark}:__'
                for but in data['examination'].get(f'{mark}_but'):
                    if data['examination'][f'{mark}_but'].get(but).get() == 1:
                        active_but += f'__{but}'
                active_but += '__<end!>__\n'

            active_but = f"{active_but}" \
                         f"complaints_text:____{render_data.get('complaints')}__<end!>__\n" \
                         f"examination_text:____{render_data.get('examination')}__<end!>__\n" \
                         f"diagnosis_text:____{render_data.get('diagnosis')}__<end!>__\n" \
                         f"prescription_text:____{render_data.get('prescription')}__<end!>__\n"
            if txt_weight.get():
                render_data['examination'] = f"Вес: {txt_weight.get()} кг. {render_data.get('examination')}"
                active_but = f"{active_but}" \
                             f"weight_text:____{float(txt_weight.get().replace(',', '.'))}__<end!>__\n"

            active_examination = f"{render_data.get('date_time')}{render_data.get('patient_info')}\n" \
                                 f"Жалобы: {render_data.get('complaints')}\n" \
                                 f"Осмотр: {render_data.get('examination')}\n" \
                                 f"Диагноз: {render_data.get('diagnosis')}\n" \
                                 f"Лечение: {render_data.get('prescription')}\n"

            if type_ln in ('Лист ВН', 'Справка ВН'):
                num_ln = ''
                for word in txt_ln_num.get().strip():
                    if not word.isdigit():
                        num_ln += word
                num_ln += '_'
                for word in txt_ln_num.get().strip():
                    if word.isdigit():
                        num_ln += word
                if data['examination'].get('ln_closed'):
                    ln_data = f"{type_ln}__{num_ln}__closed"
                else:
                    ln_data = f"{type_ln}__{num_ln}__{txt_ln_from.get().strip()}__{txt_ln_until.get().strip()}"
            else:
                ln_data = type_ln

            save_info_examination = [
                f"{datetime.now().strftime('%d.%m.%Y %H:%M')}",
                f"{user.get('doctor_name')}",
                None,
                ln_data,
                f"{patient.get('name')}__{patient.get('birth_date')}",
                active_examination,
                active_but,
                None]

            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO examination VALUES(?, ?, ?, ?, ?, ?, ?, ?)", save_info_examination)

            doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}осмотр_педиатра_{doc_size}.docx")
            doc.render(render_data)
            doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]}_осмотр.docx"
            doc_name = save_document(doc=doc, doc_name=doc_name)

            os.system(f"start {doc_name}")
            render_data.clear()
            data.clear()
            root_examination.destroy()

    def paste_hr_br():
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
        label_diagnosis = Label(master=frame_diagnosis, text=f"{all_data_diagnosis.get('diagnosis')[0]}",
                                font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_diagnosis.pack(fill='both', expand=True)
        frame_diagnosis_1 = Frame(frame_diagnosis, borderwidth=1)

        def select_diagnosis():
            data['examination']['diagnosis'] = selected_diagnosis.get()

            for mark_ in data['examination'].get('complaints_but'):
                data['examination']['complaints_but'].get(mark_).set(0)
            for mark_ in data['examination'].get('examination_but'):
                data['examination']['examination_but'].get(mark_).set(0)
            for mark_ in data['examination'].get('prescription_but'):
                data['examination']['prescription_but'].get(mark_).set(0)

            for complaints_but in all_diagnosis.get(selected_diagnosis.get()).get("complaints"):
                complaints_list = all_diagnosis.get(selected_diagnosis.get()).get("complaints").get(
                    complaints_but)
                if isinstance(complaints_list, list):
                    for complaints in complaints_list:
                        if f"{complaints_but}_{complaints}" in data['examination'].get('complaints_but'):
                            data['examination']['complaints_but'][f"{complaints_but}_{complaints}"].set(1)
                else:
                    if complaints_but in data['examination'].get('complaints_but'):
                        data['examination']['complaints_but'][complaints_but].set(1)

            select_complaints()

            for examination_but in all_diagnosis.get(selected_diagnosis.get()).get("examination"):
                examination_list = all_diagnosis.get(selected_diagnosis.get()).get("examination").get(
                    examination_but)
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

            txt_diagnosis.delete(1.0, 'end')
            txt_diagnosis.insert(1.0, f'Диагноз: {selected_diagnosis.get()} ')

            select_prescription()
            paste_diagnosis_kb()
            edit_examination_kb_text()
            if not data['examination'].get('all_kb_status'):
                change_all_kb_status()
            else:
                root_examination.update()

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
        frame_diagnosis.pack(fill='both', expand=True, side=tk.LEFT)

    def paste_frame_date_time():
        label_date_time = Label(master=frame_date_time, text="Дата и время осмотра:",
                                font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_date_time.pack(fill='both', expand=True)
        txt_date_time.pack(fill='both', expand=True)
        txt_date_time.insert(0, datetime.now().strftime("%d.%m.%Y %H:%M"))

        frame_date_time.columnconfigure(index='all', minsize=40, weight=1)
        frame_date_time.rowconfigure(index='all', minsize=20)
        frame_date_time.pack(fill='both', expand=True, side=tk.LEFT)

    def paste_frame_button_create():
        def create_examination_doc_a5():
            create_examination_doc('а5')

        def create_examination_doc_a6():
            create_examination_doc('а6')

        button_change_all_kb_status.grid(column=0, row=0, rowspan=2)

        Button(frame_button, text='Загрузить\nпрошлые\nосмотры',
               command=paste_past_examination,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=1, row=0, rowspan=2)

        Button(frame_button, text='Создать документ А5',
               command=create_examination_doc_a5,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=2, row=0, columnspan=2)

        Button(frame_button, text='Создать документ А6',
               command=create_examination_doc_a6,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=2, row=1, columnspan=2)

        frame_button.columnconfigure(index='all', minsize=40, weight=1)
        frame_button.rowconfigure(index='all', minsize=20)
        frame_button.pack(fill='both', expand=True, side=tk.LEFT)

    def my_saved_diagnosis():

        def delete_my_diagnosis():

            def get_found_diagnosis():
                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute(f"SELECT rowid, diagnosis, examination_key "
                                   f"FROM my_saved_diagnosis "
                                   f"WHERE doctor_name LIKE '{user.get('doctor_name')}' ")
                return cursor.fetchall()

            found_diagnosis = get_found_diagnosis()
            if not found_diagnosis:
                messagebox.showerror('Ошибка!', f'История о сохраненных осмотрах пуста!\n')
                examination_root.focus()

            else:
                def delete_my_diagnosis_root(delete_my_diagnosis_root_main: Frame):
                    def select_delete_diagnosis():
                        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                            cursor = connect.cursor()
                            cursor.execute(f"DELETE FROM my_saved_diagnosis WHERE rowid LIKE "
                                           f"'{selected_delete_diagnosis.get()}'")
                            messagebox.showinfo('Инфо', f'Осмотр успешно удален')
                            delete_my_diagnosis_root_main.focus()

                            destroy_elements['delete_my_diagnosis'][f"{selected_delete_diagnosis.get()}"].destroy()

                    selected_delete_diagnosis = StringVar()
                    destroy_elements['delete_my_diagnosis'] = dict()

                    for rowid, diagnosis_, examination_key_ in found_diagnosis:
                        frame_loc = Frame(delete_my_diagnosis_root_main, borderwidth=1, relief="solid", padx=3, pady=3)
                        destroy_elements['delete_my_diagnosis'][f"{rowid}"] = frame_loc
                        text = f'Имя шаблона: {diagnosis_}\n'
                        for info in examination_key_.split('__<end!>__\n'):
                            if 'complaints_text:____' in info:
                                for i in info.replace('complaints_text:____', 'Жалобы: ').split():
                                    if len(text.split('\n')[-1]) > 90:
                                        text += '\n'
                                    text += f"{i} "
                                text += "\n"
                            if 'examination_text:____' in info:
                                for i in info.replace('examination_text:____', 'Осмотр: ').split():
                                    if len(text.split('\n')[-1]) > 90:
                                        text += '\n'
                                    text += f"{i} "
                                text += "\n"
                            if 'diagnosis_text:____' in info:
                                for i in info.replace('diagnosis_text:____', 'Диагноз: ').split():
                                    if len(text.split('\n')[-1]) > 90:
                                        text += '\n'
                                    text += f"{i} "
                                text += "\n"
                            if 'prescription_text:____' in info:
                                for i in info.replace('prescription_text:____', 'Рекомендации: ').split():
                                    if len(text.split('\n')[-1]) > 90:
                                        text += '\n'
                                    text += f"{i} "
                                text += "\n"

                        Label(master=frame_loc, text=text, justify="left",
                              font=('Comic Sans MS', user.get('text_size')),
                              bg='white').pack(fill='both', expand=True)

                        Radiobutton(master=frame_loc, text=f"Удалить {diagnosis_}",
                                    font=('Comic Sans MS', user.get('text_size')),
                                    value=f"{rowid}", variable=selected_delete_diagnosis,
                                    command=select_delete_diagnosis,
                                    indicatoron=False, selectcolor='#77f1ff').pack(fill='both', expand=True)

                        frame_loc.pack(fill='both', expand=True)

                delete_diagnosis_root = ScrolledRoot(marker='delete_diagnosis_root', func=delete_my_diagnosis_root)
                delete_diagnosis_root.title(f"Удаление моих осмотров")
                delete_diagnosis_root.geometry('+0+0')
                delete_diagnosis_root.mainloop()

        def select_my_saved_diagnosis():
            my_selected_diagnosis = \
                data['examination']['my_saved_diagnosis'].get(selected_diagnosis.get().replace('my__', ''))

            for but_marker in ('complaints', 'examination', 'prescription'):
                for mark_ in data['examination'].get(f'{but_marker}_but'):
                    data['examination'][f'{but_marker}_but'].get(mark_).set(0)

            for selected_marker in my_selected_diagnosis.split('__<end!>__\n'):
                if 'selected_diagnosis_get:____' in selected_marker:
                    selected_diagnosis.set(selected_marker.split(':____')[-1])
                else:
                    for but_marker in ('complaints', 'examination', 'prescription', 'diagnosis'):
                        if f"{but_marker}:____" in selected_marker:
                            all_buttons = selected_marker.replace(f"{but_marker}:____", '').split("__")
                            for button in all_buttons:
                                if button in data['examination'].get(f'{but_marker}_but'):
                                    data['examination'][f'{but_marker}_but'].get(button).set(1)

                        elif f"{but_marker}_text:____" in selected_marker:
                            text_inserted = selected_marker.replace(f"{but_marker}_text:____", '')

                            if but_marker == 'complaints':
                                txt_complaints.delete(1.0, 'end')
                                txt_complaints.insert(1.0, text_inserted)
                            if but_marker == 'examination':
                                txt_examination.delete(1.0, 'end')
                                txt_examination.insert(1.0, text_inserted)
                            if but_marker == 'diagnosis':
                                txt_diagnosis.delete(1.0, 'end')
                                txt_diagnosis.insert(1.0, text_inserted)
                            if but_marker == 'prescription':
                                txt_prescription.delete(1.0, 'end')
                                txt_prescription.insert(1.0, text_inserted)
                edit_examination_kb_text()

        def saved_new_diagnosis():
            def final_save_new_diagnosis():
                try:
                    with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                        cursor = connect.cursor()
                        cursor.execute(f"INSERT INTO my_saved_diagnosis "
                                       f"VALUES('{user.get('doctor_name')}', "
                                       f"'{new_diagnosis_name.get()}', "
                                       f"'{render_text}')")
                except Exception as ex:
                    messagebox.showerror('Ошибка!', f'Ошибка при сохранении!\n'
                                                    f'{ex}')
                else:
                    messagebox.showinfo('Инфо', f'Осмотр успешно сохранен')
                    saved_new_diagnosis_root.destroy()
                    root_examination.destroy()

            if not new_diagnosis_name.get():
                messagebox.showerror('Ошибка!', 'Не указано имя осмотра для сохранения!')
                new_diagnosis_name.focus()
            else:
                saved_new_diagnosis_root = Toplevel()
                saved_new_diagnosis_root.title('Проверка осмотра')
                saved_new_diagnosis_root.config(bg='white')

                text = f"Имя осмотра: {new_diagnosis_name.get()}\n"
                render_text = ''
                if selected_place.get():
                    text += f"Место осмотра: {selected_place.get()}\n"
                    render_text += f"selected_place:____{selected_place.get()}__<end!>__\n"

                for mark in ('complaints', 'examination', 'prescription'):
                    render_text += f'{mark}:__'
                    # text += f"{mark}: ".replace('complaints', 'Жалобы (кнопки)') \
                    #     .replace('examination', 'Осмотр (кнопки)') \
                    #     .replace('prescription', 'Назначения (кнопки)')
                    for but in data['examination'].get(f'{mark}_but'):

                        if data['examination'][f'{mark}_but'].get(but).get() == 1:
                            if len(text.split('\n')[-1]) > 100:
                                text += '\n'
                            render_text += f'__{but}'
                            # text += f"{but} "

                    # text += '\n'
                    render_text += '__<end!>__\n'

                render_text += f"complaints_text:____{txt_complaints.get(1.0, 'end').strip()}__<end!>__\n" \
                               f"examination_text:____{txt_examination.get(1.0, 'end').strip()}__<end!>__\n" \
                               f"diagnosis_text:____{txt_diagnosis.get(1.0, 'end').strip()}__<end!>__\n" \
                               f"prescription_text:____{txt_prescription.get(1.0, 'end').strip()}__<end!>__\n"
                render_text = render_text.replace("'", '').replace("\"", '')
                if txt_complaints.get(1.0, 'end').strip():
                    text += '\nЖалобы: '
                    for word in txt_complaints.get(1.0, 'end').strip().split():
                        if len(text.split('\n')[-1]) > 100:
                            text += '\n'
                        text += word + " "
                if txt_examination.get(1.0, 'end').strip():
                    text += '\nОсмотр: '
                    for word in txt_examination.get(1.0, 'end').strip().split():
                        if len(text.split('\n')[-1]) > 100:
                            text += '\n'
                        text += word + " "
                if txt_diagnosis.get(1.0, 'end').strip():
                    text += '\nДиагноз: '
                    for word in txt_diagnosis.get(1.0, 'end').strip().split():
                        if len(text.split('\n')[-1]) > 100:
                            text += '\n'
                        text += word + " "
                if txt_prescription.get(1.0, 'end').strip():
                    text += '\nНазначения: '
                    for word in txt_prescription.get(1.0, 'end').strip().split():
                        if len(text.split('\n')[-1]) > 100:
                            text += '\n'
                        text += word + " "
                # text += f"Жалобы (текст): {txt_complaints.get(1.0, 'end').strip()}\n" \
                #         f"Осмотр (текст): {txt_examination.get(1.0, 'end').strip()}\n" \
                #         f"Диагноз (текст): {txt_diagnosis.get(1.0, 'end').strip()}\n" \
                #         f"Назначения (текст): {txt_prescription.get(1.0, 'end').strip()}"

                Label(master=saved_new_diagnosis_root, text=text, justify="left",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white').pack(fill='both', expand=True)
                Button(saved_new_diagnosis_root, text='Сохранить',
                       command=final_save_new_diagnosis,
                       font=('Comic Sans MS', user.get('text_size'))).pack(fill='both', expand=True)

                saved_new_diagnosis_root.mainloop()

        def add_frame_new_diagnosis():

            if not data['examination'].get('add_frame_new_diagnosis'):
                data['examination']['add_frame_new_diagnosis'] = 'closed'

            if data['examination'].get('add_frame_new_diagnosis') == "closed":
                data['examination']['add_frame_new_diagnosis'] = 'open'

                frame_new_my_diagnosis.columnconfigure(index='all', minsize=40, weight=1)
                frame_new_my_diagnosis.rowconfigure(index='all', minsize=20)
                frame_new_my_diagnosis.pack(fill='both', expand=True, before=frame_my_saved_diagnosis, side="bottom")

            elif data['examination'].get('add_frame_new_diagnosis') == "open":
                data['examination']['add_frame_new_diagnosis'] = 'closed'

                frame_new_my_diagnosis.pack_forget()

        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT diagnosis, examination_key "
                        f"FROM my_saved_diagnosis "
                        f"WHERE doctor_name LIKE '{user.get('doctor_name')}' ")

            found_info = cur.fetchall()
        col, row = 0, 0
        if not found_info:
            lbl_my_saved_diagnosis['text'] = "История о сохраненных осмотрах пуста"
            lbl_my_saved_diagnosis.grid(column=col, row=row, sticky='ew', columnspan=2)
            col += 2
        else:
            data['examination']['my_saved_diagnosis'] = dict()
            lbl_my_saved_diagnosis['text'] = "Мои осмотры:"
            lbl_my_saved_diagnosis.grid(column=col, row=row, sticky='ew')
            col += 1
            for diagnosis, examination_key in found_info:
                data['examination']['my_saved_diagnosis'][f"{diagnosis}"] = examination_key
                btn = Radiobutton(master=frame_my_saved_diagnosis, text=diagnosis,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=f"my__{diagnosis}", variable=selected_diagnosis,
                                  command=select_my_saved_diagnosis,
                                  indicatoron=False, selectcolor='#77f1ff')
                btn.grid(column=col, row=row, sticky='ew')
                col += 1
                if col == 5:
                    row += 1
                    col = 0
        Button(frame_my_saved_diagnosis, text='Сохранить осмотр в избранное',
               command=add_frame_new_diagnosis,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=col, row=row)
        col += 1
        Button(frame_my_saved_diagnosis, text='Удалить шаблоны',
               command=delete_my_diagnosis,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=col, row=row)

        new_diagnosis_lbl = Label(master=frame_new_my_diagnosis, text="Название осмотра",
                                  font=('Comic Sans MS', user.get('text_size')), bg='white')
        new_diagnosis_lbl.pack(fill='both', expand=True, side='left')

        new_diagnosis_name = Entry(frame_new_my_diagnosis, width=15, font=('Comic Sans MS', user.get('text_size')))
        new_diagnosis_name.pack(fill='both', expand=True, side='left')

        button_saved_new_diagnosis = Button(frame_new_my_diagnosis, text='Сохранить',
                                            command=saved_new_diagnosis,
                                            font=('Comic Sans MS', user.get('text_size')))
        button_saved_new_diagnosis.pack(fill='both', expand=True, side='left')

        button_my_saved_diagnosis.pack(fill='both', expand=True)

        frame_my_saved_diagnosis_but.columnconfigure(index='all', minsize=40, weight=1)
        frame_my_saved_diagnosis_but.rowconfigure(index='all', minsize=20)
        frame_my_saved_diagnosis_but.pack(fill='both', expand=True, side=tk.LEFT)

    def my_saved_diagnosis_change_status():
        if not data['examination'].get('my_saved_diagnosis_status'):
            data['examination']['my_saved_diagnosis_status'] = 'closed'
            button_my_saved_diagnosis['text'] = 'Закрыть мои осмотры'

        if data['examination'].get('my_saved_diagnosis_status') == "closed":
            data['examination']['my_saved_diagnosis_status'] = 'open'
            button_my_saved_diagnosis['text'] = 'Закрыть мои осмотры'

            frame_my_saved_diagnosis.columnconfigure(index='all', minsize=40, weight=1)
            frame_my_saved_diagnosis.rowconfigure(index='all', minsize=20)
            frame_my_saved_diagnosis.pack(fill='both', expand=True, before=frame_diagnosis, side="bottom")

        elif data['examination'].get('my_saved_diagnosis_status') == "open":
            data['examination']['my_saved_diagnosis_status'] = 'closed'
            button_my_saved_diagnosis['text'] = 'Открыть мои осмотры'

            frame_my_saved_diagnosis.pack_forget()

    def paste_frame_1():
        paste_frame_diagnosis()
        paste_frame_date_time()
        paste_frame_button_create()
        my_saved_diagnosis()

        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT diagnosis, examination_key "
                        f"FROM my_saved_diagnosis "
                        f"WHERE doctor_name LIKE '{user.get('doctor_name')}' ")

            found_info = cur.fetchall()
        if found_info:
            my_saved_diagnosis_change_status()

        frame_1.columnconfigure(index='all', minsize=40, weight=1)
        frame_1.rowconfigure(index='all', minsize=20)
        frame_1.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

    frame_1 = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_diagnosis = Frame(frame_1, borderwidth=1, relief="solid")
    frame_date_time = Frame(frame_1, borderwidth=1, relief="solid")
    txt_date_time = Entry(frame_date_time, width=15,
                          font=('Comic Sans MS', user.get('text_size')),
                          justify="center")
    frame_button = Frame(frame_1, borderwidth=1, relief="solid")

    button_change_all_kb_status = Button(frame_button, text='Скрыть\nвсе\nклавиатуры',
                                         command=change_all_kb_status,
                                         font=('Comic Sans MS', user.get('text_size')))

    frame_my_saved_diagnosis_but = Frame(frame_diagnosis, borderwidth=1)
    frame_my_saved_diagnosis = Frame(frame_1, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_new_my_diagnosis = Frame(frame_1, borderwidth=1, relief="solid", padx=3, pady=3)

    lbl_my_saved_diagnosis = Label(master=frame_my_saved_diagnosis, text="",
                                   font=('Comic Sans MS', user.get('text_size')), bg='white')

    button_my_saved_diagnosis = Button(frame_my_saved_diagnosis_but, text='Открыть мои осмотры',
                                       command=my_saved_diagnosis_change_status,
                                       font=('Comic Sans MS', user.get('text_size')))

    paste_frame_1()

    def paste_frame_place_company():
        def select_place():
            data['examination']['place'] = selected_place.get()
            label_place['text'] = f"{all_data_diagnosis.get('place')[0]}: {selected_place.get()}"
            if selected_place.get() == 'в поликлинике':
                frame_company.pack(fill='both', expand=True, side="left")
            else:
                frame_company.pack_forget()

        label_place = Label(master=frame_place, text=f"{all_data_diagnosis.get('place')[0]}",
                            font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_place.pack(fill='both', expand=True, side="left")

        for mark in all_data_diagnosis.get('place')[1:]:
            btn = Radiobutton(master=frame_place, text=mark,
                              font=('Comic Sans MS', user.get('text_size')),
                              value=mark, variable=selected_place, command=select_place,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.pack(fill='both', expand=True, side="left")
        selected_place.set('в поликлинике')

        Label(master=frame_company, text=" На осмотре с ",
              font=('Comic Sans MS', user.get('text_size')),
              bg='white').pack(fill='both', expand=True, side="left")

        combo_company['values'] = ['мамой', 'папой', 'братом', 'сестрой', 'бабушкой', 'дедушкой', 'один', 'одна']
        combo_company.current(0)
        combo_company.pack(fill='both', expand=True, side="left")

        frame_company.columnconfigure(index='all', minsize=40, weight=1)
        frame_company.rowconfigure(index='all', minsize=20)
        frame_company.pack(fill='both', expand=True, side="left")

        frame_place.columnconfigure(index='all', minsize=40, weight=1)
        frame_place.rowconfigure(index='all', minsize=20)
        frame_place.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

    def is_valid__weight(weight):
        weight = weight.replace(',', '.')
        if not weight:
            err_msd_weight.set('Укажите вес ребенка')
            return True
        try:
            float(weight)
        except ValueError:
            return False
        else:
            if float(weight) < 3:
                err_msd_weight.set('вес ребенка меньше 3 кг!')
            elif float(weight) > 100:
                err_msd_weight.set('вес ребенка больше 100 кг!')
            else:
                err_msd_weight.set('')
            select_prescription(float(weight))
            return True

    frame_place = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_company = Frame(frame_place)

    combo_company = Combobox(frame_company, font=('Comic Sans MS', user.get('text_size')),
                             state="readonly", justify="center")

    paste_frame_place_company()

    def paste_frame_complaints():

        label_complaints = Label(master=frame_complaints_main,
                                 text=f"{all_data_diagnosis.get('complaints')[0]}",
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

        change_complaints_kb_button.grid(column=1, row=0, sticky='ew')

        frame_complaints_main.columnconfigure(index='all', minsize=10, weight=1)
        frame_complaints_main.rowconfigure(index='all', minsize=10)
        # frame_complaints_main.pack(fill='both', expand=True, side=tk.LEFT)
        frame_complaints_main.grid(row=0, column=0, sticky='ew')

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

    def change_complaints_kb_status():

        if data['examination'].get('open_complaints_kb') == 'open':
            data['examination']['open_complaints_kb'] = 'closed'
            change_complaints_kb_button['text'] = 'открыть клавиатуру жалоб'
            txt_complaints['height'] = 2
            txt_complaints['width'] = 100
            frame_complaints_buttons.grid_forget()
            frame_complaints_main.grid_configure(row=0, column=0, sticky='ew', columnspan=3)
        else:
            data['examination']['open_complaints_kb'] = 'open'
            change_complaints_kb_button['text'] = 'скрыть клавиатуру жалоб'
            txt_complaints['height'] = 6
            txt_complaints['width'] = 15
            frame_complaints_buttons.grid(row=0, column=1, sticky='ew', columnspan=2)
            frame_complaints_main.grid_configure(row=0, column=0, sticky='ew', columnspan=1)

    def paste_complaints_kb():
        destroy_elements['complaints'] = list()
        data['examination']['complaints_buttons'] = dict()
        data['examination']['open_complaints_kb'] = 'open'

        frame_loc = Frame(frame_complaints_buttons)

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
                frame_loc = Frame(frame_complaints_buttons)
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
        frame_complaints_buttons.columnconfigure(index='all', minsize=10, weight=1)
        frame_complaints_buttons.rowconfigure(index='all', minsize=10)
        # frame_complaints_1.pack(fill='both', expand=True).grid(row=0, column=0, sticky='ew')
        frame_complaints_buttons.grid(row=0, column=1, sticky='ew', columnspan=2)

    frame_complaints = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_complaints_main = Frame(frame_complaints, padx=1, pady=1)
    frame_complaints_buttons = Frame(frame_complaints, padx=1, pady=1)
    txt_complaints = ScrolledText(frame_complaints_main, width=15, height=6,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  wrap="word")
    change_complaints_kb_button = Button(frame_complaints_main, text='скрыть клавиатуру жалоб',
                                         command=change_complaints_kb_status,
                                         font=('Comic Sans MS', user.get('text_size')))

    paste_frame_complaints()

    def paste_frame_examination():

        label_examination = Label(master=frame_examination_main,
                                  text=f"{all_data_diagnosis.get('examination')[0]}",
                                  font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_examination.grid(row=0, column=0, sticky='ew')

        txt_examination.grid(column=0, row=1, sticky='ew', columnspan=2)

        data['examination']['examination_but'] = dict()
        for mark_ in all_data_diagnosis.get('examination')[1:]:
            if isinstance(mark_, tuple):
                for mark_2_ in mark_[1:]:
                    data['examination']['examination_but'][f"{mark_[0]}_{mark_2_}"] = IntVar()

        change_examination_kb_button.grid(column=1, row=0, sticky='ew')

        frame_examination_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_examination_main.rowconfigure(index='all', minsize=20)
        frame_examination_main.pack(fill='both', expand=True, side=tk.LEFT)

        paste_examination_kb()
        frame_examination.columnconfigure(index='all', minsize=40, weight=1)
        frame_examination.rowconfigure(index='all', minsize=20)
        frame_examination.pack(fill='both', expand=True, padx=2, pady=2)

    def select_examination_frame():

        if data['examination']['examination_frame'].get('open_frame'):
            data['examination']['examination_frame'].get('open_frame').pack_forget()

        frame_loc = data['examination']['examination_frame'].get(selected_examination_frame.get())
        data['examination']['examination_frame']['open_frame'] = frame_loc
        frame_loc.pack(fill='both', expand=True)

    def change_examination_kb_status():
        if data['examination'].get('open_examination_kb') == 'open':
            data['examination']['open_examination_kb'] = 'closed'
            frame_examination_buttons.pack_forget()
            change_examination_kb_button['text'] = 'открыть клавиатуру осмотра'
            txt_examination['height'] = 8
            txt_examination['width'] = 100

        else:
            data['examination']['open_examination_kb'] = 'open'
            frame_examination_buttons.pack(fill='both', expand=True, padx=2, pady=2)
            change_examination_kb_button['text'] = 'скрыть клавиатуру осмотра'
            txt_examination['height'] = 30
            txt_examination['width'] = 20
            edit_examination_kb_text()

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

                if mark_1 == 'Дополнительно' and mark_2 in ("отрицательные", "положительные", "сомнительные"):
                    if text[-2:] == ', ':
                        text = text[:-2] + ' '
                    text += f"{mark_2}, "

                else:
                    if mark_1 not in text:
                        if text:
                            text = text[:-2] + '. '
                        text += f"{mark_1}: {mark_2}, "
                    else:
                        if mark_2[-1] == '-':
                            text += f"{mark_2} "
                        else:
                            text += f"{mark_2}, "

        txt_examination.delete(1.0, 'end')
        text = text[:-2] + '.'
        txt_examination.insert(1.0, text)
        edit_examination_kb_text()

    def edit_examination_kb_text():
        for button_name in data['examination'].get('examination_buttons'):
            text = f"{button_name}: "
            for mark_ in data['examination'].get('examination_but'):
                if mark_.startswith(button_name):
                    if data['examination']['examination_but'].get(mark_).get() == 1:
                        text += f"{mark_.split('_')[-1]}, "
                        if len(text.split('\n')[-1]) > 80:
                            text += "\n"
            text = text[:-2]
            btn = data['examination']['examination_buttons'].get(button_name)
            btn['text'] = text

        for button_name in data['examination'].get('examination_buttons_2_color'):
            if data['examination']['examination_but'].get(button_name):
                if data['examination']['examination_but'].get(button_name).get() == 1:
                    data['examination']['examination_buttons_2_color'][button_name]['bg'] = '#77f1ff'
                else:
                    data['examination']['examination_buttons_2_color'][button_name]['bg'] = '#cdcdcd'

    def paste_examination_kb():
        data['examination']['open_examination_kb'] = 'open'
        data['examination']['examination_frame'] = dict()
        data['examination']['examination_buttons'] = dict()
        data['examination']['examination_buttons_2_color'] = dict()

        Label(master=frame_weight, text=f"Вес ребенка кг",
              font=('Comic Sans MS', user.get('text_size')),
              bg='white').pack(fill='both', expand=True, side="left")
        txt_weight.pack(fill='both', expand=True, side="left")
        err_msd_lbl_weight.pack(fill='both', expand=True, side="left")

        frame_weight.columnconfigure(index='all', minsize=40, weight=1)
        frame_weight.rowconfigure(index='all', minsize=20)
        frame_weight.pack(fill='both', expand=True)

        for mark in all_data_diagnosis.get('examination')[1:]:
            if isinstance(mark, tuple):
                frame_loc = Frame(frame_examination_buttons, borderwidth=1)

                btn = Radiobutton(frame_loc, text=f"{mark[0]}",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=f"{mark[0]}", variable=selected_examination_frame,
                                  command=select_examination_frame,
                                  indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
                btn.pack(fill='both', expand=True)
                data['examination']['examination_buttons'][mark[0]] = btn

                row, col = 0, 0

                frame_loc_but = Frame(frame_loc, borderwidth=1)
                for mark_2 in mark[1:]:
                    data['examination']['examination_frame'][mark[0]] = frame_loc_but

                    btn = Checkbutton(frame_loc_but, text=mark_2,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      onvalue=1, offvalue=0,
                                      variable=data['examination']['examination_but'].get(
                                          f"{mark[0]}_{mark_2}"),
                                      command=select_examination,
                                      indicatoron=False, selectcolor='#77f1ff')
                    btn.grid(row=row, column=col, sticky='ew')
                    data['examination']['examination_buttons_2_color'][f"{mark[0]}_{mark_2}"] = btn

                    col += 1
                    if col == 5 and mark[0] != 'Температура':
                        col = 0
                        row += 1

                frame_loc_but.columnconfigure(index='all', minsize=40, weight=1)
                frame_loc_but.rowconfigure(index='all', minsize=20)

                frame_loc.columnconfigure(index='all', minsize=40, weight=1)
                frame_loc.rowconfigure(index='all', minsize=20)
                frame_loc.pack(fill='both', expand=True)

        frame_examination_buttons.columnconfigure(index='all', minsize=40, weight=1)
        frame_examination_buttons.rowconfigure(index='all', minsize=20)
        frame_examination_buttons.pack(fill='both', expand=True, padx=2, pady=2)

    frame_examination = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_examination_main = Frame(frame_examination, borderwidth=1)
    frame_examination_buttons = Frame(frame_examination, borderwidth=1)

    frame_weight = Frame(frame_examination_buttons, borderwidth=0.5, relief="solid", padx=1, pady=1)
    err_msd_lbl_weight = Label(master=frame_weight, textvariable=err_msd_weight,
                               font=('Comic Sans MS', user.get('text_size')), bg='white',
                               foreground="red")
    check_weight = (root_examination.register(is_valid__weight), "%P")
    txt_weight_variable = StringVar()
    txt_weight = Entry(frame_weight, width=10,
                       font=('Comic Sans MS', user.get('text_size')),
                       justify="center",
                       validate="all",
                       textvariable=txt_weight_variable,
                       validatecommand=check_weight)

    txt_examination = ScrolledText(frame_examination_main, width=20, height=30,
                                   font=('Comic Sans MS', user.get('text_size')),
                                   wrap="word")
    change_examination_kb_button = Button(frame_examination_main, text='скрыть клавиатуру осмотра',
                                          command=change_examination_kb_status,
                                          font=('Comic Sans MS', user.get('text_size')))

    paste_frame_examination()

    def paste_diagnosis_kb():

        def select_diagnosis_kb():
            txt_diagnosis_info = txt_diagnosis.get(1.0, 'end')[:-1]
            for but in data['examination'].get('diagnosis_add_kb'):
                if data['examination']['diagnosis_add_kb'].get(but).get() == 1:
                    if but not in txt_diagnosis_info:
                        txt_diagnosis_info += f"{but} "
                else:
                    txt_diagnosis_info = txt_diagnosis_info.replace(f'{but} ', '')

            txt_diagnosis.delete(1.0, 'end')
            txt_diagnosis.insert(1.0, txt_diagnosis_info)

        if destroy_elements.get('frame_diagnosis_kb'):
            frame_diagnosis_kb = destroy_elements.get('frame_diagnosis_kb')
            frame_diagnosis_kb.destroy()
            destroy_elements['frame_diagnosis_kb'] = None

        if data['examination'].get('diagnosis') == 'ОРИ':
            txt_diagnosis['width'] = 30
            txt_diagnosis['height'] = 5
            data['examination']['diagnosis_add_kb'] = dict()
            frame_diagnosis_kb = Frame(frame_diagnosis_txt, borderwidth=1, relief="solid")
            destroy_elements['frame_diagnosis_kb'] = frame_diagnosis_kb

            row, col = 0, 0
            for mark in all_data_diagnosis.get('diagnosis_ori'):
                data['examination']['diagnosis_add_kb'][mark] = IntVar()
                btn = Checkbutton(frame_diagnosis_kb, text=mark,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  onvalue=1, offvalue=0,
                                  variable=data['examination']['diagnosis_add_kb'].get(mark),
                                  command=select_diagnosis_kb,
                                  indicatoron=False, selectcolor='#77f1ff')
                btn.grid(row=row, column=col, sticky='ew')
                col += 1
                if col == 4:
                    col = 0
                    row += 1

            frame_diagnosis_kb.columnconfigure(index='all', minsize=40, weight=1)
            frame_diagnosis_kb.rowconfigure(index='all', minsize=20)
            frame_diagnosis_kb.pack(fill='both', expand=True, side=tk.LEFT)

        elif data['examination'].get('diagnosis') == 'ФРК':
            txt_diagnosis['width'] = 30
            txt_diagnosis['height'] = 5
            data['examination']['diagnosis_add_kb'] = dict()
            frame_diagnosis_kb = Frame(frame_diagnosis_txt, borderwidth=1, relief="solid")
            destroy_elements['frame_diagnosis_kb'] = frame_diagnosis_kb

            row, col = 0, 0
            for mark in all_data_diagnosis.get('diagnosis_ФРК'):
                data['examination']['diagnosis_add_kb'][mark] = IntVar()
                btn = Checkbutton(frame_diagnosis_kb, text=mark,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  onvalue=1, offvalue=0,
                                  variable=data['examination']['diagnosis_add_kb'].get(mark),
                                  command=select_diagnosis_kb,
                                  indicatoron=False, selectcolor='#77f1ff')
                btn.grid(row=row, column=col, sticky='ew')
                col += 1
                if col == 4:
                    col = 0
                    row += 1

            frame_diagnosis_kb.columnconfigure(index='all', minsize=40, weight=1)
            frame_diagnosis_kb.rowconfigure(index='all', minsize=20)
            frame_diagnosis_kb.pack(fill='both', expand=True, side=tk.LEFT)

        elif data['examination'].get('diagnosis') == 'Ветряная оспа':
            txt_diagnosis['width'] = 30
            txt_diagnosis['height'] = 5
            data['examination']['diagnosis_add_kb'] = dict()
            frame_diagnosis_kb = Frame(frame_diagnosis_txt, borderwidth=1, relief="solid")
            destroy_elements['frame_diagnosis_kb'] = frame_diagnosis_kb

            row, col = 0, 0
            for mark in all_data_diagnosis.get('diagnosis_Ветрянка'):
                data['examination']['diagnosis_add_kb'][mark] = IntVar()
                btn = Checkbutton(frame_diagnosis_kb, text=mark,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  onvalue=1, offvalue=0,
                                  variable=data['examination']['diagnosis_add_kb'].get(mark),
                                  command=select_diagnosis_kb,
                                  indicatoron=False, selectcolor='#77f1ff')
                btn.grid(row=row, column=col, sticky='ew')
                col += 1
                if col == 4:
                    col = 0
                    row += 1

            frame_diagnosis_kb.columnconfigure(index='all', minsize=40, weight=1)
            frame_diagnosis_kb.rowconfigure(index='all', minsize=20)
            frame_diagnosis_kb.pack(fill='both', expand=True, side=tk.LEFT)

        elif data['examination'].get('diagnosis') == 'Здоров':
            txt_diagnosis['width'] = 30
            txt_diagnosis['height'] = 5
            data['examination']['diagnosis_add_kb'] = dict()
            frame_diagnosis_kb = Frame(frame_diagnosis_txt, borderwidth=1, relief="solid")
            destroy_elements['frame_diagnosis_kb'] = frame_diagnosis_kb

            row, col = 0, 0
            for mark in all_data_diagnosis.get('diagnosis_Здоров'):
                data['examination']['diagnosis_add_kb'][mark] = IntVar()
                btn = Checkbutton(frame_diagnosis_kb, text=mark,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  onvalue=1, offvalue=0,
                                  variable=data['examination']['diagnosis_add_kb'].get(mark),
                                  command=select_diagnosis_kb,
                                  indicatoron=False, selectcolor='#77f1ff')
                btn.grid(row=row, column=col, sticky='ew')
                col += 1
                if col == 4:
                    col = 0
                    row += 1

            frame_diagnosis_kb.columnconfigure(index='all', minsize=40, weight=1)
            frame_diagnosis_kb.rowconfigure(index='all', minsize=20)
            frame_diagnosis_kb.pack(fill='both', expand=True, side=tk.LEFT)

        else:
            txt_diagnosis['width'] = 30
            txt_diagnosis['height'] = 5
            data['examination']['diagnosis_add_kb'] = dict()
            frame_diagnosis_kb = Frame(frame_diagnosis_txt, borderwidth=1, relief="solid")
            destroy_elements['frame_diagnosis_kb'] = frame_diagnosis_kb

            row, col = 0, 0
            for mark in all_data_diagnosis.get('diagnosis_ori'):
                data['examination']['diagnosis_add_kb'][mark] = IntVar()
                btn = Checkbutton(frame_diagnosis_kb, text=mark,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  onvalue=1, offvalue=0,
                                  variable=data['examination']['diagnosis_add_kb'].get(mark),
                                  command=select_diagnosis_kb,
                                  indicatoron=False, selectcolor='#77f1ff')
                btn.grid(row=row, column=col, sticky='ew')
                col += 1
                if col == 4:
                    col = 0
                    row += 1

            frame_diagnosis_kb.columnconfigure(index='all', minsize=40, weight=1)
            frame_diagnosis_kb.rowconfigure(index='all', minsize=20)
            frame_diagnosis_kb.pack(fill='both', expand=True, side=tk.LEFT)


    frame_diagnosis_txt = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    txt_diagnosis = ScrolledText(frame_diagnosis_txt, width=70, height=3,
                                 font=('Comic Sans MS', user.get('text_size')),
                                 wrap="word")
    txt_diagnosis.pack(fill='both', expand=True, side=tk.LEFT)
    txt_diagnosis.insert(1.0, 'Диагноз: ')
    frame_diagnosis_txt.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

    def paste_frame_prescription():
        label_prescription = Label(master=frame_prescription_main,
                                   text=f"{all_data_diagnosis.get('prescription')[0]}",
                                   font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_prescription.grid(row=0, column=0, sticky='ew')

        txt_prescription.grid(column=0, row=1, sticky='nwse', columnspan=2)

        data['examination']['prescription_but'] = dict()
        for mark_ in all_data_diagnosis.get('prescription')[1:]:
            if 'Антибиотик' not in mark_[0]:
                for mark_2_ in mark_[1:]:
                    data['examination']['prescription_but'][f"{mark_[0]}_{mark_2_}"] = IntVar()

        change_prescription_kb_button.grid(column=1, row=0, sticky='ew')

        frame_prescription_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription_main.rowconfigure(index='all', minsize=20)
        frame_prescription_main.pack(fill='both', expand=True, side=tk.LEFT)

        paste_prescription_kb()
        frame_prescription.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription.rowconfigure(index='all', minsize=20)
        frame_prescription.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

    def select_prescription_frame():
        if data['examination']['prescription_frame'].get('last_open_frame', '') == selected_prescription_frame.get():
            data['examination']['prescription_frame'].get('open_frame').pack_forget()
            data['examination']['prescription_frame']['last_open_frame'] = ''
            if 'Антибиотик ' in selected_prescription_frame.get():
                ab_name = selected_prescription_frame.get()
                for ab_mark in data['examination']['prescription_but_ab_value'].get(ab_name):
                    data['examination']['prescription_but_ab_value'][ab_name][ab_mark].set('')
        else:
            if 'Антибиотик' in selected_prescription_frame.get():
                txt_prescription['height'] = 16
            else:
                txt_prescription['height'] = 8

            if data['examination']['prescription_frame'].get('open_frame') and \
                    'Антибиотик ' not in selected_prescription_frame.get():
                data['examination']['prescription_frame'].get('open_frame').pack_forget()

            frame_loc = data['examination']['prescription_frame'].get(selected_prescription_frame.get())
            data['examination']['prescription_frame']['open_frame'] = frame_loc
            frame_loc.pack(fill='both', expand=True)
            data['examination']['prescription_frame']['last_open_frame'] = selected_prescription_frame.get()

    def select_prescription(weight=None):
        edit_prescription_text()

        text_paracetamol = ""
        text_ibuprofen = ""
        text_antibiotic = ""
        text_analyzes = ""
        text_prescription = ""

        for ab_name in data['examination'].get('prescription_but_ab_value'):
            ab_key_dosa = data['examination']['prescription_but_ab_value'][ab_name].get('Дозировка').get()
            ab_key_form = data['examination']['prescription_but_ab_value'][ab_name].get('Форма').get()
            ab_key_count = data['examination']['prescription_but_ab_value'][ab_name].get('Кратность').get()

            if ab_key_dosa and ab_key_form:
                text_antibiotic_loc = f"{ab_name}: {ab_key_form}"

                if txt_weight.get():
                    if not weight:
                        weight = float(txt_weight.get().replace(',', '.'))
                    if weight > 40:
                        weight = 40
                    ab_weight = ''
                    if 'сусп. ' in ab_key_form:
                        ab_weight = ab_key_form.split('/')[0].replace('сусп. ', '').strip()
                    if 'таб. ' in ab_key_form:
                        ab_weight = ab_key_form.replace('таб. ', '').split('/')[0].strip()

                    ab_dosage = int(ab_key_dosa.split()[0])
                    ab_dosage_day = weight * ab_dosage
                    ab_volume_day = ab_dosage_day / int(ab_weight)
                    if ab_key_count:
                        ab_key_count = ab_key_count.replace(' р/сут', '')
                    if not ab_key_count.isdigit():
                        ab_key_count = '2'
                    ab_key_count = int(ab_key_count)
                    ab_volume_single = ab_volume_day / ab_key_count
                    if 'сусп. ' in ab_key_form:
                        ab_volume_single = ab_volume_single * 5
                        text_antibiotic_loc += f" по {round(ab_volume_single, 1)}мл. {ab_key_count} р/сут " \
                                               f"({round(ab_dosage_day / weight)}мг/кг/сут)"

                    else:
                        if str(ab_volume_single).split('.')[-1][0] in ('4', '5', '6'):
                            ab_volume_single = float(f"{str(ab_volume_single).split('.')[0]}.5")
                        else:
                            ab_volume_single = round(ab_volume_single)
                        text_antibiotic_loc += f" по {round(ab_volume_single, 1)}таб. {ab_key_count} р/сут " \
                                               f"({round((ab_volume_single * ab_key_count * int(ab_weight)) / weight)}мг/кг/сут)"

                else:
                    text_antibiotic_loc += f" - {ab_key_dosa} {ab_key_count}"

                if text_antibiotic:
                    text_antibiotic += '\n'
                text_antibiotic += text_antibiotic_loc

        for i in txt_prescription.get(1.0, 'end')[:-1].strip().split('\n'):
            if 'Рекомендации' in i:
                text_prescription = i.strip()
                if len(text_prescription.replace('Рекомендации', '')) < 5:
                    text_prescription = ''
        if text_prescription and text_prescription[-1] in ('.', ','):
            text_prescription = text_prescription[:-1] + ', '

        for mark in data['examination'].get('prescription_but'):
            mark_1, mark_2 = mark.split('_')

            if data['examination']['prescription_but'].get(mark).get() == 1:
                if mark_2 in ('Парацетамол', 'Ибупрофен'):
                    if txt_weight.get():
                        if not weight:
                            weight = float(txt_weight.get().replace(',', '.'))
                        if weight > 40:
                            weight = 40
                        paracetamol_min, paracetamol_max = (weight * 10, weight * 15)
                        ibuprofen_min, ibuprofen_max = (weight * 5, weight * 10)

                        if mark_2 == 'Парацетамол':
                            supp = []
                            for i in (50, 80, 100, 125, 150, 170, 250, 300, 330):
                                if paracetamol_min < i < paracetamol_max:
                                    supp.append(i)
                            if supp:
                                supp_text = 'Супп. '
                                for i in supp:
                                    supp_text += str(i) + 'мг. '
                                text_paracetamol += supp_text
                            text_paracetamol += f'Cусп. 30мг/мл - {round(weight * 0.5, 1)}мл; '

                            if age > 5:
                                if paracetamol_max < 100:
                                    text_paracetamol += ""
                                elif paracetamol_max < 200:
                                    text_paracetamol += "Таб. 200 мг: 1/2 т.; "
                                elif paracetamol_max < 300:
                                    text_paracetamol += "Таб. 200 мг: 1 т.; "
                                elif paracetamol_max < 400:
                                    text_paracetamol += "Таб. 200 мг: 1.5 т.; "
                                elif 400 <= paracetamol_max:
                                    text_paracetamol += "Таб. 200 мг: 2 т.; "

                                if paracetamol_min < 250 <= paracetamol_max:
                                    text_paracetamol += "Таб. 500 мг: 1/2 т.; "
                                elif 500 <= paracetamol_max:
                                    text_paracetamol += "Таб. 500 мг: 1 т.; "
                            text_paracetamol = f"Парацетамол 15 мг/кг при темп. выше 38.5 ({text_paracetamol}) " \
                                               f"не 4 > р/сут"

                        elif mark_2 == 'Ибупрофен':

                            if ibuprofen_min < 60 <= ibuprofen_max:
                                text_ibuprofen += f'Супп. 60 мг.; '

                            text_ibuprofen += f"Cусп. 100мг/5мл - {round(ibuprofen_max / 20, 1)}мл; " \
                                              f"Cусп. 200мг/5мл - {round(ibuprofen_max / 40, 1)}мл; "
                            if age > 5:
                                if ibuprofen_max < 100:
                                    pass
                                elif ibuprofen_max < 200:
                                    text_ibuprofen += "Таб. 200 мг: 1/2 таб;"
                                elif ibuprofen_max < 300:
                                    text_ibuprofen += "Таб. 200 мг: 1 таб;"
                                elif ibuprofen_max < 400:
                                    text_ibuprofen += "Таб. 200 мг: 1.5 таб;"
                                elif 400 <= ibuprofen_max:
                                    text_ibuprofen += "Таб. 200 мг: 2 таб;"

                            text_ibuprofen = f"Ибупрофен 10 мг/кг при темп. выше 38.5 ({text_ibuprofen}) не 4 > р/сут"

                        if mark_2 in text_prescription:
                            if f"{mark_2}, " in text_prescription:
                                text_prescription = text_prescription.replace(f"{mark_2}, ", '')
                            elif f"{mark_2}." in text_prescription:
                                text_prescription = text_prescription.replace(f"{mark_2}.", '')
                            else:
                                text_prescription = text_prescription.replace(mark_2, '')

                    else:
                        if mark_2 not in text_prescription:
                            text_prescription += f"{mark_2}, "

                elif mark_1 == 'Анализы':
                    text_analyzes += f"{mark_2}, "

                elif mark_1 == 'Рекомендации':
                    if not text_prescription:
                        text_prescription = 'Рекомендации: '

                    if mark_2 not in text_prescription:
                        text_prescription += f"{mark_2}, "

            else:
                if mark_1 == 'Рекомендации':
                    if mark_2 in text_prescription:
                        if f"{mark_2}, " in text_prescription:
                            text_prescription = text_prescription.replace(f"{mark_2}, ", '')
                        elif f"{mark_2}." in text_prescription:
                            text_prescription = text_prescription.replace(f"{mark_2}.", '')
                        else:
                            text_prescription = text_prescription.replace(mark_2, '')

        txt_prescription.delete(1.0, 'end')
        text = ''

        if text_analyzes:
            text = f"Анализы: {text_analyzes[:-2]};\n"
        if text_prescription:
            text = f"{text}{text_prescription[:-2]}.\n"
        if text_paracetamol:
            text = f"{text}{text_paracetamol}\n"
        if text_ibuprofen:
            text = f"{text}{text_ibuprofen}\n"
        if text_antibiotic:
            text = f"{text}{text_antibiotic}"
        text = text.strip()
        txt_prescription.insert(1.0, text)

        frame_prescription_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription_main.rowconfigure(index='all', minsize=20)

        frame_prescription.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription.rowconfigure(index='all', minsize=20)

    def edit_prescription_text():
        for button_name in data['examination'].get('prescription_buttons'):
            text = f"{button_name}: "
            for mark_ in data['examination'].get('prescription_but'):
                if mark_.startswith(button_name):
                    if data['examination']['prescription_but'].get(mark_).get() == 1:
                        text += f"{mark_.split('_')[-1]}, "
                        if len(text.split('\n')[-1]) > 80:
                            text += "\n"
            text = text[:-2]
            btn = data['examination']['prescription_buttons'].get(button_name)
            btn['text'] = text

        for button_name in data['examination'].get('prescription_buttons_2_color'):
            if data['examination']['prescription_but'].get(button_name):
                if data['examination']['prescription_but'].get(button_name).get() == 1:
                    data['examination']['prescription_buttons_2_color'][button_name]['bg'] = '#77f1ff'
                else:
                    data['examination']['prescription_buttons_2_color'][button_name]['bg'] = '#cdcdcd'

    def paste_prescription_kb():

        data['examination']['open_prescription_kb'] = 'open'
        data['examination']['prescription_frame'] = dict()
        data['examination']['prescription_buttons'] = dict()
        data['examination']['prescription_buttons_2_color'] = dict()

        data['examination']['prescription_but_ab_value'] = dict()

        for mark in all_data_diagnosis.get('prescription')[1:]:
            if 'Антибиотик' not in mark[0]:
                frame_loc = Frame(frame_prescription_buttons, borderwidth=1)
                btn = Radiobutton(frame_loc, text=f"{mark[0]}",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=f"{mark[0]}", variable=selected_prescription_frame,
                                  command=select_prescription_frame,
                                  indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
                btn.pack(fill='both', expand=True)
                data['examination']['prescription_buttons'][mark[0]] = btn
                row, col = 0, 0
                frame_loc_but = Frame(frame_loc, borderwidth=1)
                data['examination']['prescription_frame'][mark[0]] = frame_loc_but
                for mark_2 in mark[1:]:
                    btn = Checkbutton(frame_loc_but, text=mark_2,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      onvalue=1, offvalue=0,
                                      variable=data['examination']['prescription_but'].get(
                                          f"{mark[0]}_{mark_2}"),
                                      command=select_prescription,
                                      indicatoron=False, selectcolor='#77f1ff')
                    btn.grid(row=row, column=col, sticky='ew')
                    data['examination']['prescription_buttons_2_color'][f"{mark[0]}_{mark_2}"] = btn

                    col += 1
                    if col == 6:
                        col = 0
                        row += 1

                frame_loc_but.columnconfigure(index='all', minsize=40, weight=1)
                frame_loc_but.rowconfigure(index='all', minsize=20)

                frame_loc.columnconfigure(index='all', minsize=40, weight=1)
                frame_loc.rowconfigure(index='all', minsize=20)
                frame_loc.pack(fill='both', expand=True)

        btn = Radiobutton(frame_prescription_buttons_antibiotic_main, text=f"Антибиотик",
                          font=('Comic Sans MS', user.get('text_size')),
                          value=f"Антибиотик", variable=selected_prescription_frame,
                          command=select_prescription_frame,
                          indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
        btn.pack(fill='both', expand=True)
        data['examination']['prescription_frame']['Антибиотик'] = frame_prescription_buttons_antibiotic_buttons

        for mark in all_data_diagnosis.get('prescription')[1:]:
            if 'Антибиотик' in mark[0]:
                frame_loc = Frame(frame_prescription_buttons_antibiotic_buttons, borderwidth=1)
                btn = Radiobutton(frame_loc, text=f"{mark[0]}",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=f"{mark[0]}", variable=selected_prescription_frame,
                                  command=select_prescription_frame,
                                  indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')

                btn.pack(fill='both', expand=True)
                row, col = 0, 0
                frame_loc_but = Frame(frame_loc, borderwidth=1)
                data['examination']['prescription_frame'][mark[0]] = frame_loc_but
                for mark_2 in mark[1:]:
                    if mark_2 in ('Форма', 'Дозировка', "Кратность"):
                        if not data['examination']['prescription_but_ab_value'].get(mark[0]):
                            data['examination']['prescription_but_ab_value'][mark[0]] = dict()
                        data['examination']['prescription_but_ab_value'][mark[0]][mark_2] = StringVar()

                        if mark_2 in ('Дозировка', "Кратность"):
                            row += 1
                            col = 0
                        Label(master=frame_loc_but, text=f"{mark_2}",
                              font=('Comic Sans MS', user.get('text_size')),
                              bg='white').grid(row=row, column=col, sticky='ew')
                        col += 1
                    else:
                        btn = Radiobutton(frame_loc_but, text=mark_2,
                                          font=('Comic Sans MS', user.get('text_size')),
                                          value=mark_2,
                                          command=select_prescription,
                                          indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')

                        if 'сусп.' in mark_2 or 'таб.' in mark_2:
                            btn['variable'] = \
                                data['examination']['prescription_but_ab_value'][mark[0]].get('Форма')
                        if 'мг/кг/сут' in mark_2:
                            btn['variable'] = \
                                data['examination']['prescription_but_ab_value'][mark[0]].get('Дозировка')
                        if 'р/сут' in mark_2:
                            btn['variable'] = \
                                data['examination']['prescription_but_ab_value'][mark[0]].get('Кратность')
                        btn.grid(row=row, column=col, sticky='ew')

                        col += 1
                        if col == 6:
                            col = 0
                            row += 1

                frame_loc_but.columnconfigure(index='all', minsize=40, weight=1)
                frame_loc_but.rowconfigure(index='all', minsize=20)

                frame_loc.columnconfigure(index='all', minsize=40, weight=1)
                frame_loc.rowconfigure(index='all', minsize=20)
                frame_loc.pack(fill='both', expand=True)

        frame_prescription_buttons.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription_buttons.rowconfigure(index='all', minsize=20)
        frame_prescription_buttons.pack(fill='both', expand=True, padx=2, pady=2)

        frame_prescription_buttons_antibiotic_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription_buttons_antibiotic_main.rowconfigure(index='all', minsize=20)
        frame_prescription_buttons_antibiotic_main.pack(fill='both', expand=True, padx=2, pady=2)

    def change_prescription_kb_status():
        if data['examination'].get('open_prescription_kb') == 'open':
            data['examination']['open_prescription_kb'] = 'closed'
            change_prescription_kb_button['text'] = 'открыть клавиатуру рекомендаций'
            txt_prescription['height'] = 4
            txt_prescription['width'] = 70
            frame_prescription_buttons.pack_forget()

        else:
            data['examination']['open_prescription_kb'] = 'open'
            frame_prescription_buttons.pack(fill='both', expand=True, padx=2, pady=2)
            change_prescription_kb_button['text'] = 'закрыть клавиатуру рекомендаций'
            txt_prescription['height'] = 8
            txt_prescription['width'] = 60

            edit_examination_kb_text()

    frame_prescription = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_prescription_main = Frame(frame_prescription, padx=1, pady=1)
    frame_prescription_buttons = Frame(frame_prescription, padx=1, pady=1)
    frame_prescription_buttons_antibiotic_main = Frame(frame_prescription_buttons, padx=1, pady=1)
    frame_prescription_buttons_antibiotic_buttons = Frame(frame_prescription_buttons_antibiotic_main, padx=1, pady=1)

    txt_prescription = ScrolledText(frame_prescription_main, width=15, height=8,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    wrap="word")
    change_prescription_kb_button = Button(frame_prescription_main, text='скрыть клавиатуру рекомендаций',
                                           command=change_prescription_kb_status,
                                           font=('Comic Sans MS', user.get('text_size')))

    paste_frame_prescription()

    def paste_frame_ln():
        def calendar_ln_from():
            paste_calendar(text_field='ln_from__Больничный с ...')

        def calendar_ln_until():
            paste_calendar(text_field='ln_until__Больничный по ...')

        def calendar_second_examination():
            paste_calendar(text_field='second_examination__Повторный осмотр')

        def select_type_ln():
            if data['examination'].get('open_frame_ln_my_blanks', '') == 'open':
                data['examination']['open_frame_ln_my_blanks'] = 'closed'
                frame_ln_my_blanks.pack_forget()

            type_ln = selected_type_ln.get()
            ln_num = ''

            if type_ln in ("Справка ВН", "Лист ВН"):
                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                    cur = conn.cursor()

                    cur.execute(f"SELECT date_time, LN_type FROM examination "
                                f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                                f"AND patient_info LIKE "
                                f"'{patient.get('name')}__{patient.get('birth_date')}' "
                                f"AND LN_type LIKE '{type_ln}%'")

                    found_info = cur.fetchall()
                if found_info:
                    last_visit = min(found_info,
                                     key=lambda i: (datetime.now() -
                                                    datetime.strptime(f"{i[0]}", "%d.%m.%Y %H:%M")).seconds)
                    print('last_visit', last_visit)
                    if (datetime.now() - datetime.strptime(f"{last_visit[0]}", "%d.%m.%Y %H:%M")).days < 14:
                        if last_visit[1].split('__')[-1] != 'closed':
                            ln_num = last_visit[1].split('__')[1].replace('_', '')
                            try:
                                date_from_cont = datetime.strptime(f"{last_visit[1].split('__')[3]}",
                                                                   "%d.%m.%Y") + timedelta(days=1)
                                date_from_cont = date_from_cont.strftime("%d.%m.%Y")
                                txt_ln_from.delete(0, 'end')
                                txt_ln_from.insert(0, date_from_cont)

                            except Exception:
                                pass

                if not ln_num:
                    open_frame_ln_my_blanks()
                else:
                    txt_ln_num.delete(0, 'end')
                    if ln_num:
                        txt_ln_num.insert(0, ln_num)

                    # found_info = list()
                    # found_info.clear()
                    # with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                    #     cur = conn.cursor()
                    #     cur.execute(f"SELECT LN_type FROM examination "
                    #                 f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                    #                 f"AND LN_type LIKE '{type_ln}%'")
                    #     for num in cur.fetchall():
                    #         if num[0]:
                    #             found_info.append(num[0])
                    # if found_info:
                    #     last_ln_num = max(found_info, key=lambda i: int(i.split('__')[1].split('_')[-1]))
                    #     ln_num_digit = last_ln_num.split('__')[1].split('_')[-1]
                    #     ln_num = f"{last_ln_num.split('__')[1].split('_')[0]}" \
                    #              f"{int(ln_num_digit) + 1}".replace('_', '')
                    #     txt_ln_from.delete(0, 'end')
                    #     txt_ln_from.insert(0, datetime.now().strftime("%d.%m.%Y"))

            if type_ln in ("Справка ВН", "Лист ВН"):
                lbl_type_ln['text'] = f"{type_ln} номер:"
                frame_ln_add.grid(row=0, column=3, rowspan=2, sticky='ew')
                but_ln_my_blanks.grid(row=1, column=0, columnspan=3, sticky='ew')
            else:
                frame_ln_add.grid_remove()
                but_ln_my_blanks.grid_remove()

        col = 0
        for but in ("Справка ВН", "Лист ВН", "Уход обеспечен"):
            btn = Radiobutton(frame_ln, text=but,
                              font=('Comic Sans MS', user.get('text_size')),
                              value=but, variable=selected_type_ln, command=select_type_ln,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=0, column=col, sticky='ew')
            col += 1
        lbl_type_ln.grid(row=0, column=0, sticky='ew')

        txt_ln_num.grid(row=0, column=1, sticky='ew')
        but_ln_closed.grid(row=1, column=0, columnspan=2, sticky='ew')
        lbl_ln_from.grid(row=0, column=2, sticky='ew')
        txt_ln_from.grid(row=0, column=3, sticky='ew')
        Button(frame_ln_add, text='Календарь', font=('Comic Sans MS', user.get('text_size')),
               command=calendar_ln_from).grid(row=1, column=3, sticky='ew')
        Label(master=frame_ln_add, text=" по ",
              font=('Comic Sans MS', user.get('text_size')), bg='white').grid(row=0, column=4, sticky='ew')
        txt_ln_until.grid(row=0, column=5, sticky='ew')
        Button(frame_ln_add, text='Календарь', font=('Comic Sans MS', user.get('text_size')),
               command=calendar_ln_until).grid(row=1, column=5, sticky='ew')

        Label(master=frame_second_examination, text="Повторный осмотр",
              font=('Comic Sans MS', user.get('text_size')), bg='white').grid(row=1, column=0, sticky='ew')
        txt_second_examination.grid(row=1, column=1, sticky='ew', columnspan=2)
        Button(frame_second_examination, text='Календарь', font=('Comic Sans MS', user.get('text_size')),
               command=calendar_second_examination).grid(row=1, column=3, sticky='ew')

        frame_ln.columnconfigure(index='all', minsize=40, weight=1)
        frame_ln.rowconfigure(index='all', minsize=20)
        frame_ln.pack(fill='both', expand=True, padx=2, pady=2)

        frame_second_examination.columnconfigure(index='all', minsize=40, weight=1)
        frame_second_examination.rowconfigure(index='all', minsize=20)
        frame_second_examination.pack(fill='both', expand=True, padx=2, pady=2)

        frame_ln_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_ln_main.rowconfigure(index='all', minsize=20)
        frame_ln_main.pack(fill='both', expand=True, padx=2, pady=2)

    def ln_closed():
        if not data['examination'].get('ln_closed'):
            data['examination']['ln_closed'] = True
            lbl_ln_from.grid_configure(columnspan=4)
            lbl_ln_from.tkraise()
            lbl_ln_from['text'] = f"{selected_type_ln.get()} закрыт к труду"
            but_ln_closed['text'] = "отменить закрытие"
        else:
            data['examination']['ln_closed'] = False
            lbl_ln_from.grid_configure(columnspan=1)
            lbl_ln_from['text'] = " с "
            but_ln_closed['text'] = "закрыть к труду"

    def open_frame_ln_my_blanks():
        def select_ln_num():
            txt_ln_num.delete(0, 'end')
            txt_ln_num.insert(0, selected_ln_num.get())

        def add_my_new_ln():
            if not my_new_txt_ln_num.get():
                messagebox.showerror('Ошибка!', "Не указан номер первого ЛН")
            else:
                if type_ln == 'Лист ВН':
                    insert_data = f"{my_new_txt_ln_text.get()}__{my_new_txt_ln_num.get()}"
                else:
                    insert_data = f"__{my_new_txt_ln_num.get()}"

                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute(f"DELETE FROM my_LN "
                                   f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                                   f"AND ln_type LIKE '{type_ln}'")

                    cursor.execute("INSERT INTO my_LN VALUES(?, ?, ?)",
                                   [user.get('doctor_name'), type_ln, insert_data])
                data['examination']['open_frame_ln_my_blanks'] = 'closed'
                frame_ln_my_blanks.pack_forget()

        def is_valid__new_ln(num_ln):
            if num_ln.isdigit():
                return True
            else:
                return False

        selected_ln_num = StringVar()

        if data['examination'].get('open_frame_ln_my_blanks', '') == 'open':
            data['examination']['open_frame_ln_my_blanks'] = 'closed'
            frame_ln_my_blanks.pack_forget()
        elif data['examination'].get('open_frame_ln_my_blanks', '') == 'closed':
            data['examination']['open_frame_ln_my_blanks'] = 'open'

        elif not data['examination'].get('open_frame_ln_my_blanks'):
            data['examination']['open_frame_ln_my_blanks'] = 'open'

        if data['examination'].get('open_frame_ln_my_blanks', '') == 'open':
            if data['examination'].get('frame_ln_my_blanks'):
                data['examination']['frame_ln_my_blanks'].destroy()

            frame_ln_my_blanks_local = Frame(frame_ln_my_blanks, padx=1, pady=1)

            data['examination']['frame_ln_my_blanks'] = frame_ln_my_blanks_local

            active_ln = False
            type_ln = selected_type_ln.get()

            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                cur = conn.cursor()
                cur.execute(f"SELECT ln_num FROM my_LN "
                            f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                            f"AND ln_type LIKE '{type_ln}'")
                found_info = cur.fetchone()

                cur.execute(f"SELECT LN_type FROM examination "
                            f"WHERE doctor_name LIKE '{user.get('doctor_name')}' "
                            f"AND LN_type LIKE '{type_ln}%'")
                found_info_past = cur.fetchall()

            row, col = 0, 0
            if found_info:

                frame_ln_my_blanks_local_1 = Frame(frame_ln_my_blanks_local, padx=1, pady=1)
                first_ln_num = int(found_info[0].split('__')[-1])
                first_ln_text = found_info[0].split('__')[0]
                for ln_num in range(first_ln_num, first_ln_num + 10, 1):
                    btn = Radiobutton(frame_ln_my_blanks_local_1, text=f"{first_ln_text} {first_ln_num}",
                                      font=('Comic Sans MS', user.get('text_size')),
                                      value=f"{first_ln_text} {first_ln_num}",
                                      variable=selected_ln_num, command=select_ln_num,
                                      indicatoron=False, selectcolor='#77f1ff')
                    btn.grid(row=row, column=col, sticky='ew')
                    if found_info_past:
                        for i in found_info_past:
                            if str(first_ln_num) in i[0]:
                                btn['bg'] = '#cdcdcd'
                                break
                        else:
                            btn['bg'] = "#cefeed"
                            if not active_ln:
                                active_ln = True
                                txt_ln_num.delete(0, 'end')
                                txt_ln_num.insert(0, f"{first_ln_text} {first_ln_num}")

                    col += 1
                    first_ln_num += 1
                    if col == 5:
                        col = 0
                        row += 1
                frame_ln_my_blanks_local_1.columnconfigure(index='all', minsize=40, weight=1)
                frame_ln_my_blanks_local_1.rowconfigure(index='all', minsize=20)

                frame_ln_my_blanks_local_1.pack(fill='both', expand=True)

            frame_ln_my_blanks_local_1 = Frame(frame_ln_my_blanks_local, padx=1, pady=1)
            if type_ln == 'Лист ВН':
                Label(master=frame_ln_my_blanks_local_1, text="Новый десяток Листков ВН",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white').grid(row=row, column=col, sticky='ew', columnspan=2)
                col += 2
                Label(master=frame_ln_my_blanks_local_1, text="Серия:",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white').grid(row=row, column=col, sticky='ew')
                col += 1

                my_new_txt_ln_text = Entry(frame_ln_my_blanks_local_1, width=5,
                                           justify="center",
                                           font=('Comic Sans MS', user.get('text_size')))
                my_new_txt_ln_text.grid(row=row, column=col, sticky='ew')
                my_new_txt_ln_text.insert(0, 'ВА')
                col += 1
                Label(master=frame_ln_my_blanks_local_1, text="Номер:",
                      font=('Comic Sans MS', user.get('text_size')), bg='white').grid(row=row, column=col, sticky='ew')
                col += 1

            else:
                Label(master=frame_ln_my_blanks_local_1, text="Новый десяток Справок ВН",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white').grid(row=row, column=col, sticky='ew', columnspan=2)
                col += 2
                Label(master=frame_ln_my_blanks_local_1, text="Номер:",
                      font=('Comic Sans MS', user.get('text_size')), bg='white').grid(row=row, column=col, sticky='ew')
                col += 1
            check_new_ln = (root_examination.register(is_valid__new_ln), "%P")
            my_new_txt_ln_num = Entry(frame_ln_my_blanks_local_1, width=15,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      justify="center",
                                      validatecommand=check_new_ln,
                                      validate="all")

            my_new_txt_ln_num.grid(row=row, column=col, sticky='ew')
            col += 1
            Button(frame_ln_my_blanks_local_1, text='Применить', font=('Comic Sans MS', user.get('text_size')),
                   command=add_my_new_ln).grid(row=row, column=col, sticky='ew')

            frame_ln_my_blanks_local_1.columnconfigure(index='all', minsize=40, weight=1)
            frame_ln_my_blanks_local_1.rowconfigure(index='all', minsize=20)
            frame_ln_my_blanks_local_1.pack(fill='both', expand=True)

            frame_ln_my_blanks_local.columnconfigure(index='all', minsize=40, weight=1)
            frame_ln_my_blanks_local.rowconfigure(index='all', minsize=20)
            frame_ln_my_blanks_local.pack(fill='both', expand=True, padx=2, pady=2)

            frame_ln_my_blanks.pack(fill='both', expand=True, padx=2, pady=2)

    frame_ln_main = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_ln = Frame(frame_ln_main, relief="solid", padx=1, pady=1)
    frame_ln_add = Frame(frame_ln, borderwidth=1, relief="solid", padx=1, pady=1)
    frame_ln_my_blanks = Frame(frame_ln_main, borderwidth=1, relief="solid", padx=1, pady=1)
    but_ln_my_blanks = Button(frame_ln, text='Мои бланки',
                              font=('Comic Sans MS', user.get('text_size')),
                              command=open_frame_ln_my_blanks)

    frame_second_examination = Frame(examination_root, relief="solid", padx=1, pady=1)

    txt_ln_num = Entry(frame_ln_add, width=15, font=('Comic Sans MS', user.get('text_size')))
    txt_ln_from = Entry(frame_ln_add, width=15, font=('Comic Sans MS', user.get('text_size')))
    txt_ln_until = Entry(frame_ln_add, width=15, font=('Comic Sans MS', user.get('text_size')))
    txt_second_examination = Entry(frame_second_examination, width=15,
                                   font=('Comic Sans MS', user.get('text_size')))
    lbl_type_ln = Label(master=frame_ln_add, text="",
                        font=('Comic Sans MS', user.get('text_size')), bg='white')
    lbl_ln_from = Label(master=frame_ln_add, text=" с ",
                        font=('Comic Sans MS', user.get('text_size')), bg='white')
    but_ln_closed = Button(frame_ln_add, text='закрыть к труду',
                           font=('Comic Sans MS', user.get('text_size')),
                           command=ln_closed)

    paste_frame_ln()

    def paste_calendar(text_field):
        command, marker = text_field.split('__')

        calendar_root = Toplevel()
        calendar_root.title(f'Календарь {marker}')
        calendar_root.config(bg='white')

        selected_day = StringVar()
        actual_data = dict()

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
            day = selected_day.get()
            if day.isdigit():
                year = actual_data.get('year')
                month = actual_data.get('month')
                if len(day) == 1:
                    day = f"0{day}"
                answer = f"{day}.{month}.{year}"
            else:
                answer = datetime.now().strftime("%d.%m.%Y")

            if command == 'ln_from':
                txt_ln_from.delete(0, 'end')
                txt_ln_from.insert(0, answer)

            if command == 'ln_until':
                txt_ln_until.delete(0, 'end')
                txt_ln_until.insert(0, answer)

                txt_second_examination.delete(0, 'end')
                txt_second_examination.insert(0, answer)

            if command == 'second_examination':
                txt_second_examination.delete(0, 'end')
                txt_second_examination.insert(0, answer)

            calendar_root.destroy()

        frame_month_year = Frame(calendar_root, relief="solid", padx=1, pady=1)

        but_prev_month = Button(frame_month_year, text='<', command=prev_month,
                                font=('Comic Sans MS', user.get('text_size')))
        but_prev_month.grid(column=0, row=0, sticky='ew')

        lbl_month_year = Label(frame_month_year, text="", font=('Comic Sans MS', user.get('text_size')),
                               bg='white')
        lbl_month_year.grid(column=1, row=0, sticky='ew')

        but_next_month = Button(frame_month_year, text='>', command=next_month,
                                font=('Comic Sans MS', user.get('text_size')))
        but_next_month.grid(column=2, row=0, sticky='ew')

        frame_month_year.columnconfigure(index='all', minsize=40, weight=1)
        frame_month_year.rowconfigure(index='all', minsize=20)
        frame_month_year.pack(fill='both', expand=True)

        def create_calendar():
            year = actual_data.get('year')
            month = actual_data.get('month')

            if destroy_elements.get('calendar_frame_days'):
                frame_days = destroy_elements.get('calendar_frame_days')
                frame_days.destroy()

            frame_days = Frame(calendar_root, relief="solid", padx=1, pady=1)
            destroy_elements['calendar_frame_days'] = frame_days

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

            lbl_month_year['text'] = f"{month_name.get(calendar.month_name[month])} {str(year)}"

            # Second row - Week Days
            column = 0
            for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
                lbl = Label(frame_days, text=day, font=('Comic Sans MS', user.get('text_size')), bg='white')
                lbl.grid(column=column, row=0, sticky='ew')
                column += 1

            row, col = 0, 0

            my_calendar = calendar.monthcalendar(year, month)
            for week in my_calendar:
                row += 1
                col = 0
                for day in week:
                    if day == 0:
                        col += 1
                    else:
                        day = str(day)
                        btn = Radiobutton(frame_days, text=day,
                                          font=('Comic Sans MS', user.get('text_size')),
                                          value=day, variable=selected_day, command=select_day,
                                          indicatoron=False, selectcolor='#77f1ff')
                        btn.grid(row=row, column=col, sticky='ew')
                        col += 1

                        if datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y").weekday() in (5, 6):
                            btn['bg'] = '#b4ffff'
                        if datetime.now().year == year and datetime.now().month == month and datetime.now().day == int(
                                day):
                            btn['bg'] = '#ff7b81'

            btn = Radiobutton(frame_days, text="Сегодня",
                              font=('Comic Sans MS', user.get('text_size')),
                              value="Сегодня", variable=selected_day, command=select_day,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=row + 1, column=0, sticky='ew', columnspan=7)

            frame_days.columnconfigure(index='all', minsize=40, weight=1)
            frame_days.rowconfigure(index='all', minsize=20)
            frame_days.pack(fill='both', expand=True)

        create_calendar()


def save_document(doc: Document, doc_name: str):
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


def statistic_write(user_id, info):
    date_now, time_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S").split()
    try:
        with sq.connect(r"\\SRV2\data_base\data_base.db") as conn:
            cur = conn.cursor()
            type_info, _, district = info.split('_')
            cur.execute(f"INSERT INTO statistic_DOC_db VALUES('{date_now}', '{time_now}', '{user_id}', "
                        f"'{type_info}', '{district}')")
    except Exception:
        pass


def save_certificate_ped_div(district_pd, data_cert, type_table):
    try:

        with sq.connect(r"\\SRV2\data_base\data_base.db") as conn:
            cur = conn.cursor()
            if type_table == 'certificate_ped_div':
                cur.execute(f"SELECT num"
                            f" FROM {type_table} WHERE ped_div LIKE '{district_pd}';")
            elif type_table == 'certificate_camp':
                cur.execute(f"SELECT num FROM {type_table} WHERE district LIKE '{district_pd}';")

            numbers = list()
            for num in cur.fetchall():
                if isinstance(num, tuple) and len(num) > 0:
                    num = num[0]
                if num.isdigit():
                    numbers.append(int(num))
            if len(numbers) == 0:
                numbers.append(0)

            number = max(numbers) + 1
            if type_table == 'certificate_ped_div':
                data_cert[2] = number
                cur.execute(f"INSERT INTO certificate_ped_div VALUES({'?, ' * 8}?)", data_cert)

            elif type_table == 'certificate_camp':
                data_cert[1] = number
                cur.execute(f"INSERT INTO certificate_camp VALUES({'?, ' * 6}?)", data_cert)
    except Exception as ex:
        print(ex)
        return '__________'
    return number


def data_base():
    with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS врачи "
                    "(doctor_name text, district text, ped_div text, "
                    "manager text, open_mark text, text_size text)")
        cur.execute("CREATE TABLE IF NOT EXISTS examination "
                    "(date_time text, doctor_name text, status text, "
                    "LN_type text, patient_info text, examination_text text, "
                    "examination_key text, add_info text)")
        cur.execute("CREATE TABLE IF NOT EXISTS my_saved_diagnosis "
                    "(doctor_name text, diagnosis text, examination_key text)")
        cur.execute("CREATE TABLE IF NOT EXISTS my_LN "
                    "(doctor_name text, ln_type text, ln_num text)")
        cur.execute("CREATE TABLE IF NOT EXISTS my_sport_section "
                    "(doctor_name text, sport_section text)")

        cur.execute(f"SELECT doctor_name FROM врачи")
        doctor_data = list()
        for i in cur.fetchall():
            doctor_data.append(i[0])
        if not doctor_data:
            cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)", ['Иванов И.И.', 1, 1, 'Петров П.П.', True, 20])

        cur.execute(f"SELECT doctor_name, district, ped_div, manager, open_mark FROM врачи")
        flag = False
        doctor_data = cur.fetchall()
        for doctor_name, district, ped_div, manager, open_mark in doctor_data:
            if open_mark:
                flag = True
        if not flag:
            cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE 'Иванов И.И.'")
            cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)", ['Иванов И.И.', 1, 1, 'Петров П.П.', True, 20])


def updating_patient_data_base():
    try:
        shutil.copy2(r"\\SRV2\data_base\patient_data_base.db", f".{os.sep}data_base{os.sep}patient_data_base.db")
    except Exception as ex:
        messagebox.showinfo('Ошибка', f'Ошибка обновления базы данных!\n{ex}\nПопытка логирования')
        try:
            import subprocess
            subprocess.call(r'cmd /c "net use n: \\SRV2\data_base /Иван/profkiller97"')
            shutil.copy2(r"\\SRV2\data_base\patient_data_base.db", f".{os.sep}data_base{os.sep}patient_data_base.db")

        except Exception as ex:
            messagebox.showinfo('Ошибка', f'Ошибка обновления базы данных!\n{ex}\nLOGGING FAILED')
        else:
            messagebox.showinfo('Успех!', 'База данных обновлена\nлогирование успешно')
    else:
        messagebox.showinfo('Успех!', 'База данных обновлена')


def get_doctor_data():
    with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
        cur = conn.cursor()

        cur.execute(f"SELECT doctor_name, district, ped_div, manager, text_size FROM врачи "
                    f"WHERE open_mark LIKE '1'")
    return cur.fetchone()


def get_doc_names():
    with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT doctor_name, open_mark FROM врачи")
        all_doctors = list()
        for doctor_name, mark in cur.fetchall():
            if mark == '1':
                all_doctors.insert(0, doctor_name)
            else:
                all_doctors.append(doctor_name)

    return all_doctors


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


def certificate_cmd():
    if not patient.get('name'):
        messagebox.showinfo('Ошибка', "Не выбран пациент!")
    else:
        data.clear()
        render_data.clear()

        data['text_size'] = user.get('text_size')

        if not data.get('patient'):
            data['patient'] = dict()
        data['patient']['name'] = patient.get('name', '')
        data['patient']['birth_date'] = patient.get('birth_date', '')
        data['patient']['gender'] = patient.get('gender', '')
        data['patient']['amb_cart'] = patient.get('amb_cart', '')
        data['patient']['patient_district'] = patient.get('patient_district', '')
        data['patient']['address'] = patient.get('address', '')

        if not data.get('doctor'):
            data['doctor'] = dict()
        data['doctor']['doctor_name'] = user.get('doctor_name', '')
        data['doctor']['manager'] = user.get('manager', '')
        data['doctor']['ped_div'] = user.get('ped_div', '')
        data['doctor']['doctor_district'] = user.get('doctor_district', '')

        if not data.get('certificate'):
            data['certificate'] = dict()

        certificate__ask_type_certificate()


def certificate__ask_type_certificate():
    def select_type_certificate(event):
        num = ''
        for i in str(event.widget).split('.!')[-1]:
            if i.isdigit():
                num += i
        data['certificate']['type_certificate'] = all_data_certificate.get('type')[int(num) - 2]
        type_cert_root.destroy()
        type_cert_root.quit()
        certificate__editing_certificate()

    type_cert_root = Toplevel()
    type_cert_root.geometry('+0+0')

    type_cert_root.title('Выбор справки')
    type_cert_root.config(bg='white')

    Label(type_cert_root, text='Какую справку создать?\n',
          font=('Comic Sans MS', data.get('text_size')), bg='white').grid()
    for text in all_data_certificate.get('type'):
        lbl_0 = Label(type_cert_root, text=text,
                      font=('Comic Sans MS', data.get('text_size')), border=1, compound='left',
                      bg='#f0fffe', relief='ridge')
        lbl_0.grid(ipadx=2, ipady=2, padx=2, pady=2, sticky='ew')
        lbl_0.bind('<Button-1>', select_type_certificate)

    type_cert_root.mainloop()


def certificate__editing_certificate():
    destroy_elements = dict()
    edit_cert_root = Toplevel()
    edit_cert_root.geometry('+0+0')

    edit_cert_root.bind("<Control-KeyPress>", keypress)

    type_certificate = data['certificate'].get('type_certificate')

    edit_cert_root.title(f'Редактирование справки {type_certificate}')
    edit_cert_root.config(bg='white')

    Label(edit_cert_root, text=f"Данные пациента:\n"
                               f"Участок: {data['patient'].get('patient_district')};    "
                               f"№ амб: {data['patient'].get('amb_cart')};\n"
                               f"ФИО: {data['patient'].get('name')};    "
                               f"{data['patient'].get('birth_date')};    "
                               f"пол: {data['patient'].get('gender')};\n"
                               f"Адрес: {data['patient'].get('address')};",

          font=('Comic Sans MS', data.get('text_size')), bg='white').pack(fill='both', expand=True,
                                                                          padx=2, pady=2)
    if not all_data_certificate['all_info'].get(type_certificate).get('place_of_requirement'):
        frame_place = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':
            text = "Куда оформляетесь?:"
            place = ('Детское Дошкольное Учреждение',
                     'Средняя школа (гимназия)',
                     'ВУЗ (колледж)', 'Кадетское училище')
        else:
            text = "Место требования справки:"
            place = all_data_certificate.get('place')

        Label(frame_place, text=text,
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

        frame_place.columnconfigure(index='all', minsize=40, weight=1)
        frame_place.rowconfigure(index='all', minsize=20)
        frame_place.pack(fill='both', expand=True, padx=2, pady=2)

        destroy_elements['place_of_requirement'] = list()

        def select_place():
            data['certificate']['place_of_requirement'] = selected_place.get()
            for el in destroy_elements.get('place_of_requirement'):
                el.destroy()
            Label(frame_place, text=f" {selected_place.get()}",
                  font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=1, row=0, sticky='e')

            if type_certificate == "Оформление в ДДУ / СШ / ВУЗ" and selected_place.get() == 'ВУЗ (колледж)':
                Label(frame_specialties, text="Специальности для поступления:",
                      font=('Comic Sans MS', data.get('text_size')), bg='white').pack(fill='both', expand=True,
                                                                                      padx=2, pady=2)
                specialties_txt.pack(fill='both', expand=True, padx=2, pady=2)

                frame_specialties.columnconfigure(index='all', minsize=40, weight=1)
                frame_specialties.rowconfigure(index='all', minsize=20)
                frame_specialties.pack(fill='both', after=frame_place, expand=True, padx=2, pady=2)
                frame_select_desk.destroy()

            frame_place.update()

            # el.quit()

            # frame_place.columnconfigure(index='all', minsize=1, weight=1)
            # frame_place.rowconfigure(index='all', minsize=1)
            # frame_place.config(width=1)

        frame_specialties = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)
        specialties_txt = ScrolledText(frame_specialties, width=80, height=2,
                                       font=('Comic Sans MS', data.get('text_size')), wrap="word")

        selected_place = StringVar()
        frame_place_1 = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)
        destroy_elements['place_of_requirement'].append(frame_place_1)

        row, col = 0, 0
        for mark in place:
            btn = Radiobutton(frame_place_1, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_place, command=select_place,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=row, column=col, sticky='ew')
            col += 1
            if col == 3:
                row += 1
                col = 0

            frame_place_1.columnconfigure(index='all', minsize=40, weight=1)
            frame_place_1.rowconfigure(index='all', minsize=20)
            frame_place_1.pack(fill='both', expand=True, padx=2, pady=2)

    if type_certificate in ('На кружки и секции', 'Может работать по специальности...'):

        def close_frame_hobby():
            frame_hobby.destroy()
            frame_hobby.update()

        def append_hobby():

            hobby_txt.delete(0, 'end')

            for hobby in data['certificate'].get('regime_but'):
                if data['certificate']['regime_but'][hobby].get() == 1:
                    if len(hobby_txt.get()) == 0:
                        if hobby != '+ СОРЕВНОВАНИЯ':
                            hobby_txt.insert(0, hobby)
                        else:
                            hobby_txt.insert(0, 'участия в соревнованиях по ')
                    else:
                        if hobby != '+ СОРЕВНОВАНИЯ':
                            hobby_txt.insert('end', f", {hobby}")
                        else:
                            hobby_txt.insert('end', ' и участия в соревнованиях')

        def save_new_hobby():
            if not new_hobby_txt.get():
                messagebox.showerror('Ошибка', "Не указан кружок / секция для сохранения")
                new_hobby_txt.focus()
            else:
                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                    cursor = connect.cursor()
                    cursor.execute("INSERT INTO my_sport_section VALUES(?, ?)",
                                   [user.get('doctor_name'), new_hobby_txt.get()])
                messagebox.showinfo('Инфо', "Секция сохранена в избранное")
                edit_cert_root.destroy()
                certificate__editing_certificate()

        def delete_new_hobby():

            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                cursor = connect.cursor()
                # cursor.execute("CREATE TABLE IF NOT EXISTS my_sport_section "
                #             "(doctor_name text, sport_section text)")
                cursor.execute(f"SELECT rowid, sport_section "
                                f"FROM my_sport_section "
                                f"WHERE doctor_name LIKE '{user.get('doctor_name')}' ")
                found_info = cursor.fetchall()
                print(found_info)
            if not found_info:
                messagebox.showinfo('Инфо', "Нет сохраненных данных")

            else:
                def delete_sport_section():
                    with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as connect:
                        cursor = connect.cursor()

                        cursor.execute(f"DELETE FROM my_sport_section "
                                       f"WHERE rowid LIKE '{selected_delete_sport_section.get()}'")

                    delete_new_hobby_root.destroy()
                    delete_new_hobby()

                delete_new_hobby_root = Toplevel()
                delete_new_hobby_root.title('Удаление секций')
                delete_new_hobby_root.config(bg='white')

                selected_delete_sport_section = StringVar()

                Label(delete_new_hobby_root, text="Выберите секцию для удаления", font=('Comic Sans MS', data.get('text_size')),
                      bg='white').pack(fill='both', expand=True, padx=2, pady=2)
                frame_delete_new_hobby = Frame(delete_new_hobby_root, borderwidth=1, relief="solid", padx=4, pady=4)

                col, row = 0, 0
                for rowid, sport_section in found_info:
                    btn = Radiobutton(frame_delete_new_hobby, text=sport_section,
                                      font=('Comic Sans MS', data.get('text_size')),
                                      value=f"{rowid}", variable=selected_delete_sport_section,
                                      command=delete_sport_section, indicatoron=False, selectcolor='#77f1ff')
                    btn.grid(row=row, column=col, sticky='ew')
                    col += 1
                    if col == 5:
                        col = 0
                        row += 1
                frame_delete_new_hobby.columnconfigure(index='all', minsize=40, weight=1)
                frame_delete_new_hobby.rowconfigure(index='all', minsize=20)
                frame_delete_new_hobby.pack(fill='both', expand=True, padx=2, pady=2)



        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)
        if type_certificate == 'На кружки и секции':
            txt = 'Может заниматься:'
        else:
            txt = 'Может работать по специальности:'

        Label(frame, text=txt, font=('Comic Sans MS', data.get('text_size')), bg='white').grid(row=0, column=0)
        hobby_txt = Entry(frame, width=70, font=('Comic Sans MS', data.get('text_size')))
        hobby_txt.grid(column=2, row=0, columnspan=3)

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        if type_certificate == 'На кружки и секции':
            frame_hobby = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

            row, col = 0, 0

            data['certificate']['regime_but'] = dict()
            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                cur = conn.cursor()

                cur.execute("CREATE TABLE IF NOT EXISTS my_sport_section "
                            "(doctor_name text, sport_section text)")
                cur.execute(f"SELECT sport_section "
                            f"FROM my_sport_section "
                            f"WHERE doctor_name LIKE '{user.get('doctor_name')}' ")
                found_info = cur.fetchall()
            if found_info:

                frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

                Label(frame, text='Мои кружки и секции',
                      font=('Comic Sans MS', data.get('text_size')), bg='white').grid(row=0, column=0, sticky='ew')

                col += 1
                for mark in found_info:
                    mark = mark[0]
                    data['certificate']['regime_but'][mark] = IntVar()
                    btn = Checkbutton(frame, text=mark,
                                      font=('Comic Sans MS', data.get('text_size')),
                                      variable=data['certificate']['regime_but'].get(mark), command=append_hobby,
                                      onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff')
                    btn.grid(ipadx=2, ipady=2, padx=2, pady=2, sticky='ew', row=row, column=col)

                    col += 1
                    if col == 5:
                        col = 0
                        row += 1

                    Button(frame, text='Редактировать мой список', command=delete_new_hobby,
                           font=('Comic Sans MS', data.get('text_size'))).grid(ipadx=2, ipady=2, padx=2, pady=2,
                                                                               sticky='ew', row=row, column=col)


                frame.columnconfigure(index='all', minsize=40, weight=1)
                frame.rowconfigure(index='all', minsize=20)
                frame.pack(fill='both', expand=True, padx=2, pady=2)

            frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

            Label(frame, text="Добавить кружок или секцию в избранное: ",
                  font=('Comic Sans MS', data.get('text_size')),
                  bg='white').pack(fill='both', expand=True, side='left')

            new_hobby_txt = Entry(frame, width=70, font=('Comic Sans MS', data.get('text_size')))
            new_hobby_txt.pack(fill='both', expand=True, side='left')
            Button(frame, text='Сохранить', command=save_new_hobby,
                   font=('Comic Sans MS', data.get('text_size'))).pack(fill='both', expand=True, side='left')

            frame.columnconfigure(index='all', minsize=40, weight=1)
            frame.rowconfigure(index='all', minsize=20)
            frame.pack(fill='both', expand=True, padx=2, pady=2)


            row, col = 0, 0

            for mark in all_data_certificate.get('sport_section'):
                data['certificate']['regime_but'][mark] = IntVar()

                btn = Checkbutton(frame_hobby, text=mark,
                                  font=('Comic Sans MS', data.get('text_size')),
                                  variable=data['certificate']['regime_but'].get(mark), command=append_hobby,
                                  onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff')
                btn.grid(ipadx=2, ipady=2, padx=2, pady=2, sticky='ew', row=row, column=col)

                col += 1
                if col == 5:
                    col = 0
                    row += 1


            Button(frame_hobby, text='Скрыть', command=close_frame_hobby,
                   font=('Comic Sans MS', data.get('text_size'))).grid(column=col, row=row, sticky="ew")

            frame_hobby.columnconfigure(index='all', minsize=40, weight=1)
            frame_hobby.rowconfigure(index='all', minsize=20)
            frame_hobby.pack(fill='both', expand=True, padx=2, pady=2)


            frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

            Label(frame, text="Группа здоровья:",
                  font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

            selected_health_group = StringVar()

            def select_health_group():
                data['certificate']['health_group'] = selected_health_group.get()

            for mark in all_data_certificate.get('health').get('group'):
                btn = Radiobutton(frame, text=mark,
                                  font=('Comic Sans MS', data.get('text_size')),
                                  value=mark, variable=selected_health_group,
                                  command=select_health_group, indicatoron=False, selectcolor='#77f1ff')
                btn.grid(row=0, column=(all_data_certificate.get('health').get('group').index(mark) + 1), sticky='ew')

            frame.columnconfigure(index='all', minsize=40, weight=1)
            frame.rowconfigure(index='all', minsize=20)
            frame.pack(fill='both', expand=True, padx=2, pady=2)

            frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

            Label(frame, text="Группа по физ-ре:",
                  font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

            selected_fiz_group = StringVar()

            def select_fiz_group():
                data['certificate']['physical'] = selected_fiz_group.get()

            for mark in all_data_certificate.get('health').get('physical'):
                btn = Radiobutton(frame, text=mark,
                                  font=('Comic Sans MS', data.get('text_size')),
                                  value=mark, variable=selected_fiz_group, command=select_fiz_group,
                                  indicatoron=False, selectcolor='#77f1ff')
                btn.grid(row=0, column=(all_data_certificate.get('health').get('physical').index(mark) + 1),
                         sticky='ew')

            frame.columnconfigure(index='all', minsize=40, weight=1)
            frame.rowconfigure(index='all', minsize=20)
            frame.pack(fill='both', expand=True, padx=2, pady=2)

    if type_certificate == 'По выздоровлении':
        def calendar_ori_from():
            paste_calendar(text_field='ori_from__Болеет с ...')

        def calendar_ori_until():
            paste_calendar(text_field='ori_until__Болеет по ...')

        def calendar_ori_home_regime():
            paste_calendar(text_field='ori_home_regime__Домашний режим до ...')

        def calendar_ori_add_to_childhood():
            paste_calendar(text_field='ori_add_to_childhood__Допуск в детский коллектив с ...')

        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Диагноз:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

        combo_diagnosis = Combobox(frame, font=('Comic Sans MS', data.get('text_size')), state="readonly")
        combo_diagnosis['values'] = ['ОРИ', "ФРК", "Ветряная оспа"]
        combo_diagnosis.current(0)
        combo_diagnosis.grid(column=1, row=0)

        Label(frame, text="c",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=2, row=0, sticky='ew')
        ori_from = Entry(frame, width=15,
                         font=('Comic Sans MS', data.get('text_size')))
        ori_from.grid(column=3, row=0)

        Button(frame, text='Календарь', font=('Comic Sans MS', user.get('text_size')),
               command=calendar_ori_from).grid(row=1, column=3, sticky='ew')

        Label(frame, text="по",
              font=('Comic Sans MS', data.get('text_size')), bg='white',
              compound="center").grid(column=4, row=0, sticky='ew')
        ori_until = Entry(frame, width=15,
                          font=('Comic Sans MS', data.get('text_size')))
        ori_until.grid(column=5, row=0)
        ori_until.insert(0, datetime.now().strftime("%d.%m.%Y"))
        Button(frame, text='Календарь', font=('Comic Sans MS', user.get('text_size')),
               command=calendar_ori_until).grid(row=1, column=5, sticky='ew')

        Label(frame, text="Домашний режим до:",
              font=('Comic Sans MS', data.get('text_size')),
              bg='white', compound="center").grid(column=0, row=3, columnspan=2, sticky='ew')
        ori_home_regime = Entry(frame, width=15, font=('Comic Sans MS', data.get('text_size')))
        ori_home_regime.grid(column=2, row=3)
        Button(frame, text='Календарь', font=('Comic Sans MS', user.get('text_size')),
               command=calendar_ori_home_regime).grid(row=3, column=3, sticky='ew', columnspan=3)

        Label(frame, text="Допуск в детский коллектив с",
              font=('Comic Sans MS', data.get('text_size')),
              bg='white', compound="center").grid(column=0, row=4, columnspan=2, sticky='ew')
        ori_add_to_childhood = Entry(frame, width=15, font=('Comic Sans MS', data.get('text_size')))
        ori_add_to_childhood.grid(column=2, row=4)
        Button(frame, text='Календарь', font=('Comic Sans MS', user.get('text_size')),
               command=calendar_ori_add_to_childhood).grid(row=4, column=3, sticky='ew', columnspan=3)

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

    if type_certificate in ('Годовой медосмотр',
                            'Оформление в ДДУ / СШ / ВУЗ',
                            'В детский лагерь',
                            'Об усыновлении (удочерении)',
                            'Об отсутствии контактов',
                            'Бесплатное питание',
                            'О нуждаемости в сан-кур лечении'):

        frame_chickenpox = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)
        Label(frame_chickenpox, text="Ветрянка:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)
        chickenpox = ["+", "-", "привит"]
        selected_chickenpox = StringVar()

        def select_chickenpox():
            data['certificate']['chickenpox'] = selected_chickenpox.get()

        for mark in chickenpox:
            btn = Radiobutton(frame_chickenpox, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_chickenpox, command=select_chickenpox,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=0, column=(chickenpox.index(mark) + 1), sticky='ew')

        Label(frame_chickenpox, text="Аллергия:", font=('Comic Sans MS', data.get('text_size')),
              bg='white').grid(row=1, column=0)
        allergy = ["-", "+"]
        selected_allergy = StringVar()

        allergy_txt = Entry(frame_chickenpox, width=60,
                            font=('Comic Sans MS', data.get('text_size')))

        def select_allergy():
            data['certificate']['allergy'] = selected_allergy.get()
            for el in destroy_elements.get('allergy'):
                el.destroy()
                if selected_allergy.get() == '+':
                    Label(frame_chickenpox, text="Аллергия на:",
                          font=('Comic Sans MS', data.get('text_size')), bg='white').grid(row=1, column=0)
                    allergy_txt.grid(column=1, row=1, columnspan=3)
                else:
                    Label(frame_chickenpox, text="Аллергоанамнез не отягощен",
                          font=('Comic Sans MS', data.get('text_size')),
                          bg='white').grid(row=1, column=1, columnspan=3)

                frame_chickenpox.update()

        destroy_elements['allergy'] = list()
        for mark in allergy:
            btn = Radiobutton(frame_chickenpox, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_allergy, command=select_allergy,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(column=(allergy.index(mark) + 1), row=1, sticky='ew')
            destroy_elements['allergy'].append(btn)

        frame_chickenpox.columnconfigure(index='all', minsize=40, weight=1)
        frame_chickenpox.rowconfigure(index='all', minsize=20)
        frame_chickenpox.pack(fill='both', expand=True, padx=2, pady=2)

    def diagnosis_kb():
        local_frame_diagnosis = dict()
        local_destroy_elements = list()

        def select_diagnosis(event):

            frame_ = str(event.widget).split('.!')[2].replace('frame', '')
            label_ = str(event.widget).split('.!')[4].replace('label', '')

            selected_diagnosis = all_data_certificate.get('diagnosis')[int(frame_) - 2][int(label_) - 1]
            diagnosis_text.insert(INSERT, f" {selected_diagnosis}")

        def select_category_diagnosis(event):
            widget = ''
            if len(diagnosis_text.get(1.0, 'end')) > 3 and diagnosis_text.get(1.0, 'end')[-3:-1] != '. ':
                diagnosis_text.insert(INSERT, ". ")

            for w in str(event.widget).split('.!'):
                if 'frame' in w:
                    widget = w.replace('frame', '')
            open_button = all_data_certificate.get('diagnosis')[int(widget) - 2][0]
            for el in local_destroy_elements:
                el.destroy()
            local_destroy_elements.clear()
            for key_diagnosis in local_frame_diagnosis:
                if key_diagnosis != open_button:
                    lbl_dig = Label(master=local_frame_diagnosis.get(key_diagnosis), text=f"{key_diagnosis}",
                                    font=('Comic Sans MS', data.get('text_size')), bg='white')
                    lbl_dig.grid(column=0, row=0, sticky='ew')
                    lbl_dig.bind('<Button-1>', select_category_diagnosis)
                    local_destroy_elements.append(lbl_dig)

            frame_diagnosis_in: Frame = Frame(master=local_frame_diagnosis.get(open_button),
                                              borderwidth=1, relief="solid", padx=4, pady=4)
            local_destroy_elements.append(frame_diagnosis_in)

            lbl_dig = Label(frame_diagnosis_in, text=f"{all_data_certificate.get('diagnosis')[int(widget) - 2][0]}",
                            font=('Comic Sans MS', data.get('text_size')), bg='white')
            lbl_dig.grid(column=0, row=0, columnspan=5)
            lbl_dig.bind('<Button-1>', select_category_diagnosis)

            row_, col_ = 1, 0
            for lbl_dig in all_data_certificate.get('diagnosis')[int(widget) - 2][1:]:
                if col_ == 5:
                    row_ += 1
                    col_ = 0
                lbl_01 = Label(frame_diagnosis_in, text=lbl_dig,
                               font=('Comic Sans MS', data.get('text_size')), border=1,
                               compound='left',
                               bg='#f0fffe', relief='ridge')
                lbl_01.grid(ipadx=2, ipady=2, padx=2, pady=2, column=col_, row=row_, sticky='ew')
                lbl_01.bind('<Button-1>', select_diagnosis)
                col_ += 1

            frame_diagnosis_in.columnconfigure(index='all', minsize=40, weight=1)
            frame_diagnosis_in.rowconfigure(index='all', minsize=20)
            frame_diagnosis_in.pack(fill='both', expand=True, padx=2, pady=2)

            # frame_diagnosis_in.grid(column=0, row=0)

            # if tuple_diagnosis[0] == diagnosis_local_data.get('open_buttons', ''):

            # diagnosis_root.destroy()
            # diagnosis_kb()

        def close_diagnosis_kb():
            diagnosis.delete(1.0, 'end')
            diagnosis.insert(INSERT, diagnosis_text.get(1.0, 'end')[:-1])

            diagnosis.focus()
            diagnosis_root.destroy()

        diagnosis_root = Toplevel()
        diagnosis_root.title('Клавиатура диагнозов')
        diagnosis_root.config(bg='white')

        frame_diagnosis = Frame(diagnosis_root, borderwidth=1, relief="solid", padx=2, pady=2)
        Label(frame_diagnosis, text="Диагноз:", font=('Comic Sans MS', user.get('text_size')), bg='white').grid()
        diagnosis_text = ScrolledText(frame_diagnosis, width=70, height=10,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      wrap="word")
        if diagnosis.get(1.0, 'end') == ' \n' or diagnosis.get(1.0, 'end') == '\n':
            diagnosis.delete(1.0, 'end')
        elif len(diagnosis.get(1.0, 'end')) > 1 and diagnosis.get(1.0, 'end') == '\n':
            if diagnosis.get(1.0, 'end') == '\n':
                diagnosis_text.insert(INSERT, diagnosis.get(1.0, 'end')[:-1])
        else:
            diagnosis_text.insert(INSERT, diagnosis.get(1.0, 'end'))
        diagnosis_text.focus()
        diagnosis_text.grid(column=0, row=1, rowspan=6)
        Button(frame_diagnosis, text='Закрыть\nклавиатуру',
               command=close_diagnosis_kb,
               font=('Comic Sans MS', data.get('text_size'))).grid(column=1, row=3)
        frame_diagnosis.columnconfigure(index='all', minsize=40, weight=1)
        frame_diagnosis.rowconfigure(index='all', minsize=20)
        frame_diagnosis.pack(fill='both', expand=True, padx=2, pady=2)

        # frame_diagnosis.grid(padx=2, pady=2, column=0, row=0)

        for tuple_diagnosis in all_data_certificate.get('diagnosis'):
            frame_diagnosis = Frame(diagnosis_root, borderwidth=1, relief="solid", padx=4, pady=4)

            # local_destroy_elements[tuple_diagnosis[0]] = list()
            local_frame_diagnosis[tuple_diagnosis[0]] = frame_diagnosis

            lbl_d = Label(frame_diagnosis, text=f"{tuple_diagnosis[0]}",
                          font=('Comic Sans MS', data.get('text_size')), bg='white')
            local_destroy_elements.append(lbl_d)
            lbl_d.grid(column=0, row=0, sticky="ew")
            lbl_d.bind('<Button-1>', select_category_diagnosis)

            frame_diagnosis.columnconfigure(index='all', minsize=40, weight=1)
            frame_diagnosis.rowconfigure(index='all', minsize=20)
            frame_diagnosis.pack(fill='both', expand=True, padx=2, pady=2)

    if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':
        frame_injury_operation = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame_injury_operation, text="Травмы и операции:", font=('Comic Sans MS', data.get('text_size')),
              bg='white').grid(row=0, column=0)
        injury_operation = ("-", "+")
        selected_injury_operation = StringVar()
        injury_operation_txt = Entry(frame_injury_operation, width=60,
                                     font=('Comic Sans MS', data.get('text_size')))

        def select_injury_operation():
            injury_operation_val = selected_injury_operation.get()
            data['certificate']['injury_operation'] = injury_operation_val
            for el in destroy_elements.get('injury_operation'):
                el.destroy()

            if injury_operation_val == '-':
                Label(frame_injury_operation, text="не было",
                      font=('Comic Sans MS', data.get('text_size')), bg='white').grid(row=0, column=1)
            else:
                injury_operation_txt.grid(column=1, row=0)

        destroy_elements['injury_operation'] = list()
        for mark in injury_operation:
            btn = Radiobutton(frame_injury_operation, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_injury_operation,
                              command=select_injury_operation, indicatoron=False, selectcolor='#77f1ff')
            btn.grid(column=(injury_operation.index(mark) + 1), row=0, sticky='ew')
            destroy_elements['injury_operation'].append(btn)

        frame_injury_operation.columnconfigure(index='all', minsize=40, weight=1)
        frame_injury_operation.rowconfigure(index='all', minsize=20)
        frame_injury_operation.pack(fill='both', expand=True, padx=2, pady=2)

    if type_certificate in ('Годовой медосмотр',
                            'Оформление в ДДУ / СШ / ВУЗ',
                            'В детский лагерь',
                            'Об усыновлении (удочерении)'):

        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Рост (см):",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)
        height = Entry(frame, width=15,
                       font=('Comic Sans MS', data.get('text_size')))
        height.grid(column=1, row=0)

        Label(frame, text="    Вес (кг):",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=2, row=0)
        weight = Entry(frame, width=15,
                       font=('Comic Sans MS', data.get('text_size')))
        weight.grid(column=3, row=0)

        vision = Entry(frame, width=15,
                       font=('Comic Sans MS', data.get('text_size')))
        if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ'):
            Label(frame, text="    Зрение:",
                  font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=4, row=0)
            vision.grid(column=5, row=0)
            age = get_age(data['patient'].get('birth_date'))
            if age >= 4:
                vision.insert(0, '1.0/1.0')
            else:
                vision.insert(0, 'предметное')

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Диагноз:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)
        diagnosis = ScrolledText(frame, width=80, height=4,
                                 font=('Comic Sans MS', data.get('text_size')), wrap="word")
        diagnosis.grid(column=0, row=1, rowspan=4, columnspan=4)

        selected_health_group = StringVar()
        selected_fiz_group = StringVar()
        regime_vars = dict()
        for mark in all_data_certificate.get('health').get('regime'):
            regime_vars[mark] = IntVar()
        selected_diet = StringVar()
        desk_vars = dict()
        for mark in all_data_certificate.get('health').get('desk'):
            desk_vars[mark] = IntVar()

        def diagnosis_healthy():
            diagnosis.delete(1.0, 'end')
            if data['patient'].get('gender', '') == 'женский':
                diagnosis.insert(INSERT, 'Соматически здорова. ')
            else:
                diagnosis.insert(INSERT, 'Соматически здоров. ')
            selected_health_group.set('1')
            data['certificate']['health_group'] = selected_health_group.get()
            selected_fiz_group.set('Основная')
            data['certificate']['physical'] = selected_health_group.get()
            regime_vars['общий'].set(1)
            data['certificate']['regime'] = ["общий"]
            selected_diet.set('Б')
            data['certificate']['diet'] = selected_health_group.get()
            desk_vars['по росту'].set(1)
            data['certificate']['desk'] = ["по росту"]

        Button(frame, text='Здоров', command=diagnosis_healthy,
               font=('Comic Sans MS', data.get('text_size'))).grid(column=1, row=0)

        Button(frame, text='Клавиатура диагнозов', command=diagnosis_kb,
               font=('Comic Sans MS', data.get('text_size'))).grid(column=2, row=0)

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Группа здоровья:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

        def select_health_group():
            data['certificate']['health_group'] = selected_health_group.get()

        for mark in all_data_certificate.get('health').get('group'):
            btn = Radiobutton(frame, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_health_group,
                              command=select_health_group, indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=0, column=(all_data_certificate.get('health').get('group').index(mark) + 1), sticky='ew')

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Группа по физ-ре:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

        def select_fiz_group():
            data['certificate']['physical'] = selected_health_group.get()

        for mark in all_data_certificate.get('health').get('physical'):
            btn = Radiobutton(frame, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_fiz_group,
                              command=select_fiz_group, indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=0, column=(all_data_certificate.get('health').get('physical').index(mark) + 1), sticky='ew')

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Режим:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

        def select_regime():
            result = list()
            for regime in all_data_certificate.get('health').get('regime'):
                if regime_vars.get(regime).get() == 1:
                    result.append(regime)
            data['certificate']['regime'] = result

        for mark in all_data_certificate.get('health').get('regime'):
            btn = Checkbutton(frame, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              variable=regime_vars.get(mark), command=select_regime,
                              onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=0, column=(all_data_certificate.get('health').get('regime').index(mark) + 1), sticky='ew')

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Стол:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

        def select_diet():
            data['certificate']['diet'] = selected_health_group.get()

        for mark in all_data_certificate.get('health').get('diet'):
            btn = Radiobutton(frame, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_diet, command=select_diet,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=0, column=(all_data_certificate.get('health').get('diet').index(mark) + 1), sticky='ew')

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        frame_select_desk = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame_select_desk, text="Парта:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

        def select_desk():
            result = list()
            for desk in all_data_certificate.get('health').get('desk'):
                if desk_vars.get(desk).get() == 1:
                    result.append(desk)
            data['certificate']['desk'] = result

        for mark in all_data_certificate.get('health').get('desk'):
            btn = Checkbutton(frame_select_desk, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              variable=desk_vars.get(mark), command=select_desk,
                              onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=0, column=(all_data_certificate.get('health').get('desk').index(mark) + 1), sticky='ew')

        frame_select_desk.columnconfigure(index='all', minsize=40, weight=1)
        frame_select_desk.rowconfigure(index='all', minsize=20)
        frame_select_desk.pack(fill='both', expand=True, padx=2, pady=2)

    if type_certificate == 'О нуждаемости в сан-кур лечении':
        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Диагноз:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)
        diagnosis = ScrolledText(frame, width=80, height=4,
                                 font=('Comic Sans MS', data.get('text_size')), wrap="word")
        diagnosis.grid(column=0, row=1, rowspan=4, columnspan=4)

        def diagnosis_healthy():
            diagnosis.delete(1.0, 'end')
            if data['patient'].get('gender', '') == 'женский':
                diagnosis.insert(INSERT, 'Соматически здорова. ')
            else:
                diagnosis.insert(INSERT, 'Соматически здоров. ')

        Button(frame, text='Здоров', command=diagnosis_healthy,
               font=('Comic Sans MS', data.get('text_size'))).grid(column=1, row=0)

        Button(frame, text='Клавиатура диагнозов', command=diagnosis_kb,
               font=('Comic Sans MS', data.get('text_size'))).grid(column=2, row=0)

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Профиль санатория:",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0, columnspan=3)

        def select_profile():
            result = list()
            for regime in sanatorium_profile:
                if sanatorium_profile.get(regime).get() == 1:
                    result.append(regime)
            data['certificate']['sanatorium_profile'] = result

        sanatorium_profile = dict()
        for profile in ('пульмонологического', 'гастроэнтерологического', 'ревматологического',
                        'неврологического', 'эндокринологического', 'нефрологического',
                        'гинекологического', 'кардиологического', 'дерматологического',
                        'ортопедотравматологического', 'офтальмологического'):
            sanatorium_profile[profile] = IntVar()
        row, col = 1, 0
        for mark in sanatorium_profile:
            btn = Checkbutton(frame, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              variable=sanatorium_profile.get(mark), command=select_profile,
                              onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=row, column=col, sticky='ew')
            col += 1
            if col == 3:
                col = 0
                row += 1

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

    def create_certificate():
        try:
            for marker in all_data_certificate['all_info'].get(type_certificate):
                render_data[marker] = all_data_certificate['all_info'][type_certificate].get(marker)

            render_data['time'] = datetime.now().strftime("%H:%M")
            render_data['number_cert'] = ''
            render_data['name'] = data['patient'].get('name')
            render_data['birth_date'] = data['patient'].get('birth_date')
            render_data['gender'] = data['patient'].get('gender')
            render_data['address'] = data['patient'].get('address')
            render_data['amb_cart'] = data['patient'].get('amb_cart')

            if not render_data.get('place_of_requirement'):
                if not data['certificate'].get('place_of_requirement'):
                    messagebox.showinfo('Ошибка!', 'Не выбрано место требования справки!')
                    raise ValueError

                render_data['place_of_requirement'] = data['certificate'].get('place_of_requirement')

            render_data['type'] = type_certificate
            if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':
                place_of_req = render_data.get('place_of_requirement')
                if place_of_req == 'Детское Дошкольное Учреждение':
                    render_data['type'] = 'Оформление в Детское Дошкольное Учреждение'
                    render_data['recommendation'] = \
                        render_data.get('recommendation').replace('Режим _',
                                                                  'Режим щадящий 1 мес, затем Режим _') \
                        + "\nМебель по росту"
                if place_of_req == 'Средняя школа (гимназия)':
                    render_data['place_of_requirement'] = 'Средняя школа (гимназия)'
                    render_data['type'] = 'Оформление в Среднюю школу (гимназию)'
                    if data['patient'].get('gender', '') == 'женский':
                        render_data['diagnosis'] += '\nГотова к обучению в ' \
                                                    'общеобразовательной школе с _______ лет'
                    else:
                        render_data['diagnosis'] += '\nГотов к обучению в ' \
                                                    'общеобразовательной школе с _______ лет'

                if place_of_req == 'ВУЗ (колледж)':
                    render_data['type'] = 'Оформление в ВУЗ'
                    render_data['additional_medical_information'] = \
                        render_data.get('additional_medical_information').replace(' Vis OD/OS = __________ ;', '')
                    render_data['recommendation'] = "_____________________________________________"
                    render_data['place_of_requirement'] = 'Для поступления в учреждения высшего, ' \
                                                          'среднего специального и ' \
                                                          'профессионально-технического образования '
                    render_data['diagnosis'] += "\nОтсутствуют медицинские противопоказания " \
                                                f"к обучению по специальности: \n" \
                                                f"{specialties_txt.get(1.0, 'end')}" \
                                                "(пункт 2 приложения к постановлению " \
                                                "МЗ РБ от 25.07.2022г. №71)"

                if place_of_req == 'Кадетское училище':
                    render_data['type'] = 'Оформление в Кадетское училище'
                    render_data['place_of_requirement'] = 'Для обучения в кадетском училище '

                    render_data['additional_medical_information'] = \
                        render_data.get('additional_medical_information') + \
                        '\nОфтальмолог: ________________________________________________________' \
                        '\nНевролог: ___________________________________________________________' \
                        '\nОториноларинголог : _________________________________________________' \
                        '\nСтоматолог: _________________________________________________________' \
                        '\nХирург: _____________________________________________________________' \
                        '\nПедиатр: ____________________________________________________________' \
                        '\nОАК: ________________________________________________________________' \
                        '\nОАМ: ________________________________________________________________' \
                        '\nУЗИ сердца: _________________________________________________________' \
                        '\nУЗИ щитовидной  железы : ____________________________________________'

                    render_data['diagnosis'] += '\nФизическое развитие (выше- ниже-) среднее, (дис-) гармоничное\n' \
                                                'Врачебное профессионально-консультативное заключение: ' \
                                                'отсутствуют медицинские противопоказания к обучению  в ГУО ' \
                                                '«Минском городском  кадетском училище».'

            if render_data.get('date_of_issue') == 'now':
                render_data['date_of_issue'] = datetime.now().strftime("%d.%m.%Y")

            if type_certificate == 'По выздоровлении':
                render_data['diagnosis'] = f"{combo_diagnosis.get()} c {ori_from.get()} по {ori_until.get()}"
                render_data['date_of_issue'] = ori_until.get()

                if ori_home_regime.get():
                    render_data['recommendation'] = f"{render_data.get('recommendation')}\n" \
                                                    f"Домашний режим до {ori_home_regime.get()}"
                if ori_add_to_childhood.get():
                    render_data['recommendation'] = f"{render_data.get('recommendation')}\n" \
                                                    f"Допуск в детский коллектив с {ori_add_to_childhood.get()}"

            if type_certificate == 'Годовой медосмотр':
                date = data['patient'].get('birth_date')
                while datetime.now() > datetime.strptime(date, "%d.%m.%Y"):
                    day, month, year = date.split('.')
                    year = str(int(year) + 1)
                    date = '.'.join([day, month, year])
                if (datetime.now().month == datetime.strptime(date, '%d.%m.%Y').month or
                    (datetime.now() + timedelta(30)).month == datetime.strptime(date, "%d.%m.%Y").month) and \
                        datetime.now().year >= datetime.strptime(date, '%d.%m.%Y').year:
                    day, month, year = date.split('.')
                    year = str(int(year) + 1)
                    date = '.'.join([day, month, year])

                render_data['validity_period'] = (datetime.strptime(date, '%d.%m.%Y') -
                                                  timedelta(1)).strftime('%d.%m.%Y')

            if type_certificate == 'На кружки и секции':
                render_data['place_of_requirement'] = \
                    f"{render_data.get('place_of_requirement')}{hobby_txt.get()}" \
                    f"".replace('участия в соревнованиях по ', '').replace(' и участия в соревнованиях', '')

                render_data['diagnosis'] = \
                    f"{render_data.get('diagnosis')}{hobby_txt.get()}"

                if data['certificate'].get('health_group'):
                    render_data['diagnosis'] = \
                        f"{render_data.get('diagnosis')}\n " \
                        f"Группа здоровья: {data['certificate'].get('health_group')};"

                if data['certificate'].get('physical'):
                    render_data['diagnosis'] = \
                        f"{render_data.get('diagnosis')}" \
                        f"  Группа по физкультуре: {data['certificate'].get('physical')};"

            if type_certificate == 'Может работать по специальности...':
                render_data['diagnosis'] = \
                    f"{render_data.get('diagnosis')} {hobby_txt.get()}"

            if type_certificate in ('Годовой медосмотр',
                                    'Оформление в ДДУ / СШ / ВУЗ',
                                    'В детский лагерь',
                                    'Об усыновлении (удочерении)',
                                    'Об отсутствии контактов',
                                    'Бесплатное питание',
                                    'О нуждаемости в сан-кур лечении'):
                for ex_marker in ('chickenpox', 'allergy'):
                    if not data['certificate'].get(ex_marker):
                        if ex_marker == 'chickenpox':
                            messagebox.showerror('Ошибка!', 'Не указана ветрянка!')
                        if ex_marker == 'allergy':
                            messagebox.showerror('Ошибка!', 'Не указана аллергия!')
                        raise ValueError
                text_past_illnesses = ''
                render_data['chickenpox'] = data['certificate'].get('chickenpox')
                if data['certificate'].get('chickenpox', '') == '+':
                    text_past_illnesses += 'ОРИ, Ветряная оспа; '
                if data['certificate'].get('chickenpox', '') == '-':
                    text_past_illnesses += 'ОРИ; Ветряной оспой не болел; '
                if data['certificate'].get('chickenpox', '') == 'привит':
                    text_past_illnesses += 'ОРИ; от ветряной оспы привит; '

                render_data['allergy'] = data['certificate'].get('allergy', '')
                if data['certificate'].get('allergy', '') == '-':
                    text_past_illnesses += 'Аллергоанамнез: не отягощен; '
                if data['certificate'].get('allergy', '') == '+':
                    text_past_illnesses += 'Аллергоанамнез отягощен: '

                    if len(allergy_txt.get()) > 1:
                        text_past_illnesses += f'\nАллергия на: {allergy_txt.get()}'
                        data['certificate']['allergy'] = f"+\n{allergy_txt.get()}"
                        render_data['allergy'] = f"{render_data.get('allergy')}\n{allergy_txt.get()}"
                "injury_operation"
                if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':

                    render_data['injury'] = data['certificate'].get('injury_operation', '')
                    if data['certificate'].get('injury_operation', '') == '-':
                        text_past_illnesses += 'Травм и операций не было; '
                    if data['certificate'].get('allergy', '') == '+':
                        text_past_illnesses += 'Травмы и операции: '
                        if len(injury_operation_txt.get()) > 1:
                            text_past_illnesses += f'\n{injury_operation_txt.get()}'
                            data['certificate']['injury'] = f"+\n{injury_operation_txt.get()}"
                            render_data['injury'] = f"{render_data.get('allergy')}\n{allergy_txt.get()}"

                if render_data.get('past_illnesses'):
                    render_data['past_illnesses'] = f"{text_past_illnesses}\n{render_data.get('past_illnesses')}"
                else:
                    render_data['past_illnesses'] = text_past_illnesses

            if type_certificate in ('Годовой медосмотр',
                                    'Оформление в ДДУ / СШ / ВУЗ',
                                    'В детский лагерь',
                                    'Об усыновлении (удочерении)'):

                for ex_marker in ('health_group', 'physical', 'regime', 'diet', 'desk'):
                    if not data['certificate'].get(ex_marker):
                        if ex_marker == 'health_group':
                            messagebox.showerror('Ошибка!', 'Не указана группа здоровья!')
                        if ex_marker == 'physical':
                            messagebox.showerror('Ошибка!', 'Не указана группа по физкультуре!')
                        if ex_marker == 'regime':
                            messagebox.showerror('Ошибка!', 'Не указан режим!')
                        if ex_marker == 'diet':
                            messagebox.showerror('Ошибка!', 'Не указана диета!')
                        if ex_marker == 'desk':
                            messagebox.showerror('Ошибка!', 'Не указана рассадка!')
                        raise ValueError

                if not weight.get():
                    messagebox.showerror('Ошибка!', 'Не указан вес!')
                    raise ValueError

                if not weight.get().replace('.', '').replace(',', '').isdigit():
                    messagebox.showerror('Ошибка!', 'Укажите вес цифрами!')
                    raise ValueError

                if not height.get():
                    messagebox.showerror('Ошибка!', 'Не указан рост!')
                    raise ValueError

                if not height.get().replace('.', '').replace(',', '').isdigit():
                    messagebox.showerror('Ошибка!', 'Укажите рост цифрами!')
                    raise ValueError

                if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ'):
                    render_data['visus'] = f"VIS OD/OS\n= {vision.get()}\n"
                    render_data['additional_medical_information'] = \
                        render_data.get('additional_medical_information',
                                        '').replace('Vis OD/OS = __________', f"Vis OD/OS = {vision.get()}")
                else:
                    render_data['visus'] = ''
                render_data["add_diagnosis"] = diagnosis.get(1.0, 'end')[:-1]
                render_data['height'] = height.get().replace(',', '.')
                render_data['weight'] = weight.get().replace(',', '.')
                render_data['group'] = selected_health_group.get()
                render_data['physical'] = selected_fiz_group.get()

                add_med_info = render_data.get('additional_medical_information', '')
                add_med_info = add_med_info.replace('Рост _____ см', f'Рост {height.get()} см')
                add_med_info = add_med_info.replace('Вес _____ кг', f'Вес {weight.get()} кг')
                render_data['additional_medical_information'] = add_med_info

                diagnosis_certificate = render_data.get('diagnosis', '')
                if type_certificate in ('В детский лагерь',
                                        'Об усыновлении (удочерении)'):

                    if len(diagnosis.get(1.0, 'end')) > 2:
                        if diagnosis.get(1.0, 'end').endswith('\n'):
                            diagnosis_certificate = f"{diagnosis.get(1.0, 'end')[:-2]}\n{diagnosis_certificate}"
                        else:
                            diagnosis_certificate = f"{diagnosis.get(1.0, 'end')}\n{diagnosis_certificate}"

                diagnosis_certificate = diagnosis_certificate.replace('Группа здоровья: _',
                                                                      f'Группа здоровья: '
                                                                      f'{selected_health_group.get()}')
                diagnosis_certificate = diagnosis_certificate.replace('Группа по физкультуре: _',
                                                                      f'Группа по физкультуре: '
                                                                      f'{selected_fiz_group.get()}')
                render_data['diagnosis'] = diagnosis_certificate

                recommendation = render_data.get('recommendation', '')
                result = ''
                for regime in data['certificate'].get('regime'):
                    result += f"{regime}, "
                result = result[:-2]
                recommendation = recommendation.replace('Режим _', f'Режим {result}')
                render_data['regime'] = result

                recommendation = recommendation.replace('Стол _', f'Стол {selected_diet.get()}')
                render_data['diet'] = selected_diet.get()

                if (type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ')
                        and render_data.get('type', '') != 'Оформление в ВУЗ'):
                    recommendation += ' Парта _;'
                    result = ''
                    desk_num = list()
                    for desk in data['certificate'].get('desk'):
                        if desk.isdigit():
                            desk_num.append(int(desk))
                    for desk in sorted(desk_num):
                        result += f'{desk} - '
                    if result:
                        result = result[:-2]
                    if 'средний ряд' in data['certificate'].get('desk'):
                        result += 'средний ряд '
                    if 'по росту' in data['certificate'].get('desk'):
                        result += 'по росту'
                    if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ'):
                        if 'Детское Дошкольное Учреждение' in data['certificate'].get('place_of_requirement'):
                            recommendation = recommendation.replace('Парта _', f" Мебель {result}")
                            render_data['desk'] = f"Мебель {result}"
                        else:
                            recommendation = recommendation.replace('Парта _', f" Парта {result}")
                            render_data['desk'] = f"Парта {result}"

                render_data['recommendation'] = recommendation

            if type_certificate == 'О нуждаемости в сан-кур лечении':
                diagnosis_certificate = render_data.get('diagnosis', '')
                if len(diagnosis.get(1.0, 'end')) > 2:
                    if diagnosis.get(1.0, 'end').endswith('\n'):
                        diagnosis_certificate = f"{diagnosis.get(1.0, 'end')[:-2]}\n{diagnosis_certificate}"
                    else:
                        diagnosis_certificate = f"{diagnosis.get(1.0, 'end')}\n{diagnosis_certificate}"
                render_data['diagnosis'] = diagnosis_certificate

                profile_rec = 'Ребенок нуждается в санаторно-курортном лечении: \n'
                for i in data['certificate'].get('sanatorium_profile'):
                    profile_rec += f"{i} профиля \n"
                render_data['recommendation'] = profile_rec[:-2]

        except ValueError:
            edit_cert_root.focus_force()
        else:
            edit_cert_root.quit()
            edit_cert_root.destroy()
            certificate__create_doc()

    Button(edit_cert_root, text='Создать справку', command=create_certificate,
           font=('Comic Sans MS', data.get('text_size'))).pack(fill='both', expand=True, padx=2, pady=2)

    if type_certificate in ('Об обслуживании в поликлинике', 'ЦКРОиР'):
        create_certificate()

    def paste_calendar(text_field):
        command, marker = text_field.split('__')

        calendar_root = Toplevel()
        calendar_root.title(f'Календарь {marker}')
        calendar_root.config(bg='white')

        selected_day = StringVar()
        actual_data = dict()

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
            day = selected_day.get()
            if day.isdigit():
                year = actual_data.get('year')
                month = actual_data.get('month')
                if len(day) == 1:
                    day = f"0{day}"
                answer = f"{day}.{month}.{year}"
            else:
                answer = datetime.now().strftime("%d.%m.%Y")

            if command == 'ori_from':
                ori_from.delete(0, 'end')
                ori_from.insert(0, answer)

            if command == 'ori_until':
                ori_until.delete(0, 'end')
                ori_until.insert(0, answer)

            if command == 'ori_home_regime':
                ori_home_regime.delete(0, 'end')
                ori_home_regime.insert(0, answer)

            if command == 'ori_add_to_childhood':
                ori_add_to_childhood.delete(0, 'end')
                ori_add_to_childhood.insert(0, answer)

            calendar_root.destroy()

        frame_month_year = Frame(calendar_root, relief="solid", padx=1, pady=1)

        but_prev_month = Button(frame_month_year, text='<', command=prev_month,
                                font=('Comic Sans MS', user.get('text_size')))
        but_prev_month.grid(column=0, row=0, sticky='ew')

        lbl_month_year = Label(frame_month_year, text="", font=('Comic Sans MS', user.get('text_size')),
                               bg='white')
        lbl_month_year.grid(column=1, row=0, sticky='ew')

        but_next_month = Button(frame_month_year, text='>', command=next_month,
                                font=('Comic Sans MS', user.get('text_size')))
        but_next_month.grid(column=2, row=0, sticky='ew')

        frame_month_year.columnconfigure(index='all', minsize=40, weight=1)
        frame_month_year.rowconfigure(index='all', minsize=20)
        frame_month_year.pack(fill='both', expand=True)

        def create_calendar():
            year = actual_data.get('year')
            month = actual_data.get('month')

            if destroy_elements.get('calendar_frame_days'):
                frame_days = destroy_elements.get('calendar_frame_days')
                frame_days.destroy()

            frame_days = Frame(calendar_root, relief="solid", padx=1, pady=1)
            destroy_elements['calendar_frame_days'] = frame_days

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

            lbl_month_year['text'] = f"{month_name.get(calendar.month_name[month])} {str(year)}"

            # Second row - Week Days
            column = 0
            for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
                lbl = Label(frame_days, text=day, font=('Comic Sans MS', user.get('text_size')), bg='white')
                lbl.grid(column=column, row=0, sticky='ew')
                column += 1

            row, col = 0, 0

            my_calendar = calendar.monthcalendar(year, month)
            for week in my_calendar:
                row += 1
                col = 0
                for day in week:
                    if day == 0:
                        col += 1
                    else:
                        day = str(day)
                        btn = Radiobutton(frame_days, text=day,
                                          font=('Comic Sans MS', user.get('text_size')),
                                          value=day, variable=selected_day, command=select_day,
                                          indicatoron=False, selectcolor='#77f1ff')
                        btn.grid(row=row, column=col, sticky='ew')
                        col += 1

                        if datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y").weekday() in (5, 6):
                            btn['bg'] = '#b4ffff'
                        if datetime.now().year == year and datetime.now().month == month and datetime.now().day == int(
                                day):
                            btn['bg'] = '#ff7b81'

            btn = Radiobutton(frame_days, text="Сегодня",
                              font=('Comic Sans MS', user.get('text_size')),
                              value="Сегодня", variable=selected_day, command=select_day,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=row + 1, column=0, sticky='ew', columnspan=7)

            frame_days.columnconfigure(index='all', minsize=40, weight=1)
            frame_days.rowconfigure(index='all', minsize=20)
            frame_days.pack(fill='both', expand=True)

        create_calendar()

    edit_cert_root.mainloop()


def certificate__create_doc():
    type_certificate = data['certificate'].get('type_certificate', '')

    if not render_data.get('additional_medical_information'):
        render_data['additional_medical_information'] = '_' * 60
    if not render_data.get('past_illnesses'):
        render_data['past_illnesses'] = '_' * 60
    if not render_data.get('recommendation'):
        render_data['recommendation'] = '_' * 50

    render_data['doctor_name'] = data['doctor'].get('doctor_name')

    if (type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ')
            and render_data.get('place_of_requirement') in ('Средняя школа (гимназия)',
                                                            'Детское Дошкольное Учреждение')):
        render_data['recommendation'] = f"{render_data.get('recommendation', '')} \nРазрешены занятия в бассейне"
        if (data['doctor'].get('doctor_district') == '19'
                and render_data.get('place_of_requirement') != 'Средняя школа (гимназия)'):
            render_data['recommendation'] = \
                render_data.get('recommendation', '').replace('\nРазрешены занятия в бассейне', '')

    if type_certificate in ('ЦКРОиР', 'О нуждаемости в сан-кур лечении',
                            'Об усыновлении (удочерении)', 'Бесплатное питание') \
            or (data['certificate'].get('type_certificate') == 'Оформление в ДДУ / СШ / ВУЗ' and not
    ('Для поступления в учреждения высшего' in render_data.get('place_of_requirement') or
     ('Для обучения в кадетском училище' in render_data.get('place_of_requirement')))):
        doctor_name, district, pediatric_division = (data['doctor'].get('doctor_name'),
                                                     data['doctor'].get('doctor_district'),
                                                     data['doctor'].get('ped_div'))
        if pediatric_division in ('1', '2'):
            if data['certificate'].get('type_certificate') in ('ЦКРОиР', 'Бесплатное питание'):
                type_cert = '7.9'
            else:
                type_cert = '7.6'
            info = [pediatric_division,
                    district,
                    None,
                    datetime.now().strftime("%d.%m.%Y"),
                    render_data.get('name'),
                    render_data.get('birth_date'),
                    render_data.get('address'),
                    type_cert,
                    doctor_name]
            number = save_certificate_ped_div(data_cert=info,
                                              type_table='certificate_ped_div',
                                              district_pd=pediatric_division)
            render_data['number_cert'] = f"№ {number}"
        else:
            render_data['number_cert'] = f"№ _________"

    if data['certificate'].get('type_certificate') in ('Годовой медосмотр',
                                                       'Оформление в ДДУ / СШ / ВУЗ',
                                                       'В детский лагерь',
                                                       'Об усыновлении (удочерении)'):

        age = get_age(data['patient'].get('birth_date'))
        if age >= 5:
            render_data['covid_vac'] = 'Предложена вакцинация против инфекции COVID-19\n' \
                                       'Родители отказываются от проведения вакцинации'
        else:
            render_data['covid_vac'] = ' '

        if data['certificate'].get('type_certificate') == 'Оформление в ДДУ / СШ / ВУЗ' or age >= 11:
            render_data['hearing'] = '\nСлух в норме.'
        else:
            render_data['hearing'] = ''

        if age >= 4:
            render_data['posture'] = '\nОсанка не нарушена.'
        else:
            render_data['posture'] = ''
        anthropometry = {
            'мужской': {
                'weight': {
                    1: [8.5, 8.9, 9.4, 10, 10.9, 11.6, 12.1, 1000],
                    2: [10.6, 11, 11.7, 12.6, 13.5, 14.2, 15, 1000],
                    3: [12.1, 12.8, 13.8, 14.8, 16, 16.9, 17.7, 1000],
                    4: [13.4, 14.2, 15.1, 16.4, 17.8, 19.4, 20.3, 1000],
                    5: [14.8, 15.7, 16.8, 18.3, 20, 21.7, 23.4, 1000],
                    6: [16.3, 17.5, 18.8, 20.4, 22.6, 24.7, 26.7, 1000],
                    7: [18, 19.5, 21, 22.9, 25.4, 28, 30.8, 1000],
                    8: [20, 21.5, 23.3, 25.5, 28.3, 31.4, 35.5, 1000],
                    9: [21.9, 23.5, 25.6, 28.1, 31.5, 35.1, 39.1, 1000],
                    10: [23.9, 25.6, 28.2, 31.4, 35.1, 39.7, 44.7, 1000],
                    11: [26, 28, 31, 34.9, 39.9, 44.9, 51.5, 1000],
                    12: [28.2, 30.7, 34.4, 38.8, 45.1, 50.6, 58.7, 1000],
                    13: [30.9, 33.8, 38, 43.4, 50.6, 56.8, 66, 1000],
                    14: [34.3, 38, 42.8, 48.8, 56.6, 63.4, 73.2, 1000],
                    15: [38.7, 43, 48.3, 54.8, 62.8, 70, 80.1, 1000],
                    16: [44, 48.3, 54, 61, 69.6, 76.5, 84.7, 1000],
                    17: [49.3, 54.6, 59.8, 66.3, 74, 80.1, 87.8, 1000]},
                'height': {
                    1: [71.2, 72.3, 74, 75.5, 77.3, 79.7, 81.7, 1000],
                    2: [81.3, 83, 84.5, 86.8, 89, 90.8, 94, 1000],
                    3: [88, 90, 92.3, 96, 99.8, 102, 104.5, 1000],
                    4: [93.2, 95.5, 98.3, 102, 105.5, 108, 110.6, 1000],
                    5: [98.9, 101.5, 104.4, 108.3, 112, 114.5, 117, 1000],
                    6: [105, 107.7, 110.9, 115, 118.7, 121.1, 123.8, 1000],
                    7: [111, 113.6, 116.8, 121.2, 125, 128, 130.6, 1000],
                    8: [116.3, 119, 122.1, 126.9, 130.8, 134.5, 137, 1000],
                    9: [121.5, 124.7, 125.6, 133.4, 136.3, 140.3, 143, 1000],
                    10: [126.3, 129.4, 133, 137.8, 142, 146.7, 149.2, 1000],
                    11: [131.3, 134.5, 138.5, 143.2, 148.3, 152.9, 156.2, 1000],
                    12: [136.2, 140, 143.6, 149.2, 154.5, 159.5, 163.5, 1000],
                    13: [141.8, 145.7, 149.8, 154.8, 160.6, 166, 170.7, 1000],
                    14: [148.3, 152.3, 156.2, 161.2, 167.7, 172, 176.7, 1000],
                    15: [154.6, 158.6, 162.5, 166.8, 173.5, 177.6, 181.6, 1000],
                    16: [158.8, 163.2, 166.8, 173.3, 177.8, 182, 186.3, 1000],
                    17: [162.8, 166.6, 171.6, 177.3, 181.6, 186, 188.5, 1000]}},

            'женский': {
                'weight': {
                    1: [8, 8.5, 9, 9.6, 10.2, 10.8, 11.3, 1000],
                    2: [10.2, 10.8, 11.3, 12.1, 12.8, 13.5, 14.1, 1000],
                    3: [11.7, 12.5, 13.3, 13.7, 15.5, 16.5, 17.6, 1000],
                    4: [13, 14, 14.8, 15.9, 17.6, 18.9, 20, 1000],
                    5: [14.7, 15.7, 16.6, 18.1, 19.7, 21.6, 23.2, 1000],
                    6: [16.3, 17.4, 18.7, 20.4, 22.5, 24.8, 27.1, 1000],
                    7: [17.9, 19.4, 20.6, 22.7, 25.3, 28.3, 31.6, 1000],
                    8: [20, 21.4, 23, 25.1, 28.5, 32.1, 36.3, 1000],
                    9: [21.9, 23.4, 25.5, 28.2, 32, 36.3, 41, 1000],
                    10: [22.7, 25, 27.7, 30.6, 34.9, 39.8, 47.4, 1000],
                    11: [24.9, 27.8, 30.7, 34.3, 38.9, 44.6, 55.2, 1000],
                    12: [27.8, 31.8, 36, 40, 45.4, 51.8, 63.4, 1000],
                    13: [32, 38.7, 43, 47.5, 52.5, 59, 69, 1000],
                    14: [37.6, 43.8, 48.2, 52.8, 58, 64, 72.2, 1000],
                    15: [42, 46.8, 50.6, 55.2, 60.4, 66.5, 74.9, 1000],
                    16: [45.2, 48.4, 51.8, 56.5, 61.3, 67.6, 75.6, 1000],
                    17: [46.2, 49.2, 52.9, 57.3, 61.9, 68, 76, 1000]},
                'height': {
                    1: [70.1, 71.4, 72.8, 74.1, 75.8, 78, 79.6, 1000],
                    2: [80.1, 81.7, 83.3, 85.2, 87.5, 90.1, 92.5, 1000],
                    3: [89, 90.8, 93, 95.5, 98.1, 100.7, 103.1, 1000],
                    4: [94, 96.1, 98.5, 101.5, 104.1, 106.9, 109.7, 1000],
                    5: [100, 102.5, 104.7, 107.5, 110.7, 113.6, 116.7, 1000],
                    6: [105.3, 108, 110.9, 114.1, 118, 120.6, 124, 1000],
                    7: [111.1, 113.6, 116.9, 120.8, 124.8, 128, 131.3, 1000],
                    8: [116.5, 119.3, 123, 127.2, 131, 134.3, 137.7, 1000],
                    9: [122, 124.8, 128.4, 132.8, 137, 140.5, 144.8, 1000],
                    10: [127, 130.5, 134.3, 139, 142.9, 146.7, 151, 1000],
                    11: [131.8, 136.2, 140.2, 145.3, 148.8, 153.2, 157.7, 1000],
                    12: [137.6, 142.2, 145.9, 150.4, 154.2, 159.2, 163.2, 1000],
                    13: [143, 148.3, 151.8, 155.5, 159.8, 163.7, 168, 1000],
                    14: [147.8, 152.6, 155.4, 159, 163.6, 167.2, 171.2, 1000],
                    15: [150.7, 154.4, 157.2, 161.2, 166, 169.2, 173.4, 1000],
                    16: [151.6, 155.2, 158, 162.5, 166.8, 170.2, 173.8, 1000],
                    17: [152.2, 155.8, 158.6, 162.8, 169.2, 170.4, 174.2, 1000]}
            }
        }

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

        render_data['temp'] = random.choice(['36,6', '36,7', '36,5'])
        render_data['br'] = random.randrange(start=indicator['br'][0], stop=indicator['br'][1], step=2)
        render_data['hr'] = random.randrange(start=indicator['hr'][0], stop=indicator['hr'][1], step=2)
        render_data['bp'] = f"{random.randrange(start=indicator['bp'][0], stop=indicator['bp'][1], step=1)}/" \
                            f"{random.randrange(start=indicator['bp'][2], stop=indicator['bp'][3], step=1)}"

        anthro = ' (выше- ниже-) среднее, (дис-) гармоничное'
        try:
            height = float(render_data.get('height'))
            weight = float(render_data.get('weight'))
            if render_data.get('gender').lower().startswith('м'):
                anthro_height = anthropometry['мужской']['height'].get(age, [])
                anthro_weight = anthropometry['мужской']['weight'].get(age, [])
            else:
                anthro_height = anthropometry['женский']['height'].get(age, [])
                anthro_weight = anthropometry['женский']['weight'].get(age, [])
            for a_height in anthro_height:
                if height < a_height:
                    index_height = anthro_height.index(a_height)
                    break
            else:
                index_height = 7

            for a_weight in anthro_weight:
                if weight <= a_weight:
                    index_weight = anthro_weight.index(a_weight)
                    break
            else:
                index_weight = 7
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
            elif abs(index_weight - index_height) < 3:
                anthro += 'дисгармоничное'
            else:
                anthro += 'резко дисгармоничное'

            if 'Физическое развитие (выше- ниже-) среднее, (дис-) гармоничное' in render_data.get('diagnosis'):
                render_data['diagnosis'] = \
                    render_data.get('diagnosis').replace('Физическое развитие (выше- ниже-) '
                                                         'среднее, (дис-) гармоничное',
                                                         f"Физическое развитие: {anthro}")
        except Exception:
            pass
        render_data['anthro'] = anthro

        render_data['imt'] = round(float(render_data.get('weight')) /
                                   (float(render_data.get('height')) / 100) ** 2, 1)

        render_data['additional_medical_information'] = render_data.get('additional_medical_information',
                                                                        '').replace(
            'АД ________', f"АД {render_data['bp']} мм.рт.ст.")
        render_data['diagnosis'] = render_data.get('diagnosis', '').replace(
            'школе с _______ лет', f"школе с {age} лет")

    if (type_certificate == "Оформление в ДДУ / СШ / ВУЗ" and "Детское Дошкольное Учреждение"
        not in render_data.get('place_of_requirement')) or type_certificate == 'Об усыновлении (удочерении)':
        doc_name = ""
        if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':
            doc_name = f".{os.sep}generated{os.sep}{data['patient'].get('name').split()[0]}_справка_Оформление.docx"
            if not render_data.get('number_cert'):
                render_data['number_cert'] = '№ ______'
        elif data['certificate'].get('type_certificate') == 'Об усыновлении (удочерении)':
            doc_name = f".{os.sep}generated{os.sep}{data['patient'].get('name').split()[0]}_справка_Об_усыновлении.docx"

        if 'Для поступления в учреждения высшего' in render_data.get('place_of_requirement'):
            render_data['name'] += f'\nИдентификационный № _______________________________'
            age = get_age(data['patient'].get('birth_date'))
            if age >= 17:
                render_data['additional_medical_information'] += '\nФлюорография: № _________ от __ . __ . ____ ' \
                                                                 'Заключение: ОГК без патологии'
            else:
                render_data['additional_medical_information'] += '\nФлюорография: не подлежит по возрасту.'

        manager = data["doctor"].get('manager')
        if manager:
            render_data['manager'] = manager
        else:
            render_data['manager'] = '______________________'

        doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}справка а4 годовая.docx")
        doc.render(render_data)
        doc_name = save_document(doc=doc, doc_name=doc_name)

        file_name_vac = create_vaccination(user_id=data['patient'].get('amb_cart'), size=4)
        if file_name_vac:
            master = Document(doc_name)
            master.add_page_break()
            composer = Composer(master)
            doc_temp = Document(file_name_vac)
            composer.append(doc_temp)
            doc_name = save_document(doc=composer, doc_name=doc_name)

            # composer.save(doc_name)

        os.system(f"start {doc_name}")

        doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}осмотр.docx")
        doc.render(render_data)
        doc_name_exam = f".{os.sep}generated{os.sep}{data['patient'].get('name').split()[0]}_осмотр.docx"
        doc_name_exam = save_document(doc=doc, doc_name=doc_name_exam)

        os.system(f"start {doc_name_exam}")


    else:

        if type_certificate.startswith('ЦКРОиР'):
            doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}выписка ЦКРОиР.docx")
            doc.render(render_data)
            doc_name = f".{os.sep}generated{os.sep}{data['patient'].get('name').split()[0]}_ЦКРОиР.docx"
            doc_name = save_document(doc=doc, doc_name=doc_name)

        elif type_certificate.startswith('Бесплатное питание'):
            doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}Выписка.docx")
            doc.render(render_data)
            doc_name = f".{os.sep}generated{os.sep}{data['patient'].get('name').split()[0]}_" \
                       f"Выписка_Бесплатное_питание.docx"
            doc_name = save_document(doc=doc, doc_name=doc_name)

        elif type_certificate in ('Годовой медосмотр', 'В детский лагерь', "Оформление в ДДУ / СШ / ВУЗ"):
            if data['certificate'].get('type_certificate').startswith('В детский лагерь'):
                info = [data['doctor'].get('doctor_district'),
                        None,
                        datetime.now().strftime("%d.%m.%Y"),
                        render_data.get('name'),
                        render_data.get('birth_date'),
                        render_data.get('gender'),
                        render_data.get('address')]
                number = save_certificate_ped_div(data_cert=info,
                                                  type_table='certificate_camp',
                                                  district_pd=data['doctor'].get('doctor_district'))

                # save_certificate_ped_div(data=info, type_table='certificate_camp')
                render_data['number_cert'] = f"№ {data['doctor'].get('doctor_district')} / {number}"
            if data['certificate'].get('type_certificate').startswith('Оформление в ДДУ / СШ / ВУЗ'):
                manager = data["doctor"].get('manager')
                if manager:
                    render_data['manager'] = manager
                else:
                    render_data['manager'] = '______________________'

            doc_name = f".{os.sep}generated{os.sep}{data['patient'].get('name').split()[0]}_" \
                       f"справка_{type_certificate}.docx".replace(' в ДДУ / СШ / ВУЗ', '').replace(' ', '_')

            master = Document(f".{os.sep}example{os.sep}certificate{os.sep}справка а5.docx")
            master.add_page_break()
            composer = Composer(master)

            if type_certificate in ('В детский лагерь', "Оформление в ДДУ / СШ / ВУЗ"):
                file_name_vac = create_vaccination(user_id=data['patient'].get('amb_cart'), size=5)
                if file_name_vac:
                    doc_temp = Document(file_name_vac)
                    composer.append(doc_temp)
                    master.add_page_break()

            master.add_section()
            master.sections[-1].orientation = WD_ORIENT.LANDSCAPE
            master.sections[-1].page_width = master.sections[0].page_height
            master.sections[-1].page_height = master.sections[0].page_width
            doc_temp = Document(f".{os.sep}example{os.sep}certificate{os.sep}осмотр.docx")
            composer.append(doc_temp)
            doc_name = save_document(doc=composer, doc_name=doc_name)

            # composer.save(doc_name)

            doc = DocxTemplate(doc_name)
            doc.render(render_data)

            doc_name = save_document(doc=doc, doc_name=doc_name)


        else:
            doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}справка а5.docx")
            doc.render(render_data)
            doc_name = f".{os.sep}generated{os.sep}{data['patient'].get('name').split()[0]} " \
                       f"справка {type_certificate}.docx".replace(' ', '_')
            doc_name = save_document(doc=doc, doc_name=doc_name)

            if (data['certificate'].get('type_certificate') in ('В детский лагерь',
                                                                'Может работать по специальности...') or
                    (data['certificate'].get('type_certificate') == 'Об отсутствии контактов' and
                     data['certificate'].get('place_of_requirement') == 'В стационар')):
                file_name_vac = create_vaccination(user_id=data['patient'].get('amb_cart'), size=5)
                if file_name_vac:
                    master = Document(doc_name)
                    master.add_page_break()
                    composer = Composer(master)
                    doc_temp = Document(file_name_vac)
                    composer.append(doc_temp)
                    doc_name = save_document(doc=composer, doc_name=doc_name)

                    # composer.save(doc_name)

        os.system(f"start {doc_name}")

    statistic_write('приложение', f"Справка_DOC_{data['doctor'].get('doctor_name')}")
    data.clear()
    render_data.clear()


def analyzes_cmd():
    if not patient.get('name'):
        messagebox.showinfo('Ошибка', "Не выбран пациент!")
    else:
        data.clear()
        render_data.clear()

        data['text_size'] = user.get('text_size')
        data['patient_name'] = patient.get('name', '')
        data['birth_date'] = patient.get('birth_date', '')
        data['gender'] = patient.get('gender', '')
        data['amb_cart'] = patient.get('amb_cart', '')
        data['patient_district'] = patient.get('patient_district', '')
        data['address'] = patient.get('address', '')

        data['doctor_name'] = user.get('doctor_name', '')
        data['ped_div'] = user.get('ped_div', '')

        analyzes__ask_analyzes()


def analyzes__ask_analyzes():
    analyzes_root = Toplevel()
    analyzes_root.title('Выбор анализов')
    analyzes_root.config(bg='white')
    analyzes_root.geometry('+0+0')

    Label(analyzes_root, text='Выберите анализы',
          font=('Comic Sans MS', data.get('text_size')), bg='white').pack(fill='both', expand=True,
                                                                          padx=2, pady=2)

    def create_analyzes():
        user_analyzes = dict()
        for category_b in all_blanks_anal:
            for analyzes_lbl in analyzes_vars.get(category_b):
                if analyzes_vars[category_b].get(analyzes_lbl).get() == 1:
                    if not user_analyzes.get(category_b):
                        user_analyzes[category_b] = list()
                    user_analyzes[category_b].append(analyzes_lbl)
        analyzes_root.quit()
        analyzes_root.destroy()
        analyzes__create_doc(user_analyzes)

    def select_analyzes():
        for category_b in all_blanks_anal:
            for analyzes_lbl in analyzes_vars.get(category_b):
                if analyzes_vars[category_b].get(analyzes_lbl).get() == 1:
                    active_btn = analyzes_buttons.get(analyzes_lbl)
                    active_btn['text'] = f"✔{analyzes_lbl}"
                    active_btn['bg'] = '#2efefa'
                else:
                    active_btn = analyzes_buttons.get(analyzes_lbl)
                    active_btn['text'] = f"{analyzes_lbl}"
                    active_btn['bg'] = '#cdcdcd'

    def select_category_analyzes():
        for analyzes_lbl in analyzes_category_vars:
            if analyzes_category_vars.get(analyzes_lbl).get() == 1:
                for button in analyzes_lbl.split(' + '):
                    active_btn = analyzes_buttons.get(button)
                    active_btn['text'] = f"✔{button}"
                    active_btn['bg'] = '#2efefa'

                    for category_b in all_blanks_anal:
                        if button in all_blanks_anal.get(category_b):
                            active_btn = analyzes_vars[category_b].get(button)
                            active_btn.set(1)

    analyzes_vars = dict()
    analyzes_buttons = dict()
    for category in all_blanks_anal:
        analyzes_vars[category] = dict()
        for analyzes in all_blanks_anal.get(category)[1:]:
            analyzes_vars[category][analyzes] = IntVar()

    analyzes_category_vars = dict()
    for analyzes in all_blanks_anal.get('add')[1:]:
        analyzes_category_vars[analyzes] = IntVar()

    for category in all_blanks_anal:
        frame = Frame(analyzes_root, borderwidth=1, relief="solid", padx=4, pady=4)

        row, col = 1, 0
        Label(frame, text=f"{all_blanks_anal.get(category)[0]}",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0, columnspan=3,
                                                                              sticky='ew')
        if category == 'add':

            for analyzes in all_blanks_anal.get(category)[1:]:
                btn = Checkbutton(frame, text=analyzes,
                                  font=('Comic Sans MS', data.get('text_size')),
                                  variable=analyzes_category_vars.get(analyzes), command=select_category_analyzes,
                                  onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff', bg='#cdcdcd')
                btn.grid(row=row, column=col, sticky='ew')
                analyzes_buttons[analyzes] = btn
                col += 1
                if col == 3:
                    row += 1
                    col = 0

        else:
            for analyzes in all_blanks_anal.get(category)[1:]:

                btn = Checkbutton(frame, text=analyzes,
                                  font=('Comic Sans MS', data.get('text_size')),
                                  variable=analyzes_vars[category].get(analyzes), command=select_analyzes,
                                  onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff', bg='#cdcdcd')
                btn.grid(row=row, column=col, sticky='ew')
                analyzes_buttons[analyzes] = btn
                col += 1
                if col == 3:
                    row += 1
                    col = 0

        frame.columnconfigure(index='all', minsize=40, weight=1)
        frame.rowconfigure(index='all', minsize=20)
        frame.pack(fill='both', expand=True, padx=2, pady=2)

    Button(analyzes_root, text='Создать документ', command=create_analyzes,
           font=('Comic Sans MS', data.get('text_size'))).pack(fill='both', expand=True, padx=2, pady=2)

    analyzes_root.mainloop()


def analyzes__create_doc(analyzes):
    render_data['ped_div'] = data.get('ped_div')
    render_data['district'] = data.get('patient_district')
    render_data['doc_name'] = data.get('doctor_name')
    render_data['name'] = data.get('patient_name')
    render_data['birth_date'] = data.get('birth_date')
    render_data['address'] = data.get('address')
    render_data['gender'] = data.get('gender')
    render_data['date'] = datetime.now().strftime("%d.%m.%Y")
    render_data['amb_cart'] = data.get('amb_cart')

    if 'ОАК' in analyzes.get('blood', []) \
            and ('ОАК + ФОРМУЛА' in analyzes.get('blood', [])
                 or 'ОАК + СВЕРТЫВАЕМОСТЬ' in analyzes.get('blood', [])):
        pass
        analyzes['blood'].remove('ОАК')

    if 'ГЕПАТИТ' in analyzes.get('blood-inf', []):
        with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT Прививки FROM patient_data WHERE amb_cart LIKE '{data.get('amb_cart')}'")
            vaccination = cur.fetchone()[0]
        if vaccination:
            vaccination = vaccination.split('\n')
            start = vaccination.index('Прививки против гепатита В')
            stop = vaccination.index('Прививки против кори, эпидемического паротита и краснухи')
            text = ''
            counter = 0
            for index in range(start + 1, stop):
                counter += 1
                if counter % 2 == 0:
                    end = '\n'
                else:
                    end = '\t\t'

                index_str = vaccination[index].split('__')
                text += f"V_{counter}: {index_str[1]} --- {index_str[3]} --- {index_str[6]}{end}"
            if not text:
                text = 'Нет данных о вакцинации\n'

        else:
            text = 'Нет данных о вакцинации\n'

        render_data['VGB_vaccination'] = text

    if 'МАЗОК НА КОВИД' in analyzes.get('swab', []):

        with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT Домашний_телефон FROM patient_data WHERE amb_cart LIKE '{data.get('amb_cart')}'")

            phone = cur.fetchone()
        if phone:
            render_data['phone'] = phone[0]
        else:
            render_data['phone'] = '__________________________'

    all_links = list()
    for category in analyzes:
        for anal in analyzes.get(category):
            doc = DocxTemplate(f".{os.sep}example{os.sep}{category}{os.sep}{anal}.docx")
            doc.render(render_data)
            doc.save(f".{os.sep}generated{os.sep}{anal}.docx")
            all_links.append(f".{os.sep}generated{os.sep}{anal}.docx")

    master = Document(all_links.pop(0))
    composer = Composer(master)
    for link in all_links:
        master.add_page_break()
        doc_temp = Document(link)
        composer.append(doc_temp)
    doc_name = f".{os.sep}generated{os.sep}Анализы.docx"
    doc_name = save_document(doc=composer, doc_name=doc_name)

    # composer.save(")
    os.system(f"start {doc_name}")
    statistic_write('приложение', f"Анализы_DOC_{data.get('doctor_name')}")
    render_data.clear()
    data.clear()


def vaccination_cmd():
    file_name_vac = create_vaccination(user_id=patient.get('amb_cart'), size=5)
    if file_name_vac:
        os.system(f"start {file_name_vac}")
    else:
        messagebox.showinfo('Ошибка!', 'Не удалось создать прививки!')


def blanks_cmd():
    if not patient.get('name'):
        messagebox.showinfo('Ошибка', "Не выбран пациент!")
    else:
        data.clear()
        render_data.clear()

        data['text_size'] = user.get('text_size')
        data['patient_name'] = patient.get('name', '')
        data['birth_date'] = patient.get('birth_date', '')
        data['gender'] = patient.get('gender', '')
        data['amb_cart'] = patient.get('amb_cart', '')
        data['patient_district'] = patient.get('patient_district', '')
        data['address'] = patient.get('address', '')

        data['doctor_name'] = user.get('doctor_name', '')
        data['ped_div'] = user.get('ped_div', '')

        create_blanks__ask_type_blanks()


def create_blanks__ask_type_blanks():
    def select_type_blanks(event):
        num = ''
        for i in str(event.widget).split('.!')[-1]:
            if i.isdigit():
                num += i

        doc = DocxTemplate(f".{os.sep}example{os.sep}амб_карта{os.sep}{blanks[int(num) - 2]}.docx")
        doc.render(render_data)
        file_name = f".{os.sep}generated{os.sep}{blanks[int(num) - 2]}_{data.get('patient_name').split()[0]}.docx"
        file_name = save_document(doc=doc, doc_name=file_name)
        os.system(f"start {file_name}")
        statistic_write('приложение', f"Вкладыши_DOC_{data.get('doctor_name')}")

    def close_window():
        data.clear()
        render_data.clear()
        type_blanks_root.destroy()
        type_blanks_root.quit()

    type_blanks_root = Toplevel()
    type_blanks_root.title('Выбор бланков')
    type_blanks_root.config(bg='white')
    type_blanks_root.geometry('+0+0')


    Label(type_blanks_root, text='Какие бланки создать?\n',
          font=('Comic Sans MS', data.get('text_size')), bg='white').pack(fill='both', expand=True, padx=2, pady=2)
    for text in blanks:
        lbl_0 = Label(type_blanks_root, text=text,
                      font=('Comic Sans MS', data.get('text_size')), border=1, compound='left',
                      bg='#f0fffe', relief='ridge')
        lbl_0.pack(fill='both', expand=True, padx=2, pady=2)
        lbl_0.bind('<Button-1>', select_type_blanks)

    Button(type_blanks_root, text='Закрыть окно', command=close_window,
           font=('Comic Sans MS', data.get('text_size'))).pack(fill='both', expand=True, padx=2, pady=2)

    render_data['ped_div'] = data.get('ped_div')
    render_data['district'] = data.get('patient_district')
    render_data['doc_name'] = data.get('doctor_name')
    render_data['name'] = data.get('patient_name')
    render_data['birth_date'] = data.get('birth_date')
    render_data['address'] = data.get('address')
    render_data['gender'] = data.get('gender')
    render_data['date'] = datetime.now().strftime("%d.%m.%Y")
    render_data['amb_cart'] = data.get('amb_cart')

    type_blanks_root.mainloop()


def direction_cmd():
    if not patient.get('name'):
        messagebox.showinfo('Ошибка', "Не выбран пациент!")
    else:
        data.clear()
        render_data.clear()

        data['text_size'] = user.get('text_size')
        data['patient_name'] = patient.get('name', '')
        data['birth_date'] = patient.get('birth_date', '')
        data['gender'] = patient.get('gender', '')
        data['amb_cart'] = patient.get('amb_cart', '')
        data['patient_district'] = patient.get('patient_district', '')
        data['address'] = patient.get('address', '')

        data['doctor_name'] = user.get('doctor_name', '')
        data['ped_div'] = user.get('ped_div', '')
        direction__ask_type_blanks()


def direction__ask_type_blanks():
    type_direct = ('НА ГОСПИТАЛИЗАЦИЮ', 'НА КОНСУЛЬТАЦИЮ', 'НА РЕНТГЕНОГРАММУ')

    type_blanks_root = Toplevel()
    type_blanks_root.title('Направление')
    type_blanks_root.config(bg='white')

    frame_where = Frame(type_blanks_root, borderwidth=1, relief="solid", padx=4, pady=4)
    Label(frame_where, text="Тип направления:",
          font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0)

    selected_where = StringVar()

    def select_where():
        type_direction = selected_where.get()
        data['type_direction'] = type_direction

        if type_direction == 'НА ГОСПИТАЛИЗАЦИЮ':
            frame_hospital.pack(fill='both', expand=True, padx=2, pady=2)
            but_create_doc.pack(fill='both', expand=True, padx=2, pady=2)

        elif type_direction == 'НА КОНСУЛЬТАЦИЮ':
            frame_hospital.pack(fill='both', expand=True, padx=2, pady=2)
            frame_doctor.pack(fill='both', expand=True, padx=2, pady=2)
            but_create_doc.pack(fill='both', expand=True, padx=2, pady=2)
        else:
            type_blanks_root.quit()
            type_blanks_root.destroy()
            direction__create_direction()

    for mark in type_direct:
        btn = Radiobutton(frame_where, text=mark,
                          font=('Comic Sans MS', data.get('text_size')),
                          value=mark, variable=selected_where,
                          command=select_where, indicatoron=False, selectcolor='#77f1ff')
        btn.grid(row=0, column=(type_direct.index(mark) + 1), sticky='ew')

    frame_where.columnconfigure(index='all', minsize=40, weight=1)
    frame_where.rowconfigure(index='all', minsize=20)
    frame_where.pack(fill='both', expand=True, padx=2, pady=2)

    frame_hospital = Frame(type_blanks_root, borderwidth=1, relief="solid", padx=4, pady=4)
    Label(frame_hospital, text="Куда направить:",
          font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0, columnspan=5)

    selected_hospital = StringVar()

    def select_hospital():
        data['hospital'] = selected_hospital.get()

    row, col = 1, 0
    for mark in all_blanks_direction.get('hospital'):
        if '- - -' in mark:
            col = 0
            row += 2
            Label(frame_hospital, text=mark,
                  font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=col, row=row - 1, columnspan=5)
        else:

            btn = Radiobutton(frame_hospital, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_hospital,
                              command=select_hospital, indicatoron=False, selectcolor='#77f1ff')
            btn.grid(row=row, column=col, sticky='ew')
            col += 1
            if col == 5:
                row += 1
                col = 0

    frame_hospital.columnconfigure(index='all', minsize=40, weight=1)
    frame_hospital.rowconfigure(index='all', minsize=20)

    frame_doctor = Frame(type_blanks_root, borderwidth=1, relief="solid", padx=4, pady=4)
    Label(frame_doctor, text="На консультацию:",
          font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0, columnspan=5)

    selected_doctor = StringVar()

    def select_doctor():
        data['direction_doctor'] = selected_doctor.get()

    row, col = 1, 0
    for mark in all_blanks_direction.get('doctor'):

        btn = Radiobutton(frame_doctor, text=mark,
                          font=('Comic Sans MS', data.get('text_size')),
                          value=mark, variable=selected_doctor,
                          command=select_doctor, indicatoron=False, selectcolor='#77f1ff')
        btn.grid(row=row, column=col, sticky='ew')
        col += 1
        if col == 5:
            row += 1
            col = 0

    frame_doctor.columnconfigure(index='all', minsize=40, weight=1)
    frame_doctor.rowconfigure(index='all', minsize=20)

    def create_doc():
        if not data.get('hospital'):
            messagebox.showinfo('Ошибка', 'Не указан стационар')
        else:
            type_blanks_root.quit()
            type_blanks_root.destroy()
            direction__create_direction()

    but_create_doc = Button(type_blanks_root, text='Создать направление', command=create_doc,
                            font=('Comic Sans MS', data.get('text_size')))

    type_blanks_root.mainloop()


def direction__create_direction():
    render_data['ped_div'] = data.get('ped_div')
    render_data['district'] = data.get('patient_district')
    render_data['doc_name'] = data.get('doctor_name')
    render_data['name'] = data.get('patient_name')
    render_data['birth_date'] = data.get('birth_date')
    render_data['address'] = data.get('address')
    render_data['gender'] = data.get('gender')
    render_data['date'] = datetime.now().strftime("%d.%m.%Y")
    render_data['amb_cart'] = data.get('amb_cart')
    render_data['doctor'] = data.get('direction_doctor')
    render_data['address_hospital'] = address_hospital.get(data.get('hospital', ''))

    hospital = data.get('hospital', '')
    if 'РНПЦ' in hospital:
        dispanser = {
            'РНПЦ ДХ': 'РНПЦ Детской хирургии',
            'РНПЦ НиН': 'РНПЦ Неврологии и Нейрохирургии',
            'РНПЦ ТиО': 'РНПЦ Травматологии и Ортопедии',
            'РНПЦ ЛОР': 'РНПЦ Оториноларингологии'}
        if hospital in dispanser:
            hospital = dispanser.get(hospital)
    elif "-я" in hospital:
        dispanser = {
            'ГДП': 'Городская детская поликлиника',
            'ГДКБ': 'Городская детская клиническая больница',
            'ГКБ': 'Городская клиническая больница',
            'ДИКБ': 'Детская инфекционная клиническая больница',
            'ГП': 'Городская поликлиника'
        }

        disp = hospital.split()[-1]
        hospital = hospital.replace(disp, dispanser.get(disp))

    elif "ДИКБ" in hospital:
        hospital = 'Детская инфекционная клиническая больница'
    elif "МГЦМР" in hospital:
        hospital = "Минский городской центр медицинской реабилитации"
    elif "ГККВД" in hospital:
        hospital = "Городской клинический кожно-венерологический диспансер"

    render_data['hospital'] = hospital

    doc = DocxTemplate(f".{os.sep}example{os.sep}direction{os.sep}{data.get('type_direction')}.docx")
    doc.render(render_data)
    file_name = f".{os.sep}generated{os.sep}Направление.docx"
    file_name = save_document(doc=doc, doc_name=file_name)

    if data.get('type_direction') == 'НА ГОСПИТАЛИЗАЦИЮ':
        file_name_vac = create_vaccination(user_id=patient.get('amb_cart'), size=5)
        if file_name_vac:
            master = Document(file_name)
            master.add_page_break()
            composer = Composer(master)
            doc_temp = Document(file_name_vac)
            composer.append(doc_temp)
            file_name = save_document(doc=composer, doc_name=file_name)

            # composer.save(f".{os.sep}generated{os.sep}Направление.docx")

    os.system(f"start {file_name}")
    statistic_write('приложение', f"Направления_DOC_{data.get('doctor_name')}")
    data.clear()
    render_data.clear()


def examination_cmd():
    if not patient.get('name'):
        messagebox.showinfo('Ошибка', "Не выбран пациент!")
    else:
        app_examination = ScrolledRoot(marker='paste_examination_cmd_main')
        app_examination.title(f"Осмотр "
                              f"{patient.get('name').split()[0]} "
                              f"{patient.get('name').split()[1]} "
                              f"{patient.get('birth_date')}")
        app_examination.geometry('+0+0')
        app_examination.mainloop()


def create_vaccination(user_id, size):
    try:
        if size == 5:
            size = 1
        elif size == 4:
            size = 2

        with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT Прививки_шапка, Прививки FROM patient_data WHERE amb_cart LIKE '{user_id}'")
            user_data, vaccination = cur.fetchone()

        document = Document()

        paragraph = document.add_paragraph()
        p = paragraph.add_run(f'{user_data}')
        r_fmt = p.font
        r_fmt.name = 'Times New Roman'
        if size == 2:
            r_fmt.size = Pt(12)
        else:
            r_fmt.size = Pt(10)

        info = ["Возраст",
                "Дата проведения прививки",
                "Тип иммуни-\nзации",
                "Наименование препарата",
                "Страна изготови-\nтель препарата",
                "Доза",
                "Серия",
                "Реакция",
                "Мед. отвод"]

        all_tabs = (
            'Прививки против туберкулёза',
            'Прививки против гепатита В',
            'Прививки против кори, эпидемического паротита и краснухи',
            'Прививки против полиомиелита',
            'Прививки против дифтерии, коклюша, столбняка',
            'Прививки против других инфекций')

        table = document.add_table(rows=(len(vaccination.split('\n')) + 1), cols=9)
        table.style = 'Table Grid'
        # if size == 2:
        #     widths = (Cm(1.5*1.5), Cm(1.8*1.5), Cm(1.5*1.5), Cm(1.5*1.5), Cm(1.5*1.5), Cm(1.5*1.5),
        #     Cm(1.5*1.5), Cm(1.5*1.5), Cm(1.4*1.5))
        # else:
        #     widths = (Cm(1.5), Cm(1.8), Cm(1.2), Cm(1.5), Cm(1.5), Cm(1.5), Cm(1.5), Cm(1.5), Cm(1.4))
        # for row in table.rows:
        #     for idx, width in enumerate(widths):
        #         row.cells[idx].width = width

        hdr_cells = table.rows[0].cells
        for i in range(9):
            hdr_cells[i].text = info[i]

            rc = hdr_cells[i].paragraphs[0].runs[0]
            rc.font.name = 'Times New Roman'
            # rc.font.bold = True
            if size == 2:
                rc.font.size = Pt(10)
            else:
                rc.font.size = Pt(7)

        info = vaccination.split('\n')

        for i in range(1, len(info) + 1):
            hdr_cells = table.rows[i].cells
            if info[i - 1] in all_tabs:
                hdr_cells[0].text = info[i - 1]
                rc = hdr_cells[0].paragraphs[0].runs[0]
                if size == 2:
                    rc.font.size = Pt(10)
                else:
                    rc.font.size = Pt(8)

                hdr_cells[0].merge(hdr_cells[8])
            else:
                loc_info = info[i - 1].split('__')
                for q in range(9):
                    hdr_cells[q].text = loc_info[q]

                    rc = hdr_cells[q].paragraphs[0].runs[0]
                    rc.font.name = 'Times New Roman'
                    if size == 2:
                        rc.font.size = Pt(10)
                    else:
                        rc.font.size = Pt(8)

        if size == 2:
            widths = (
                Cm(1.5 * 1.5), Cm(1.8 * 1.5), Cm(1.5 * 1.5), Cm(1.5 * 1.5), Cm(1.5 * 1.5), Cm(1.5 * 1.5), Cm(1.5 * 1.5),
                Cm(1.5 * 1.5), Cm(1.4 * 1.5))
        else:
            widths = (Cm(1.6), Cm(2.0), Cm(1.0), Cm(1.5), Cm(1.5), Cm(1.5), Cm(1.5), Cm(1.5), Cm(1.4))
        for row in table.rows:
            for idx, width in enumerate(widths):
                row.cells[idx].width = width

        sections = document.sections
        for section in sections:
            section.top_margin = Cm(1.5)
            section.bottom_margin = Cm(1.5)
            section.left_margin = Cm(1.5)
            section.right_margin = Cm(1.5)
            if size == 1:
                section.page_height = Cm(21)
                section.page_width = Cm(14.8)

        file_name_vac = f'.{os.sep}generated{os.sep}прививки.docx'
        file_name_vac = save_document(doc=document, doc_name=file_name_vac)

        if info:
            statistic_write('приложение', f"Прививки_DOC_{user.get('doctor_name')}")

            return file_name_vac

        else:
            return False

    except Exception as ex:
        print('Exception create_vaccination: ', ex)
        return False


def decoding_name(patient_data):
    user_decoded = {
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
                        user_decoded['name'] = f'{info[counter]} {info[counter + 1]}'
                        if '№' not in info[counter + 2]:
                            user_decoded['name'] += f' {info[counter + 2]}'
                    elif i == 'рождения:':
                        user_decoded['birth_date'] = info[counter]
                    elif i == 'Пол:':
                        if info[counter] == 'Жен.':
                            user_decoded['gender'] = 'женский'
                        elif info[counter] == 'Муж.':
                            user_decoded['gender'] = 'мужской'
                    elif i == 'карты:':
                        user_decoded['amb_cart'] = info[counter]
                    elif i == 'Участок:':
                        user_decoded['patient_district'] = ''
                        district = info[counter]
                        for q in district:
                            if q.isdigit():
                                user_decoded['patient_district'] += q
                    elif i == 'Адрес:':
                        address = ''
                        for q in info[counter:]:
                            if ':' in q:
                                break
                            address += q + ' '
                        user_decoded['address'] = address

            elif '№ амб. карты' in text:
                for i in text.split('\n'):
                    if i.split()[0].isdigit():
                        if len(i.split('  ')) == 8:
                            info = i.split('  ')

                            user_decoded['amb_cart'] = info[0]
                            user_decoded['name'] = info[1]
                            user_decoded['birth_date'] = info[2]
                            user_decoded['address'] = info[4]
                            user_decoded['patient_district'] = ''
                            district = info[3]
                            for q in district:
                                if q.isdigit():
                                    user_decoded['patient_district'] += q
                            if len(info[1].split()) == 3:
                                if info[1][-1] == 'ч':
                                    user_decoded['gender'] = 'мужской'
                                elif info[1][-1] == 'а':
                                    user_decoded['gender'] = 'женский'
                                else:
                                    user_decoded['gender'] = 'мужской/женский'
                            else:
                                user_decoded['gender'] = 'мужской/женский'
                            break
                        else:
                            info = i.split()
                            user_decoded['amb_cart'] = info.pop(0)
                            user_decoded['name'] = ''
                            for _ in range(3):
                                if info[0].isalpha():
                                    user_decoded['name'] += f'{info[0]} '
                                    info.pop(0)
                            user_decoded['birth_date'] = info.pop(0)
                            user_decoded['patient_district'] = ''
                            district = info.pop(0)
                            for q in district:
                                if q.isdigit():
                                    user_decoded['patient_district'] += q
                            user_decoded['address'] = ''
                            for i_ in info[info.index('г'):]:
                                if len(i_) == 10 and '.' in i_:
                                    break
                                else:
                                    user_decoded['address'] += f'{i_} '
                            if len(user_decoded.get('name').split()) == 3:
                                if user_decoded.get('name').split()[2][-1] == 'ч':
                                    user_decoded['gender'] = 'мужской'
                                elif user_decoded.get('name').split()[2][-1] == 'а':
                                    user_decoded['gender'] = 'женский'
                                else:
                                    user_decoded['gender'] = 'мужской/женский'
                            else:
                                user_decoded['gender'] = 'мужской/женский'

                            break

            elif '№ амбулаторной карты' in text:

                for i in text.split('\n'):
                    if i.split()[0].isdigit():

                        info = i.split()
                        user_decoded['amb_cart'] = info.pop(0)
                        user_decoded['name'] = ''
                        for _ in range(3):
                            if info[0].isalpha() or info[0] not in ('Ж', 'М'):
                                user_decoded['name'] += f'{info[0]} '
                                info.pop(0)

                        gender = info.pop(0)
                        if gender == 'М':
                            user_decoded['gender'] = 'мужской'
                        elif gender == 'Ж':
                            user_decoded['gender'] = 'женский'
                        else:
                            user_decoded['gender'] = 'мужской/женский'

                        user_decoded['birth_date'] = info.pop(0)

                        user_decoded['patient_district'] = ''
                        district = info.pop(0)
                        for q in district:
                            if q.isdigit():
                                user_decoded['patient_district'] += q

                        user_decoded['address'] = 'г. '
                        for i_ in info[info.index('Минск'):]:
                            if i_.isdigit():
                                user_decoded['address'] += f'{i_} - '
                            else:
                                user_decoded['address'] += f'{i_} '
                        else:
                            user_decoded['address'] = user_decoded['address'][:-2]

                        break

            if not user_decoded.get('gender'):
                user_decoded['gender'] = 'мужской/женский'
            for key, value in user_decoded.items():
                if not value:
                    if key != 'gender':
                        print(f'1) Exception! decoding_name: \ntext:{text}\n', user_decoded.get('amb_cart'),
                              user_decoded.get('district'),
                              user_decoded.get('name'), user_decoded.get('birth_date'), user_decoded.get('gender'),
                              user_decoded.get('address'))

                        raise ValueError

        except (IndexError, ValueError):
            print(f'2) Exception! decoding_name: \ntext:{text}\n', user_decoded.get('amb_cart'),
                  user_decoded.get('district'),
                  user_decoded.get('name'), user_decoded.get('birth_date'), user_decoded.get('gender'),
                  user_decoded.get('address'))
            messagebox.showinfo('Ошибка', 'Ошибка имени! \nВведите шапку полностью!')

        else:
            return user_decoded


def keypress(event):
    if event.keycode == 86 or event.keycode == 150994966:
        event.widget.event_generate('<<Paste>>')
    elif event.keycode == 67 or event.keycode == 134217731:
        event.widget.event_generate('<<Copy>>')
    elif event.keycode == 88 or event.keycode == 117440536:
        event.widget.event_generate('<<Cut>>')


def main_root():

    def paste_log_in_root():
        def edit_local_db():
            edit_local_data = {
                'my_saved_diagnosis': {
                    'my_saved_diagnosis_loc': list(),
                    'my_saved_diagnosis_global': list(),
                    'my_saved_diagnosis_dif': list()},
                'my_LN': {
                    'my_LN_loc': list(),
                    'my_LN_global': list(),
                    'my_LN_dif': list()},
                'my_sport_section': {
                    'my_sport_section_loc': list(),
                    'my_sport_section_global': list(),
                    'my_sport_section_dif': list()}
            }

            doctor_name = selected_doctor_name.get()
            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                cur = conn.cursor()

                cur.execute(f"SELECT date_time, doctor_name, status, LN_type, patient_info, "
                            f"examination_text, examination_key, add_info "
                            f"FROM examination")
                examination_loc = cur.fetchall()

                for marker in edit_local_data:
                    cur.execute(f"SELECT * FROM {marker} "
                                f"WHERE doctor_name LIKE '{doctor_name}'")
                    for i in cur.fetchall():
                        edit_local_data[f"{marker}"][f"{marker}_loc"].append(i)

            try:
                with sq.connect(database=r"\\SRV2\data_base\application_data_base.db", timeout=10.0) as conn:
                    cur = conn.cursor()
                    if examination_loc:
                        for ex_info in examination_loc:
                            cur.execute("INSERT INTO examination VALUES(?, ?, ?, ?, ?, ?, ?, ?)", ex_info)

                    for marker in edit_local_data:
                        cur.execute(f"SELECT * FROM {marker} "
                                    f"WHERE doctor_name LIKE '{doctor_name}'")
                        for i in cur.fetchall():
                            edit_local_data[f"{marker}"][f"{marker}_global"].append(i)

                    for marker in ('my_saved_diagnosis', 'my_sport_section'):
                        for marker_0 in edit_local_data[f"{marker}"].get(f"{marker}_loc"):
                            if marker_0 not in edit_local_data[f"{marker}"].get(f"{marker}_global"):
                                cur.execute(f"INSERT INTO {marker} VALUES({'?, ' * (len(marker_0) - 1) + '?'})",
                                            marker_0)

            except Exception as ex:
                print('Exception edit_local_db()\n', ex)

            else:
                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                    cur = conn.cursor()
                    cur.execute(f"DELETE FROM examination")

                    for marker in ('my_saved_diagnosis', 'my_sport_section'):
                        for marker_0 in edit_local_data[f"{marker}"].get(f"{marker}_global"):
                            if marker_0 not in edit_local_data[f"{marker}"].get(f"{marker}_loc"):
                                cur.execute(f"INSERT INTO {marker} VALUES({'?, ' * (len(marker_0) - 1) + '?'})",
                                            marker_0)

                    if edit_local_data["my_LN"].get("my_LN_global"):
                        cur.execute(f"DELETE FROM my_LN WHERE doctor_name LIKE '{doctor_name}'")
                        for marker_0 in edit_local_data["my_LN"].get("my_LN_global"):
                            cur.execute(f"INSERT INTO my_LN VALUES({'?, ' * (len(marker_0) - 1) + '?'})", marker_0)

        def select_doctor_name():
            if users_passwords.get(selected_doctor_name.get()):
                frame_pass.pack_configure(fill='both', expand=True, padx=2, pady=2)
            else:
                open_main_root()
                frame_pass.pack_forget()

        def open_main_root():
            try:
                edit_local_db()
            except Exception as ex:
                print(ex)
            load_info_text.set(f"LOADING {selected_doctor_name.get()}")
            time.sleep(1)
            log_in_root.update()

            if not user.get('error_connection'):
                user['doctor_name'] = all_users_info.get(selected_doctor_name.get())[0]
                user['password'] = all_users_info.get(selected_doctor_name.get())[1]
                user['doctor_district'] = all_users_info.get(selected_doctor_name.get())[2]
                user['ped_div'] = all_users_info.get(selected_doctor_name.get())[3]
                user['manager'] = all_users_info.get(selected_doctor_name.get())[4]
                user['text_size'] = all_users_info.get(selected_doctor_name.get())[5]
                user['add_info'] = all_users_info.get(selected_doctor_name.get())[6]

            print('USER')
            for i in user:
                print(i, user.get(i))

            data_base()
            paste_frame_main()
            # log_in_root.quit()

        def is_valid__password(password):
            if password == users_passwords.get(selected_doctor_name.get()):
                text_is_correct_password.set('OK')
                open_main_root()
            else:
                text_is_correct_password.set('Пароль не верен!')

            return True

        def connect_to_srv_data_base():

            load_info_text.set(f"{load_info_text.get()}\n"
                               f"Попытка подключения к базе данных...")
            time.sleep(1)
            log_in_root.update()
            if not os.path.exists(path=f".{os.sep}data_base"):
                os.mkdir(path=f".{os.sep}data_base")
            last_edit_srv = None

            try:
                with sq.connect(r"\\SRV2\data_base\patient_data_base.db") as conn:
                    cur = conn.cursor()
                    cur.execute(f"SELECT last_edit FROM last_edit")
                    last_edit_srv = cur.fetchall()[0]
                    load_info_text.set(f"{load_info_text.get()}\n"
                                       f"Соединение с сервером установлено")

            except Exception as ex:
                load_info_text.set(f"{load_info_text.get()}\n"
                                   f"Ошибка подключения к базе данных!\n{ex}\nПопытка логирования")
                try:
                    import subprocess
                    subprocess.call(r'cmd /c "net use n: \\SRV2\patient_data_base /Иван/profkiller97"')

                    with sq.connect(r"\\SRV2\data_base\patient_data_base.db") as conn:
                        cur = conn.cursor()
                        cur.execute(f"SELECT last_edit FROM last_edit")
                        last_edit_srv = cur.fetchall()[0]

                except Exception as ex:
                    load_info_text.set(f"{load_info_text.get()}\n"
                                       f"LOGGING FAILED!\n{ex}\nЗагрузка сохраненных данных")
                    user['error_connection'] = True
                else:
                    load_info_text.set(f"{load_info_text.get()}\n"
                                       f"Логирование завершено успешно")
            time.sleep(1)
            log_in_root.update()

            if last_edit_srv:
                with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
                    cur = conn.cursor()
                    cur.execute(f"SELECT last_edit FROM last_edit")
                    last_edit_loc = cur.fetchall()[0]

                if last_edit_loc != last_edit_srv:
                    load_info_text.set(f"{load_info_text.get()}\n"
                                       f"Обнаружена новая версия базы данных пациентов\n"
                                       f"Начинаю обновление...")

                    shutil.copy2(r"\\SRV2\data_base\patient_data_base.db",
                                 f".{os.sep}data_base{os.sep}patient_data_base.db")
                    load_info_text.set(f"{load_info_text.get()}\n"
                                       f"База данных пациентов обновлена")
                else:
                    load_info_text.set(f"{load_info_text.get()}\n"
                                       f"У вас актуальная версия базы данных")

            time.sleep(1)
            log_in_root.update()

            if not user.get('error_connection'):
                try:
                    with sq.connect(r"\\SRV2\data_base\application_data_base.db") as conn:
                        cur = conn.cursor()
                        # cur.execute("CREATE TABLE IF NOT EXISTS врачи "
                        #             "(doctor_name text, password text, district text, ped_div text, "
                        #             "manager text, open_mark text, text_size text, add_info text)")
                        # cur.execute("CREATE TABLE IF NOT EXISTS examination "
                        #             "(date_time text, doctor_name text, status text, "
                        #             "LN_type text, patient_info text, examination_text text, "
                        #             "examination_key text, add_info text)")
                        # cur.execute("CREATE TABLE IF NOT EXISTS my_saved_diagnosis "
                        #             "(doctor_name text, diagnosis text, examination_key text)")
                        # cur.execute("CREATE TABLE IF NOT EXISTS my_LN "
                        #             "(doctor_name text, ln_type text, ln_num text)")
                        # cur.execute("CREATE TABLE IF NOT EXISTS my_sport_section "
                        #             "(doctor_name text, sport_section text)")

                        cur.execute("SELECT * FROM врачи")
                        all_doctor_info = cur.fetchall()
                    frame_doc = Frame(log_in_root, borderwidth=1, relief="solid", padx=8, pady=10)

                    load_info_text.set("Выберите учетную запись")

                    for doctor_name, password, district, ped_div, manager, open_mark, text_size, add_info \
                            in sorted(all_doctor_info, key=lambda i: i[0]):
                        users_passwords[doctor_name] = str(password)
                        all_users_info[doctor_name] = [doctor_name, password, district, ped_div, manager, text_size,
                                                       add_info]
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
                              font=('Comic Sans MS', 12), bg='white').grid(row=row, column=0, sticky='ew', columnspan=4)
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

                    frame_doc.pack(fill='both', expand=True, padx=2, pady=2)

                    Label(frame_pass, text='Введите пароль: ',
                          font=('Comic Sans MS', 12), bg='white').grid(row=0, column=0, sticky='ew')

                    check_pass = (log_in_root.register(is_valid__password), "%P")

                    password_txt = Entry(frame_pass, width=20, font=('Comic Sans MS', user.get('text_size')),
                                         justify="center",
                                         validate="all",
                                         textvariable=txt_password_variable,
                                         validatecommand=check_pass)
                    password_txt.grid(row=0, column=1, sticky='ew')

                    Label(frame_pass, textvariable=text_is_correct_password,
                          font=('Comic Sans MS', 12), bg='white', foreground="red").grid(row=0, column=2, sticky='ew')

                except Exception:
                    user['error_connection'] = True

            if user.get('error_connection'):
                open_main_root()

        import time

        if user.get('frame_main'):
            user['frame_main'].destroy()

        log_in_root = Frame(master=root)
        user['log_in_root'] = log_in_root

        load_info_text = StringVar()
        load_info_text.set('Запуск программы...')
        selected_doctor_name = StringVar()
        txt_password_variable = StringVar()
        text_is_correct_password = StringVar()

        users_passwords = dict()
        all_users_info = dict()
        users_sorted_pd = dict()

        load_info = Label(log_in_root, textvariable=load_info_text,
                          font=('Comic Sans MS', 12), bg='white')
        load_info.pack(fill='both', expand=True, padx=2, pady=2)
        frame_pass = Frame(log_in_root, borderwidth=1, relief="solid", padx=8, pady=10)

        log_in_root.columnconfigure(index='all', minsize=40, weight=1)
        log_in_root.rowconfigure(index='all', minsize=20)
        log_in_root.pack(fill='both', expand=True, padx=2, pady=2)

        connect_to_srv_data_base()

    def paste_frame_main():

        def search_loop():
            patient_found_data = list()

            def select_patient(event=None):
                num = ''
                if event:
                    for i in str(event.widget).split('.!')[-1]:
                        if i.isdigit():
                            num += i
                if not num:
                    num = 3
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
                delete_txt_patient_data()

            def button_search_in_db(*args, **kwargs):
                delete_txt_patient_data()
                txt_patient_data.insert(index=0,
                                        string=text_patient_data.get())
                search_root.destroy()
                search_loop()

            def search_in_db():
                word_list = ["qwertyuiopasdfghjkl;'zxcvbnm,.", "йцукенгшщзфывапролджэячсмитьбю"]
                delete_txt_patient_data()
                txt_patient_data.insert(0, text_patient_data.get())

                patient_data = text_patient_data.get()
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
                    messagebox.showinfo('Ошибка', 'По введенной информации не удалось сформулировать sql запрос')

                else:
                    with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
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
                        counter_patient['text'] = "По введенной информации не удалось найти пациента"
                        # messagebox.showinfo('Ошибка', 'По введенной информации не удалось найти пациента')

                    elif len(found_data) == 1:
                        patient_found_data.append(found_data[0])
                        select_patient()

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
                            lbl_0 = Label(search_root, text=text, font=('Comic Sans MS', user.get('text_size')),
                                          border=1, compound='left',
                                          bg='#bbfffe', relief='ridge')
                            lbl_0.grid(columnspan=3, sticky='w', padx=2, pady=2, ipadx=2, ipady=2)
                            lbl_0.bind('<Double-Button-1>', select_patient)
                            patient_found_data.append(found_data[num])

            search_root = Toplevel()
            search_root.title('Поиск пациента')
            search_root.config(bg='white')
            search_root.geometry('+0+0')

            counter_patient = Label(search_root, text='', font=('Comic Sans MS', 16), bg='white')
            counter_patient.grid(column=0, row=2, columnspan=3)

            Label(search_root, text='Окно данных пациента',
                  font=('Comic Sans MS', user.get('text_size')), bg='white').grid(column=0, row=0, columnspan=3)
            text_patient_data = Entry(search_root, width=30, font=('Comic Sans MS', user.get('text_size')))
            text_patient_data.grid(column=0, row=1, columnspan=2)
            text_patient_data.insert(0, txt_patient_data.get())
            text_patient_data.focus()
            text_patient_data.bind('<Return>', button_search_in_db)

            Button(search_root, text='Найти', command=button_search_in_db,
                   font=('Comic Sans MS', user.get('text_size'))).grid(column=2, row=1)
            search_in_db()
            search_root.mainloop()

        def append_doctor_data():
            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                cur = conn.cursor()

                cur.execute(f"SELECT doctor_name, district, ped_div, manager, text_size FROM врачи "
                            f"WHERE doctor_name LIKE '{combo_doc.get()}'")
            doctor_name, district, ped_div, manager, text_size = cur.fetchone()
            user['text_size'] = int(text_size)
            user['doctor_name'] = doctor_name
            user['doctor_district'] = district
            user['ped_div'] = ped_div
            user['manager'] = manager

        def redact_doctor():
            change_doctor(command='redact')

        def add_new_doctor():
            change_doctor(command='new')

        def change_doctor(command):
            def save():
                doctor_name = txt_doctor_name.get()
                manager = txt_manager.get()
                district = txt_district.get()
                ped_div = txt_ped_div.get()
                text_size = txt_text_size.get()

                if not doctor_name:
                    messagebox.showinfo('Ошибка', 'Ошибка имени доктора!')
                elif not manager:
                    messagebox.showinfo('Ошибка', 'Ошибка имени заведующего!')
                elif not district or not district.isdigit():
                    messagebox.showinfo('Ошибка', 'Ошибка участка!\nУкажите участок числом')
                elif not ped_div or not ped_div.isdigit():
                    messagebox.showinfo('Ошибка', 'Ошибка ПО\nУкажите номер ПО числом')
                elif not text_size or not text_size.isdigit() or (4 > int(text_size) or int(text_size) > 30):
                    messagebox.showinfo('Ошибка', 'Ошибка размера текста\n'
                                                  'Укажите размер текста числом от 5 до 30')

                else:
                    new_doctor = [doctor_name, district, ped_div, manager, True, text_size]

                    try:
                        with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                            cur = conn.cursor()
                            cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{doctor_name}'")

                            cur.execute(f"SELECT doctor_name, district, ped_div, manager, text_size FROM врачи")
                            for doctor_name, district, ped_div, manager, text_size in cur.fetchall():
                                cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{doctor_name}'")
                                cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)",
                                            [doctor_name, district, ped_div, manager, False, text_size])

                            cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)", new_doctor)
                    except Exception as ex:
                        messagebox.showinfo('Ошибка', f'Ошибка записи в базу данных:\n{ex}')
                    else:
                        messagebox.showinfo('Успешно', 'Данные успешно сохранены!')
                        combo_doc['values'] = get_doc_names()
                        combo_doc.current(0)

                        user['text_size'] = int(txt_text_size.get())

                        new_root.destroy()
                        root.update()
                        write_lbl_doc()
                        append_doctor_data()
                        update_font_main()

            new_root = Toplevel()
            new_root.title('Новая учетная запись')

            Label(new_root, text='ФИО доктора: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=0)
            Label(new_root, text='ФИО заведующего: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0,
                                                                                                          row=1)
            Label(new_root, text='Номер участка: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=2)
            Label(new_root, text='Номер ПО: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=3)
            Label(new_root, text='Размер текста: ', font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=4)

            txt_doctor_name = Entry(new_root, width=30, font=('Comic Sans MS', user.get('text_size')))
            txt_doctor_name.grid(column=1, row=0)

            txt_manager = Entry(new_root, width=30, font=('Comic Sans MS', user.get('text_size')))
            txt_manager.grid(column=1, row=1)

            txt_district = Entry(new_root, width=5, font=('Comic Sans MS', user.get('text_size')))
            txt_district.grid(column=1, row=2)

            txt_ped_div = Entry(new_root, width=5, font=('Comic Sans MS', user.get('text_size')))
            txt_ped_div.grid(column=1, row=3)

            txt_text_size = Entry(new_root, width=5, font=('Comic Sans MS', user.get('text_size')))
            txt_text_size.grid(column=1, row=4)

            Button(new_root, text='Сохранить', command=save, font=('Comic Sans MS', user.get('text_size'))).grid()
            if command == 'redact':
                old_doctor_name, old_district, old_ped_div, old_manager, old_text_size = get_doctor_data()
                txt_doctor_name.insert(0, old_doctor_name)
                txt_manager.insert(0, old_manager)
                txt_district.insert(0, old_district)
                txt_ped_div.insert(0, old_ped_div)
                txt_text_size.insert(0, old_text_size)

            new_root.mainloop()

        def paste_txt_patient_data(event=None):
            if event:
                print(event.widget)
            text_patient_data = pyperclip.paste()
            txt_patient_data.delete(0, last=END)
            txt_patient_data.insert(index=0,
                                    string=text_patient_data)
            search_patient()

        def save_doctor(new_doctor_name):
            with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                cur = conn.cursor()

                cur.execute(f"SELECT doctor_name, district, ped_div, manager, text_size FROM врачи")

                for doctor_name, district, ped_div, manager, text_size in cur.fetchall():
                    cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{doctor_name}'")
                    if doctor_name == new_doctor_name:
                        cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)",
                                    [doctor_name, district, ped_div, manager, True, text_size])
                    else:
                        cur.execute("INSERT INTO врачи VALUES(?, ?, ?, ?, ?, ?)",
                                    [doctor_name, district, ped_div, manager, False, text_size])
            write_lbl_doc()
            update_font_main()

        def search_patient(*args, **kwargs):
            patient_data = txt_patient_data.get()

            if ('Фамилия, имя, отчество пациента:' in patient_data or
                    '№ амб. карты' in patient_data or
                    '№ амбулаторной карты' in patient_data):
                patient_data = decoding_name(patient_data)
                for key in patient:
                    if patient_data.get(key):
                        patient[key] = patient_data.get(key)
                patient_info['text'] = f"ФИО: {patient_data.get('name')}\t" \
                                       f"Дата рождения: {patient_data.get('birth_date')}\n" \
                                       f"Адрес: {patient_data.get('address')}\n" \
                                       f"№ амб: {patient_data.get('amb_cart')}\t" \
                                       f"Участок: {patient_data.get('patient_district')}"
                delete_txt_patient_data()
                return True
            else:
                search_loop()

        def write_lbl_doc(info_doc=None):
            if not info_doc:
                info_doc = get_doctor_data()
            user['text_size'] = int(info_doc[4])
            lbl_doc['text'] = f'Учетная запись:\n' \
                              f'Доктор: {info_doc[0]}\n' \
                              f'Зав: {info_doc[3]};    ' \
                              f'Участок: {info_doc[1]};    ' \
                              f'ПО: {info_doc[2]}'
            if 'константинова' in info_doc[0].lower():
                lbl_doc['text'] = f'Учетная запись:\n' \
                                  f'Доктор: Яночка Константиновна\n' \
                                  f'Зав: {info_doc[3]};    ' \
                                  f'Участок: {info_doc[1]};    ' \
                                  f'ПО: {info_doc[2]}'

            root.update()

        def selected(event=None):
            save_doctor(new_doctor_name=combo_doc.get())
            append_doctor_data()
            update_font_main()

        def delete_txt_patient_data():
            txt_patient_data.delete(0, last=END)

        def update_font_main():
            lbl_doc['font'] = ('Comic Sans MS', user.get('text_size'))
            combo_doc['font'] = ('Comic Sans MS', user.get('text_size'))
            button_add_new_doctor['font'] = ('Comic Sans MS', user.get('text_size'))
            button_redact_doctor['font'] = ('Comic Sans MS', user.get('text_size'))
            lbl_patient_main['font'] = ('Comic Sans MS', user.get('text_size'))
            txt_patient_data['font'] = ('Comic Sans MS', user.get('text_size'))
            patient_info['font'] = ('Comic Sans MS', user.get('text_size'))
            button_search_patient['font'] = ('Comic Sans MS', user.get('text_size'))
            button_updating_patient_data_base['font'] = ('Comic Sans MS', user.get('text_size'))
            button_delete_txt_patient_data['font'] = ('Comic Sans MS', user.get('text_size'))
            button_paste_txt_patient_data['font'] = ('Comic Sans MS', user.get('text_size'))
            lbl_to_do_main['font'] = ('Comic Sans MS', user.get('text_size'))
            button_certificate_cmd['font'] = ('Comic Sans MS', user.get('text_size'))
            button_analyzes_cmd['font'] = ('Comic Sans MS', user.get('text_size'))
            button_blanks_cmd['font'] = ('Comic Sans MS', user.get('text_size'))
            button_vaccination_cmd['font'] = ('Comic Sans MS', user.get('text_size'))
            button_direction_cmd['font'] = ('Comic Sans MS', user.get('text_size'))
            button_examination_cmd['font'] = ('Comic Sans MS', user.get('text_size'))
            button_delete_doctor['font'] = ('Comic Sans MS', user.get('text_size'))
            button_change_account['font'] = ('Comic Sans MS', user.get('text_size'))

            root.update()

        def delete_doc_local():
            result = messagebox.askyesno(title='Удаление учетной записи',
                                         message=f"Удалить пользователя?\n"
                                                 f"{combo_doc.get()}")
            if result:
                with sq.connect(f".{os.sep}data_base{os.sep}data_base.db") as conn:
                    cur = conn.cursor()
                    cur.execute(f"DELETE FROM врачи WHERE doctor_name LIKE '{combo_doc.get()}'")

                messagebox.showinfo("Результат", "Учетная запись удалена")
                data_base()
                combo_doc['values'] = get_doc_names()
                combo_doc.current(0)
                selected()
                write_lbl_doc()

        def change_account():
            paste_log_in_root()

        if user.get('log_in_root'):
            user['log_in_root'].destroy()

        frame_main = Frame(master=root)
        user['frame_main'] = frame_main

        frame_main_loc = Frame(master=frame_main, borderwidth=1, relief="solid", padx=8, pady=10)

        lbl_doc = Label(frame_main_loc, text='')

        button_add_new_doctor = Button(frame_main_loc, text='Добавить доктора', command=add_new_doctor)
        button_redact_doctor = Button(frame_main_loc, text='Редактировать данные', command=redact_doctor)
        button_delete_doctor = Button(frame_main_loc, text='Удалить пользователя', command=delete_doc_local)
        button_change_account = Button(frame_main_loc, text='Сменить пользователя', command=change_account)
        combo_doc = Combobox(frame_main_loc, state="readonly")

        if user.get('error_connection'):
            lbl_doc.grid(column=0, row=0, columnspan=3)

            write_lbl_doc()
            combo_doc['values'] = get_doc_names()
            combo_doc.current(0)
            combo_doc.grid(column=0, row=1, columnspan=3)
            combo_doc.bind("<<ComboboxSelected>>", selected)

            button_add_new_doctor.grid(column=0, row=2, sticky='ew')
            button_redact_doctor.grid(column=1, row=2, sticky='ew')
            button_delete_doctor.grid(column=2, row=2, sticky='ew')

            append_doctor_data()

        else:
            lbl_doc.grid(column=0, row=0, columnspan=2)

            lbl_doc['text'] = f"Учетная запись:\n" \
                              f"Доктор: {user.get('doctor_name')}\n" \
                              f"Зав: {user.get('manager')};    " \
                              f"Участок: {user.get('doctor_district')};    " \
                              f"ПО: {user.get('ped_div')}"

            button_change_account.grid(column=0, row=2, sticky='ew')
            button_redact_doctor.grid(column=1, row=2, sticky='ew')

        frame_main_loc.columnconfigure(index='all', minsize=40, weight=1)
        frame_main_loc.rowconfigure(index='all', minsize=20)
        frame_main_loc.pack(fill='both', expand=True, padx=2, pady=2)

        frame_main_loc = Frame(master=frame_main, borderwidth=1, relief="solid", padx=8, pady=10)

        lbl_patient_main = Label(frame_main_loc, text='Окно данных пациента')
        lbl_patient_main.grid(column=0, row=2, columnspan=3, sticky='ew')

        txt_patient_data = Entry(frame_main_loc, width=40)
        txt_patient_data.grid(column=0, row=3)
        txt_patient_data.bind('<Control-v>', paste_txt_patient_data)
        txt_patient_data.bind('<Return>', search_patient)

        patient_info = Label(frame_main_loc, text='')
        patient_info.grid(column=0, row=4, sticky='ew')

        button_search_patient = Button(frame_main_loc, text='Поиск', command=search_patient)
        button_search_patient.grid(column=1, row=3, sticky='ew')

        button_updating_patient_data_base = Button(frame_main_loc, text='Обновить БД',
                                                   command=updating_patient_data_base)
        button_updating_patient_data_base.grid(column=1, row=4, sticky='ew')

        button_delete_txt_patient_data = Button(frame_main_loc, text='Удалить', command=delete_txt_patient_data)
        button_delete_txt_patient_data.grid(column=2, row=3, sticky='ew')

        button_paste_txt_patient_data = Button(frame_main_loc, text='Вставить', command=paste_txt_patient_data)
        button_paste_txt_patient_data.grid(column=2, row=4, sticky='ew')

        frame_main_loc.columnconfigure(index='all', minsize=40, weight=1)
        frame_main_loc.rowconfigure(index='all', minsize=20)
        frame_main_loc.pack(fill='both', expand=True, padx=2, pady=2)

        frame_main_loc = Frame(master=frame_main, borderwidth=1, relief="solid", padx=8, pady=10)

        lbl_to_do_main = Label(frame_main_loc, text='Что хотите сделать?',
                               anchor='center')
        lbl_to_do_main.grid(column=0, row=0, columnspan=2, sticky='ew')

        button_certificate_cmd = Button(frame_main_loc, text='Справка', command=certificate_cmd)
        button_certificate_cmd.grid(column=0, row=1, sticky='ew')

        button_analyzes_cmd = Button(frame_main_loc, text='Анализы', command=analyzes_cmd)
        button_analyzes_cmd.grid(column=1, row=1, sticky='ew')

        button_blanks_cmd = Button(frame_main_loc, text='Вкладыши', command=blanks_cmd)
        button_blanks_cmd.grid(column=0, row=2, sticky='ew')

        button_vaccination_cmd = Button(frame_main_loc, text='Прививки', command=vaccination_cmd)
        button_vaccination_cmd.grid(column=1, row=2, sticky='ew')

        button_direction_cmd = Button(frame_main_loc, text='Направления', command=direction_cmd)
        button_direction_cmd.grid(column=0, row=3, sticky='ew')

        button_examination_cmd = Button(frame_main_loc, text='Осмотры', command=examination_cmd)
        button_examination_cmd.grid(column=1, row=3, sticky='ew')

        frame_main_loc.columnconfigure(index='all', minsize=40, weight=1)
        frame_main_loc.rowconfigure(index='all', minsize=20)
        frame_main_loc.pack(fill='both', expand=True, padx=2, pady=2)

        frame_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_main.rowconfigure(index='all', minsize=20)
        frame_main.pack(fill='both', expand=True, padx=2, pady=2)

        update_font_main()

    root = Tk()
    root.title('Генератор справок v_0.1.1')
    root.config(bg='white')
    root.geometry('+0+0')
    root.bind("<Control-KeyPress>", keypress)

    try:
        frame_lbl = Frame(padx=3, pady=3, bg="#36566d")
        pil_image = Image.open('Crynet_systems.png')
        pil_image = pil_image.resize((200, 50))
        image = ImageTk.PhotoImage(pil_image)
        Label(frame_lbl, image=image, anchor='ne', bg="#36566d").pack(fill='both', expand=True)
        frame_lbl.pack(fill='both', expand=True, padx=2, pady=2)
    except Exception:
        pass

    paste_log_in_root()

    root.mainloop()


if __name__ == "__main__":
    main_root()
