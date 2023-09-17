from tkinter import *
from tkinter import ttk
import sqlite3 as sq
from datetime import datetime, timedelta
from tkinter.ttk import Combobox
from tkinter.scrolledtext import ScrolledText
from tkinter import scrolledtext, messagebox
from docx import Document
from docx.shared import Cm
from docx.shared import Pt
import os

certificate = {
    "patient": {
        'name': '',
        'birth_date': '',
        'gender': '',
        'amb_cart': '',
        'patient_district': '',
        'address': ''},
    "doctor": {
        'doctor_name': '',
        'manager': '',
        'ped_div': '',
        'doctor_district': ''},

    'certificate': {
        'type_certificate': ''
    }

}

all_data = {
    'sport_section': ('баскетболом', 'волейболом', 'вольной борьбой', 'гандболом', 'греблей', 'каратэ',
                      'легкой атлетикой', 'музыкой', 'плаванием в бассейне', 'спортивной гимнастикой', 'танцами',
                      'теннисом', 'тхэквондо', 'фигурным катанием', 'фигурным катанием', 'футболом', 'хоккеем',
                      'шахматами', 'шашками'),
    "health": {
        "group": ("<< Группы здоровья >>", "1", "2", "3", "4"),
        "physical": ("<< Группы по физкультуре >>", "Основная", "Подготовительная", "СМГ", "ЛФК"),
        "regime": ("<< Режимы >>", "общий", "ортопедический", "зрительный", "щадящий", "охранительный"),
        "diet": ("<< Диетические столы >>", "А", "Б", "Д", "М", 'П', 'ПП', 'Ц'),
        "desk": ("<< Парта >>", "по росту", "1", "2", "3", "средний ряд"),
        "vision": ("<< Зрение >>", "Указать", "1.0/1.0", "предметное", "_______")

    },
    "diagnosis": (("<< КАРДИОЛОГИЯ >>", "САС:", "ООО", "ДХЛЖ", "НК0", "НБПНПГ", "ФСШ", "ВПС:", "ДМЖП", "ДМПП"),
                  ("<< ОФТАЛЬМОЛОГИЯ >>", "Спазм аккомодации", "Миопия", "Гиперметропия",
                             "слабой степени", "средней степени", "тяжелой степени", "OD", "OS", "OU", "с ast"),
                  ("<< ОРТОПЕДИЯ >>", "Нарушение осанки", "Сколиотическая осанка", "Плоскостопие", "ПВУС",
                            "ИС:", "левосторонняя", "правосторонняя", "кифотическая", "грудная", "поясничная",
                            "грудо-поясничная", "деформация позвоночника", "ГПС", "1 ст.", "2 ст.", "3 ст."),
                  ("<< ЛОГОПЕДИЯ >>", "ОНР", "ФНР", "ФФНР", "ЗРР", "стертая дизартрия",
                           "ур.р.р.", "1", "2", "3"),
                  ("<< ЛОР >>", "ГА", "ГНМ", "хр. тонзиллит", "1ст", "2ст", "3ст"),
                  ("<< ПРОЧЕЕ >>", "рецидивирующие заболевания ВДП", "Атопический дерматит", "Кариес",
                          "угроза", "БРА", "хр. гастрит", "СДН", "ВСД")),

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
            "diagnosis": "ОРИ с _ по _",
            "validity_period": "5 дней",
            "next_step": "create_calendar"},

        "Годовой медосмотр": {
            "additional_medical_information": "Рост _____ см; Вес _____ кг; Vis OD/OS = __________; АД ________\n"
                                              "| Осмотрен на чесотку, педикулез, микроспорию |",
            "diagnosis": "Группа здоровья: _ ; Группа по физкультуре: _ ;",
            "recommendation": "Режим _; Стол _; Парта _;",
            "date_of_issue": "now",
            "count_of_certificates": "1",
            "next_step": "chickenpox"},

        "На кружки и секции": {
            "place_of_requirement": "Для занятия ",
            "diagnosis": "Не имеется медицинских противопоказаний, "
                         "включенных в перечень медицинских противопоказаний для занятия ",
            "date_of_issue": "now",
            "validity_period": "1 год",
            "next_step": "special_fraze"},

        "Бесплатное питание": {
            "place_of_requirement": "Управление социальной защиты Первомайского района",
            "additional_medical_information": "Ребенок находится на искусственном вскармливании. "
                                              "Получает питание по возрасту",
            "diagnosis": "Соматически здоров",
            "recommendation": "Рекомендован рацион питания ребенку в соответствии с возрастом и примерным месячным "
                              "набором продуктов питания согласно приложения №1 к постановлению Министерства труда "
                              "и социальной защиты РБ и МЗРБ от 13.03.2012 № 37/20",
            "date_of_issue": "now",
            "validity_period": "6 месяцев",
            "count_of_certificates": "1",
            "next_step": "allergy"},

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
            "validity_period": "1 год",
            "count_of_certificates": "1",
            "next_step": "None"},

        "Оформление в ДДУ / СШ / ВУЗ": {
            "additional_medical_information": "Рост _____ см; Вес _____ кг; Vis OD/OS = __________; АД ________\n"
                                              "| Осмотрен на чесотку, педикулез, микроспорию |\n"
                                              "Данные о профилактических прививках прилагаются",
            "diagnosis": f"Группа здоровья: _ ; Группа по физкультуре: _ ;",
            "recommendation": "Режим _; Стол _;",
            "date_of_issue": "now",
            "validity_period": "1 год",
            "count_of_certificates": "1",
            "next_step": "kb_where"},

        "Об отсутствии контактов": {
            "additional_medical_information": "В контакте с инфекционными больными в течение 35 дней не был\n"
                                              "| Осмотрен на чесотку, педикулез, микроспорию |",
            "diagnosis": "На момент осмотра соматически здоров",
            "recommendation": "Может находиться в детском коллективе",
            "date_of_issue": "now",
            "validity_period": "5 дней",
            "count_of_certificates": "1",
            "next_step": "chickenpox"},

        "О нуждаемости в сан-кур лечении": {
            "place_of_requirement": "О нуждаемости в санаторно-курортном лечении",
            "diagnosis": f"{'_' * 55}\n{'_' * 65}",
            "recommendation": "Ребенок нуждается в санаторно-курортном лечении:\n"
                              "пульмонологического профиля\n"
                              "гастроэнтерологического профиля\n"
                              "ревматологического профиля\n"
                              "неврологического профиля\n"
                              "эндокринологического профиля\n"
                              "нефрологического профиля\n"
                              "гинекологического профиля\n"
                              "кардиологического профиля \n"
                              "дерматологического профиля\n"
                              "ортопедотравматологического профиля\n"
                              "офтальмологического профиля",
            "date_of_issue": "now",
            "validity_period": "1 год",
            "count_of_certificates": "1",
            "next_step": "chickenpox"},

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
            "validity_period": "5 дней",
            "count_of_certificates": "1",
            "next_step": "chickenpox"},

        "Может работать по специальности...": {
            "place_of_requirement": "Проведение обязательного предварительного / внеочередного медицинского осмотра",
            "diagnosis": "Годен к работе по специальности: ",
            "date_of_issue": "now",
            "validity_period": "До следующего обязательного периодического медицинского осмотра",
            "next_step": "special_fraze"},

        "Об обслуживании в поликлинике": {
            "place_of_requirement": "По месту требования",
            "diagnosis": "Ребенок обслуживается в УЗ '19-я городская детская поликлиника с ___________'",
            "date_of_issue": "now",
            "validity_period": "1 год",
            "next_step": "None"},

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
            "validity_period": "1 год",
            "next_step": "chickenpox"
        }
    }}


