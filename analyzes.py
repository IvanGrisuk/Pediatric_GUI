from tkinter import *
from datetime import datetime
import os

from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document as Document_compose
import sqlite3 as sq


import data_base

data = dict()
all_blanks = {
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


def append_info(info):
    if isinstance(info, tuple):
        info = info[0]
    for key in info:
        print(key)
        data[key] = info.get(key)
    ask_analyzes()


def ask_analyzes():

    analyzes_root = Toplevel()
    analyzes_root.title('Выбор анализов')
    analyzes_root.config(bg='white')

    Label(analyzes_root, text='Выберите анализы',
          font=('Comic Sans MS', data.get('text_size')), bg='white').pack(fill='both', expand=True,
                                                                          padx=2, pady=2)

    def create_analyzes():
        user_analyzes = dict()
        for category_b in all_blanks:
            for analyzes_lbl in analyzes_vars.get(category_b):
                if analyzes_vars[category_b].get(analyzes_lbl).get() == 1:
                    if not user_analyzes.get(category_b):
                        user_analyzes[category_b] = list()
                    user_analyzes[category_b].append(analyzes_lbl)
        create_doc(user_analyzes)
        analyzes_root.quit()

    def select_analyzes():
        for category_b in all_blanks:
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
                    print(button)
                    active_btn = analyzes_buttons.get(button)
                    active_btn['text'] = f"✔{button}"
                    active_btn['bg'] = '#2efefa'

                    for category_b in all_blanks:
                        if button in all_blanks.get(category_b):

                            active_btn = analyzes_vars[category_b].get(button)
                            active_btn.set(1)

    analyzes_vars = dict()
    analyzes_buttons = dict()
    for category in all_blanks:
        analyzes_vars[category] = dict()
        for analyzes in all_blanks.get(category)[1:]:
            analyzes_vars[category][analyzes] = IntVar()

    analyzes_category_vars = dict()
    for analyzes in all_blanks.get('add')[1:]:
        analyzes_category_vars[analyzes] = IntVar()

    for category in all_blanks:
        frame = Frame(analyzes_root, borderwidth=1, relief="solid", padx=4, pady=4)

        row, col = 1, 0
        Label(frame, text=f"{all_blanks.get(category)[0]}",
              font=('Comic Sans MS', data.get('text_size')), bg='white').grid(column=0, row=0, columnspan=3,
                                                                              sticky='ew')
        if category == 'add':

            for analyzes in all_blanks.get(category)[1:]:
                btn = Checkbutton(frame, text=analyzes,
                                  font=('Comic Sans MS', data.get('text_size')),
                                  variable=analyzes_category_vars.get(analyzes), command=select_category_analyzes,
                                  onvalue=1, offvalue=0, indicatoron=False, selectcolor='blue', bg='#cdcdcd')
                btn.grid(row=row, column=col, sticky='ew')
                analyzes_buttons[analyzes] = btn
                col += 1
                if col == 3:
                    row += 1
                    col = 0

        else:
            for analyzes in all_blanks.get(category)[1:]:

                btn = Checkbutton(frame, text=analyzes,
                                  font=('Comic Sans MS', data.get('text_size')),
                                  variable=analyzes_vars[category].get(analyzes), command=select_analyzes,
                                  onvalue=1, offvalue=0, indicatoron=False, selectcolor='blue', bg='#cdcdcd')
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


def create_doc(analyzes):
    print(analyzes)
    render_data = dict()

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
        with sq.connect(f'patient_data_base.db') as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT Прививки FROM patient_data WHERE amb_cart LIKE '{data.get('amb_cart')}'")
            vaccination = cur.fetchone()[0]
        if vaccination:
            print(vaccination)
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
            print(text)
            if not text:
                text = 'Нет данных о вакцинации\n'

        else:
            text = 'Нет данных о вакцинации\n'

        render_data['VGB_vaccination'] = text

    if 'МАЗОК НА КОВИД' in analyzes.get('swab', []):

        with sq.connect('patient_data_base.db') as conn:
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

    master = Document_compose(all_links.pop(0))
    composer = Composer(master)
    for link in all_links:
        master.add_page_break()
        doc_temp = Document_compose(link)
        composer.append(doc_temp)
    composer.save(f".{os.sep}generated{os.sep}Анализы.docx")
    os.system(f"start .{os.sep}generated{os.sep}Анализы.docx")
    data_base.statistic_write('приложение', f"Анализы_DOC_{data.get('doctor_name')}")
    render_data.clear()
    data.clear()
