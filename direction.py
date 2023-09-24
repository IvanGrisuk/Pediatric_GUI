from tkinter import *
from datetime import datetime
import os

from docx import Document
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from tkinter import messagebox

import vaccinations
import data_base


all_blanks = {
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

address = {'РНПЦ ДХ': 'пр. Независимости 64',
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

type_direct = ('НА ГОСПИТАЛИЗАЦИЮ', 'НА КОНСУЛЬТАЦИЮ', 'НА РЕНТГЕНОГРАММУ')

render_data = dict()
data = dict()


def append_info(info):
    if isinstance(info, tuple):
        info = info[0]
    for key in info:
        print(key)
        data[key] = info.get(key)
    ask_type_blanks()


def ask_type_blanks():
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
            create_direction()

    for mark in type_direct:
        btn = Radiobutton(frame_where, text=mark,
                          font=('Comic Sans MS', data.get('text_size')),
                          value=mark, variable=selected_where,
                          command=select_where, indicatoron=False, selectcolor='blue')
        btn.grid(row=0, column=(type_direct.index(mark) + 1), sticky='ew')

    frame_where.columnconfigure(index='all', minsize=40, weight=1)
    frame_where.rowconfigure(index='all', minsize=20)
    frame_where.pack(fill='both', expand=True, padx=2, pady=2)

    frame_hospital = Frame(type_blanks_root, borderwidth=1, relief="solid", padx=4, pady=4)
    Label(frame_hospital, text="Куда направить:",
          font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0, rowspan=5)

    selected_hospital = StringVar()

    def select_hospital():
        data['hospital'] = selected_hospital.get()

    row, col = 1, 0
    for mark in all_blanks.get('hospital'):
        if '- - -' in mark:
            col = 0
            row += 2
            Label(frame_hospital, text=mark,
                  font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=col, row=row - 1, rowspan=5)
        else:

            btn = Radiobutton(frame_hospital, text=mark,
                              font=('Comic Sans MS', data.get('text_size')),
                              value=mark, variable=selected_hospital,
                              command=select_hospital, indicatoron=False, selectcolor='blue')
            btn.grid(row=row, column=col, sticky='ew')
            col += 1
            if col == 5:
                row += 1
                col = 0

    frame_hospital.columnconfigure(index='all', minsize=40, weight=1)
    frame_hospital.rowconfigure(index='all', minsize=20)

    frame_doctor = Frame(type_blanks_root, borderwidth=1, relief="solid", padx=4, pady=4)
    Label(frame_doctor, text="На консультацию:",
          font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0, rowspan=5)

    selected_doctor = StringVar()

    def select_doctor():
        data['direction_doctor'] = selected_doctor.get()

    row, col = 1, 0
    for mark in all_blanks.get('doctor'):

        btn = Radiobutton(frame_doctor, text=mark,
                          font=('Comic Sans MS', data.get('text_size')),
                          value=mark, variable=selected_doctor,
                          command=select_doctor, indicatoron=False, selectcolor='blue')
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
            create_direction()

    but_create_doc = Button(type_blanks_root, text='Создать направление', command=create_doc,
                            font=('Comic Sans MS', data.get('text_size')))

    type_blanks_root.mainloop()


async def create_direction():

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
    render_data['address_hospital'] = address.get(data.get('hospital', ''))

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
    doc.save(f".{os.sep}generated{os.sep}Направление.docx")

    if data.get('type_direction') == 'НА ГОСПИТАЛИЗАЦИЮ':
        if vaccinations.create_vaccination(user_id=data.get('amb_cart'), size=5):
            master = Document(f".{os.sep}generated{os.sep}Направление.docx")
            master.add_page_break()
            composer = Composer(master)
            doc_temp = Document(f'.{os.sep}generated{os.sep}прививки.docx')
            composer.append(doc_temp)
            composer.save(f".{os.sep}generated{os.sep}Направление.docx")

    os.system(f"start .{os.sep}generated{os.sep}Направление.docx")
    data_base.statistic_write('приложение', f"Направления_DOC_{data.get('doctor_name')}")