def append_info(info):
    for key_0 in info:
        for key_1 in info.get(key_0):
            certificate[key_0][key_1] = info[key_0].get(key_1)
    print(certificate)
    ask_type_certificate()


def ask_type_certificate():

    def select_type_certificate(event):
        print(event.widget)
        num = ''
        for i in str(event.widget):
            if i.isdigit():
                num += i
        certificate['certificate']['type_certificate'] = all_data.get('type')[int(num)-2]
        type_cert_root.destroy()
        editing_certificate()

    type_cert_root = Tk()
    type_cert_root.title('Выбор справки')
    type_cert_root.config(bg='white')

    Label(type_cert_root, text='Какую справку создать?\n', font=('Comic Sans MS', 20), bg='white').grid()
    for text in all_data.get('type'):
        lbl_0 = Label(type_cert_root, text=text, font=('Comic Sans MS', 20), border=1, compound='left',
                      bg='#f0fffe', relief='ridge')
        lbl_0.grid(ipadx=6, ipady=6, padx=4, pady=4)
        lbl_0.bind('<Double-Button-1>', select_type_certificate)

    type_cert_root.mainloop()


def editing_certificate():

    edit_cert_root = Tk()
    edit_cert_root.title(f'Редактирование справки')
    edit_cert_root.config(bg='white')

    type_certificate = certificate['certificate'].get('type_certificate')
    Label(edit_cert_root, text=f"Данные пациента:\n"
                               f"Участок: {certificate['patient'].get('patient_district')};    "
                               f"№ амб: {certificate['patient'].get('amb_cart')};\n"
                               f"ФИО: {certificate['patient'].get('name')};    "
                               f"{certificate['patient'].get('birth_date')};    "
                               f"пол: {certificate['patient'].get('gender')};\n"
                               f"Адрес: {certificate['patient'].get('address')};\n",
          font=('Comic Sans MS', 20), bg='white').grid()

    # name_label = ttk.Label(frame, text="Введите имя")
    # name_label.pack(anchor=NW)
    #
    # name_entry = ttk.Entry(frame)
    # name_entry.pack(anchor=NW)

    if type_certificate == 'По выздоровлении':
        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Диагноз:", font=('Comic Sans MS', 20), bg='white').grid(column=0, row=0)

        combo_doc = Combobox(frame, font=('Comic Sans MS', 20), state="readonly")
        combo_doc['values'] = ['ОРИ', "ФРК", "Ветряная оспа"]
        combo_doc.current(0)
        combo_doc.grid(column=1, row=0)

        Label(frame, text="c", font=('Comic Sans MS', 20), bg='white').grid(column=2, row=0)
        ori_from = Entry(frame, width=15, font=('Comic Sans MS', 20))
        ori_from.grid(column=3, row=0)

        Label(frame, text="по", font=('Comic Sans MS', 20), bg='white', compound="center").grid(column=4, row=0)
        ori_until = Entry(frame, width=15, font=('Comic Sans MS', 20))
        ori_until.grid(column=5, row=0)

        frame.grid(padx=5, pady=5)

    if type_certificate in ('Годовой медосмотр',
                            'Оформление в ДДУ / СШ / ВУЗ',
                            'В детский лагерь',
                            'Об усыновлении (удочерении)',
                            'Об отсутствии контактов',
                            'Бесплатное питание',
                            'О нуждаемости в сан-кур лечении'):
        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Ветрянка:", font=('Comic Sans MS', 20), bg='white').grid(column=0, row=0)

        chickenpox = ["+", "-", "привит"]
        selected_chickenpox = StringVar(value=chickenpox[0])

        def select_chickenpox():
            certificate['certificate']['chickenpox'] = selected_chickenpox.get()

        for mark in chickenpox:
            btn = Radiobutton(frame, text=mark, font=('Comic Sans MS', 20),
                              value=mark, variable=selected_chickenpox, command=select_chickenpox)
            btn.grid(row=0, column=(chickenpox.index(mark) + 1))

        Label(frame, text="Аллергия:", font=('Comic Sans MS', 20), bg='white').grid(row=1, column=0)
        allergy = ["-", "+"]
        selected_allergy = StringVar(value=allergy[0])

        def select_allergy():
            certificate['certificate']['allergy'] = selected_allergy.get()

        for mark in allergy:
            btn = Radiobutton(frame, text=mark, font=('Comic Sans MS', 20),
                              value=mark, variable=selected_allergy, command=select_allergy)
            btn.grid(column=(allergy.index(mark) + 1), row=1)

        Label(frame, text="Аллергия на:", font=('Comic Sans MS', 20), bg='white').grid(row=2, column=0)
        allergy_txt = Entry(frame, width=60, font=('Comic Sans MS', 20))
        allergy_txt.grid(column=1, row=2, columnspan=3)

        frame.grid(padx=5, pady=5, sticky='w')

    if type_certificate in ('Годовой медосмотр',
                            'Оформление в ДДУ / СШ / ВУЗ',
                            'В детский лагерь',
                            'Об усыновлении (удочерении)'):
        frame = Frame(edit_cert_root, borderwidth=1, relief="solid", padx=4, pady=4)

        Label(frame, text="Рост:", font=('Comic Sans MS', 20), bg='white').grid(column=0, row=0)
        height = Entry(frame, width=15, font=('Comic Sans MS', 20))
        height.grid(column=1, row=0)

        Label(frame, text="    Вес:", font=('Comic Sans MS', 20), bg='white').grid(column=2, row=0)
        weight = Entry(frame, width=15, font=('Comic Sans MS', 20))
        weight.grid(column=3, row=0)

        Label(frame, text="    Зрение:", font=('Comic Sans MS', 20), bg='white').grid(column=4, row=0)
        vision = Entry(frame, width=15, font=('Comic Sans MS', 20))
        vision.grid(column=5, row=0)

        Label(frame, text="Диагноз:", font=('Comic Sans MS', 20), bg='white').grid(column=0, row=2)
        diagnosis = ScrolledText(frame, width=50, height=4, font=('Comic Sans MS', 20), wrap="word")
        diagnosis.grid(column=0, row=3, rowspan=4, columnspan=4)

        def diagnosis_healthy():
            if certificate['patient'].get('gender', '') == 'женский':
                diagnosis.insert(INSERT, 'Соматически здорова. ')
            else:
                diagnosis.insert(INSERT, 'Соматически здоров. ')
        Button(frame, text='Здоров', command=diagnosis_healthy, font=('Comic Sans MS', 20)).grid(column=4, row=3)

        def diagnosis_kb():
            def close_diagnosis_kb():
                diagnosis_root.destroy()

            def select_diagnosis(event):
                print(event.widget)
                num = ''
                for i in str(event.widget):
                    if i.isdigit():
                        num += i
                print(num)
                # certificate['certificate']['type_certificate'] = all_data.get('type')[int(num) - 2]
                # type_cert_root.destroy()
                # editing_certificate()

            diagnosis_root = Tk()
            diagnosis_root.title('Клавиатура диагнозов')
            diagnosis_root.config(bg='white')

            frame_diagnosis = Frame(diagnosis_root, borderwidth=1, relief="solid", padx=4, pady=4)
            Label(frame_diagnosis, text="Диагноз:", font=('Comic Sans MS', 20), bg='white').grid()
            diagnosis_text = ScrolledText(frame_diagnosis, width=50, height=4, font=('Comic Sans MS', 20), wrap="word")
            diagnosis_text.insert(INSERT, diagnosis.get(index1=1.0, index2='end'))
            diagnosis_text.focus()
            diagnosis_text.grid(column=0, row=1, rowspan=4)
            Button(frame_diagnosis, text='Закрыть\nклавиатуру',
                   command=close_diagnosis_kb, font=('Comic Sans MS', 20)).grid(column=1, row=3)
            frame_diagnosis.grid(padx=5, pady=5, column=0, row=0)

            tuple_diagnosis_row = 1
            for tuple_diagnosis in all_data.get('diagnosis'):
                frame_diagnosis = Frame(diagnosis_root, borderwidth=1, relief="solid", padx=4, pady=4)
                Label(frame_diagnosis, text=f"{tuple_diagnosis[0]}",
                      font=('Comic Sans MS', 20), bg='white').grid(columnspan=5)
                row, column = 1, 0
                for lbl in tuple_diagnosis[1:]:
                    print(lbl, row, column)
                    if column == 10:
                        row += 1
                        column = 0
                    lbl_0 = Label(frame_diagnosis, text=lbl, font=('Comic Sans MS', 20), border=1, compound='left',
                                  bg='#f0fffe', relief='ridge')
                    lbl_0.grid(ipadx=2, ipady=2, padx=2, pady=2, column=column, row=row)
                    lbl_0.bind('<Button-1>', select_diagnosis)
                    column += 1
                frame_diagnosis.grid(padx=1, pady=1, row=tuple_diagnosis_row)
                tuple_diagnosis_row += 1


        Button(frame, text='Клавиатура', command=diagnosis_kb, font=('Comic Sans MS', 20)).grid(column=4, row=4)

        frame.grid(padx=5, pady=5)


    edit_cert_root.mainloop()


