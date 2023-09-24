from tkinter import *
from datetime import datetime, timedelta
import os

from docxtpl import DocxTemplate

import data_base


render_data = dict()
data = dict()
blanks = ('Диспансеризация',
          "Информирование_законного_представителя",
          "Тест_аутизма_у_детей",
          "Анкета_по_слуху",
          "Анкета_ПАВ")


def append_info(info):
    if isinstance(info, tuple):
        info = info[0]
    for key in info:
        print(key)
        data[key] = info.get(key)
    ask_type_blanks()


def ask_type_blanks():
    def select_type_blanks(event):
        num = ''
        for i in str(event.widget).split('.!')[-1]:
            if i.isdigit():
                num += i

        doc = DocxTemplate(f".{os.sep}example{os.sep}амб_карта{os.sep}{blanks[int(num)-2]}.docx")
        doc.render(render_data)
        file_name = f".{os.sep}generated{os.sep}{blanks[int(num)-2]}_{data.get('patient_name').split()[0]}.docx"
        doc.save(file_name)
        os.system(f"start {file_name}")
        data_base.statistic_write('приложение', f"Вкладыши_DOC_{data.get('doctor_name')}")

    def close_window():
        data.clear()
        render_data.clear()
        type_blanks_root.destroy()
        type_blanks_root.quit()

    type_blanks_root = Toplevel()
    type_blanks_root.title('Выбор бланков')
    type_blanks_root.config(bg='white')

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