#
#     elif (data.get('certificate').get('doctor_flag')
#           and data['certificate'].get('type_certificate') in ('Годовой медосмотр',
#                                                               'Оформление в ДДУ / СШ / ВУЗ',
#                                                               'В детский лагерь',
#                                                               'Об усыновлении (удочерении)')
#           and not data['certificate'].get('health').get('height')):
#         try:
#             await message.edit_text(text='Введите рост в сантиметрах и вес в килограммах через пробел\n'
#                                          "Например: '110 16'")
#         except exceptions.MessageToEditNotFound:
#             await message.answer(text='Введите рост в сантиметрах и вес в килограммах через пробел\n'
#                                       "Например: '110 16'")
#         await FastCertificate.height_weight.set()
#
#     elif (data.get('certificate').get('doctor_flag')
#           and data['certificate'].get('type_certificate') in ('Годовой медосмотр',
#                                                               'Оформление в ДДУ / СШ / ВУЗ',
#                                                               'В детский лагерь',
#                                                               'Об усыновлении (удочерении)')
#           and not data['certificate'].get('health').get('add_diagnosis')):
#         await message.answer(text="Выберите основные диагнозы")
#         await send_add_diagnosis(message, state)
#
#     elif (data.get('certificate').get('doctor_flag')
#           and data['certificate'].get('type_certificate') in ('Годовой медосмотр',
#                                                               'Оформление в ДДУ / СШ / ВУЗ',
#                                                               'В детский лагерь',
#                                                               'Об усыновлении (удочерении)')
#           and not data['certificate'].get('health', dict()).get('group')):
#
#         await ask_health_group_physical_regime_diet(message, state)
#
#     elif (data.get('certificate').get('doctor_flag')
#           and data['certificate'].get('type_certificate') == 'На кружки и секции'
#           and data.get('certificate').get('doctor_district') == '21'
#           and not data['certificate'].get('health', dict()).get('group')):
#         async with state.proxy() as data:
#             data['certificate']['health']['regime'] = '_'
#             data['certificate']['health']['diet'] = '_'
#             data['certificate']['health']['desk'] = '_'
#             data['certificate']['health']['vision'] = '_'
#
#         await ask_health_group_physical(message, state)
#
#     elif (data.get('certificate').get('doctor_flag')
#           and data['certificate'].get('type_certificate', '') == 'Оформление в ДДУ / СШ / ВУЗ'
#           and 'Для поступления в учреждения высшего' in data['certificate'].get('place_of_requirement', "")
#           and not data['certificate'].get('health').get('specialties')):
#         await message.answer(text="Введите специальности для поступления")
#         await FastCertificate.specialties.set()
#
#     elif not data['certificate'].get('birth_date'):
#         await message.answer(text='Введите дату рождения ребенка в формате ДД-ММ-ГГГГ')
#         await FastCertificate.birth_date.set()
#     elif not data['certificate'].get('gender'):
#         await ask_gender(message)
#     elif not data['certificate'].get('address'):
#         await ask_address(message, state)
#     elif not data['certificate'].get('place_of_requirement'):
#         await place_of_requirement(message, state)
#     elif not data['certificate'].get('count_of_certificates'):
#         if data.get('certificate').get('doctor_flag'):
#             await create_doc(message, state)
#         else:
#             await ask_count_of_certificate(message)
#     else:
#         if data.get('certificate').get('doctor_flag'):
#             await create_doc(message, state)
#         else:
#             await check_all_data(message, state)


# async def create_doc(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if not data['certificate'].get('amb_cart'):
#             await get_amb_card(message, state)
#     async with state.proxy() as data:
#         if data.get('certificate').get('doctor_flag'):
#             statistic_write(message.chat.id, f"Справка_DOC_{data['certificate'].get('doctor_name')}")
#
#         if not data['certificate'].get('additional_medical_information'):
#             data['certificate']['additional_medical_information'] = '_' * 60
#         if not data['certificate'].get('past_illnesses'):
#             data['certificate']['past_illnesses'] = '_' * 60
#         if not data['certificate'].get('validity_period'):
#             data['certificate']['validity_period'] = '_' * 15
#
#         if data['certificate'].get('type_certificate') in ('Годовой медосмотр', ''):
#             date = data['certificate']['birth_date']
#             while datetime.now() > datetime.strptime(date, "%d.%m.%Y"):
#                 day, month, year = date.split('.')
#                 year = str(int(year) + 1)
#                 date = '.'.join([day, month, year])
#             if (datetime.now().month == datetime.strptime(date, '%d.%m.%Y').month or
#                 (datetime.now() + timedelta(30)).month == datetime.strptime(date, "%d.%m.%Y").month) and \
#                     datetime.now().year >= datetime.strptime(date, '%d.%m.%Y').year:
#                 day, month, year = date.split('.')
#                 year = str(int(year) + 1)
#                 date = '.'.join([day, month, year])
#
#             data['certificate']['validity_period'] = (datetime.strptime(date, '%d.%m.%Y') -
#                                                       timedelta(1)).strftime('%d.%m.%Y')
#
#         if not data['certificate'].get('date_of_issue'):
#             data['certificate']['date_of_issue'] = '_' * 17
#         if not data['certificate'].get('recommendation'):
#             data['certificate']['recommendation'] = f"{'_' * 47}"
#         if not data['certificate']['gender']:
#             data['certificate']['gender'] = 'мужской/женский (подчеркнуть)'
#
#         render_data = dict()
#         doc_name = ''
#         render_data['time'] = datetime.now().strftime("%H:%M")
#         render_data['number_cert'] = ''
#         render_data['name'] = data['certificate']['name']
#         render_data['birth_date'] = data['certificate']['birth_date']
#         render_data['gender'] = data['certificate']['gender']
#         render_data['address'] = data['certificate']['address']
#         render_data['place_of_requirement'] = data['certificate'].get('place_of_requirement')
#         render_data['past_illnesses'] = data['certificate'].get('past_illnesses')
#         render_data['additional_medical_information'] = data['certificate'].get('additional_medical_information')
#         render_data['diagnosis'] = data['certificate'] \
#             .get('diagnosis', '').replace('diagnosis', data['certificate'].get('health', dict())
#                                           .get('add_diagnosis', '_' * 20))
#         render_data['recommendation'] = data['certificate'].get('recommendation')
#         render_data['date_of_issue'] = data['certificate'].get('date_of_issue')
#         render_data['validity_period'] = data['certificate'].get('validity_period')
#         render_data['doctor_name'] = data['certificate'].get('doctor_name')
#
#         if (data['certificate'].get('type_certificate') in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ')
#                 and data['certificate'].get('place_of_requirement') in ('Средняя школа (гимназия)',
#                                                                         'Детское Дошкольное Учреждение')):
#             render_data['recommendation'] = render_data.get('recommendation', '') + '\nРазрешены занятия в бассейне'
#             if (data['certificate'].get('doctor_district') == '19'
#                     and data['certificate'].get('place_of_requirement') != 'Средняя школа (гимназия)'):
#                 render_data['recommendation'] = \
#                     render_data.get('recommendation', '').replace('\nРазрешены занятия в бассейне', '')
#
#         if data['certificate'].get('type_certificate') in ('ЦКРОиР', 'О нуждаемости в сан-кур лечении',
#                                                            'Об усыновлении (удочерении)', 'Бесплатное питание') \
#                 or (data['certificate'].get('type_certificate') == 'Оформление в ДДУ / СШ / ВУЗ' and not
#         ('Для поступления в учреждения высшего' in data['certificate'].get('place_of_requirement') or
#          ('Для обучения в кадетском училище' in data['certificate'].get('place_of_requirement')))):
#             doctor_name, district, pediatric_division = doctors_info.get_info(message.chat.id)
#             if pediatric_division in ('1', '2'):
#                 number = get_max_number(pediatric_division, 'certificate_ped_div')
#                 if data['certificate'].get('type_certificate') in ('ЦКРОиР', 'Бесплатное питание'):
#                     type_cert = '7.9'
#                 else:
#                     type_cert = '7.6'
#                 info = (
#                     pediatric_division,
#                     district,
#                     number,
#                     datetime.now().strftime("%d.%m.%Y"),
#                     data['certificate'].get('name'),
#                     data['certificate'].get('birth_date'),
#                     data['certificate'].get('address'),
#                     type_cert,
#                     doctor_name
#                 )
#                 save_certificate_ped_div(data=info, type_table='certificate_ped_div')
#                 render_data['number_cert'] = f"№ {number}"
#
#         if (data.get('certificate').get('doctor_district') == '21'
#                 and data.get('certificate').get('doctor_flag')
#                 and data['certificate'].get('type_certificate') == 'На кружки и секции'):
#             render_data['diagnosis'] = render_data.get('diagnosis', '') + \
#                                        (f"\nГруппа здоровья: {data['certificate']['health'].get('group')}; "
#                                         f"Группа по физкультуре: "
#                                         f"{data['certificate']['health'].get('physical')};")
#
#         if data['certificate'].get('type_certificate') in ('Годовой медосмотр',
#                                                            'Оформление в ДДУ / СШ / ВУЗ',
#                                                            'В детский лагерь',
#                                                            'Об усыновлении (удочерении)'):
#
#             render_data['add_diagnosis'] = data['certificate'].get('health').get('add_diagnosis', '_' * 20)
#             age = get_age(data['certificate'].get('birth_date'))
#             if age >= 5:
#                 render_data['covid_vac'] = 'Предложена вакцинация против инфекции COVID-19\n' \
#                                            'Родители отказываются от проведения вакцинации'
#             else:
#                 render_data['covid_vac'] = ' '
#
#             if data['certificate'].get('type_certificate') == 'Оформление в ДДУ / СШ / ВУЗ' or age >= 11:
#                 render_data['hearing'] = '\nСлух в норме.'
#             else:
#                 render_data['hearing'] = ''
#             if age >= 4:
#                 render_data['posture'] = '\nОсанка не нарушена.'
#             else:
#                 render_data['posture'] = ''
#             anthropometry = {
#                 'мужской': {
#                     'weight': {
#                         1: [8.5, 8.9, 9.4, 10, 10.9, 11.6, 12.1, 1000],
#                         2: [10.6, 11, 11.7, 12.6, 13.5, 14.2, 15, 1000],
#                         3: [12.1, 12.8, 13.8, 14.8, 16, 16.9, 17.7, 1000],
#                         4: [13.4, 14.2, 15.1, 16.4, 17.8, 19.4, 20.3, 1000],
#                         5: [14.8, 15.7, 16.8, 18.3, 20, 21.7, 23.4, 1000],
#                         6: [16.3, 17.5, 18.8, 20.4, 22.6, 24.7, 26.7, 1000],
#                         7: [18, 19.5, 21, 22.9, 25.4, 28, 30.8, 1000],
#                         8: [20, 21.5, 23.3, 25.5, 28.3, 31.4, 35.5, 1000],
#                         9: [21.9, 23.5, 25.6, 28.1, 31.5, 35.1, 39.1, 1000],
#                         10: [23.9, 25.6, 28.2, 31.4, 35.1, 39.7, 44.7, 1000],
#                         11: [26, 28, 31, 34.9, 39.9, 44.9, 51.5, 1000],
#                         12: [28.2, 30.7, 34.4, 38.8, 45.1, 50.6, 58.7, 1000],
#                         13: [30.9, 33.8, 38, 43.4, 50.6, 56.8, 66, 1000],
#                         14: [34.3, 38, 42.8, 48.8, 56.6, 63.4, 73.2, 1000],
#                         15: [38.7, 43, 48.3, 54.8, 62.8, 70, 80.1, 1000],
#                         16: [44, 48.3, 54, 61, 69.6, 76.5, 84.7, 1000],
#                         17: [49.3, 54.6, 59.8, 66.3, 74, 80.1, 87.8, 1000]},
#                     'height': {
#                         1: [71.2, 72.3, 74, 75.5, 77.3, 79.7, 81.7, 1000],
#                         2: [81.3, 83, 84.5, 86.8, 89, 90.8, 94, 1000],
#                         3: [88, 90, 92.3, 96, 99.8, 102, 104.5, 1000],
#                         4: [93.2, 95.5, 98.3, 102, 105.5, 108, 110.6, 1000],
#                         5: [98.9, 101.5, 104.4, 108.3, 112, 114.5, 117, 1000],
#                         6: [105, 107.7, 110.9, 115, 118.7, 121.1, 123.8, 1000],
#                         7: [111, 113.6, 116.8, 121.2, 125, 128, 130.6, 1000],
#                         8: [116.3, 119, 122.1, 126.9, 130.8, 134.5, 137, 1000],
#                         9: [121.5, 124.7, 125.6, 133.4, 136.3, 140.3, 143, 1000],
#                         10: [126.3, 129.4, 133, 137.8, 142, 146.7, 149.2, 1000],
#                         11: [131.3, 134.5, 138.5, 143.2, 148.3, 152.9, 156.2, 1000],
#                         12: [136.2, 140, 143.6, 149.2, 154.5, 159.5, 163.5, 1000],
#                         13: [141.8, 145.7, 149.8, 154.8, 160.6, 166, 170.7, 1000],
#                         14: [148.3, 152.3, 156.2, 161.2, 167.7, 172, 176.7, 1000],
#                         15: [154.6, 158.6, 162.5, 166.8, 173.5, 177.6, 181.6, 1000],
#                         16: [158.8, 163.2, 166.8, 173.3, 177.8, 182, 186.3, 1000],
#                         17: [162.8, 166.6, 171.6, 177.3, 181.6, 186, 188.5, 1000]}},
#
#                 'женский': {
#                     'weight': {
#                         1: [8, 8.5, 9, 9.6, 10.2, 10.8, 11.3, 1000],
#                         2: [10.2, 10.8, 11.3, 12.1, 12.8, 13.5, 14.1, 1000],
#                         3: [11.7, 12.5, 13.3, 13.7, 15.5, 16.5, 17.6, 1000],
#                         4: [13, 14, 14.8, 15.9, 17.6, 18.9, 20, 1000],
#                         5: [14.7, 15.7, 16.6, 18.1, 19.7, 21.6, 23.2, 1000],
#                         6: [16.3, 17.4, 18.7, 20.4, 22.5, 24.8, 27.1, 1000],
#                         7: [17.9, 19.4, 20.6, 22.7, 25.3, 28.3, 31.6, 1000],
#                         8: [20, 21.4, 23, 25.1, 28.5, 32.1, 36.3, 1000],
#                         9: [21.9, 23.4, 25.5, 28.2, 32, 36.3, 41, 1000],
#                         10: [22.7, 25, 27.7, 30.6, 34.9, 39.8, 47.4, 1000],
#                         11: [24.9, 27.8, 30.7, 34.3, 38.9, 44.6, 55.2, 1000],
#                         12: [27.8, 31.8, 36, 40, 45.4, 51.8, 63.4, 1000],
#                         13: [32, 38.7, 43, 47.5, 52.5, 59, 69, 1000],
#                         14: [37.6, 43.8, 48.2, 52.8, 58, 64, 72.2, 1000],
#                         15: [42, 46.8, 50.6, 55.2, 60.4, 66.5, 74.9, 1000],
#                         16: [45.2, 48.4, 51.8, 56.5, 61.3, 67.6, 75.6, 1000],
#                         17: [46.2, 49.2, 52.9, 57.3, 61.9, 68, 76, 1000]},
#                     'height': {
#                         1: [70.1, 71.4, 72.8, 74.1, 75.8, 78, 79.6, 1000],
#                         2: [80.1, 81.7, 83.3, 85.2, 87.5, 90.1, 92.5, 1000],
#                         3: [89, 90.8, 93, 95.5, 98.1, 100.7, 103.1, 1000],
#                         4: [94, 96.1, 98.5, 101.5, 104.1, 106.9, 109.7, 1000],
#                         5: [100, 102.5, 104.7, 107.5, 110.7, 113.6, 116.7, 1000],
#                         6: [105.3, 108, 110.9, 114.1, 118, 120.6, 124, 1000],
#                         7: [111.1, 113.6, 116.9, 120.8, 124.8, 128, 131.3, 1000],
#                         8: [116.5, 119.3, 123, 127.2, 131, 134.3, 137.7, 1000],
#                         9: [122, 124.8, 128.4, 132.8, 137, 140.5, 144.8, 1000],
#                         10: [127, 130.5, 134.3, 139, 142.9, 146.7, 151, 1000],
#                         11: [131.8, 136.2, 140.2, 145.3, 148.8, 153.2, 157.7, 1000],
#                         12: [137.6, 142.2, 145.9, 150.4, 154.2, 159.2, 163.2, 1000],
#                         13: [143, 148.3, 151.8, 155.5, 159.8, 163.7, 168, 1000],
#                         14: [147.8, 152.6, 155.4, 159, 163.6, 167.2, 171.2, 1000],
#                         15: [150.7, 154.4, 157.2, 161.2, 166, 169.2, 173.4, 1000],
#                         16: [151.6, 155.2, 158, 162.5, 166.8, 170.2, 173.8, 1000],
#                         17: [152.2, 155.8, 158.6, 162.8, 169.2, 170.4, 174.2, 1000]}
#                 }
#             }
#
#             indicators = {
#                 '0-3': {
#                     'br': (22, 28),
#                     'hr': (80, 100),
#                     'bp': (90, 100, 60, 70)},
#                 '3-6': {
#                     'br': (20, 28),
#                     'hr': (80, 100),
#                     'bp': (96, 110, 60, 70)},
#                 '6-12': {
#                     'br': (18, 22),
#                     'hr': (70, 90),
#                     'bp': (100, 110, 60, 75)},
#                 '>12': {
#                     'br': (18, 22),
#                     'hr': (70, 80),
#                     'bp': (110, 120, 70, 78)},
#             }
#
#             if age <= 3:
#                 indicator = indicators['0-3']
#             elif age <= 6:
#                 indicator = indicators['3-6']
#             elif age <= 12:
#                 indicator = indicators['6-12']
#             else:
#                 indicator = indicators['>12']
#
#             render_data['temp'] = random.choice(['36,6', '36,7', '36,5'])
#             render_data['br'] = random.randrange(start=indicator['br'][0], stop=indicator['br'][1], step=2)
#             render_data['hr'] = random.randrange(start=indicator['hr'][0], stop=indicator['hr'][1], step=2)
#             render_data['bp'] = f"{random.randrange(start=indicator['bp'][0], stop=indicator['bp'][1], step=1)}/" \
#                                 f"{random.randrange(start=indicator['bp'][2], stop=indicator['bp'][3], step=1)}"
#
#             render_data['diagnosis'] = render_data.get('diagnosis', '').replace(
#                 'Группа здоровья: _ ; Группа по физкультуре: _ ;',
#                 f"Группа здоровья: {data['certificate']['health'].get('group')}; "
#                 f"Группа по физкультуре: "
#                 f"{data['certificate']['health'].get('physical')};")
#
#             render_data['recommendation'] = render_data.get('recommendation', '').replace(
#                 'Режим _', f"Режим {data['certificate']['health'].get('regime')}")
#             render_data['recommendation'] = render_data.get('recommendation', '').replace(
#                 'Стол _', f"Стол {data['certificate']['health'].get('diet')}")
#             if render_data.get('place_of_requirement', '') == 'Детское Дошкольное Учреждение':
#                 desk = 'Мебель'
#             else:
#                 desk = 'Парта'
#             render_data['recommendation'] = render_data.get('recommendation', '').replace(
#                 'Парта _', f"{desk} {data['certificate']['health'].get('desk')}")
#
#             render_data['height'] = data['certificate']['health'].get('height')
#             render_data['weight'] = data['certificate']['health'].get('weight')
#             render_data['group'] = data['certificate']['health'].get('group')
#             render_data['physical'] = data['certificate']['health'].get('physical')
#             render_data['regime'] = data['certificate']['health'].get('regime')
#             render_data['diet'] = data['certificate']['health'].get('diet')
#             render_data['desk'] = f"{desk}: {data['certificate']['health'].get('desk')}"
#
#             height = None
#             weight = None
#             anthro = ' (выше- ниже-) среднее, (дис-) гармоничное'
#
#             if render_data.get('height')[0].isdigit():
#                 height = float(render_data.get('height'))
#                 weight = float(render_data.get('weight'))
#                 if render_data.get('gender').lower().startswith('м'):
#                     anthro_height = anthropometry['мужской']['height'].get(age, [])
#                     anthro_weight = anthropometry['мужской']['weight'].get(age, [])
#                 else:
#                     anthro_height = anthropometry['женский']['height'].get(age, [])
#                     anthro_weight = anthropometry['женский']['weight'].get(age, [])
#                 if anthro_height:
#                     for a_height in anthro_height:
#                         if height < a_height:
#                             index_height = anthro_height.index(a_height)
#                             break
#                     else:
#                         index_height = 7
#
#                 if anthro_weight:
#                     for a_weight in anthro_weight:
#                         if weight <= a_weight:
#                             index_weight = anthro_weight.index(a_weight)
#                             break
#                     else:
#                         index_weight = 7
#                     if index_height == 0:
#                         anthro = 'Низкое '
#                     elif index_height <= 2:
#                         anthro = 'Ниже среднего '
#                     elif index_height <= 4:
#                         anthro = 'Среднее '
#                     elif index_height <= 6:
#                         anthro = 'Выше среднего '
#                     elif index_height == 7:
#                         anthro = 'Высокое '
#
#                     if abs(index_weight - index_height) <= 1:
#                         anthro += 'гармоничное'
#                     elif abs(index_weight - index_height) < 3:
#                         anthro += 'дисгармоничное'
#                     else:
#                         anthro += 'резко дисгармоничное'
#
#                     if 'Физическое развитие (выше- ниже-) среднее, (дис-) гармоничное' in render_data.get('diagnosis'):
#                         render_data['diagnosis'] = \
#                             render_data.get('diagnosis').replace('Физическое развитие (выше- ниже-) '
#                                                                  'среднее, (дис-) гармоничное',
#                                                                  f"Физическое развитие: {anthro}")
#
#             render_data['anthro'] = anthro
#
#             if data['certificate'].get('type_certificate') in ('Годовой медосмотр',
#                                                                'Оформление в ДДУ / СШ / ВУЗ'):
#                 render_data['visus'] = f"VIS OD/OS\n= {data['certificate']['health'].get('vision')}\n"
#             else:
#                 render_data['visus'] = ''
#             render_data['additional_medical_information'] = \
#                 render_data.get('additional_medical_information',
#                                 '').replace('Vis OD/OS = __________',
#                                             f"Vis OD/OS = {data['certificate']['health'].get('vision')}")
#
#             if render_data.get('height')[0].isdigit():
#                 render_data['imt'] = round(float(render_data.get('weight')) /
#                                            (float(render_data.get('height')) / 100) ** 2, 1)
#             else:
#                 render_data['imt'] = '______'
#
#             render_data['additional_medical_information'] = render_data.get('additional_medical_information',
#                                                                             '').replace(
#                 'Рост _____ см', f"Рост: {data['certificate']['health'].get('height')} см")
#             render_data['additional_medical_information'] = render_data.get('additional_medical_information',
#                                                                             '').replace(
#                 'Вес _____ кг', f"Вес {data['certificate']['health'].get('weight')} кг")
#             render_data['additional_medical_information'] = render_data.get('additional_medical_information',
#                                                                             '').replace(
#                 'АД ________', f"АД {render_data['bp']} мм.рт.ст.")
#             render_data['diagnosis'] = render_data.get('diagnosis', '').replace(
#                 'школе с _______ лет', f"школе с {age} лет")
#
#             if data['certificate']['health'].get('type'):
#                 render_data['type'] = data['certificate']['health']['type']
#             else:
#                 render_data['type'] = data['certificate'].get('type_certificate')
#
#             if data['certificate']['health'].get('allergy'):
#                 render_data['allergy'] = data['certificate']['health']['allergy']
#             else:
#                 render_data['allergy'] = ' '
#
#             if data['certificate']['health'].get('chickenpox'):
#                 render_data['chickenpox'] = data['certificate']['health']['chickenpox']
#             else:
#                 render_data['chickenpox'] = ' '
#
#             if data['certificate']['health'].get('injury'):
#                 render_data['injury'] = data['certificate']['health']['injury']
#             else:
#                 render_data['injury'] = ' '
#
#         if data['certificate'].get('type_certificate') in ('Оформление в ДДУ / СШ / ВУЗ',
#                                                            'Об усыновлении (удочерении)'):
#             doc_name = ""
#             if data['certificate'].get('type_certificate') == 'Оформление в ДДУ / СШ / ВУЗ':
#                 doc_name = f".{os.sep}generated{os.sep}{data['certificate'].get('name').split()[0]} " \
#                            f"справка Оформление.docx"
#                 if not render_data.get('number_cert'):
#                     render_data['number_cert'] = '№ ______'
#             elif data['certificate'].get('type_certificate') == 'Об усыновлении (удочерении)':
#                 doc_name = f".{os.sep}generated{os.sep}{data['certificate'].get('name').split()[0]} " \
#                            f"справка Об усыновлении.docx"
#
#             if 'Для поступления в учреждения высшего' in data['certificate'].get('place_of_requirement'):
#                 render_data['name'] += f'\nИдентификационный № _______________________________'
#                 render_data['diagnosis'] = render_data.get('diagnosis'). \
#                     replace('специальности: _', f"специальности: \n"
#                                                 f"{data['certificate'].get('health').get('specialties')}")
#                 age = get_age(data['certificate'].get('birth_date'))
#                 if age >= 17:
#                     render_data['additional_medical_information'] += '\nФлюорография: № _________ от __ . __ . ____ ' \
#                                                                      'Заключение: ОГК без патологии'
#                 else:
#                     render_data['additional_medical_information'] += '\nФлюорография: не подлежит по возрасту.'
#
#             manager = doctors_info.get_manager(message.chat.id)
#             if manager:
#                 render_data['manager'] = manager
#             else:
#                 render_data['manager'] = '______________________'
#
#             doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}справка а4 годовая.docx")
#             doc.render(render_data)
#             doc.save(doc_name)
#
#             if create_vaccination(user_id=data['certificate'].get('amb_cart'),
#                                   size=4,
#                                   doctor_id=message.chat.id):
#                 master = Document(doc_name)
#                 master.add_page_break()
#                 composer = Composer(master)
#                 doc_temp = Document(f'.{os.sep}generated{os.sep}прививки.docx')
#                 composer.append(doc_temp)
#                 composer.save(doc_name)
#             text = f"Дата оформления: {data['certificate'].get('date_of_issue')}\n" \
#                    f"ФИО: {data['certificate'].get('name')}; {data['certificate'].get('birth_date')} ; " \
#                    f"Тип справки: {data['certificate'].get('type_certificate')}\n" \
#                    f"Адрес: {data['certificate'].get('address')}\n" \
#                    f"Порядковый номер справки: {render_data.get('number_cert')}"
#
#             if data.get('create_doc'):
#                 text += f"\npatient_id: {data['certificate'].get('patient_id')}"
#
#             file = open(doc_name, 'rb')
#             await bot.send_document(chat_id=message.chat.id, document=file, caption=text)
#
#             doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}осмотр.docx")
#             doc.render(render_data)
#             doc.save(f".{os.sep}generated{os.sep}{data['certificate'].get('name').split()[0]} осмотр.docx")
#             file = open(f".{os.sep}generated{os.sep}{data['certificate'].get('name').split()[0]} осмотр.docx", 'rb')
#             await bot.send_document(chat_id=message.chat.id, document=file)
#             await delete_message(message, state)
#
#         else:
#
#             if data['certificate'].get('type_certificate').startswith('ЦКРОиР'):
#                 doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}выписка ЦКРОиР.docx")
#                 doc.render(render_data)
#                 doc_name = f".{os.sep}generated{os.sep}{data['certificate'].get('name').split()[0]} выписка ЦКРОиР.docx"
#                 doc.save(doc_name)
#
#             elif data['certificate'].get('type_certificate').startswith('Бесплатное питание'):
#                 doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}Выписка.docx")
#                 doc.render(render_data)
#                 doc_name = f".{os.sep}generated{os.sep}{data['certificate'].get('name').split()[0]} Выписка.docx"
#                 doc.save(doc_name)
#
#             elif data['certificate'].get('type_certificate') in ('Годовой медосмотр', 'В детский лагерь'):
#                 if data['certificate'].get('type_certificate').startswith('В детский лагерь'):
#                     number = get_max_number(data['certificate'].get('doctor_district'), 'certificate_camp')
#                     info = (
#
#                         data['certificate'].get('doctor_district'),
#                         number,
#                         datetime.now().strftime("%d.%m.%Y"),
#                         data['certificate'].get('name'),
#                         data['certificate'].get('birth_date'),
#                         data['certificate'].get('gender'),
#                         data['certificate'].get('address')
#                     )
#                     save_certificate_ped_div(data=info, type_table='certificate_camp')
#                     render_data['number_cert'] = f"№ {data['certificate'].get('doctor_district')} / {number}"
#                 doc_name = f".{os.sep}generated{os.sep}{data['certificate'].get('name').split()[0]} " \
#                            f"справка {data['certificate'].get('type_certificate')}.docx"
#
#                 master = Document(f".{os.sep}example{os.sep}certificate{os.sep}справка а5.docx")
#                 master.add_page_break()
#                 composer = Composer(master)
#
#                 if data['certificate'].get('type_certificate').startswith('В детский лагерь'):
#                     if create_vaccination(user_id=data['certificate'].get('amb_cart'),
#                                           size=5,
#                                           doctor_id=message.chat.id):
#                         doc_temp = Document(f'.{os.sep}generated{os.sep}прививки.docx')
#                         composer.append(doc_temp)
#                         master.add_page_break()
#
#                 master.add_section()
#                 master.sections[-1].orientation = WD_ORIENT.LANDSCAPE
#                 master.sections[-1].page_width = master.sections[0].page_height
#                 master.sections[-1].page_height = master.sections[0].page_width
#                 doc_temp = Document(f".{os.sep}example{os.sep}certificate{os.sep}осмотр.docx")
#                 composer.append(doc_temp)
#
#                 composer.save(doc_name)
#
#                 doc = DocxTemplate(doc_name)
#                 doc.render(render_data)
#
#                 doc.save(doc_name)
#
#             else:
#                 doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}справка а5.docx")
#                 doc.render(render_data)
#                 doc_name = f".{os.sep}generated{os.sep}{data['certificate'].get('name').split()[0]} " \
#                            f"справка {data['certificate'].get('type_certificate')}.docx"
#                 doc.save(doc_name)
#
#                 if (data['certificate'].get('type_certificate') in ('В детский лагерь',
#                                                                     'Может работать по специальности...') or
#                         (data['certificate'].get('type_certificate') == 'Об отсутствии контактов' and
#                          data['certificate'].get('place_of_requirement') == 'В стационар')):
#                     print("data['certificate'].get('amb_cart') _________: ", data['certificate'].get('amb_cart'))
#
#                     if create_vaccination(user_id=data['certificate'].get('amb_cart'),
#                                           size=5,
#                                           doctor_id=message.chat.id):
#                         master = Document(doc_name)
#                         master.add_page_break()
#                         composer = Composer(master)
#                         doc_temp = Document(f'.{os.sep}generated{os.sep}прививки.docx')
#                         composer.append(doc_temp)
#                         composer.save(doc_name)
#
#             text = f"ФИО: {data['certificate'].get('name')}; {data['certificate'].get('birth_date')} ; " \
#                    f"Тип справки: {data['certificate'].get('type_certificate')}\n" \
#                    f"Адрес: {data['certificate'].get('address')}\n" \
#                    f"Порядковый номер справки: {render_data.get('number_cert')}\n" \
#                    f"Дата оформления: {data['certificate'].get('date_of_issue')}\n" \
#                    f"Количество справок: {data['certificate'].get('count_of_certificates')}"
#
#             if data.get('create_doc'):
#                 text += f"\npatient_id: {data['certificate'].get('patient_id')}"
#             file = open(doc_name, 'rb')
#             await bot.send_document(chat_id=message.chat.id, document=file, caption=text)
#
#     if data.get('certificate') and data['certificate'].get('doctor_flag'):
#         if data.get('card_file'):
#             async with state.proxy() as data:
#                 data['certificate'] = None
#             from .card_file import ask_to_do, CardFile
#             await ask_to_do(message, state)
#             await CardFile.ask_to_do.set()
#         # elif data.get('create_doc'):
#         #     return doc_name
#         else:
#             await exit_in_main(message, state)
#     else:
#         await exit_in_main(message, state)
