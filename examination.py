

def paste_examination(root_examination: Toplevel, examination_root: Frame, child_marker=False):

    destroy_elements = dict()
    data['examination'] = dict()
    render_data = dict()
    data['examination']['all_kb_status'] = 'open'
    data['examination']['selected_drugs'] = dict()

    selected_place = StringVar()
    selected_diagnosis = StringVar()
    selected_type_ln = StringVar()
    # err_msd_weight = StringVar()
    selected_examination_frame = StringVar()
    selected_prescription_frame = StringVar()

    selected_button = StringVar()
    selected_examination_button = StringVar()
    selected_diagnosis_button = StringVar()
    selected_recommendation_button = StringVar()

    patient_age = get_age_d_m_y(patient.get('birth_date'))
    age = patient_age.get('year')
    patient_age_local = StringVar()
    txt_date_time = StringVar()

    patient_banner = StringVar()
    animation = StringVar()

    # Label(examination_root, textvariable=patient_banner,
    #       font=('Comic Sans MS', user.get('text_size')),
    #       bg="#36566d", fg='white').pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)
    Label(examination_root, textvariable=animation,
          font=('Comic Sans MS', user.get('text_size')),
          bg="#36566d", fg='white').pack(fill='both', expand=True)

    def start_action(func=None):
        def check_thread(thread):
            if thread.is_alive():

                animation.set(animation.get()[-1] + animation.get()[:-1])
                # root.update()
                root_examination.after(200, lambda: check_thread(thread))
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

    def upload_last_data():

        found_info = data_base(command='examination__upload_last_data')
        local_info = {
            'select_past_examination': list(),
            'get_last_doc_LN': {
                "Справка ВН": list(),
                "Лист ВН": list()},
            'get_last_patient_ln': {
                "Справка ВН": list(),
                "Лист ВН": list()},
            'get_last_anthro_data': dict(),
            'LN_data': {
                'last_patient_ln': dict()},
            'anamnesis': ''
        }

        if found_info.get('get_last_doc_LN'):
            for ln_info in found_info.get('get_last_doc_LN'):
                for ln_data in ("Справка ВН", "Лист ВН"):
                    if ln_info[0].startswith(ln_data):
                        local_info['get_last_doc_LN'][ln_data].append(ln_info[0])

        if found_info.get('select_past_examination'):
            for rowid, date_time, doctor_name, status, LN_type, patient_info, examination_text, examination_key \
                    in sorted(found_info.get('select_past_examination'),
                              key=lambda i: (datetime.now() -
                                             datetime.strptime(f"{i[1]}", "%d.%m.%Y %H:%M:%S")).total_seconds()):

                local_info['select_past_examination'].append((rowid, date_time, doctor_name, status, LN_type,
                                                              patient_info, examination_text, examination_key))
                for ln_data in ("Справка ВН", "Лист ВН"):
                    if LN_type.startswith(ln_data):
                        local_info['get_last_patient_ln'][ln_data].append((date_time, LN_type))


                if child_marker:
                    if not local_info.get('get_last_anthro_data'):
                        if ('type_examination:____child__' in examination_key
                                and 'txt_weight_variable' in examination_key):
                            for string in examination_key.split('__<end!>__\n'):
                                if string.startswith('patient_anthro_data:____'):
                                    for marker in string.replace('patient_anthro_data:____', '').split("____"):
                                        if len(marker.split('__')) == 2:
                                            name, variable = marker.split('__')
                                            if name in ('txt_weight_bir_variable', 'txt_weight_variable'):
                                                local_info['get_last_anthro_data'][name] = variable
                    if not local_info.get('get_last_diagnosis_text'):
                        for string in examination_key.split('__<end!>__\n'):
                            if string.startswith('diagnosis_text:____'):
                                local_info['get_last_diagnosis_text'] = string.replace('diagnosis_text:____', '')

                else:
                    if not local_info.get('anamnesis'):
                        if (datetime.now() - datetime.strptime(date_time, "%d.%m.%Y %H:%M:%S")).total_seconds() < 2592000:
                            if 'anamnesis:____' in examination_key:
                                for string in examination_key.split('__<end!>__\n'):
                                    if string.startswith('anamnesis:____'):
                                        txt_anamnesis.insert(1.0, string.replace('anamnesis:____', ''))
                                        local_info['anamnesis'] = 'True'
                        else:
                            local_info['anamnesis'] = 'None'

                    if not local_info.get('get_last_anthro_data'):
                        if ('type_examination:____adult__' in examination_key
                                and 'txt_weight_variable' in examination_key) or (
                                'type_examination:____certificate__' in examination_key
                            and 'weight__' in examination_key
                        ):

                            for string in examination_key.split('__<end!>__\n'):
                                if string.startswith('patient_anthro'):
                                    for marker in string.split("____"):
                                        if len(marker.split('__')) == 2:
                                            name, variable = marker.split('__')
                                            if name in ('txt_weight_variable', 'weight'):
                                                local_info['get_last_anthro_data']['txt_weight_variable'] = variable


                    if 'LN_blank_data:____' in examination_key:
                        for string in examination_key.split('__<end!>__\n'):
                            if string.startswith('LN_blank_data:____'):
                                local_ln_data = {
                                    "Дата осмотра": date_time,
                                    "Фамилия": "",
                                    "Имя": "",
                                    "Отчество": "",
                                    "Дата рождения": "",
                                    "Место работы (службы, учебы)": "",
                                    "Информация про ребенка (в корешок)": ""}
                                for marker in string.replace('LN_blank_data:____', '').split("____"):
                                    if len(marker.split('__')) == 2:
                                        name, variable = marker.split('__')
                                        if name in local_ln_data:
                                            local_ln_data[name] = variable
                                if (local_ln_data.get('Фамилия')
                                        and local_ln_data.get('Дата рождения')):

                                    key = f"{local_ln_data.get('Фамилия')} " \
                                          f"{local_ln_data.get('Имя')} " \
                                          f"{local_ln_data.get('Отчество')} -- " \
                                          f"{local_ln_data.get('Дата рождения')} -- " \
                                          f"{local_ln_data.get('Место работы (службы, учебы)')} -- " \
                                          f"{local_ln_data.get('Информация про ребенка (в корешок)')}"
                                    local_info['LN_data']['last_patient_ln'][key] = local_ln_data.copy()

        for ln_data in ("Справка ВН", "Лист ВН"):
            if local_info['get_last_patient_ln'].get(ln_data):
                last_visit = min(local_info['get_last_patient_ln'].get(ln_data),
                                 key=lambda i: (datetime.now() -
                                                datetime.strptime(f"{i[0]}", "%d.%m.%Y %H:%M:%S")).total_seconds())

                local_info['get_last_patient_ln'][ln_data] = None
                if ((datetime.now() - datetime.strptime(f"{last_visit[0]}", "%d.%m.%Y %H:%M:%S")).total_seconds() / (
                        60 * 60 * 24) < 14 and last_visit[1].split('__')[-1] != 'closed'):

                    local_info['get_last_patient_ln'][ln_data] = last_visit[1]


        for marker in local_info:
            data['examination'][marker] = local_info.get(marker)

        if child_marker:
            if data['examination']['get_last_anthro_data'].get('txt_weight_bir_variable'):
                data['examination']['anthro']['txt_weight_bir_variable'].set(
                    data['examination']['get_last_anthro_data'].get('txt_weight_bir_variable'))

            if data['examination']['get_last_anthro_data'].get('txt_weight_variable'):

                data['examination']['last_txt_weight_variable'] = data['examination']['get_last_anthro_data'].get('txt_weight_variable')


        else:
            if data['examination']['get_last_anthro_data'].get('txt_weight_variable'):
                data['examination']['anthro']['txt_weight_variable'].set(
                    data['examination']['get_last_anthro_data'].get('txt_weight_variable'))
            # if data['examination'].get('anamnesis') and data['examination'].get('anamnesis') != 'None':
            #     txt_anamnesis.insert(1.0, data['examination'].get('anamnesis').strip())

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
                    if command in ('Удалить осмотр', 'Удалить справку'):
                        result = messagebox.askyesno(title='Удаление осмотра',
                                                     message="Удалить осмотр?")
                        if result:
                            answer, message = data_base(command='examination__delete',
                                                        insert_data=rowid_)
                            if not answer:
                                messagebox.showerror('Ошибка', f"Ошибка удаления записи: \n{message}")
                            else:
                                past_examination_data['destroy_elements'].get(rowid_).destroy()
                        past_examination_frame.focus()

                    elif command == 'Загрузить в текущий':
                        for but_marker in ('complaints', 'examination', 'prescription'):
                            for mark_ in data['examination'].get(f'{but_marker}_but'):
                                data['examination'][f'{but_marker}_but'].get(mark_).set(0)
                        if data['examination'].get('selected_drugs'):
                            data['examination']['selected_drugs'].clear()
                        txt_epicrisis_add.delete(1.0, 'end')
                        all_markers = past_examination_data['found_info'].get(rowid_). \
                            get('examination_key').split('__<end!>__\n')
                        for selected_marker in all_markers:
                            if 'selected_diagnosis_get:____' in selected_marker:
                                selected_diagnosis.set(selected_marker.split(':____')[-1])

                            elif "drugs:____" in selected_marker:
                                all_buttons = selected_marker.replace('drugs:____', '').split("____")

                                for drugs_but in all_buttons:
                                    if len(drugs_but.split('__')) == 4:
                                        select_drugs_item(drug_name=drugs_but)

                            elif "epicrisis_add_text:____" in selected_marker:
                                txt_epicrisis_add.insert(1.0, selected_marker.replace("epicrisis_add_text:____", ""))
                                txt_epicrisis_add["height"] = len(selected_marker.split('\n')) + 1


                            elif "patient_anthro_data:____" in selected_marker:
                                for marker in selected_marker.replace('patient_anthro_data:____', '').split("____"):
                                    if len(marker.split('__')) == 2:
                                        name, variable = marker.split('__')
                                        if name in data['examination'].get('anthro'):
                                            data['examination']['anthro'][name].set(variable)

                            elif "selected_place:____" in selected_marker:
                                selected_place.set(selected_marker.replace('selected_place:____', ''))

                            elif "anamnesis:____" in selected_marker:
                                txt_anamnesis.delete(1.0, 'end')
                                txt_anamnesis.insert(1.0, selected_marker.replace('anamnesis:____', ''))

                            else:
                                for but_marker in ('complaints', 'examination', 'prescription',
                                                   'diagnosis'):

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

                        past_examination_root.destroy()
                        examination_root.update()
                        edit_examination_kb_text()
                        edit_complaints_kb_color()

                    elif command == 'Сохранить изменения':
                        saved_text = past_examination_data['found_info'][f"{rowid_}"]. \
                            get('txt_examination_past').get(1.0, 'end').strip()
                        if saved_text == past_examination_data['found_info'][f"{rowid_}"].get("examination_text"):
                            messagebox.showinfo('Инфо', f"Осмотры совпадают\n"
                                                        f"Нет изменений для сохранения")
                        else:
                            answer, message = data_base(command='examination__delete',
                                                        insert_data=rowid_)
                            if not answer:
                                messagebox.showerror('Ошибка', f"Ошибка удаления записи: \n{message}")
                            else:

                                save_info_examination = [
                                    f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
                                    f"{user.get('doctor_name')}",
                                    None,
                                    past_examination_data['found_info'][f"{rowid_}"].get("ln_type"),
                                    past_examination_data['found_info'][f"{rowid_}"].get("patient_info_"),
                                    saved_text,
                                    past_examination_data['found_info'][f"{rowid_}"].get("examination_key"),
                                    None]

                                answer, message = data_base(command='examination__save',
                                                            insert_data=save_info_examination)
                                if not answer:
                                    messagebox.showerror("Ошибка", f"Ошибка сохранения осмотра\n{message}")
                                else:
                                    messagebox.showinfo('Инфо', f"Осмотр успешно сохранен")
                                    text = past_examination_data['found_info'][f"{rowid_}"].get("past_exam_text")
                                    text.set(f"Время редактирования: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}    "
                                             f"Пользователь: {user.get('doctor_name')}")
                                    past_examination_frame.update()

                        past_examination_frame.focus()

                    elif command in ('Печать А5', 'Печать А6'):
                        if command == 'Печать А5':
                            text_size = 11
                        else:
                            text_size = 8
                        exam_text = past_examination_data['found_info'][f"{rowid_}"]. \
                                        get('txt_examination_past').get(1.0, 'end')[:-1]

                        document = Document()
                        paragraph = document.add_paragraph()
                        for text in exam_text.split('\n'):
                            text = text.strip()

                            for marker in ('Жалобы:', 'Данные объективного обследования:', 'Диагноз:'):
                                if text.startswith(marker):
                                    text = text.replace(marker, '')
                                    p = paragraph.add_run(marker)
                                    r_fmt = p.font
                                    r_fmt.name = 'Times New Roman'
                                    r_fmt.size = Pt(text_size)
                                    r_fmt.bold = True
                            if text:
                                p = paragraph.add_run(f"{text}\n")
                                r_fmt = p.font
                                r_fmt.name = 'Times New Roman'
                                r_fmt.size = Pt(text_size)

                        sections = document.sections
                        for section in sections:
                            section.top_margin = Cm(1.5)
                            section.bottom_margin = Cm(1.5)
                            section.left_margin = Cm(1.5)
                            section.right_margin = Cm(1.5)
                            if command == 'Печать А5':
                                section.page_height = Cm(14.8)
                                section.page_width = Cm(21)
                            else:
                                section.page_height = Cm(10.5)
                                section.page_width = Cm(14.8)

                        doc_name = f'.{os.sep}generated{os.sep}осмотр.docx'
                        doc_name = save_document(doc=document, doc_name=doc_name)
                        run_document(doc_name)

            past_examination_data = dict()
            past_examination_data['buttons'] = dict()
            past_examination_data['found_info'] = dict()
            past_examination_data['destroy_elements'] = dict()
            past_examination_data['frame_info'] = dict()

            past_examination_connect_status = StringVar()
            Label(master=past_examination_frame, textvariable=past_examination_connect_status,
                  font=('Comic Sans MS', user.get('text_size')), bg="#36566d", fg='white').pack(fill='both',
                                                                                                expand=True)

            past_examination_connect_status.set("Подключение к базе данных")
            past_examination_frame.update()
            found_info = data['examination'].get('select_past_examination')
            if found_info:
                past_examination_connect_status.set("Подключение к базе данных: успешно")
            past_examination_frame.update()

            if not found_info:
                past_examination_connect_status.set(f"{past_examination_connect_status.get()}\n"
                                                    f"История о прошлых осмотрах пациента пуста")
            else:
                for info in found_info:
                    local_frame = Frame(past_examination_frame, borderwidth=1, relief="solid", padx=3, pady=3)
                    rowid, date_time, doctor_name, status, ln_type, patient_info_, examination_text, examination_key = info

                    past_examination_data['destroy_elements'][f"{rowid}"] = local_frame

                    past_examination_data['found_info'][f"{rowid}"] = {
                        "date_time": date_time,
                        "doctor_name": doctor_name,
                        "ln_type": ln_type,
                        "patient_info_": patient_info_,
                        "examination_text": examination_text,
                        "examination_key": examination_key
                    }
                    past_exam_text = StringVar()
                    past_examination_data['found_info'][f"{rowid}"]['past_exam_text'] = past_exam_text
                    past_exam_text.set(f"Время редактирования: {date_time}    Пользователь: {doctor_name}    Статус: {status}")
                    Label(master=local_frame, width=100,
                          textvariable=past_exam_text,
                          justify='left',
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').pack(fill='both', expand=True, side="top")
                    height = 1
                    for string in examination_text.split('\n'):
                        height += (1 + len(string) // 100)

                    txt_examination_past = ScrolledText(local_frame, width=100, height=height,
                                                        font=('Comic Sans MS', user.get('text_size')),
                                                        wrap="word")

                    txt_examination_past.insert(1.0, f"{examination_text}\n")
                    txt_examination_past.pack(fill='both', expand=True, side="top")
                    past_examination_data['found_info'][f"{rowid}"]['txt_examination_past'] = txt_examination_past
                    # counter = 0
                    # for text in examination_text.split(" "):
                    #     counter += len(text)
                    #     if '\n' in text:
                    #         counter = 0
                    #     if counter >= 90:
                    #         past_exam_text += '\n'
                    #         counter = 0
                    #
                    #     past_exam_text += text + ' '
                    # past_exam_text += f"\nЛН: {ln_type}\nВрач: {doctor_name}".replace('_', ' ')
                    # Label(master=local_frame, width=100,
                    #       text=past_exam_text,
                    #       justify='left',
                    #       font=('Comic Sans MS', user.get('text_size')),
                    #       bg='white').pack(fill='both', expand=True, side="top")

                    if examination_key.startswith('type_examination:____certificate__'):
                        if doctor_name == user.get('doctor_name'):
                            mark = 'Удалить справку'
                            past_examination_data['buttons'][f"{rowid}__{mark}"] = IntVar()
                            Checkbutton(local_frame, text=mark,
                                        font=('Comic Sans MS', user.get('text_size')),
                                        onvalue=1, offvalue=0,
                                        variable=past_examination_data['buttons'].get(f"{rowid}__{mark}"),
                                        command=selected_past_but,
                                        indicatoron=False,
                                        selectcolor='#77f1ff').pack(fill='both', expand=True)
                    else:
                        for mark in ('Удалить осмотр',
                                     'Загрузить в текущий',
                                     "Печать А5",
                                     "Печать А6",
                                     "Сохранить изменения"):
                            past_examination_data['buttons'][f"{rowid}__{mark}"] = IntVar()

                            if mark not in ("Сохранить изменения", 'Удалить осмотр') \
                                    or doctor_name == user.get('doctor_name'):
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

    def create_examination_doc(doc_size=None):

        type_ln = selected_type_ln.get()
        if type_ln in ('Лист ВН', 'Справка ВН') and not txt_ln_num.get():
            messagebox.showerror('Ошибка!', 'Не указан номер документа ВН!')
            txt_ln_num.focus()
        else:
            render_data.clear()

            date_time_str = txt_date_time.get().strip()
            if date_time_str:
                render_data['date_time'] = f"Дата осмотра: {date_time_str}\n"
            else:
                render_data['date_time'] = ""

            render_data['patient_info'] = f"ФИО: {patient.get('name')}\t" \
                                          f"Дата рождения: {patient.get('birth_date')}\t" \
                                          f"Возраст: {patient['age'].get('age_txt')}\n" \
                                          f"Место осмотра: {selected_place.get()}"
            age_loc = patient_age_local.get().replace("Текущий возраст: ", "")
            if age_loc != "Ошибка даты осмотра":
                render_data['patient_info'] = render_data.get("patient_info").replace(patient['age'].get('age_txt'),
                                                                                      age_loc)
            if selected_place.get() == 'в поликлинике':
                render_data['patient_info'] = f"{render_data.get('patient_info')}\tна приеме: {combo_company.get()}"
            render_data['patient_info'] = f"{render_data.get('patient_info')}    {patient.get('patient_district')}-й уч"

            render_data['complaints'] = f"{txt_complaints.get(1.0, 'end').strip()}"
            examination_text = txt_examination.get(1.0, 'end').replace('\n', ' ').replace('  ', ' ').strip()
            render_data['examination'] = f" {examination_text}"
            render_data['diagnosis'] = f"{txt_diagnosis.get(1.0, 'end').strip()}"
            render_data['prescription'] = f"{txt_prescription.get(1.0, 'end').strip()}"

            add_info = ''
            if type_ln == 'Уход обеспечен':
                add_info += "Уход обеспечен\n"
            elif type_ln in ('Лист ВН', 'Справка ВН'):
                if data['examination'].get('ln_closed'):
                    if type_ln == 'Лист ВН':
                        add_info += f"{type_ln} № {txt_ln_num.get()} закрыт к труду c {txt_ln_until.get()}\n"
                    else:
                        add_info += f"{type_ln} № {txt_ln_num.get()} закрыта к труду c {txt_ln_until.get()}\n"
                else:
                    add_info += f"{type_ln} № {txt_ln_num.get()} c {txt_ln_from.get()} по {txt_ln_until.get()}\n"
            if txt_second_examination.get():
                add_info += f"Повторный осмотр: {txt_second_examination.get()}\n"
                render_data['second_exam'] = f"Повторный осмотр: {txt_second_examination.get()}"
            else:
                render_data['second_exam'] = ''
            # add_info += f"Врач-педиатр: {user.get('doctor_name')}"

            render_data['doctor_name'] = user.get('doctor_name')
            render_data['add_info'] = add_info.strip()

            active_but = ""
            if child_marker:
                active_but += "type_examination:____child__<end!>__\n"
            else:
                active_but += "type_examination:____adult__<end!>__\n"
            if selected_diagnosis.get():
                active_but += f"selected_diagnosis_get:____{selected_diagnosis.get()}__<end!>__\n"

            active_but += f"selected_place:____{selected_place.get()}__<end!>__\n"

            for mark in ('complaints', 'examination', 'prescription'):
                active_but += f'{mark}:__'
                for but in data['examination'].get(f'{mark}_but'):
                    if data['examination'][f'{mark}_but'].get(but).get() == 1:
                        active_but += f'__{but}'
                active_but += '__<end!>__\n'

            local_drugs_text = ''
            for drug_category in data['examination'].get('selected_drugs', []):
                for drug_name in data['examination']['selected_drugs'].get(drug_category, []):
                    for mark_flag in data['examination']['selected_drugs'][drug_category].get(drug_name, []):
                        mark = data['examination']['selected_drugs'][drug_category][drug_name].get(mark_flag)
                        if mark:
                            if isinstance(mark, list):
                                for mark_2 in mark:
                                    local_drugs_text += f"____{drug_category}__{drug_name}__{mark_flag}__{mark_2}"
                            else:
                                local_drugs_text += f"____{drug_category}__{drug_name}__{mark_flag}__{mark}"
            if local_drugs_text:
                active_but += f"drugs:{local_drugs_text}__<end!>__\n"
            if data['examination']['anthro']['patient_anthro_data'].get():
                patient_anthro_data_loc = ''
                patient_anthro_data_but_loc = 'patient_anthro_data:____'

                npr_flag = False
                for mark in local_data_anthro:


                    for name, variable in local_data_anthro.get(mark):
                        select_name = data['examination']['anthro'][variable].get()
                        if select_name:
                            if mark == 'anal' and not npr_flag:
                                patient_anthro_data_loc += '\nНПР: \n'
                                npr_flag = True

                            patient_anthro_data_loc += f"{name}".replace('_', select_name)
                            patient_anthro_data_but_loc += f"{variable}__{select_name}____".replace(',', '.')
                            if child_marker and doc_size == 'а5_child_disp':
                                patient_anthro_data_loc += '\n'
                            else:
                                patient_anthro_data_loc += '  '
                render_data['patient_anthro_data'] = f"{patient_anthro_data_loc}".strip()
                active_but = f"{active_but}" \
                             f"{patient_anthro_data_but_loc}__<end!>__\n"

                active_but += f"drugs:{local_drugs_text}__<end!>__\n"
            render_data['epicrisis_add_text'] = txt_epicrisis_add.get(1.0, 'end').strip()
            if (type_ln in ('Лист ВН', 'Справка ВН')
                    and data['examination']['LN_data'].get('current_data')
                    and data['examination']['LN_data']['current_data'].get('save')):
                local_ln_data = ''
                for marker in ('Фамилия', 'Имя', 'Отчество',
                               'Дата рождения', 'Место работы (службы, учебы)',
                               'Информация про ребенка (в корешок)'):
                    local_ln_data += f"____{marker}__{data['examination']['LN_data']['current_data'].get(marker).get().strip()}"
                active_but += f"LN_blank_data:{local_ln_data}__<end!>__\n"

            active_but = f"{active_but}" \
                         f"complaints_text:____{render_data.get('complaints')}__<end!>__\n" \
                         f"examination_text:____{render_data.get('examination')}__<end!>__\n" \
                         f"diagnosis_text:____{render_data.get('diagnosis')}__<end!>__\n" \
                         f"prescription_text:____{render_data.get('prescription')}__<end!>__\n" \
                         f"epicrisis_add_text:____{render_data.get('epicrisis_add_text')}__<end!>__\n"

            anamnesis = txt_anamnesis.get(1.0, 'end').strip()
            if not child_marker:
                active_but = f"{active_but}" \
                             f"anamnesis:____{anamnesis}__<end!>__\n"
                if anamnesis:
                    anamnesis = f"\nАнамнез заболевания: {anamnesis}"
            render_data['anamnesis'] = anamnesis


            patient_anthro_data = render_data.get('patient_anthro_data', '').replace('\n', '  ')
            active_examination = f"{render_data.get('date_time')}{render_data.get('patient_info')}\n" \
                                 f"{render_data.get('epicrisis_add_text')}\n" \
                                 f"Жалобы: {render_data.get('complaints')}{anamnesis}\n" \
                                 f"Данные объективного обследования: " \
                                 f"{patient_anthro_data}\n" \
                                 f"{render_data.get('examination')}\n" \
                                 f"{render_data.get('diagnosis')}\n" \
                                 f"{render_data.get('prescription')}\n" \
                                 f"{render_data.get('add_info')}\n" \
                                 f"Врач-педиатр: {user.get('doctor_name')}"

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
                f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
                f"{user.get('doctor_name')}",
                'loc',
                ln_data,
                f"{patient.get('name').strip()}__{patient.get('birth_date').strip()}",
                active_examination,
                active_but,
                None]
            if doc_size:
                render_data['diagnosis'] = render_data.get('diagnosis', '').replace('Диагноз:', '')

                doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}осмотр_педиатра_{doc_size}.docx")
                doc.render(render_data)
                doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]}_осмотр__" \
                           f"{datetime.now().strftime('%d_%m_%Y_%H_%M')}.docx"
                doc_name = save_document(doc=doc, doc_name=doc_name)
                run_document(doc_name)

            answer, message = data_base(command='examination__save',
                                        insert_data=save_info_examination)
            if not answer:
                messagebox.showerror("Ошибка", f"Ошибка сохранения осмотра\n{message}")

            render_data.clear()
            data.clear()
            root_examination.destroy()
            data_base(command="statistic_write",
                      insert_data="Осмотр")

    def paste_hr_br():
        indicators = {
            '0-1': {
                'br': (26, 28),
                'hr': (104, 112),
                'bp': (90, 100, 60, 70)},

            '0-3': {
                'br': (24, 28),
                'hr': (96, 110),
                'bp': (90, 100, 60, 70)},
            '3-6': {
                'br': (22, 28),
                'hr': (80, 100),
                'bp': (96, 110, 60, 70)},
            '6-12': {
                'br': (20, 22),
                'hr': (70, 90),
                'bp': (100, 110, 60, 75)},
            '>12': {
                'br': (18, 22),
                'hr': (70, 80),
                'bp': (110, 120, 70, 78)},
        }
        if age <= 1:
            indicator = indicators['0-1']
        elif age <= 3:
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
        def select_diagnosis():
            data['examination']['diagnosis'] = selected_diagnosis.get()

            for mark_ in data['examination'].get('complaints_but'):
                data['examination']['complaints_but'].get(mark_).set(0)
            for mark_ in data['examination'].get('examination_but'):
                data['examination']['examination_but'].get(mark_).set(0)
            for mark_ in data['examination'].get('prescription_but'):
                data['examination']['prescription_but'].get(mark_).set(0)

            if data['examination'].get('selected_drugs'):
                data['examination']['selected_drugs'].clear()

            if child_marker:
                if selected_diagnosis.get() in ('Врачебно-сестринский патронаж', 'Патронаж'):
                    for mark_ in data['examination'].get('anthro', []):
                        if mark_.startswith('txt_anal_'):
                            data['examination']['anthro'].get(mark_).set('')
                else:
                    patient_age_month = patient_age.get('month')
                    if patient_age.get('year') > 0:
                        patient_age_month = 12

                    for mark_ in data['examination'].get('anthro', []):
                        if mark_.startswith('txt_anal_'):
                            data['examination']['anthro'].get(mark_).set(f"{patient_age_month} мес.")


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

            for prescription_but in all_diagnosis.get(selected_diagnosis.get()).get("prescription"):
                prescription_list = all_diagnosis.get(selected_diagnosis.get()).get("prescription").get(
                    prescription_but)
                if isinstance(prescription_list, list):
                    for prescription in prescription_list:
                        if f"{prescription_but}_{prescription}" in data['examination'].get('prescription_but'):
                            data['examination']['prescription_but'][f"{prescription_but}_{prescription}"].set(1)
                else:
                    if prescription_but in data['examination'].get('prescription_but'):
                        data['examination']['prescription_but'][prescription_but].set(1)

            for drugs_but in all_diagnosis.get(selected_diagnosis.get()).get("drugs", []):

                if len(drugs_but.split('__')) == 4:
                    select_drugs_item(drug_name=drugs_but)


            txt_complaints.delete(1.0, 'end')
            txt_complaints.insert(1.0, all_diagnosis.get(selected_diagnosis.get()).get("complaints_text", ''))

            txt_examination.delete(1.0, 'end')
            txt_examination.insert(1.0, all_diagnosis.get(selected_diagnosis.get()).get("examination_text", ''))

            txt_prescription.delete(1.0, 'end')
            txt_prescription.insert(1.0, all_diagnosis.get(selected_diagnosis.get()).get("prescription_text", ''))

            txt_epicrisis_add.delete(1.0, 'end')

            if "Проведена беседа: Безопасность ____" in all_diagnosis.get(selected_diagnosis.get()).get("epicrisis_add_text", ''):
                conversation = ("Ответственность родителей за детей",
                                "Безопасность сна",
                                "Безопасность в кроватке",
                                "Безопасность при купании",
                                "Безопасность детской одежды",
                                "Отравления детей",
                                "Домашние животные и безопасность ребёнка")

                txt_epicrisis_add.insert(1.0, all_diagnosis.get(selected_diagnosis.get()).get("epicrisis_add_text", '').replace('Проведена беседа: Безопасность ____', f"Проведена беседа: {random.choice(conversation)}"))
            else:
                txt_epicrisis_add.insert(1.0, all_diagnosis.get(selected_diagnosis.get()).get("epicrisis_add_text", ''))
            txt_epicrisis_add["height"] = len(all_diagnosis.get(selected_diagnosis.get()).get("epicrisis_add_text", '\n').split('\n')) + 1


            if all_diagnosis.get(selected_diagnosis.get()).get("selected_place"):
                selected_place.set(all_diagnosis.get(selected_diagnosis.get()).get("selected_place"))

            txt_diagnosis.delete(1.0, 'end')
            if child_marker and data['examination'].get('get_last_diagnosis_text'):
                txt_diagnosis.insert(1.0, data['examination'].get('get_last_diagnosis_text'))

            elif all_diagnosis.get(selected_diagnosis.get()).get("diagnosis_text"):
                txt_diagnosis.insert(1.0, all_diagnosis.get(selected_diagnosis.get()).get("diagnosis_text"))
            else:
                txt_diagnosis.insert(1.0, f'Диагноз: {selected_diagnosis.get()} ')

            edit_examination_kb_text()
            if not data['examination'].get('all_kb_status'):
                change_all_kb_status()
            else:
                root_examination.update()

        loc_data = all_data_diagnosis.get('diagnosis')
        if child_marker:
            loc_data = all_data_diagnosis.get('diagnosis_child')


        label_diagnosis = Label(master=frame_diagnosis, text=f"{loc_data[0]}",
                                font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_diagnosis.pack(fill='both', expand=True)
        frame_diagnosis_1 = Frame(frame_diagnosis, borderwidth=1)
        row, col = 0, 0

        for mark in loc_data[1:]:
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
        def is_valid__(date):
            try:
                date_exam = datetime.strptime(date.split()[0], "%d.%m.%Y")
                age_loc = get_age_d_m_y(birth_date=patient.get('birth_date'), today=date_exam)
                patient_age_local.set(f"Текущий возраст: {age_loc.get('age_txt')}")
            except Exception:
                patient_age_local.set("Ошибка даты осмотра")
            return True

        check = (root_examination.register(is_valid__), "%P")

        Label(master=frame_date_time, text="Дата и время осмотра:",
              font=('Comic Sans MS', user.get('text_size')), bg='white'
              ).pack(fill='both', expand=True)
        txt = Entry(frame_date_time, width=15, textvariable=txt_date_time,
              font=('Comic Sans MS', user.get('text_size')),
              justify="center",
              validate="key",
              validatecommand=check
              )
        txt.pack(fill='both', expand=True)
        txt_date_time.set(datetime.now().strftime("%d.%m.%Y %H:%M"))

        Label(master=frame_date_time, textvariable=patient_age_local,
              font=('Comic Sans MS', user.get('text_size')), bg='white'
              ).pack(fill='both', expand=True)

        frame_date_time.columnconfigure(index='all', minsize=40, weight=1)
        frame_date_time.rowconfigure(index='all', minsize=20)
        frame_date_time.pack(fill='both', expand=True, side=tk.LEFT)

    def my_saved_diagnosis():

        def delete_my_diagnosis():

            found_diagnosis = user.get('my_saved_diagnosis')
            if not found_diagnosis:
                messagebox.showerror('Ошибка!', f'История о сохраненных осмотрах пуста!\n')
                examination_root.focus()

            else:
                def delete_my_diagnosis_root(delete_my_diagnosis_root_main: Frame):
                    def select_delete_diagnosis():
                        answer, mess = data_base(command='examination__delete_my_diagnosis',
                                                 delete_data=selected_delete_diagnosis.get())
                        if answer:
                            messagebox.showinfo('Инфо', f'Осмотр успешно удален')
                            delete_my_diagnosis_root_main.focus()

                            destroy_elements['delete_my_diagnosis'][f"{selected_delete_diagnosis.get()}"].destroy()



                    selected_delete_diagnosis = StringVar()
                    destroy_elements['delete_my_diagnosis'] = dict()

                    for diagnosis_, examination_key_ in found_diagnosis:
                        frame_loc = Frame(delete_my_diagnosis_root_main, borderwidth=1, relief="solid", padx=3, pady=3)
                        destroy_elements['delete_my_diagnosis'][f"{diagnosis_}"] = frame_loc
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
                                    value=f"{diagnosis_}", variable=selected_delete_diagnosis,
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
            if data['examination'].get('selected_drugs'):
                data['examination']['selected_drugs'].clear()
            txt_epicrisis_add.delete(1.0, 'end')

            for selected_marker in my_selected_diagnosis.split('__<end!>__\n'):
                if 'selected_diagnosis_get:____' in selected_marker:
                    selected_diagnosis.set(selected_marker.split(':____')[-1])
                elif "selected_place:____" in selected_marker:
                    selected_place.set(selected_marker.replace('selected_place:____', ''))

                elif "drugs:____" in selected_marker:
                    all_buttons = selected_marker.replace('drugs:____', '').split("____")

                    for drugs_but in all_buttons:
                        if len(drugs_but.split('__')) == 4:
                            select_drugs_item(drug_name=drugs_but)

                #
                # elif "drugs:____" in selected_marker:
                #     if not data['examination'].get('selected_drugs'):
                #         data['examination']['selected_drugs'] = dict()
                #
                #     all_buttons = selected_marker.replace('drugs:____', '').split("____")
                #     for button in all_buttons:
                # if len(drugs_but.split('__')) == 4:
                #         if button.split('__') == 4:
                #             drug_category, drug_name, mark_flag, mark = button.split('__')
                #             if not data['examination']['selected_drugs'].get(drug_category):
                #                 data['examination']['selected_drugs'][drug_category] = dict()
                #             if not data['examination']['selected_drugs'][drug_category].get(
                #                     drug_name):
                #                 data['examination']['selected_drugs'][drug_category][
                #                     drug_name] = dict()
                #
                #             if mark_flag == "Способ применения":
                #                 if not data['examination']['selected_drugs'][drug_category][
                #                     drug_name].get(mark_flag):
                #                     data['examination']['selected_drugs'][drug_category][
                #                         drug_name][mark_flag] = list()
                #                 data['examination']['selected_drugs'][drug_category][
                #                     drug_name][mark_flag].append(mark)
                #
                #             else:
                #                 data['examination']['selected_drugs'][drug_category][drug_name][
                #                     mark_flag] = mark
                elif "epicrisis_add_text:____" in selected_marker:
                    txt_epicrisis_add.insert(1.0, selected_marker.replace("epicrisis_add_text:____", ""))
                    txt_epicrisis_add["height"] = len(selected_marker.split('\n')) + 1


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
                edit_complaints_kb_color()

        def saved_new_diagnosis():
            def final_save_new_diagnosis():
                if data_base(command='save_new_diagnosis',
                             insert_data=[user.get('doctor_name'), new_diagnosis_name.get(), render_text]):
                    messagebox.showinfo('Инфо', f'Осмотр успешно сохранен')
                    saved_new_diagnosis_root.destroy()
                    root_examination.destroy()
                else:
                    messagebox.showerror('Ошибка!', f'Ошибка при сохранении!')

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
                text += f"Дополнительная информация: {txt_epicrisis_add.get(1.0, 'end').strip()}\n"
                for mark in ('complaints', 'examination', 'prescription'):
                    render_text += f'{mark}:__'
                    # text += f"{mark}: ".replace('complaints', 'Жалобы (кнопки)') \
                    #     .replace('examination', 'Осмотр (кнопки)') \
                    #     .replace('prescription', 'Назначения (кнопки)')
                    for but in data['examination'].get(f'{mark}_but'):

                        if data['examination'][f'{mark}_but'].get(but).get() == 1:
                            render_text += f'__{but}'

                    render_text += '__<end!>__\n'
                local_drugs_text = ''
                for drug_category in data['examination'].get('selected_drugs', []):
                    for drug_name in data['examination']['selected_drugs'].get(drug_category, []):
                        for mark_flag in data['examination']['selected_drugs'][drug_category].get(drug_name, []):
                            mark = data['examination']['selected_drugs'][drug_category][drug_name].get(mark_flag)
                            if mark:
                                if isinstance(mark, list):
                                    for mark_2 in mark:
                                        local_drugs_text += f"____{drug_category}__{drug_name}__{mark_flag}__{mark_2}"
                                else:
                                    local_drugs_text += f"____{drug_category}__{drug_name}__{mark_flag}__{mark}"
                if local_drugs_text:
                    render_text += f"drugs:{local_drugs_text}__<end!>__\n"
                examination_text = txt_examination.get(1.0, 'end').replace('\n', ' ').replace('  ', ' ').strip()
                render_text += f"complaints_text:____{txt_complaints.get(1.0, 'end').strip()}__<end!>__\n" \
                               f"examination_text:____{examination_text}__<end!>__\n" \
                               f"diagnosis_text:____{txt_diagnosis.get(1.0, 'end').strip()}__<end!>__\n" \
                               f"prescription_text:____{txt_prescription.get(1.0, 'end').strip()}__<end!>__\n" \
                               f"epicrisis_add_text:____{txt_epicrisis_add.get(1.0, 'end').strip()}__<end!>__\n"


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

        col, row = 0, 0
        if not user.get('my_saved_diagnosis'):
            lbl_my_saved_diagnosis['text'] = "История о сохраненных осмотрах пуста"
            lbl_my_saved_diagnosis.grid(column=col, row=row, sticky='ew', columnspan=2)
            col += 2
        else:
            data['examination']['my_saved_diagnosis'] = dict()
            lbl_my_saved_diagnosis['text'] = "Мои осмотры:"
            lbl_my_saved_diagnosis.grid(column=col, row=row, sticky='ew')
            col += 1
            for diagnosis, examination_key in user.get('my_saved_diagnosis'):
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
        def paste_button_title():
            Button(frame_button, text='Загрузить\nпрошлые\nосмотры',
                   command=paste_past_examination,
                   font=('Comic Sans MS', user.get('text_size'))).pack(fill='both', expand=True, side=tk.LEFT)

            # button_change_all_kb_status.grid(column=0, row=0, rowspan=3, sticky='nswe')
            button_change_all_kb_status.pack(fill='both', expand=True, side=tk.LEFT)

            frame_button.pack(fill='both', expand=True, side=tk.LEFT)
        paste_frame_diagnosis()
        paste_frame_date_time()
        paste_button_title()
        my_saved_diagnosis()

        if user.get('my_saved_diagnosis'):
            my_saved_diagnosis_change_status()

        frame_1.columnconfigure(index='all', minsize=40, weight=1)
        frame_1.rowconfigure(index='all', minsize=20)
        frame_1.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

    frame_1 = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_diagnosis = Frame(frame_1, borderwidth=1, relief="solid")
    frame_date_time = Frame(frame_1, borderwidth=1, relief="solid")

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
            label_place['text'] = f"место осмотра: {selected_place.get()}"
            if selected_place.get() == 'в поликлинике':
                frame_company.pack(fill='both', expand=True, side="left")
            else:
                frame_company.pack_forget()

        label_place = Label(master=frame_place, text=f"место осмотра: ",
                            font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_place.pack(fill='both', expand=True, side="left")

        for mark in all_data_diagnosis.get('place'):
            btn = Radiobutton(master=frame_place, text=mark,
                              font=('Comic Sans MS', user.get('text_size')),
                              value=mark, variable=selected_place, command=select_place,
                              indicatoron=False, selectcolor='#77f1ff')
            btn.pack(fill='both', expand=True, side="left")
        selected_place.set('в поликлинике')

        Label(master=frame_company, text=" На осмотре ",
              font=('Comic Sans MS', user.get('text_size')),
              bg='white').pack(fill='both', expand=True, side="left")

        combo_company['values'] = ['c мамой', 'c папой', 'c братом', 'c сестрой', 'c бабушкой', 'c дедушкой',
                                   'без сопровождения']

        combo_company.current(0)
        combo_company.pack(fill='both', expand=True, side="left")

        frame_company.columnconfigure(index='all', minsize=40, weight=1)
        frame_company.rowconfigure(index='all', minsize=20)
        frame_company.pack(fill='both', expand=True, side="left")

        frame_place.columnconfigure(index='all', minsize=40, weight=1)
        frame_place.rowconfigure(index='all', minsize=20)
        frame_place.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)


    def is_valid__anthro(num, marker):

        text = ''

        mark, name, variable = marker.split('__')

        if num:

            if variable in ("txt_weight_variable", "txt_weight_bir_variable", "txt_weight_must_variable",
                            "txt_weight_delta_variable", "txt_height_variable",
                            "txt_head_variable", "txt_chest_variable"):
                try:
                    num = float(num.replace(',', '.'))
                except ValueError:
                    return False




        if not child_marker and variable in ("txt_weight_variable", "txt_height_variable"):
            if num:

                txt_imt_variable = None
                if variable == "txt_weight_variable" and data['examination']['anthro']["txt_height_variable"].get():
                    height = float(data['examination']['anthro']["txt_height_variable"].get().replace(',', '.'))
                    txt_imt_variable = round(num / float(height/100)**2, 1)


                elif variable == "txt_height_variable" and data['examination']['anthro']["txt_weight_variable"].get():
                    weight = float(data['examination']['anthro']["txt_weight_variable"].get().replace(',', '.'))
                    txt_imt_variable = round(weight / (num/100) ** 2, 1)

                if txt_imt_variable:
                    data['examination']['anthro']["txt_imt_variable"].set(txt_imt_variable)
            else:
                data['examination']['anthro']["txt_imt_variable"].set('')


        if variable == "txt_weight_variable":
            if not num:
                edit_drugs_weight(weight='None')

            else:
                if child_marker:
                    edit_drugs_weight(weight=num / 1000)
                    if data['examination'].get('last_txt_weight_variable'):
                        try:
                            last_txt_weight = float(data['examination'].get('last_txt_weight_variable'))
                        except ValueError:
                            pass
                        else:
                            data['examination']['anthro']['txt_weight_delta_variable'].set(
                                round(num - last_txt_weight))
                else:
                    edit_drugs_weight(weight=num)

        if variable == "txt_weight_bir_variable":
            if num:
                if patient_age.get('year') in (0, 1):
                    loc_data = {
                        0: 0,
                        1: 600,
                        2: 1400,
                        3: 2200,
                        4: 2950,
                        5: 3650,
                        6: 4300,
                        7: 4900,
                        8: 5450,
                        9: 5950,
                        10: 6400,
                        11: 6800,
                        12: 7150}
                    if patient_age.get('year') == 0:
                        age_month = patient_age.get('month')
                        age_day = patient_age.get('day')

                        weight_must = round(float(num) + loc_data.get(age_month) +
                                            ((loc_data.get(age_month + 1) - loc_data.get(age_month)) / 30 * age_day))
                        data['examination']['anthro']['txt_weight_must_variable'].set(weight_must)
                    else:
                        data['examination']['anthro']['txt_weight_must_variable'].set(round(float(num) + 7150))
            else:
                data['examination']['anthro']['txt_weight_must_variable'].set('')

        for mark in local_data_anthro:
            for name_, variable_ in local_data_anthro.get(mark):
                if variable_ == variable:
                    select_name = str(num)
                else:
                    select_name = data['examination']['anthro'][variable_].get()
                if select_name:
                    if len(text.split('\n')[-1]) > 70:
                        text += '\n'

                    text += f"{name_}    ".replace('_', select_name)


        if variable in ('txt_weight_variable', 'txt_height_variable'):

            if not data['examination']['anthro'].get('anthro_height_weight'):
                marker_age_y = 'после года'
                marker_age = patient_age.get('year')
                if marker_age > 17:
                    marker_age = 17
                if child_marker:
                    marker_age_y = 'до года'
                    marker_age = patient_age.get('month')
                    if patient_age.get('year') > 0:
                        marker_age = 12

                data['examination']['anthro']['anthro_height_weight'] = dict()
                marker_gender = 'женский'
                if patient.get('gender').lower().startswith('м'):
                    marker_gender = 'мужской'

                data['examination']['anthro']['anthro_height_weight']['anthro_height'] = \
                    anthropometry[marker_age_y][marker_gender]['height'].get(marker_age)
                data['examination']['anthro']['anthro_height_weight']['anthro_weight'] = \
                    anthropometry[marker_age_y][marker_gender]['weight'].get(marker_age)

            anthro_height = data['examination']['anthro']['anthro_height_weight'].get('anthro_height')
            anthro_weight = data['examination']['anthro']['anthro_height_weight'].get('anthro_weight')


            height, weight = None, None
            if variable == 'txt_weight_variable':
                if num:
                    weight = num
            elif data['examination']['anthro'].get('txt_weight_variable').get():
                weight = float(data['examination']['anthro'].get('txt_weight_variable').get().replace(',', '.'))
            if variable == 'txt_height_variable':
                if num:
                    height = num
            elif data['examination']['anthro'].get('txt_height_variable').get():
                height = float(data['examination']['anthro'].get('txt_height_variable').get().replace(',', '.'))


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

                        if not  2 < index_height < 5 and not  2 < index_weight < 5:
                            anthro += ' по росту и по весу'
                        elif not  2 < index_height < 5:
                            anthro += ' по росту'
                        elif not  2 < index_weight < 5:
                            anthro += ' по весу'

                    patient_physical_anthro = f"Физическое развитие: {anthro}"
                    text = f"{text.strip()}\nФизическое развитие: {anthro}"

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
            data['examination']['anthro']['patient_physical_anthro'].set(patient_physical_anthro)


        data['examination']['anthro']['patient_anthro_data'].set(text.strip())

        return True

    frame_place = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_company = Frame(frame_place)

    combo_company = Combobox(frame_company, font=('Comic Sans MS', user.get('text_size')),
                             state="readonly", justify="center")

    paste_frame_place_company()

    frame_epicrisis_add = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    txt_epicrisis_add = ScrolledText(frame_epicrisis_add, width=15, height=3,
                                     font=('Comic Sans MS', user.get('text_size')),
                                     wrap="word")
    txt_epicrisis_add.insert(1.0, "Осмотрен на чесотку, педикулез, микроспорию\n"
                                  "Согласие на простое медицинское вмешательство получено")
    Label(master=frame_epicrisis_add,
          text="Дополнительная информация",
          font=('Comic Sans MS', user.get('text_size')), bg='white').pack(fill='both', expand=True, padx=2, pady=2)
    txt_epicrisis_add.pack(fill='both', expand=True)
    frame_epicrisis_add.pack(fill='both', expand=True, padx=2, pady=2)


    def paste_frame_complaints():

        label_complaints = Label(master=frame_complaints_main,
                                 text=f"{all_data_diagnosis.get('complaints')[0]}",
                                 font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_complaints.grid(row=0, column=0, sticky='ew')

        txt_complaints.grid(column=0, row=1, sticky='ew', columnspan=2)
        data['examination']['complaints_but'] = dict()

        for mark in all_data_diagnosis.get('complaints'):
            if isinstance(mark, tuple):
                data['examination']['complaints_but'][f"{mark[0]}_main"] = IntVar()

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
        local_complaints = dict()
        text = txt_complaints.get(1.0, 'end').strip()
        if text and text[-1] == '.':
            text = text[:-1] + ', '
        for mark in all_data_diagnosis.get('complaints'):
            if isinstance(mark, tuple):
                text = text.replace(mark[0], f"\n__!__{mark[0]}")
                local_complaints[mark[0]] = ""
        for string in text.split('\n__!__'):
            for i in local_complaints.keys():
                if i in string:
                    local_complaints[i] = string
                    if data['examination']['complaints_but'].get(f"{i}_main"):
                        data['examination']['complaints_but'].get(f"{i}_main").set(1)

                    break
            else:
                if not local_complaints.get("add"):
                    local_complaints["add"] = ""
                local_complaints["add"] += string

        complaints_button = selected_button.get()
        if text == 'нет':
            text = ''

        selected_button.set('')
        if complaints_button:
            if complaints_button in ('нет', 'обусловлены основным заболеванием'):
                for mark_ in data['examination'].get('complaints_but'):
                    data['examination']['complaints_but'].get(mark_).set(0)
                text = complaints_button

            else:
                if data['examination']['complaints_but'].get(complaints_button):
                    if data['examination']['complaints_but'].get(complaints_button).get() == 1:
                        data['examination']['complaints_but'].get(complaints_button).set(0)

                    else:
                        data['examination']['complaints_but'].get(complaints_button).set(1)

        if complaints_button not in ('нет', 'обусловлены основным заболеванием'):
            if '_' in complaints_button:
                mark_1, mark_2 = complaints_button.split('_')
                if data['examination']['complaints_but'].get(complaints_button).get() == 1:
                    if not data['examination']['complaints_but'].get(f"{mark_1}_main").get() == 1:
                        data['examination']['complaints_but'].get(f"{mark_1}_main").set(1)
                    text += ' '
                    if mark_2 == 'main':
                        text += f" {mark_1}, "
                    elif not local_complaints.get(mark_1):

                        text += f" {mark_1} {mark_2}, "
                    else:
                        if local_complaints.get(mark_1) == f"{mark_1}, ":
                            local_complaints[mark_1] = f"{mark_1} "
                        if mark_1 == 'температура':
                            if local_complaints.get(mark_1).strip()[-1] in (",", "."):
                                local_complaints[mark_1] = local_complaints.get(mark_1).strip()[:-1]
                            if local_complaints.get(mark_1).strip()[-1].isdigit():

                                text = text.replace(local_complaints.get(mark_1),
                                                    local_complaints.get(mark_1) + f" - {mark_2}, ")
                            else:
                                text = text.replace(local_complaints.get(mark_1),
                                                    f"{local_complaints.get(mark_1)} {mark_2}, ")
                        else:

                            text = text.replace(local_complaints.get(mark_1),
                                                local_complaints.get(mark_1, f" {mark_1} ") + f" {mark_2}, ")

                else:
                    if mark_2 == 'main':
                        text = text.replace(local_complaints.get(mark_1, '').split('\n')[0], "")
                        for but in data['examination'].get('complaints_but'):
                            if mark_1 in but:
                                data['examination']['complaints_but'].get(but).set(0)
                    elif mark_1 == 'температура':
                        for i in (f" - {mark_2}", f"{mark_2} - ", f"{mark_2}, ", f", {mark_2}", f"{mark_2}"):
                            if i in text:
                                text = text.replace(i, '')
                                break

                    else:
                        for i in (f"{mark_2}, ", f"{mark_2},", f", {mark_2}", f"{mark_2}"):
                            if i in text:
                                text = text.replace(i, '')
                                break
            else:
                if data['examination']['complaints_but'].get(complaints_button).get() == 1:
                    if local_complaints.get("add"):
                        text = text.replace(local_complaints.get("add"),
                                            local_complaints.get("add") + f"{complaints_button}, ")
                    else:
                        text = f"{complaints_button}, " + text

                else:
                    if local_complaints.get("add"):
                        for i in (f"{complaints_button}, ", f"{complaints_button},", f", {complaints_button}", f"{complaints_button}"):
                            if i in local_complaints.get("add"):
                                text = text.replace(local_complaints.get("add"),
                                                    local_complaints.get("add").replace(i, ''))
                                break
                    else:
                        for i in (f"{complaints_button}, ", f"{complaints_button},", f", {complaints_button}", f"{complaints_button}"):
                            if i in text:
                                text = text.replace(i, '')
                                break

        text = text.replace('\n__!__', ' ').strip().replace(', ,', ',').replace('  ', ' ').replace(' ,', ',')
        txt_complaints.delete(1.0, 'end')
        if text != 'нет' and text[-2:] == ', ':
            text = text[:-2] + '. '
        txt_complaints.insert(1.0, text)

        edit_complaints_kb_color()

        # if data['examination'].get('open_complaints_kb'):
        #     for but in data['examination'].get('complaints_buttons'):
        #         if data['examination']['complaints_but'].get(but).get() == 1:
        #             data['examination']['complaints_buttons'][but]['bg'] = '#77f1ff'
        #         else:
        #             data['examination']['complaints_buttons'][but]['bg'] = '#cdcdcd'

    def change_complaints_kb_status():

        if data['examination'].get('open_complaints_kb') == 'open':
            data['examination']['open_complaints_kb'] = 'closed'
            change_complaints_kb_button['text'] = 'открыть клавиатуру жалоб'
            txt_complaints['height'] = 4
            txt_complaints['width'] = 100
            frame_complaints_buttons.grid_forget()
            frame_complaints_main.grid_configure(row=0, column=0, sticky='ew', columnspan=3)
        else:
            data['examination']['open_complaints_kb'] = 'open'
            change_complaints_kb_button['text'] = 'скрыть клавиатуру жалоб'
            txt_complaints['height'] = 8
            txt_complaints['width'] = 15
            frame_complaints_buttons.grid(row=0, column=1, sticky='ew', columnspan=2)
            frame_complaints_main.grid_configure(row=0, column=0, sticky='ew', columnspan=1)

    def paste_complaints_kb():
        destroy_elements['complaints'] = list()
        data['examination']['complaints_buttons'] = dict()
        data['examination']['open_complaints_kb'] = 'open'

        frame_loc = Frame(frame_complaints_buttons)

        row, col = 0, 0
        for mark in all_data_diagnosis.get('complaints'):
            if mark == '_':
                frame_loc.columnconfigure(index='all', minsize=10, weight=1)
                frame_loc.rowconfigure(index='all', minsize=10)
                frame_loc.pack(fill='both', expand=True)
                frame_loc = Frame(frame_complaints_buttons)
                continue
            if not isinstance(mark, tuple):
                btn = Radiobutton(frame_loc, text=f"{mark}",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=f"{mark}", variable=selected_button,
                                  command=select_complaints,
                                  indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')

                btn.grid(row=1, column=col, sticky='ew')
                data['examination']['complaints_buttons'][mark] = btn

                col += 1
        frame_loc.columnconfigure(index='all', minsize=10, weight=1)
        frame_loc.rowconfigure(index='all', minsize=10)
        frame_loc.pack(fill='both', expand=True)

        for mark in all_data_diagnosis.get('complaints'):
            if isinstance(mark, tuple):
                row, col = 0, 0
                frame_loc = Frame(frame_complaints_buttons)
                destroy_elements['complaints'].append(frame_loc)

                btn = Radiobutton(frame_loc, text=f"{mark[0]}",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=f"{mark[0]}_main", variable=selected_button,
                                  command=select_complaints,
                                  indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
                btn.grid(row=row, column=col, sticky='ew')
                data['examination']['complaints_buttons'][f"{mark[0]}_main"] = btn

                col += 1
                for mark_2 in mark[1:]:
                    btn = Radiobutton(frame_loc, text=f"{mark_2}",
                                      font=('Comic Sans MS', user.get('text_size')),
                                      value=f"{mark[0]}_{mark_2}", variable=selected_button,
                                      command=select_complaints,
                                      indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')

                    # btn = Checkbutton(frame_loc, text=mark_2,
                    #                   font=('Comic Sans MS', user.get('text_size')),
                    #                   onvalue=1, offvalue=0,
                    #                   variable=data['examination']['complaints_but'].get(f"{mark[0]}_{mark_2}"),
                    #                   command=select_complaints,
                    #                   indicatoron=False, selectcolor='#77f1ff')
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

    def edit_complaints_kb_color():
        for but in data['examination'].get('complaints_buttons'):
            if data['examination']['complaints_but'].get(but).get() == 1:
                data['examination']['complaints_buttons'][but]['bg'] = '#77f1ff'
            else:
                data['examination']['complaints_buttons'][but]['bg'] = '#cdcdcd'

        # for button_name in data['examination'].get('examination_buttons_2_color'):
        #     if data['examination']['examination_but'].get(button_name):
        #         if data['examination']['examination_but'].get(button_name).get() == 1:
        #             data['examination']['examination_buttons_2_color'][button_name]['bg'] = '#77f1ff'
        #         else:
        #             data['examination']['examination_buttons_2_color'][button_name]['bg'] = '#cdcdcd'


    frame_complaints = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    frame_complaints_main = Frame(frame_complaints, padx=1, pady=1)
    frame_complaints_buttons = Frame(frame_complaints, padx=1, pady=1)
    txt_complaints = ScrolledText(frame_complaints_main, width=15, height=8,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  wrap="word")
    change_complaints_kb_button = Button(frame_complaints_main, text='скрыть клавиатуру жалоб',
                                         command=change_complaints_kb_status,
                                         font=('Comic Sans MS', user.get('text_size')))

    paste_frame_complaints()

    frame_anamnesis = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    txt_anamnesis = ScrolledText(frame_anamnesis, width=15, height=3,
                                 font=('Comic Sans MS', user.get('text_size')),
                                 wrap="word")

    if not child_marker:
        Label(master=frame_anamnesis,
              text="Анамнез заболевания",
              font=('Comic Sans MS', user.get('text_size')), bg='white').pack(fill='both', expand=True, padx=2, pady=2)
        txt_anamnesis.pack(fill='both', expand=True)
        frame_anamnesis.pack(fill='both', expand=True, padx=2, pady=2)

    def paste_patient_anthro_data():
        def paste_npr_root():
            def selected_age_month(event=None):
                for age_month in data['examination'].get('npr_frame'):
                    frame = data['examination']['npr_frame'].get(age_month)
                    frame.pack_forget()

                frame = data['examination']['npr_frame'].get(int(combo_age_month.get()))
                frame.pack(fill='both', expand=True)

            local_data_npr = {
                1: {
                    "Аз": "Плавное прослеживание движущегося предмета",
                    "Ас": "Длительное слуховое сосредоточение (прислушивается к голосу взрослого, звуку игрушки и .т д.)",
                    "Э": "Первая улыбка в ответ на речь взрослого",
                    "ДР": "Ручки чаще слегка раскрыты",
                    "ДО": "Лежа на животе, пытается поднимать и удерживать голову",
                    "ПР": "Не оценивается",
                    "PA": "Издает отдельные звуки в ответ на разговор с ним",
                    "Н": "Не оценивается"
                },
                2: {
                    "Аз": "Длительное сосредоточение, смотрит на лицо взрослого или неподвижный предмет. \n"
                          "Длительно следит за движущейся игрушкой или взрослым",
                    "Ас": "Ищущие повороты головы при длительном звуке. Поворачивает голову в сторону взрослого",
                    "Э": "Быстро отвечает улыбкой на речь взрослого",
                    "ДР": "Ручки чаще слегка раскрыты",
                    "ДО": "Лежа на животе,поднимает и некоторое время удерживает голову",
                    "ПР": "Не оценивается",
                    "PA": "Произносит отдельные звуки",
                    "Н": "Не оценивается"},
                3: {
                    "Аз": "Зрительное сосредоточение в вертикальном положении на руках взрослого \n"
                          "(на лице говорящего, на игрушке), длительно рассматривает свои ручки",
                    "Ас": "Ищущие повороты головы при длительном звуке. Поворачивает голову в сторону взрослого",
                    "Э": "Отвечает «комплексом оживления» в ответ на эмоциональное общение со взрослым (разговор). \n"
                         "Ищет глазами ребенка, издающего звуки",
                    "ДР": "Случайно наталкивается ручками на игрушки, низко висящие над грудью",
                    "ДО": "Лежит на животе несколько минут, опираясь на предплечья и высоко подняв голову. \n"
                          "Удерживает голову в вертикальном положении",
                    "ПР": "Не оценивается",
                    "PA": "Произносит отдельные звуки",
                    "Н": "Не оценивается"},
                4: {
                    "Аз": "Узнает мать или близкого человека (радуется)",
                    "Ас": "Поворачивает голову в сторону невидимого источника звука инаходит его глазами. \n"
                          "Адекватно реагирует на спокойную и плясовую мелодию",
                    "Э": "Комплекс «оживления» во время бодрствования. Громко смеется в ответ на эмоциональное речевое общение. \n"
                         "Ищет взглядом другого ребенка, рассматривает, радуется, тянется к нему",
                    "ДР": "Рассматривает, ощупывает и захватывает низко висящие над грудью игрушки",
                    "ДО": "При поддержке под мышки крепко упирается о твердую опору ногами, согнутыми в тазобедренном суставе",
                    "ПР": "Не оценивается",
                    "PA": "Гулит",
                    "Н": "Во время кормления придерживает ручками грудь матери или бутылочку"
                },
                5: {
                    "Аз": "Отличает близких людей от чужих по внешнему виду \n"
                          "(по разному реагирует на лицо знакомого и незнакомого)",
                    "Ас": "Узнает голос матери или близкого человека. \n"
                          "Различает строгую и ласковую интонацию обращенной к нему речи, по-разному реагирует",
                    "Э": "Радуется ребенку, берет унего из рук игрушку, гулит",
                    "ДР": "Берет игрушку из рук взрослого иудерживает ее в ручке",
                    "ДО": "Долго лежит на животе, подняв корпус и опираясь на ладони выпрямленных рук. \n"
                          "Переворачивается со спины на живот. Ровно, устойчиво стоит при поддержке под мышки",
                    "ПР": "Не оценивается",
                    "PA": "Подолгу певуче гулит",
                    "Н": "Ест с ложки полугустую и густую пищу"
                },
                6: {
                    "Аз": "Не оценивается",
                    "Ас": "По-разному реагирует на свое и чужое имя",
                    "Э": "Не оценивается",
                    "ДР": "Уверенно берет игрушки, находясь в любом положении, и подолгу занимается ими, \n"
                          "перекладывает из одной ручки вдругую",
                    "ДО": "Переворачивается с живота на спину. \n"
                          "Передвигается, переставляя ручки или немного подползая",
                    "ПР": "Не оценивается",
                    "PA": "Произносит отдельные слоги (начало лепета)",
                    "Н": "Хорошо ест с ложки, снимая пищу губами. \n"
                         "Небольшое количество жидкой пищи пьет из блюдца или из чашки"},
                7: {
                    "Аз": "Не оценивается",
                    "Ас": "Не оценивается",
                    "Э": "Не оценивается",
                    "ДР": "Игрушкой стучит, размахивает, перекладывает, бросает ее и пр.",
                    "ДО": "Хорошо ползает (много, быстро, в различном направлении)",
                    "ПР": "На вопрос «где?» находит взглядом предмет на постоянном определенном месте \n"
                          "(например, часы, куклу и пр.)",
                    "PA": "Подолгу лепечет, произнося одни и те же слоги (2-3)",
                    "Н": "Пьет из чашки, которую держит взрослый"},
                8: {
                    "Аз": "Не оценивается",
                    "Ас": "Не оценивается",
                    "Э": "Смотрит на действия другого ребенка и смеется или лепечет",
                    "ДР": "Игрушками занимается долго и разнообразно действует ими в зависимости от их свойств. \n"
                          "Подражает действиям взрослого с игрушками (толкает мяч, стучит и тд.)",
                    "ДО": "Сам садится, сидит, ложится. Держась за барьер, сам встает, стоит и опускается. \n"
                          "Переступает, держась за барьер",
                    "ПР": "На вопрос «где?» находит несколько предметов (2-3) на постоянных местах. \n"
                          "По вербальной просьбе взрослого выполняет разученные ранее действия (без показа), \n"
                          "например «ладушки», «дай ручку» и пр.",
                    "PA": "Громко, четко, выразительно произносит различные слоги и повторяет их",
                    "Н": "Ест корочку хлеба, которую сам держит в ручке. Пьет из чашки, которую держит взрослый"},
                9: {
                    "Аз": "Не оценивается",
                    "Ас": "Выполняет плясовые движения под музыку",
                    "Э": "Подражает действиям другого ребенка. Догоняет ребенка или ползет ему навстречу",
                    "ДР": "Выполняет различные действия с предметами в зависимости от их свойств "
                          "(катает, открывает, гремит и т. д.)",
                    "ДО": "Не оценивается",
                    "ПР": "На вопрос «где?» находит несколько знакомых предметов независимо от их местоположения. "
                          "Знает свое имя",
                    "PA": "Подражает взрослому, повторяя за ним слоги, которые уже есть в лепете",
                    "Н": "Пьет из чашки, слегка придерживая е руками, спокойно относится к высаживанию на горшок"},
                10: {
                    "Аз": "Не оценивается",
                    "Ас": "Выполняет плясовые движения под музыку",
                    "Э": "Действует рядом с ребенком или одной игрушкой с ним",
                    "ДР": "По просьбе выполняет разученные действия с игрушками, \n"
                          "действия с предметами принимают устойчивый характер",
                    "ДО": "Всходит на невысокую наклонную поверхность или горку, держась за перила, и сходит с нее. \n"
                          "Идет вперед с поддержкой за оберуки",
                    "ПР": "По просьбе «дай» находит и дает знакомые предметы. \n"
                          "При игре с ним выполняет разученные движения (догоню-догоню, игра в прятки и т.д.)",
                    "PA": "Подражая взрослому, повторяет за ним новые слоги, которых нет в его лепете",
                    "Н": "Закрепляет навыки иумения, приобретенные в 9 месяцев \n"
                         "(Пьет из чашки, слегка придерживая е руками, спокойно относится к высаживанию на горшок)"},
                11: {
                    "Аз": "Не оценивается",
                    "Ас": "Выполняет плясовые движения под музыку",
                    "Э": "Радуется приходу детей, относится к ним избирательно",
                    "ДР": "Овладевает новыми движениями и начинает выполнять их по команде взрослого \n"
                          "(снимает и надевает кольца на стержень, ставит кубик на кубик)",
                    "ДО": "Стоит самостоятельно, делает первые самостоятельные шаги",
                    "ПР": "Понимает речь и общается (по просьбе взрослого находит любую куклу, \n"
                          "которую видит среди игрушек, любой мяч, все машины и пр.)",
                    "PA": "Произносит первые слова-обозначения (например: «дай», «мама», «на» и др.)",
                    "Н": "Закрепляет навыки и умения, приобретенные в 9 месяцев \n"
                         "(Пьет из чашки, слегка придерживая ее руками, спокойно относится к высаживанию на горшок)"},
                12: {
                    "Аз": "Различает предметы по форме (отличает кирпичик от кубика по просьбе взрослого). \n"
                          "Узнает на фотографии знакомого взрослого",
                    "Ас": "Выполняет плясовые движения под музыку",
                    "Э": "Ищет игрушку, спрятанную другим ребенком. \n"
                         "Протягивает другому ребенку игрушку, сопровождая свои действия смехом и лепетом",
                    "ДР": "Выполняет самостоятельно разученные действия с игрушками (катает, кормит, возит и пр.). \n"
                          "Переносит действия, разученные с одним предметом, на другой (всех кормит, всех баюкает и пр.)",
                    "ДО": "Ходит самостоятельно, без опоры",
                    "ПР": "Знает имена взрослых, названия нескольких предметов, выполняет отдельные поручения (принеси, найди и пр.). \n"
                          "Понимает слово «нельзя». Некоторые слова в речи взрослых принимают обобщенный характер. \n"
                          "По просьбе взрослого выполняет ранее разученные действия с игрушками",
                    "PA": "Легко подражает новым слогам. Произносит 5-10 облегченных слов",
                    "Н": "Самостоятельно пьет из чашки"}
            }
            npr_name = {
                "Аз": "анализатор зрительный",
                "Ас": "анализатор слуховой",
                "Э": "эмоции",
                "ДР": "движения руки",
                "ДО": "движения общие",
                "ПР": "понимаемая речь",
                "PA": "речь активная",
                "Н": "навыки"
            }

            local_data_npr_anthro = {
                "Аз": ("Аз: _ ", "txt_anal_1_variable"),
                "Ас": ("Ас: _ ", "txt_anal_2_variable"),
                "Э": ("Э: _ ", "txt_anal_3_variable"),
                "ДР": ("ДР: _ ", "txt_anal_4_variable"),
                "ДО": ("ДО: _ ", "txt_anal_5_variable"),
                "ПР": ("ПР: _ ", "txt_anal_6_variable"),
                "PA": ("PA: _ ", "txt_anal_7_variable"),
                "Н": ("Н: _ ", "txt_anal_8_variable")
            }
            patient_age_month = patient_age.get('month')
            if patient_age.get('year') > 0:
                patient_age_month = 12
            elif patient_age.get('month') == 0:
                patient_age_month = 1

            frame_npr = Frame(examination_root, borderwidth=0.5, relief="solid", padx=1, pady=1, bg="#36566d")

            data['examination']['npr_frame'] = dict()
            for age_month in local_data_npr:
                frame = Frame(frame_npr)
                row = 0
                for npr_marker in local_data_npr.get(age_month):
                    name, variable = local_data_npr_anthro.get(npr_marker)

                    check = (root_examination.register(is_valid__anthro), "%P",
                             f"anal__{name}__{variable}")

                    Label(master=frame, text=name.replace(' _', ''),
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white'
                          ).grid(column=0, row=row, sticky='nwse', pady=2)

                    Entry(frame, width=10,
                          font=('Comic Sans MS', user.get('text_size')),
                          justify="center",
                          validate="all",
                          textvariable=data['examination']['anthro'][variable],
                          validatecommand=check
                          ).grid(column=1, row=row, sticky='nwse')

                    data['examination']['anthro'][variable].set(f"{patient_age_month} мес.")


                    Label(master=frame, text=f"{npr_name.get(npr_marker)}",
                          font=('Comic Sans MS', user.get('text_size')), bg='white'
                          ).grid(row=row, column=2, sticky='nwse', pady=2)

                    Label(master=frame, text=f"{local_data_npr[age_month].get(npr_marker)}",
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').grid(row=row, column=3, sticky='nwse', columnspan=2, pady=2)
                    row += 1

                frame.columnconfigure(index='all', minsize=40, weight=1)
                frame.rowconfigure(index='all', minsize=20)
                data['examination']['npr_frame'][age_month] = frame

            frame = Frame(frame_npr)
            Label(master=frame, text="Показатели НПР для возраста (месяцев): ",
                  font=('Comic Sans MS', user.get('text_size')), bg='white').grid(row=0, column=0, sticky='ew')

            combo_age_month = Combobox(frame, font=('Comic Sans MS', user.get('text_size')),  state="readonly", width=10)
            combo_age_month['values'] = [i for i in range(1, 13)]
            combo_age_month.set(patient_age_month)
            combo_age_month.grid(row=0, column=1, sticky='ew')
            combo_age_month.bind("<<ComboboxSelected>>", selected_age_month)

            frame.columnconfigure(index='all', minsize=40, weight=1)
            frame.rowconfigure(index='all', minsize=20)
            frame.pack(fill='both', expand=True)
            data['examination']['npr_frame'][patient_age_month].pack(fill='both', expand=True)

            frame_npr.pack(fill='both', expand=True, padx=2, pady=2)

        frame_patient_anthro_main = Frame(examination_root, borderwidth=0.5, relief="solid", padx=1, pady=1)
        Label(master=frame_patient_anthro_main,
              text="Данные обследования",
              font=('Comic Sans MS', user.get('text_size')), bg='white').pack(fill='both', expand=True, padx=2, pady=2)


        frame_patient_anthro = Frame(frame_patient_anthro_main, borderwidth=0.5, relief="solid", padx=1, pady=1, bg="#36566d")

        if not render_data.get('hr'):
            paste_hr_br()
        data['examination']['anthro'] = dict()
        data['examination']['anthro']['patient_anthro_data'] = StringVar()
        data['examination']['anthro']['patient_physical_anthro'] = StringVar()

        for mark in local_data_anthro:
            for name, variable in local_data_anthro.get(mark):
                data['examination']['anthro'][variable] = StringVar()

        counter_col = 0
        for mark in local_data_anthro:
            if mark == 'anal':
                continue

            frame = Frame(frame_patient_anthro, padx=3, pady=3)
            row = 0
            for name, variable in local_data_anthro.get(mark):
                check = (root_examination.register(is_valid__anthro), "%P",
                         f"{mark}__{name}__{variable}")

                Label(master=frame, text=name.replace(' _', ''),
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white'
                      ).grid(column=0, row=row, sticky='ew')

                Entry(frame, width=10,
                      font=('Comic Sans MS', user.get('text_size')),
                      justify="center",
                      validate="all",
                      textvariable=data['examination']['anthro'][variable],
                      validatecommand=check
                      ).grid(column=1, row=row, sticky='ew')
                if variable == 'txt_hr_variable':
                    data['examination']['anthro'][variable].set(render_data.get('hr'))
                elif variable == 'txt_br_variable':
                    data['examination']['anthro'][variable].set(render_data.get('br'))
                elif variable == 'txt_temp_variable':
                    data['examination']['anthro'][variable].set(random.choice(['36,6', '36,7', '36,5']))


                row += 1

            frame.columnconfigure(index='all', minsize=40, weight=1)
            frame.rowconfigure(index='all', minsize=20)
            frame.grid(column=counter_col, row=0, sticky='nwse')
            if child_marker and mark == 'weight':
                frame.grid_configure(rowspan=2)
            counter_col += 1
            # frame.pack(fill='both', expand=True, side="left")


        lbl = Label(master=frame_patient_anthro,
                    textvariable=data['examination']['anthro'].get('patient_physical_anthro'),
                    font=('Comic Sans MS', user.get('text_size')),
                    bg='white')
        if child_marker:
            lbl.grid(column=1, row=1, sticky='nwse', columnspan=3)
        else:
            lbl.grid(column=0, row=1, sticky='nwse', columnspan=4)


        frame_patient_anthro.columnconfigure(index='all', minsize=40, weight=1)
        frame_patient_anthro.rowconfigure(index='all', minsize=20)
        frame_patient_anthro.pack(fill='both', expand=True)
        frame_patient_anthro_main.pack(fill='both', expand=True, padx=2, pady=2)

        if child_marker:
            paste_npr_root()


    local_data_anthro = {
        "weight":
            (("Вес: _ кг.", "txt_weight_variable"),
             ("Рост: _ см.", "txt_height_variable")),
        "hr_br":
            (("ЧД: _ /мин.", "txt_br_variable"),
             ("ЧСС: _ /мин.", "txt_hr_variable")),
        "temp":
            (("Температура: _ ℃.", "txt_temp_variable"),
             ("sp O₂: _ %.", "txt_sp02_variable")),
        "bp":
            (("АД: _ мм.рт.ст.", "txt_bp_variable"),
             ("ИМТ: _ кг/м²", "txt_imt_variable"))

    }

    if child_marker:
        local_data_anthro = {
        "weight":
            (("Фактическиий вес: _ гр.", "txt_weight_variable"),
             ("Вес при рождении: _ гр.", "txt_weight_bir_variable"),
             ("Должный вес: _ гр.", "txt_weight_must_variable"),
             ("Прибавка: _ гр.", "txt_weight_delta_variable")),
        "height":
            (("Длинна тела: _ см.", "txt_height_variable"),
             ("Окр. головы: _ см.", "txt_head_variable"),
             ("Окр. груди: _  см.", "txt_chest_variable")),
        "other":
            (("Родничок: _ ", "txt_hole_head_variable"),
             ("Зубы: _ ", "txt_teeth_variable"),
             ("БЦЖ _ ", "txt_tubic_variable")),
        "hr_br":
            (("ЧД: _ /мин.", "txt_br_variable"),
             ("ЧСС: _ /мин.", "txt_hr_variable"),
             ("Температура: _ ℃.", "txt_temp_variable")),
        "anal":
            (("Аз: _ ", "txt_anal_1_variable"),
             ("Ас: _ ", "txt_anal_2_variable"),
             ("Э: _ ", "txt_anal_3_variable"),
             ("ДР: _ ", "txt_anal_4_variable"),
             ("ДО: _ ", "txt_anal_5_variable"),
             ("ПР: _ ", "txt_anal_6_variable"),
             ("PA: _ ", "txt_anal_7_variable"),
             ("Н: _ ", "txt_anal_8_variable")),

        }


    def edit_drugs_weight(weight):

        for drug_category in ['Антибиотики', 'ОРИ']:
            if data['examination'].get('selected_drugs', dict()).get(drug_category):
                for drug_name in data['examination']['selected_drugs'].get(drug_category):
                    drug_form = data['examination']['selected_drugs'][drug_category][drug_name].get('Форма')
                    if drug_form:
                        select_drugs_item(weight=weight,
                                          drug_name=f"{drug_category}__{drug_name}__Форма__{drug_form}")

    paste_patient_anthro_data()


    def paste_frame_examination():

        label_examination = Label(master=frame_examination_main,
                                  text=f"Осмотр:",
                                  font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_examination.grid(row=0, column=0, sticky='ew')


        label_examination = Label(master=frame_examination_main,
                                  textvariable=data['examination']['anthro']['patient_anthro_data'],
                                  font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_examination.grid(column=0, row=1, sticky='ew', columnspan=2)


        txt_examination.grid(column=0, row=2, sticky='ew', columnspan=2)


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

        local_examination = dict()


        text = txt_examination.get(1.0, 'end').strip()
        if text and text[-1] == '.':
            text = text[:-1] + ', '

        loc_examination = all_data_diagnosis.get('examination')
        if child_marker:
            loc_examination = all_data_diagnosis.get('examination_child')

        for mark in loc_examination:
            if isinstance(mark, tuple):
                text = text.replace(mark[0], f"\n__!__{mark[0]}")
                local_examination[mark[0]] = ""
        for string in text.split('\n__!__'):
            for i in local_examination.keys():
                if i in string:
                    local_examination[i] = string
                    break

        examination_button = selected_button.get()
        selected_button.set('')
        if examination_button:
            if data['examination']['examination_but'].get(examination_button):
                if data['examination']['examination_but'].get(examination_button).get() == 1:
                    data['examination']['examination_but'].get(examination_button).set(0)
                else:
                    data['examination']['examination_but'].get(examination_button).set(1)

        if len(examination_button.split('_')) == 3:
            mark_1, side, mark_2 = examination_button.split('_')
        else:
            mark_1, mark_2 = examination_button.split('_')

        if (data['examination']['examination_but'].get(examination_button).get() == 1
                and not local_examination.get(mark_1)):
            text += '\n'
            if mark_1 in ('Глаза', 'Отоскопия'):
                text += f"{mark_1}: {side} - {mark_2}, "
            else:
                if mark_2[-1] != '-':
                    text += f"{mark_1}: {mark_2}, "
                else:
                    text += f"{mark_1}: {mark_2} "
        else:
            if mark_1 in ('Глаза', 'Отоскопия'):
                loc_data = {
                    'Глаза': ("OD", "OS", "OU"),
                    'Отоскопия': ("AD", "AS", "AU")}
                for i in loc_data.get(mark_1):
                    if i in local_examination.get(mark_1):
                        local_examination[mark_1] = local_examination.get(mark_1).replace(i, f"__!!__{i}")
                loc_data_side = dict()
                for side_str in local_examination.get(mark_1).split('__!!__'):
                    for i in loc_data.get(mark_1):
                        if i in side_str:
                            loc_data_side[i] = side_str
                edited_text = ''
                for examination_but in data['examination'].get('examination_but'):
                    if (examination_but.startswith(f"{mark_1}_{side}")
                            and data['examination']['examination_but'].get(examination_but).get() == 1):
                        edited_text += f"{examination_but.split('_')[-1]}, "
                if edited_text:
                    edited_text = f"{side} - " + edited_text

                    if loc_data_side.get(side):
                        text = text.replace(loc_data_side.get(side), edited_text)
                    else:
                        local_examination[mark_1] = local_examination.get(mark_1).replace("__!!__", '')
                        text = text.replace(local_examination.get(mark_1), f"{local_examination.get(mark_1)}, "
                                                                           f"{edited_text}")

            else:
                edited_text = ''
                for examination_but in data['examination'].get('examination_but'):
                    if (examination_but.startswith(f"{mark_1}")
                            and data['examination']['examination_but'].get(examination_but).get() == 1):
                        if examination_but[-1] != '-':
                            edited_text += f"{examination_but.split('_')[-1]}, "
                        else:
                            edited_text += f"{examination_but.split('_')[-1]} "

                if edited_text:
                    edited_text = f"{mark_1}: " + edited_text

                text = text.replace(local_examination.get(mark_1), edited_text)


        if data['examination'].get('open_complaints_kb'):
            for but in data['examination'].get('complaints_buttons'):
                if data['examination']['complaints_but'].get(but).get() == 1:
                    data['examination']['complaints_buttons'][but]['bg'] = '#77f1ff'
                else:
                    data['examination']['complaints_buttons'][but]['bg'] = '#cdcdcd'


        text = text.replace('__!__', '').replace('  ', ' ').replace(' .', '.').replace(' ,', ',').replace(
            ',,', ',').replace('\n\n', '\n').replace(',.', ',').strip()
        if text[-1] == ',':
            text = text[:-1] + '.'

        txt_examination.delete(1.0, 'end')
        txt_examination.insert(1.0, text)
        edit_examination_kb_text()

    def edit_examination_kb_text():
        for button_name in data['examination'].get('examination_buttons'):
            text = f"{button_name}: "
            if button_name in ('Глаза', 'Отоскопия'):
                loc_data = dict()
                for examination_but in data['examination'].get('examination_but'):
                    if (examination_but.startswith(button_name)
                            and data['examination']['examination_but'].get(examination_but).get() == 1):
                        mark_1, side, mark_2 = examination_but.split('_')
                        if not loc_data.get(side):
                            loc_data[side] = f"{side} - "

                        if len(loc_data.get(side, '').split('\n')[-1]) > 70:
                            loc_data[side] += "\n"
                        loc_data[side] += f"{mark_2}, "

                for side in loc_data.keys():
                    text += loc_data.get(side, '') + '\n'
            else:
                for examination_but in data['examination'].get('examination_but'):
                    if (examination_but.startswith(button_name)
                            and data['examination']['examination_but'].get(examination_but).get() == 1):
                        if len(text.split('\n')[-1]) > 80:
                            text += "\n"

                        text += f"{examination_but.split('_')[-1]}, "
            text = text[:-2]
            btn = data['examination']['examination_buttons'].get(button_name)
            btn['text'] = text.strip()

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

        data['examination']['examination_but'] = dict()
        local_examination = all_data_diagnosis.get('examination')
        if child_marker:
            local_examination = all_data_diagnosis.get('examination_child')

        for mark_ in local_examination:
            if isinstance(mark_, tuple):

                if mark_[0] in ('Глаза', 'Отоскопия'):
                    loc_data = {
                        'Глаза': ("OD", "OS", "OU"),
                        'Отоскопия': ("AD", "AS", "AU")}
                    for mark_2_ in mark_[1:]:
                        for mark_3_ in loc_data.get(mark_[0], []):
                            data['examination']['examination_but'][f"{mark_[0]}_{mark_3_}_{mark_2_}"] = IntVar()
                else:

                    for mark_2_ in mark_[1:]:
                        data['examination']['examination_but'][f"{mark_[0]}_{mark_2_}"] = IntVar()


        for mark in local_examination:
            if isinstance(mark, tuple):
                frame_loc = Frame(frame_examination_buttons, borderwidth=1)

                btn = Radiobutton(frame_loc, text=f"{mark[0]}",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=f"{mark[0]}", variable=selected_examination_frame,
                                  command=select_examination_frame,
                                  indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff',
                                  justify='left', anchor='w', padx=10)
                btn.pack(fill='both', expand=True)
                data['examination']['examination_buttons'][mark[0]] = btn

                row, col = 0, 0

                frame_loc_but = Frame(frame_loc, borderwidth=1)

                data['examination']['examination_frame'][mark[0]] = frame_loc_but
                if mark[0] in ('Глаза', 'Отоскопия'):
                    loc_data = {
                        'Глаза': ("OD", "OS", "OU"),
                        'Отоскопия': ("AD", "AS", "AU")}
                    for mark_3 in loc_data.get(mark[0], []):

                        frame_loc_but_side = Frame(frame_loc_but, borderwidth=1)
                        row_counter, col = 1, 0
                        loc_lbl = Label(master=frame_loc_but_side, text=f"{mark_3}",
                              font=('Comic Sans MS', user.get('text_size')),
                              bg='white')
                        loc_lbl.grid(row=row, column=col, sticky='nwse', pady=2, padx=2)
                        col += 1

                        for mark_2 in mark[1:]:
                            if col == 5:
                                row_counter += 1
                                col = 1
                                row += 1
                                loc_lbl.grid_configure(rowspan=row_counter)

                            btn = Radiobutton(frame_loc_but_side, text=f"{mark_2}",
                                              font=('Comic Sans MS', user.get('text_size')),
                                              value=f"{mark[0]}_{mark_3}_{mark_2}",
                                              variable=selected_button,
                                              command=select_examination,
                                              indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
                            btn.grid(row=row, column=col, sticky='ew')
                            data['examination']['examination_buttons_2_color'][f"{mark[0]}_{mark_3}_{mark_2}"] = btn

                            col += 1

                        frame_loc_but_side.columnconfigure(index='all', minsize=40, weight=1)
                        frame_loc_but_side.rowconfigure(index='all', minsize=20)
                        frame_loc_but_side.pack(fill='both', expand=True, padx=2, pady=3)


                else:
                    frame_loc_but_string = Frame(frame_loc_but)
                    for mark_2 in mark[1:]:
                        if mark_2 != '\n':
                            btn = Radiobutton(frame_loc_but_string, text=f"{mark_2}",
                                              font=('Comic Sans MS', user.get('text_size')),
                                              value=f"{mark[0]}_{mark_2}",
                                              variable=selected_button,
                                              command=select_examination,
                                              indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
                            btn.pack(fill='both', expand=True, side='left')
                            data['examination']['examination_buttons_2_color'][f"{mark[0]}_{mark_2}"] = btn

                            col += 1

                        if mark_2 == '\n' or col == 5:

                            col = 0

                            frame_loc_but_string.columnconfigure(index='all', minsize=40, weight=1)
                            frame_loc_but_string.rowconfigure(index='all', minsize=20)
                            frame_loc_but_string.pack(fill='both', expand=True)
                            frame_loc_but_string = Frame(frame_loc_but)


                    frame_loc_but_string.columnconfigure(index='all', minsize=40, weight=1)
                    frame_loc_but_string.rowconfigure(index='all', minsize=20)
                    frame_loc_but_string.pack(fill='both', expand=True)

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

    txt_examination = ScrolledText(frame_examination_main, width=20, height=30,
                                   font=('Comic Sans MS', user.get('text_size')),
                                   wrap="word")
    change_examination_kb_button = Button(frame_examination_main, text='скрыть клавиатуру осмотра',
                                          command=change_examination_kb_status,
                                          font=('Comic Sans MS', user.get('text_size')))

    paste_frame_examination()

    def open_mkb_10_root():
        if not data['examination'].get('is_mkb_10_root_open'):
            data['examination']['is_mkb_10_root_open'] = True
            mkb_10_root_main.grid()
        else:
            data['examination']['is_mkb_10_root_open'] = False
            mkb_10_root_main.grid_remove()

    def create_mkb_10_root():
        def celect_code():
            txt_diagnosis.insert('end', f"\n{celected_code.get()}")

        def search_mkb(event=None):
            def resize(event=None):
                region = canvas.bbox(tk.ALL)
                canvas.configure(scrollregion=region)

            def on_binds(event):
                canvas.idbind = canvas.bind_all("<MouseWheel>", on_mousewheel)

            def off_binds(event=None):
                canvas.unbind_all("<MouseWheel>")

            def on_mousewheel(event):

                region = canvas.bbox(tk.ALL)
                canvas.configure(scrollregion=region)

                if os.name == 'posix':
                    canvas.yview_scroll(int(-1 * event.delta), "units")
                else:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


            if data['examination'].get('frame_found_data_mkb'):
                frame_found_data_mkb = data['examination'].get('frame_found_data_mkb')
                frame_found_data_mkb.destroy()
            master_frame = Frame(mkb_frame_scrolled)
            data['examination']['frame_found_data_mkb'] = master_frame
            master_frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)


            found_data = list()
            mkb_code_edit = ''
            mkb_name_edit = mkb_name.get()

            if mkb_code.get():
                word_list = ["qwertyuiopasdfghjkl;'zxcvbnm,.", "йцукенгшщзфывапролджэячсмитьбю"]

                for word in mkb_code.get().lower():
                    if word in word_list[1]:
                        mkb_code_edit += word_list[0][word_list[1].index(word)]
                    elif word == ',':
                        mkb_code_edit += '.'
                    else:
                        mkb_code_edit += word
                mkb_code_edit = mkb_code_edit.upper()

            if mkb_code_edit and mkb_name_edit:
                for key, value in mkb_10.items():
                    if mkb_code_edit in key and mkb_name_edit.lower() in value.lower():
                        found_data.append(f"{key} - {value}")
            elif mkb_code_edit:
                for key, value in mkb_10.items():
                    if mkb_code_edit in key:
                        found_data.append(f"{key} - {value}")
            elif mkb_name_edit:
                for key, value in mkb_10.items():
                    if mkb_name_edit.lower() in value.lower():
                        found_data.append(f"{key} - {value}")


            if found_data:

                scroll_x = tk.Scrollbar(master_frame, orient=tk.HORIZONTAL)
                scroll_y = tk.Scrollbar(master_frame, orient=tk.VERTICAL)

                canvas = tk.Canvas(master_frame,
                                   xscrollcommand=scroll_x.set,
                                   yscrollcommand=scroll_y.set)
                scroll_x.config(command=canvas.xview)
                scroll_y.config(command=canvas.yview)

                canvas_frame = Frame(canvas)

                for mkb_data in found_data:
                    but_text = ''
                    for i in mkb_data.split():
                        if len(but_text.split('\n')[-1]) > 40:
                            but_text += '\n'
                        but_text += i + ' '
                    Radiobutton(canvas_frame, text=but_text,
                                font=('Comic Sans MS', user.get('text_size')),
                                value=f"{mkb_data}",
                                variable=celected_code,
                                command=celect_code,
                                indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff'
                                ).pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)


                # canvas_frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)


                canvas['width'] = int(canvas.winfo_geometry().split('x')[0])
                canvas_frame['width'] = int(canvas.winfo_geometry().split('x')[0])
                canvas.grid(row=0, column=0, sticky="nsew")
                scroll_x.grid(row=1, column=0, sticky="we")
                scroll_y.grid(row=0, column=1, sticky="ns")

                master_frame.rowconfigure(0, weight=1)
                master_frame.columnconfigure(0, weight=1)

                master_frame.bind("<Configure>", resize)
                master_frame.update_idletasks()
                canvas_frame['height'] = int(mkb_10_root_main.winfo_height() - frame_main_mkb_10.winfo_height())



                canvas.bind("<Enter>", on_binds)
                canvas.bind("<Leave>", off_binds)

                canvas.create_window((0, 0), window=canvas_frame, anchor="nw",
                                     width=canvas.winfo_width())

            else:
                Label(master_frame, text="Поиск не дал результатов!",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')

        mkb_code = StringVar()
        mkb_name = StringVar()
        celected_code = StringVar()

        frame_main_mkb_10 = Frame(mkb_10_root_main, bg="#36566d")
        Label(frame_main_mkb_10, text="Поиск по МКБ-10",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')
        Button(frame_main_mkb_10, text=f"Закрыть окно",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_mkb_10_root,
               bg='#f0fffe').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')


        mkb_title_frame = Frame(frame_main_mkb_10, bg="#36566d")
        Label(mkb_title_frame, text="Код: ",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, side='left')
        txt_mkb = Entry(mkb_title_frame, width=10,
              font=('Comic Sans MS', user.get('text_size')),
              justify="center",
              textvariable=mkb_code)
        txt_mkb.pack(fill='x', expand=True, pady=3, padx=3, side='left')
        txt_mkb.bind('<Return>', search_mkb)

        Label(mkb_title_frame, text="Нозология: ",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, side='left')
        txt_mkb = Entry(mkb_title_frame, width=30,
              font=('Comic Sans MS', user.get('text_size')),
              textvariable=mkb_name)
        txt_mkb.pack(fill='x', expand=True, pady=3, padx=3, side='left')
        txt_mkb.bind('<Return>', search_mkb)


        mkb_title_frame.pack(fill='x', anchor='n')
        frame_main_mkb_10.pack(fill='x', anchor='n')

        mkb_frame_scrolled = Frame(mkb_10_root_main)
        mkb_frame_scrolled.pack(fill='both', expand=True)

        data['examination']['is_mkb_10_root_open'] = False
        mkb_10_root_main.grid(row=0, column=3, sticky="nwse", rowspan=3)

        mkb_10_root_main.grid_remove()

    mkb_10_root_main = Frame(master=root_examination, padx=3, pady=3, bg="#36566d")
    mkb_10_root_main.update_idletasks()
    create_mkb_10_root()

    def paste_diagnosis_kb():

        def edti__txt_diagnosis(event=None):
            txt_diagnosis_info = txt_diagnosis.get(1.0, 'end').strip()
            txt_diagnosis_info = txt_diagnosis_info.replace('  ', ' ')
            txt_diagnosis.delete(1.0, 'end')
            txt_diagnosis.insert(1.0, txt_diagnosis_info)


        def select_diagnosis_kb():
            diagnosis_button = selected_button.get()
            selected_button.set('')
            txt_diagnosis.insert("insert", f" {diagnosis_button} ")


        txt_diagnosis['width'] = 30
        txt_diagnosis['height'] = 5
        txt_diagnosis.bind("<FocusOut>", edti__txt_diagnosis)

        frame_diagnosis_kb = Frame(frame_diagnosis_txt, borderwidth=1, relief="solid")
        destroy_elements['frame_diagnosis_kb'] = frame_diagnosis_kb

        row, col = 0, 0
        local_diagnosis_kb = all_data_diagnosis.get('diagnosis_ori')
        if child_marker:
            local_diagnosis_kb = all_data_diagnosis.get('diagnosis_key_child')

        for mark_group in local_diagnosis_kb:
            mark_group_frame = Frame(frame_diagnosis_kb)
            for mark in mark_group:
                btn = Radiobutton(mark_group_frame, text=mark,
                                  font=('Comic Sans MS', user.get('text_size')),
                                  value=f"{mark}",
                                  variable=selected_button,
                                  command=select_diagnosis_kb,
                                  indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')

                btn.grid(row=row, column=col, sticky='ew')
                col += 1
                # if col == 4:
                #     col = 0
                #     row += 1
            mark_group_frame.columnconfigure(index='all', minsize=40, weight=1)
            mark_group_frame.rowconfigure(index='all', minsize=20)

            mark_group_frame.pack(fill='both', expand=True)

        Button(frame_diagnosis_kb, text='MKБ-10',
               command=open_mkb_10_root,
               font=('Comic Sans MS', user.get('text_size'))).pack(fill='both', expand=True)

        frame_diagnosis_kb.columnconfigure(index='all', minsize=40, weight=1)
        frame_diagnosis_kb.rowconfigure(index='all', minsize=20)
        frame_diagnosis_kb.pack(fill='both', expand=True, side=tk.LEFT)


    frame_diagnosis_txt = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
    Label(master=frame_diagnosis_txt, text="Диагноз",
          font=('Comic Sans MS', user.get('text_size')), bg='white'
          ).pack(fill='both', expand=True, padx=2, pady=2)

    txt_diagnosis = ScrolledText(frame_diagnosis_txt, width=70, height=3,
                                 font=('Comic Sans MS', user.get('text_size')),
                                 wrap="word")
    txt_diagnosis.pack(fill='both', expand=True, side=tk.LEFT)
    txt_diagnosis.insert(1.0, 'Диагноз: ')
    frame_diagnosis_txt.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

    paste_diagnosis_kb()

    def paste_diagnosis_add_but():
        def select_button_risk():
            if data['examination']['diagnosis_add_but'].get('Группа риска__нет').get():
                for but_name in data['examination'].get('diagnosis_add_but'):
                    if (but_name.startswith('Группа риска')
                            and data['examination']['diagnosis_add_but'].get(but_name).get()
                            and but_name.split('__')[-1] != 'нет'):

                        data['examination']['diagnosis_add_but'].get(but_name).set(0)

            select_button()
            risk_data = {
                "нет": {},
                "реализации ВУИ": {
                    1: ("ОАК + ОАМ (даны направления)", ),
                    3: ("ОАК + ОАМ (даны направления)", )},
                "патологии ЦНС": {
                    1: ('Консультация невролога + УЗИ ГМ', ),
                    3: ("Консультация невролога", ),
                    6: ("Консультация невролога", )},
                "Анемии": {
                    1: ('ОАК + ретикулоциты', ),
                    3: ("ОАК + ретикулоциты", ),
                    6: ("ОАК + ретикулоциты", )},

                "Внезапной смерти": {
                    1: ('ЭКГ', ),
                    12: ("ЭКГ", )},

                "Диспансеризация": {
                    1: ("ОАК + ОАМ (даны направления)", "ОАЭ и ЭКГ при отсутствии данных о проведении",
                        "Консультация невролога (запись через справку)", "Консультация хирурга (ортопеда)"),
                    6: ("Консультация офтальмолога и оториноларинголога (запись через справку)", ),

                    11: ("ОАК + ОАМ (даны направления)", "Консультация стоматолога в 12 мес")
                }
            }

            if patient_age.get('year') == 0:
                age_month = patient_age.get('month')
                if age_month == 0 and patient_age.get('day') > 20:
                    age_month = 1
                elif age_month == 1 and patient_age.get('day') > 20:
                    age_month = 2

                text = txt_prescription.get(1.0, 'end').strip()
                edited_string_risk = ''
                edited_string_disp = ''

                new_string_risk = ''
                new_string_disp = ''

                for string in text.split('\n'):
                    if string.startswith('На основании групп риска:'):
                        edited_string_risk = string
                    elif string.startswith('На основании диспансеризации:'):
                        edited_string_disp = string

                for but_name in data['examination'].get('diagnosis_add_but'):
                    if (but_name.startswith('Группа риска')
                            and data['examination']['diagnosis_add_but'].get(but_name).get()):
                        risk_name = but_name.split('__')[-1]
                        if risk_data[risk_name].get(age_month):
                            if risk_name == 'Анемии' and 'ОАК' in new_string_risk:
                                new_string_risk = new_string_risk.replace('ОАК', "ОАК с ретикулоцитами")
                            elif risk_name in risk_data:
                                for mark in risk_data[risk_name].get(age_month):
                                    new_string_risk += f"{mark}, "

                if risk_data["Диспансеризация"].get(age_month):
                    for mark in risk_data["Диспансеризация"].get(age_month):
                        if mark not in new_string_risk:
                            new_string_disp += f"{mark}, "


                for mark, old_string, new_string in (("На основании групп риска:", edited_string_risk, new_string_risk),
                                                     ("На основании диспансеризации:", edited_string_disp, new_string_disp)):
                    if not old_string:
                        if new_string:
                            text += f"\n{mark} {new_string}"
                    else:
                        if new_string:
                            text = text.replace(old_string, f"{mark} {new_string}")
                        else:
                            text = text.replace(old_string, "")

                txt_prescription.delete(1.0, 'end')
                txt_prescription.insert(1.0, text)

        def select_button():
            text = txt_diagnosis.get(1.0, 'end').strip()
            edited_string = ''
            for string in text.split('\n'):
                for but_category in local_but_name:
                    if string.startswith(but_category):
                        edited_string = string

            new_string = ''
            for but_name in data['examination'].get('diagnosis_add_but'):
                if but_name.startswith('Группа риска'):
                    if data['examination']['diagnosis_add_but'].get(but_name).get():
                        if 'Группа риска' not in new_string:
                            new_string += "  Группа риска: "
                        new_string += f"{but_name.split('__')[-1]}"
                        if ((but_name.split('__')[-1] ==  'реализации ВУИ' and patient_age.get('month') > 3)
                            or (but_name.split('__')[-1] !=  'нет' and patient_age.get('year') > 0)):
                            new_string += " - риск не реализовался, "
                        else:
                            new_string += ", "


                else:
                    if data['examination']['diagnosis_add_but'].get(but_name).get():
                        new_string += f"  {but_name}: {data['examination']['diagnosis_add_but'].get(but_name).get()}"

            if edited_string:
                text = text.replace(edited_string, new_string.strip())
            else:
                text += f"\n{new_string.strip()}"

            txt_diagnosis.delete(1.0, 'end')
            txt_diagnosis.insert(1.0, text)


        frame_diagnosis_add_but = Frame(examination_root, borderwidth=1, relief="solid", padx=3, pady=3)
        data['examination']['diagnosis_add_but'] = dict()
        local_but_name = {
            'Группа здоровья': ("1", "2", "3", "4"),
            'Группа риска': ("нет", "реализации ВУИ", "патологии ЦНС", "Анемии", "Внезапной смерти"),
            'НПР': ("1-я группа", "2-я группа", "3-я группа", "4-я группа"),
            'Режим дня №': ("1", "2", "3", "4", "5"),
        }

        for but_category in local_but_name:
            frame = Frame(frame_diagnosis_add_but)

            Label(master=frame,
                  text=but_category,
                  font=('Comic Sans MS', user.get('text_size')), bg='white'
                  ).pack(fill='both', expand=True, side='left', pady=2, padx=2)


            if but_category == 'Группа риска':

                for but_name in local_but_name.get(but_category):
                    data['examination']['diagnosis_add_but'][f"{but_category}__{but_name}"] = IntVar()

                    Checkbutton(frame, text=but_name,
                                font=('Comic Sans MS', user.get('text_size')),
                                variable=data['examination']['diagnosis_add_but'].get(f"{but_category}__{but_name}"),
                                command=select_button_risk,
                                onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff'
                                ).pack(fill='both', expand=True, side='left')

            else:
                data['examination']['diagnosis_add_but'][but_category] = StringVar()
                for but_name in local_but_name.get(but_category):
                    Radiobutton(frame, text=but_name,
                                font=('Comic Sans MS', user.get('text_size')),
                                value=but_name,
                                variable=data['examination']['diagnosis_add_but'].get(but_category),
                                command=select_button,
                                indicatoron=False, selectcolor='#77f1ff'
                                ).pack(fill='both', expand=True, side='left')

            frame.columnconfigure(index='all', minsize=40, weight=1)
            frame.rowconfigure(index='all', minsize=20)
            frame.pack(fill='both', expand=True)

        data['examination']['diagnosis_add_but']['Группа здоровья'].set('2')
        if patient_age.get('month') > 0:
            data['examination']['diagnosis_add_but']['НПР'].set('1-я группа')
        if patient_age.get('month') < 3:
            data['examination']['diagnosis_add_but']['Режим дня №'].set('1')
        elif patient_age.get('month') < 6:
            data['examination']['diagnosis_add_but']['Режим дня №'].set('2')
        elif patient_age.get('month') < 9:
            data['examination']['diagnosis_add_but']['Режим дня №'].set('3')
        elif patient_age.get('year') == 0:
            data['examination']['diagnosis_add_but']['Режим дня №'].set('4')
        else:
            data['examination']['diagnosis_add_but']['Режим дня №'].set('4')
        select_button()



        frame_diagnosis_add_but.columnconfigure(index='all', minsize=40, weight=1)
        frame_diagnosis_add_but.rowconfigure(index='all', minsize=20)
        frame_diagnosis_add_but.pack(fill='both', expand=True)

    if child_marker:
        paste_diagnosis_add_but()

    def open_analyzes_root():
        if not data['examination']['analyzes'].get('is_analyzes_root_open'):
            data['examination']['analyzes']['is_analyzes_root_open'] = True
            analyzes_root_main.grid()
        else:
            data['examination']['analyzes']['is_analyzes_root_open'] = False
            analyzes_root_main.grid_remove()

    def create_analyzes_root():
        def create_anal_doc():
            if not data['examination']['analyzes'].get('patient_anal'):
                messagebox.showerror('Ошибка!', "Выберите хотя бы один анализ!")
            else:
                render_data.clear()

                render_data['ped_div'] = user.get('ped_div')
                render_data['doc_name'] = user.get('doctor_name')
                render_data['district'] = patient.get('patient_district')
                render_data['name'] = patient.get('name')
                render_data['birth_date'] = patient.get('birth_date')
                render_data['address'] = patient.get('address')
                render_data['gender'] = patient.get('gender')
                render_data['date'] = datetime.now().strftime("%d.%m.%Y")
                render_data['amb_cart'] = patient.get('amb_cart')
                render_data['diagnosis'] = txt_diagnosis.get(1.0, 'end').strip().replace('Диагноз:', "")

                if 'blood-inf__ГЕПАТИТ' in data['examination']['analyzes'].get('patient_anal'):
                    with sq.connect(f".{os.sep}data_base{os.sep}patient_data_base.db") as conn:
                        cur = conn.cursor()
                        cur.execute(f"SELECT Прививки FROM patient_data WHERE amb_cart LIKE '{patient.get('amb_cart')}'")
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

                all_links = list()
                for anal_name in data['examination']['analyzes'].get('patient_anal'):
                    category, anal_name = anal_name.split('__')

                    doc = DocxTemplate(f".{os.sep}example{os.sep}{category}{os.sep}{anal_name}.docx")
                    doc.render(render_data)
                    doc.save(f".{os.sep}generated{os.sep}{anal_name}.docx")
                    all_links.append(f".{os.sep}generated{os.sep}{anal_name}.docx")

                master = Document(all_links.pop(0))
                composer = Composer(master)
                for link in all_links:
                    master.add_page_break()
                    doc_temp = Document(link)
                    composer.append(doc_temp)
                doc_name = f".{os.sep}generated{os.sep}Анализы.docx"
                doc_name = save_document(doc=composer, doc_name=doc_name)
                data['examination']['analyzes']['patient_anal'].clear()
                for btn_name in data['examination']['analyzes'].get('anal_name_buttons'):
                    active_btn = data['examination']['analyzes']['anal_name_buttons'].get(btn_name)
                    active_btn['bg'] = '#cdcdcd'
                    active_btn['text'] = f"{btn_name.split('__')[-1]}"

                selected_anal.set('')
                render_data.clear()
                open_analyzes_root()

                run_document(doc_name)

                data_base(command="statistic_write",
                          insert_data="Анализы")


        def select_anal_name():

            category, anal_name = selected_button.get().split('__')
            if category == 'add':
                if anal_name == 'ОАК  +  ФОРМУЛА':
                    anal_name = 'blood__ОАК + ФОРМУЛА'
                    if anal_name not in data['examination']['analyzes'].get('patient_anal'):
                        data['examination']['analyzes']['patient_anal'].append("blood__ОАК + ФОРМУЛА")
                        active_btn = data['examination']['analyzes']['anal_name_buttons'].get("blood__ОАК + ФОРМУЛА")
                        active_btn['bg'] = '#77f1ff'
                        active_btn['text'] = f"✔{anal_name}"
                else:
                    for marker in anal_name.split(' + '):
                        for btn_name in data['examination']['analyzes'].get('anal_name_buttons'):
                            if (marker in btn_name
                                    and 'add' not in btn_name
                                    and btn_name not in data['examination']['analyzes'].get('patient_anal')):
                                data['examination']['analyzes']['patient_anal'].append(btn_name)
                                active_btn = data['examination']['analyzes']['anal_name_buttons'].get(btn_name)
                                active_btn['bg'] = '#77f1ff'
                                active_btn['text'] = f"✔{marker}"
                                break
            else:
                btn_name = f"{category}__{anal_name}"
                active_btn = data['examination']['analyzes']['anal_name_buttons'].get(btn_name)

                if btn_name in data['examination']['analyzes'].get('patient_anal'):
                    data['examination']['analyzes']['patient_anal'].remove(btn_name)
                    active_btn['bg'] = '#cdcdcd'
                    active_btn['text'] = f"{anal_name}"
                else:
                    data['examination']['analyzes']['patient_anal'].append(btn_name)
                    active_btn['bg'] = '#77f1ff'
                    active_btn['text'] = f"✔{anal_name}"



            if 'blood__ОАК' in data['examination']['analyzes'].get('patient_anal') and \
                ('blood__ОАК + ФОРМУЛА' in data['examination']['analyzes'].get('patient_anal')
                 or 'blood__ОАК + СВЕРТЫВАЕМОСТЬ' in data['examination']['analyzes'].get('patient_anal')):
                data['examination']['analyzes']['patient_anal'].remove("blood__ОАК")
                data['examination']['analyzes']['anal_name_buttons'][f"blood__ОАК"]['bg'] = '#cdcdcd'
                data['examination']['analyzes']['anal_name_buttons'][f"blood__ОАК"]['text'] = "ОАК"

            lbl_text = "Анализы: "
            for anal_name in data['examination']['analyzes'].get('patient_anal'):
                category, anal_name = anal_name.split('__')
                lbl_text += f"{anal_name}, "
                if len(lbl_text.split('\n')[-1]) > 40:
                    lbl_text += '\n'


            lbl_text = lbl_text.strip()[:-1]
            selected_anal.set(lbl_text)
            lbl_text = lbl_text.replace('\n', '').lower().replace('анализы', 'Анализы')

            prescription_text = txt_prescription.get(1.0, 'end').strip()
            for string in prescription_text.split('\n'):
                if string.startswith("Анализы:"):
                    prescription_text = prescription_text.replace(string, lbl_text)
                    break
            else:
                prescription_text = f"{lbl_text}\n{prescription_text}"
            txt_prescription.delete(1.0, 'end')
            txt_prescription.insert(1.0, prescription_text)

        def select_anal_category():
            if data['examination']['analyzes'].get('frame_anal_active'):
                frame_anal_active = data['examination']['analyzes'].get('frame_anal_active')
                frame_anal_active.pack_forget()
            master_frame = data['examination']['analyzes']['anal_category_frames'].get(selected_button.get())
            data['examination']['analyzes']['frame_anal_active'] = master_frame
            master_frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

        data['examination']['analyzes'] = {
            'is_analyzes_root_open': False,
            'frame_anal_active': None,
            'anal_name_buttons': dict(),
            'anal_category_frames': dict(),
            'patient_anal': list()}

        frame_main_analyzes = Frame(analyzes_root_main, bg="#36566d")
        anal_frame_category = Frame(analyzes_root_main)

        selected_anal = StringVar()

        Label(frame_main_analyzes, textvariable=selected_anal,
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')

        Button(frame_main_analyzes, text=f"Закрыть окно",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_analyzes_root,
               bg='#f0fffe').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')
        Button(frame_main_analyzes, text=f"Создать документ",
               font=('Comic Sans MS', user.get('text_size')),
               command=create_anal_doc,
               bg='#f0fffe').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')

        Label(frame_main_analyzes, text=f"Категории анализов:\n{'_'*50}",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')


        for category in all_blanks_anal:
            Radiobutton(frame_main_analyzes, text=all_blanks_anal.get(category)[0],
                        font=('Comic Sans MS', user.get('text_size')),
                        value=category, variable=selected_button,
                        command=select_anal_category,
                        indicatoron=False, selectcolor='#77f1ff',
                        bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3)

            master_frame = Frame(anal_frame_category)
            for anal_name in all_blanks_anal.get(category)[1:]:
                btn = Radiobutton(master_frame, text=f'{anal_name}',
                                    font=('Comic Sans MS', user.get('text_size')),
                                    value=f"{category}__{anal_name}", variable=selected_button,
                                    command=select_anal_name,
                                    indicatoron=False, selectcolor='#77f1ff',
                                    bg='#cdcdcd')
                btn.pack(fill='both', expand=True, anchor='n')
                data['examination']['analyzes']['anal_name_buttons'][f"{category}__{anal_name}"] = btn
            data['examination']['analyzes']['anal_category_frames'][category] = master_frame



        frame_main_analyzes.pack(fill='x', anchor='n')
        anal_frame_category.pack(fill='both', expand=True)
        analyzes_root_main.grid(row=0, column=3, sticky="nwse", rowspan=3)
        analyzes_root_main.grid_remove()

    analyzes_root_main = Frame(master=root_examination, padx=3, pady=3, bg="#36566d")
    analyzes_root_main.update_idletasks()
    create_analyzes_root()

    def open_consultation_root():
        if not data['examination']['consultation'].get('is_consultation_root_open'):
            data['examination']['consultation']['is_consultation_root_open'] = True
            consultation_root_main.grid()
        else:
            data['examination']['consultation']['is_consultation_root_open'] = False
            consultation_root_main.grid_remove()

    def create_consultation_root():
        cons_doc = ("офтальмолога", "хирурга", "оториноларинголога",
                    "гастроэнтеролога", "пульмонолога", "невролога",
                    "R-грамма ОГК", "R-грамма ППН", "ЭКГ")

        def create_consult_doc():
            if not data['examination']['consultation'].get('patient_consult'):
                messagebox.showerror('Ошибка!', "Выберите хотя бы одного специалиста!")
            else:

                render_data['address_hospital'] = ' '
                render_data['hospital'] = 'УЗ 19-я Городская детская поликлиника'
                render_data['diagnosis'] = txt_diagnosis.get(1.0, 'end').strip().replace('Диагноз:', "")

                render_data['ped_div'] = user.get('ped_div')
                render_data['doc_name'] = user.get('doctor_name')
                render_data['district'] = patient.get('patient_district')
                render_data['name'] = patient.get('name')
                render_data['birth_date'] = patient.get('birth_date')
                render_data['address'] = patient.get('address')
                render_data['gender'] = patient.get('gender')
                render_data['date'] = datetime.now().strftime("%d.%m.%Y")
                render_data['amb_cart'] = patient.get('amb_cart')


                all_links = list()
                for consult_name in data['examination']['consultation'].get('patient_consult'):
                    render_data['doctor'] = consult_name

                    doc = DocxTemplate(f".{os.sep}example{os.sep}direction{os.sep}НА КОНСУЛЬТАЦИЮ.docx")
                    doc.render(render_data)
                    doc.save(f".{os.sep}generated{os.sep}напр_{consult_name}.docx")
                    all_links.append(f".{os.sep}generated{os.sep}напр_{consult_name}.docx")

                master = Document(all_links.pop(0))
                composer = Composer(master)
                for link in all_links:
                    master.add_page_break()
                    doc_temp = Document(link)
                    composer.append(doc_temp)
                doc_name = f".{os.sep}generated{os.sep}Направление.docx"
                doc_name = save_document(doc=composer, doc_name=doc_name)
                data['examination']['consultation']['patient_consult'].clear()
                for btn_name in data['examination']['consultation'].get('consult_name_buttons'):
                    active_btn = data['examination']['consultation']['consult_name_buttons'].get(btn_name)
                    active_btn['bg'] = '#cdcdcd'
                    active_btn['text'] = f"{btn_name.split('__')[-1]}"

                selected_consult.set('')
                render_data.clear()
                open_consultation_root()
                run_document(doc_name)

                data_base(command="statistic_write",
                          insert_data="Направление")

        def select_consult_name():

            consult_name = selected_button.get()
            active_btn = data['examination']['consultation']['consult_name_buttons'].get(consult_name)

            if consult_name in data['examination']['consultation'].get('patient_consult'):
                data['examination']['consultation']['patient_consult'].remove(consult_name)
                active_btn['bg'] = '#cdcdcd'
                active_btn['text'] = f"{consult_name}"
            else:
                data['examination']['consultation']['patient_consult'].append(consult_name)
                active_btn['bg'] = '#77f1ff'
                active_btn['text'] = f"✔{consult_name}"


            lbl_text = "Консультация: "
            for consult_name in data['examination']['consultation'].get('patient_consult'):
                lbl_text += f"{consult_name}, "
                if len(lbl_text.split('\n')[-1]) > 40:
                    lbl_text += '\n'

            lbl_text = lbl_text.strip()[:-1]
            selected_consult.set(lbl_text)
            lbl_text = lbl_text.replace('\n', '')
            prescription_text = txt_prescription.get(1.0, 'end').strip()
            for string in prescription_text.split('\n'):
                if string.startswith("Консультация:"):
                    prescription_text = prescription_text.replace(string, lbl_text)
                    break
            else:
                prescription_text = f"{lbl_text}\n{prescription_text}"
            txt_prescription.delete(1.0, 'end')
            txt_prescription.insert(1.0, prescription_text)

        data['examination']['consultation'] = {
            'is_consultation_root_open': False,
            'consult_name_buttons': dict(),
            'patient_consult': list()}

        frame_main_consultation = Frame(consultation_root_main, bg="#36566d")
        consult_frame_category = Frame(consultation_root_main)

        selected_consult = StringVar()

        Label(frame_main_consultation, textvariable=selected_consult,
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')

        Button(frame_main_consultation, text=f"Закрыть окно",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_consultation_root,
               bg='#f0fffe').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')
        Button(frame_main_consultation, text=f"Создать документ",
               font=('Comic Sans MS', user.get('text_size')),
               command=create_consult_doc,
               bg='#f0fffe').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')

        Label(frame_main_consultation, text=f"Специалисты:\n{'_' * 50}",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')

        for consult_name in cons_doc:
            btn = Radiobutton(consult_frame_category, text=consult_name,
                              font=('Comic Sans MS', user.get('text_size')),
                              value=consult_name, variable=selected_button,
                              command=select_consult_name,
                              indicatoron=False, selectcolor='#77f1ff',
                              bg='#cdcdcd')
            btn.pack(fill='both', expand=True, anchor='n')
            data['examination']['consultation']['consult_name_buttons'][consult_name] = btn

        frame_main_consultation.pack(fill='x', anchor='n')
        consult_frame_category.pack(fill='both', expand=True)
        consultation_root_main.grid(row=0, column=3, sticky="nwse", rowspan=3)
        consultation_root_main.grid_remove()

    consultation_root_main = Frame(master=root_examination, padx=3, pady=3, bg="#36566d")
    consultation_root_main.update_idletasks()
    create_consultation_root()

    def paste_frame_prescription():
        label_prescription = Label(master=frame_prescription_main,
                                   text="Рекомендации",
                                   font=('Comic Sans MS', user.get('text_size')), bg='white')
        label_prescription.grid(row=0, column=0, sticky='ew')

        txt_prescription.grid(column=0, row=1, sticky='nwse', columnspan=2)

        data['examination']['prescription_but'] = dict()
        for mark_ in all_data_diagnosis.get('prescription'):
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
        else:

            if data['examination']['prescription_frame'].get('open_frame'):
                data['examination']['prescription_frame'].get('open_frame').pack_forget()

            frame_loc = data['examination']['prescription_frame'].get(selected_prescription_frame.get())
            data['examination']['prescription_frame']['open_frame'] = frame_loc
            frame_loc.pack(fill='both', expand=True)
            data['examination']['prescription_frame']['last_open_frame'] = selected_prescription_frame.get()

    def select_prescription():
        prescription_text = txt_prescription.get(1.0, 'end').strip()
        prescription_button = selected_button.get()
        selected_button.set('')
        mark_1, mark_2 = prescription_button.split('_')


        edited_string = ''
        if mark_1 == 'Разрешена вакцинация':
            if 'Информирован(а)' in mark_2 and mark_2 in prescription_text:
                prescription_text = prescription_text.replace(mark_2, '')
            if 'Медотвод от проф' in mark_2 and mark_2 in prescription_text:
                prescription_text = prescription_text.replace(mark_2, '')

            else:
                if mark_2[-1] != '-':
                    mark_2 = f"{mark_2},"
                for string in prescription_text.split('\n'):
                    if string.startswith(mark_1):
                        edited_string = string
                        if edited_string[-1] in (',', '-'):
                            edited_string += ' '
                        edited_string += f"{mark_2} "
                        prescription_text = prescription_text.replace(string, edited_string)

                        break
                else:
                    prescription_text = f"{mark_1}: {mark_2} " \
                                        f"\nИнформирован(а) о проводимой прививке. " \
                                        f"\nС особенностями течения периода после иммунизации ОЗНАКОМЛЕН(А) _________" \
                                        f"\n{prescription_text}"




        elif data['examination']['prescription_but'].get(prescription_button):
            if data['examination']['prescription_but'][prescription_button].get():
                data['examination']['prescription_but'][prescription_button].set(0)

                for string in prescription_text.split('\n'):
                    if string.startswith(mark_1):
                        edited_string = string
                        if mark_2 in edited_string:
                            for i in (f"{mark_2}, ", f"{mark_2},", f", {mark_2}",
                                      f"{mark_2} ", f"{mark_2}"):
                                if i in edited_string:
                                    edited_string = edited_string.replace(i, '')
                                    prescription_text = prescription_text.replace(string, edited_string)

                            for btn in data['examination'].get('prescription_but'):
                                if btn.startswith(mark_1) and data['examination']['prescription_but'][btn].get():
                                    break
                            else:
                                prescription_text = prescription_text.replace(edited_string, '')

            else:
                data['examination']['prescription_but'][prescription_button].set(1)

                for string in prescription_text.split('\n'):
                    if string.startswith(mark_1):
                        edited_string = string
                        if edited_string[-1] == ',':
                            edited_string += ' '
                        edited_string += f"{mark_2}, "
                        prescription_text = prescription_text.replace(string, edited_string)

                        break
                else:
                    prescription_text = f"{mark_1}: {mark_2}, \n" + prescription_text

        for button_name in data['examination'].get('prescription_buttons_color'):
            if data['examination']['prescription_but'].get(button_name):
                if data['examination']['prescription_but'].get(button_name).get() == 1:
                    data['examination']['prescription_buttons_color'][button_name]['bg'] = '#77f1ff'
                else:
                    data['examination']['prescription_buttons_color'][button_name]['bg'] = '#cdcdcd'




        txt_prescription.delete(1.0, 'end')
        txt_prescription.insert(1.0, prescription_text.strip().replace('\n\n', '\n'))

        frame_prescription_main.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription_main.rowconfigure(index='all', minsize=20)

        frame_prescription.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription.rowconfigure(index='all', minsize=20)

    def select_drugs_item(drug_name=None, weight=None):
        if drug_name:
            drug_category, drug_name, mark_flag, mark = drug_name.split('__')
        else:
            drug_category, drug_name, mark_flag, mark = selected_button.get().split('__')
            selected_button.set('')


        if not data['examination'].get('selected_drugs'):
            data['examination']['selected_drugs'] = dict()

        if not data['examination']['selected_drugs'].get(drug_category):
            data['examination']['selected_drugs'][drug_category] = dict()
        if not data['examination']['selected_drugs'][drug_category].get(drug_name):
            data['examination']['selected_drugs'][drug_category][drug_name] = dict()

        if mark_flag == "Способ применения":
            if not data['examination']['selected_drugs'][drug_category][drug_name].get(mark_flag):
                data['examination']['selected_drugs'][drug_category][drug_name][mark_flag] = list()
            if mark in data['examination']['selected_drugs'][drug_category][drug_name].get(mark_flag):
                data['examination']['selected_drugs'][drug_category][drug_name][mark_flag].remove(mark)
            else:
                data['examination']['selected_drugs'][drug_category][drug_name][mark_flag].append(mark)

        else:
            data['examination']['selected_drugs'][drug_category][drug_name][mark_flag] = mark

        prescription_text = txt_prescription.get(1.0, 'end').strip()
        edited_string = ''

        if not weight:
            weight = data['examination']['anthro']['txt_weight_variable'].get()
            if child_marker:
                if weight:
                    weight = float(weight.replace(',', '.')) / 1000
                else:
                    weight = "None"

        if weight:
            if weight == "None":
                weight = None
            else:
                if isinstance(weight, str):
                    weight = float(weight.replace(',', '.'))
                if weight > 40:
                    weight = 40

        if drug_category == 'Антибиотики':
            if drug_name == "Амоксициллин":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 7:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 250/5'
                    elif age < 10:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 250 мг'
                    elif age < 15:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 500 мг'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 1000 мг'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '50 мг/кг/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '2 р/сут'

            elif drug_name == "Амоксициллин + клавулановая кислота":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 4:
                        data['examination']['selected_drugs'][drug_category][drug_name][
                            'Форма'] = 'суспензия 200/28.5/5'
                    elif age < 8:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 400/57/5'
                    elif age < 15:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 500/125 мг'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 875/125 мг'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '50 мг/кг/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '2 р/сут'

            elif drug_name == "Цефуроксим":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 7:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 125/5'
                    elif age < 14:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 125'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 250'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '20 мг/кг/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '2 р/сут'

            elif drug_name == "Кларитромицин":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 4:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 125/5'
                    elif age < 13:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 250/5'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 250'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '15 мг/кг/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '2 р/сут'

            elif drug_name == "Азитромицин":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 12:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 200/5'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 250'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '10 мг/кг/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '1 р/сут'

            elif drug_name == "Цефдинир":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 4:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 125/5'
                    elif age < 13:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 250/5'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 300'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '14 мг/кг/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '2 р/сут'

        elif drug_category == 'ОРИ':

            if drug_name == "Парацетамол":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'автоматически'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '15 мг/кг'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Способ применения'):
                    if mark_flag != 'Способ применения':

                        data['examination']['selected_drugs'][drug_category][drug_name]['Способ применения'] = \
                            ['принимать при температуре 38.5 и выше', 'с интервалом не меньше 6 часов']

            elif drug_name == "Ибупрофен":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'автоматически'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '10 мг/кг'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Способ применения'):
                    if mark_flag != 'Способ применения':
                        data['examination']['selected_drugs'][drug_category][drug_name]['Способ применения'] = \
                            ['принимать при температуре 38.5 и выше', 'с интервалом не меньше 8 часов']

            elif drug_name == "Оксиметазолин - капли в нос":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 1:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = '0.01%'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = '0.025%'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '2 р/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Длительность'):
                    data['examination']['selected_drugs'][drug_category][drug_name][
                        'Длительность'] = 'не дольше 5 дней'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Способ применения'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Способ применения'] = \
                        ['при заложенности носа']

            elif drug_name == "Ксилометазолин - капли в нос":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 13:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = '0.05%'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = '0.1%'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '3 р/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Длительность'):
                    data['examination']['selected_drugs'][drug_category][drug_name][
                        'Длительность'] = 'не дольше 5 дней'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Способ применения'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Способ применения'] = \
                        ['при заложенности носа']

            elif drug_name == "Феназон+Лидокаин (отисфен) - капли ушные":

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = 'по 1-2 капли'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '3 р/сут'

            elif drug_name == "Рифамицин (отофа) - капли ушные":

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = 'по 1-2 капли'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '3 р/сут'

        elif drug_category == 'Бронхолитики':

            if drug_name == "Монтелукаст":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 7:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 4мг'
                    elif age < 17:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 5мг'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 10мг'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '1 таб'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '1 р/сут на ночь'

        elif drug_category == 'Глазные капли':

            if drug_name == "Нитрофурал (фурацилин)":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = \
                        'раствор для наружного применения 0.02%'

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = \
                        'промывать глаза по мере загноения'

            elif drug_name in ("Тобрамицин - капли глазные 0.3%", "Дексаметазон+Тобрамицин - капли глазные",
                               "Дексаметазон - капли глазные 0.1%", "Диклофенак - капли глазные 0.1%"):

                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = 'по 1-2 капли'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '3 р/сут'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Длительность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Длительность'] = '5 дней'


        elif drug_category == 'Антигистаминные':

            if drug_name == "Цетиризин":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 7:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'кап. 10мг/мл-20мл'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 10мг'

                if not (data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка') and
                        data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность')):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '1 р/сут'
                    if data['examination']['selected_drugs'][drug_category][drug_name].get('Форма') == 'кап. 10мг/мл-20мл':
                        if age < 3:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '5 капель'
                        elif age < 12:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '10 капель'
                        else:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '20 капель'

                    if data['examination']['selected_drugs'][drug_category][drug_name].get('Форма') == 'таб. 10мг':
                        if age < 12:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '1/2 таб'
                        else:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '1 таб'


            elif drug_name == "Лоратадин":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 7:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 5мг/5мл'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 10мг'

                if not (data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка') and
                        data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность')):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '1 р/сут'
                    if data['examination']['selected_drugs'][drug_category][drug_name].get(
                            'Форма') == 'суспензия 5мг/5мл':
                        if age < 12:
                            data['examination']['selected_drugs'][drug_category][drug_name][
                                'Дозировка'] = '5 миллилитров'
                        else:
                            data['examination']['selected_drugs'][drug_category][drug_name][
                                'Дозировка'] = '10 миллилитров'

                    if data['examination']['selected_drugs'][drug_category][drug_name].get('Форма') == 'таб. 10мг':
                        if age < 12:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '1/2 таб'
                        else:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '1 таб'


            elif drug_name == "Дезлоратадин":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    if age < 12:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'суспензия 0.5мг/мл'
                    else:
                        data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = 'таб. 5мг'

                if not (data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка') and
                        data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность')):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '1 р/сут'
                    if data['examination']['selected_drugs'][drug_category][drug_name].get(
                            'Форма') == 'суспензия 0.5мг/мл':
                        if age < 6:
                            data['examination']['selected_drugs'][drug_category][drug_name][
                                'Дозировка'] = '2.5 миллилитра'
                        elif age < 12:
                            data['examination']['selected_drugs'][drug_category][drug_name][
                                'Дозировка'] = '5 миллилитров'
                        else:
                            data['examination']['selected_drugs'][drug_category][drug_name][
                                'Дозировка'] = '10 миллилитров'

                    if data['examination']['selected_drugs'][drug_category][drug_name].get('Форма') == 'таб. 5мг':
                        if age < 12:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '1/2 таб'
                        else:
                            data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '1 таб'

        elif drug_category == 'Льготные':
            if drug_name == "Холекальциферол":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = \
                        'масляный раствор для приема внутрь 0.5мг/мл 10мл'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = 'по 1 капле'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '1 р/сут'

            elif drug_name == "Бифидумбактерин":
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Форма'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Форма'] = \
                        'порошок для приг. раствора внутр. 5доз N10'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Дозировка'] = '5 доз (1 флакон)'
                if not data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность'):
                    data['examination']['selected_drugs'][drug_category][drug_name]['Кратность'] = '3 р/сут'




        all_but_names = list()
        for marker in data['examination']['selected_drugs'][drug_category].get(drug_name):
            if data['examination']['selected_drugs'][drug_category][drug_name].get(marker):
                if marker == "Способ применения":
                    for marker_2 in data['examination']['selected_drugs'][drug_category][drug_name].get(marker):
                        all_but_names.append(f"{drug_category}__{drug_name}__{marker}__{marker_2}")
                else:
                    marker_2 = data['examination']['selected_drugs'][drug_category][drug_name].get(marker)
                    all_but_names.append(f"{drug_category}__{drug_name}__{marker}__{marker_2}")

        for button_name in data['examination'].get('all_drug_buttons'):
            if button_name.startswith(f"{drug_category}__{drug_name}"):
                if button_name in all_but_names:
                    data['examination']['all_drug_buttons'][button_name]['bg'] = '#77f1ff'
                else:
                    data['examination']['all_drug_buttons'][button_name]['bg'] = '#cdcdcd'

        if drug_category == 'Антибиотики':
            ab_weight = []

            if weight and drug_name not in ('Фосфомицин', 'Фуразидин (Фурагин)'):

                ab_key_dosa = data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка')
                ab_key_form = data['examination']['selected_drugs'][drug_category][drug_name].get('Форма')
                ab_key_count = data['examination']['selected_drugs'][drug_category][drug_name].get('Кратность', '')

                edited_string = f"{drug_name}: {ab_key_form}  -- "

                ab_weight = ab_key_form.split('/')[0].split(' ')[-1].strip()

                ab_dosage = int(ab_key_dosa.split()[0])
                ab_dosage_day = weight * ab_dosage
                ab_volume_day = ab_dosage_day / int(ab_weight)

                ab_key_count_loc = None
                if ab_key_count:
                    if ab_key_count == '1-й день - 2 р/сут, далее - 1 р/сут':
                        ab_key_count_loc = 1
                    else:
                        ab_key_count_loc = int(ab_key_count.replace(' р/сут', ''))
                if not ab_key_count_loc:
                    ab_key_count_loc = 2
                    if drug_name == 'Азитромицин':
                        ab_key_count_loc = 1

                ab_volume_single = ab_volume_day / ab_key_count_loc
                if 'суспензия' in ab_key_form:
                    ab_volume_single = ab_volume_single * 5
                    edited_string += f" по {round(ab_volume_single, 1)} мл. "
                    if ab_key_count:
                        edited_string += f"{ab_key_count} "
                    else:
                        edited_string += f"{ab_key_count_loc} р/сут "
                    edited_string += f"({round(ab_dosage_day / weight)}мг/кг/сут)  "


                else:
                    if str(ab_volume_single).split('.')[-1][0] in ('4', '5', '6'):
                        ab_volume_single = float(f"{str(ab_volume_single).split('.')[0]}.5")
                    else:
                        ab_volume_single = round(ab_volume_single)
                    edited_string += f" по {round(ab_volume_single, 1)} таб. "

                    if ab_key_count:
                        edited_string += f"{ab_key_count} "
                    else:
                        edited_string += f"{ab_key_count_loc} р/сут "
                    edited_string += f"({round((ab_volume_single * ab_key_count_loc * int(ab_weight)) / weight)}" \
                                     f"мг/кг/сут) "

                edited_string += \
                    data['examination']['selected_drugs'][drug_category][drug_name].get('Длительность', '') + ' -- '
                for marker in data['examination']['selected_drugs'][drug_category][drug_name].get('Способ применения',
                                                                                                  []):
                    edited_string += marker + ', '


            else:
                edited_string = f"{drug_name}: "
                for marker in ("Форма", "Дозировка", "Кратность", "Длительность"):
                    if data['examination']['selected_drugs'][drug_category][drug_name].get(marker, ''):
                        edited_string += \
                            data['examination']['selected_drugs'][drug_category][drug_name].get(marker, '') + ' -- '
                for marker in data['examination']['selected_drugs'][drug_category][drug_name].get('Способ применения',
                                                                                                  []):
                    edited_string += marker + ', '

        elif drug_category == 'ОРИ':
            if drug_name in ('Парацетамол', 'Ибупрофен'):
                drug__form = data['examination']['selected_drugs'][drug_category][drug_name].get('Форма', "")
                drug__dosa = data['examination']['selected_drugs'][drug_category][drug_name].get('Дозировка', "")

                if weight:

                    if drug_name == 'Парацетамол' and drug__form:
                        text_paracetamol = f"{drug_name}: "
                        if drug__dosa:
                            drug__dosa = float(drug__dosa.replace(' мг/кг', ''))
                        else:
                            drug__dosa = 12.5
                        paracetamol_min, paracetamol_max = (weight * 10, weight * 15)

                        if drug__form == 'суппозитории' or (drug__form == 'автоматически' and age <= 5):

                            supp = []
                            for i in (50, 80, 100, 125, 150, 170, 250, 300, 330):
                                if paracetamol_min < i <= paracetamol_max:
                                    supp.append(i)
                            if supp:
                                supp_text = 'суппозитории '
                                for i in supp:
                                    supp_text += str(i) + 'мг., '
                                text_paracetamol += supp_text

                        if "суспензия" in drug__form or "раствор" in drug__form or (drug__form == 'автоматически' and age <= 12):
                            if drug__form == 'автоматически':
                                text_paracetamol += f'Раствор 30мг/мл -- ' \
                                                    f'по {round(weight * drug__dosa / 30, 1)} мл; '

                            else:
                                if '30' in drug__form:
                                    text_paracetamol += f'Раствор 30мг/мл -- ' \
                                                        f'по {round(weight * drug__dosa / 30, 1)} мл; '
                                else:
                                    text_paracetamol += f'Cуспензия 120 мг/5мл -- ' \
                                                        f'по {round(weight * drug__dosa / 24, 1)} мл; '

                        if "таб." in drug__form or age > 5 and drug__form == 'автоматически':
                            if '200' in drug__form or (drug__form == 'автоматически' and weight < 35):

                                if paracetamol_max < 100:
                                    text_paracetamol += ""
                                elif paracetamol_max < 200:
                                    text_paracetamol += "Таб. 200 мг -- по 1/2 таб; "
                                elif paracetamol_max < 300:
                                    text_paracetamol += "Таб. 200 мг -- по 1 таб; "
                                elif paracetamol_max < 400:
                                    text_paracetamol += "Таб. 200 мг -- по 1.5 таб; "
                                elif 400 <= paracetamol_max:
                                    text_paracetamol += "Таб. 200 мг -- по 2 таб; "

                            if '500' in drug__form or drug__form == 'автоматически':

                                if paracetamol_min < 250 <= paracetamol_max:
                                    text_paracetamol += "Таб. 500 мг -- по 1/2 т.; "
                                elif 500 <= paracetamol_max:
                                    text_paracetamol += "Таб. 500 мг -- по 1 т.; "
                        edited_string = text_paracetamol.strip() + ' '

                    elif drug_name == 'Ибупрофен':
                        if drug__dosa:
                            drug__dosa = float(drug__dosa.replace(' мг/кг', ''))
                        else:
                            drug__dosa = 7.5
                        text_ibuprofen = f"{drug_name}: "
                        ibuprofen_min, ibuprofen_max = (weight * 5, weight * 10)
                        if drug__form in ('автоматически', 'суппозитории'):
                            if ibuprofen_min < 60 <= ibuprofen_max:
                                text_ibuprofen += f'Супп. 60 мг.; '
                        if drug__form == 'суспензия 100 мг/5мл' or (drug__form == 'автоматически' and age < 3):
                            text_ibuprofen += f"суспензия 100мг/5мл -- по {round(drug__dosa * weight / 20, 1)}мл; "

                        if drug__form == 'суспензия 200 мг/5мл' or (drug__form == 'автоматически' and age >= 3):
                            text_ibuprofen += f"Cуспензия 200мг/5мл -- по {round(drug__dosa * weight / 40, 1)}мл; "

                        if drug__form == 'таб. 200 мг' or (drug__form == 'автоматически' and age > 5):
                            if ibuprofen_max < 100:
                                pass
                            elif ibuprofen_max < 200:
                                text_ibuprofen += "Таб. 200 мг -- по 1/2 таб; "
                            elif ibuprofen_max < 300:
                                text_ibuprofen += "Таб. 200 мг -- по 1 таб; "
                            elif ibuprofen_max < 400:
                                text_ibuprofen += "Таб. 200 мг -- по 1.5 таб; "
                            elif 400 <= ibuprofen_max:
                                text_ibuprofen += "Таб. 200 мг -- по 2 таб; "

                        if drug__form == 'таб. 400 мг':
                            if ibuprofen_max < 200:
                                pass
                            elif ibuprofen_max < 400:
                                text_ibuprofen += "Таб. 400 мг -- по 1/2 таб; "
                            elif 400 == ibuprofen_max:
                                text_ibuprofen += "Таб. 400 мг -- по 1 таб; "

                        edited_string = text_ibuprofen.strip() + ' '
                    edited_string += ' --  '
                    for marker in data['examination']['selected_drugs'][drug_category][drug_name].get(
                            'Способ применения', []):
                        edited_string += marker + ', '

                else:
                    edited_string = f"{drug_name}: "
                    if drug_name == 'Парацетамол' and drug__form == 'автоматически':
                        if age < 12:
                            edited_string += 'суспензия 30 мг/мл -- '
                        elif age < 15:
                            edited_string += 'таб. 200 мг -- '
                        else:
                            edited_string += 'таб. 500 мг -- '

                    elif drug_name == 'Ибупрофен' and drug__form == 'автоматически':
                        if age < 4:
                            edited_string += 'суспензия 100 мг/5мл -- '
                        elif age < 12:
                            edited_string += 'суспензия 200 мг/5мл -- '
                        else:
                            edited_string += 'таб. 200 мг -- '

                    else:
                        if drug__form:
                            edited_string += f'{drug__form} -- '

                    edited_string += f'{drug__dosa} -- '

                    for marker in data['examination']['selected_drugs'][drug_category][drug_name].get(
                            'Способ применения', []):
                        edited_string += marker + ', '

            else:
                edited_string = f"{drug_name}: "
                for marker in ("Форма", "Дозировка", "Кратность", "Длительность"):
                    if data['examination']['selected_drugs'][drug_category][drug_name].get(marker, ''):
                        edited_string += \
                            data['examination']['selected_drugs'][drug_category][drug_name].get(marker,
                                                                                                '') + ' -- '
                for marker in data['examination']['selected_drugs'][drug_category][drug_name].get(
                        'Способ применения', []):
                    edited_string += marker + ', '

        else:
            edited_string = f"{drug_name}: "
            for marker in ("Форма", "Дозировка", "Кратность", "Длительность"):
                if data['examination']['selected_drugs'][drug_category][drug_name].get(marker, ''):
                    edited_string += \
                        data['examination']['selected_drugs'][drug_category][drug_name].get(marker,
                                                                                            '') + ' -- '
            for marker in data['examination']['selected_drugs'][drug_category][drug_name].get(
                    'Способ применения', []):
                edited_string += marker + ', '

        edited_string = edited_string.strip()
        if edited_string[-1] == ',':
            edited_string = edited_string[:-1]
        elif edited_string[-1] == '-':
            edited_string = edited_string[:-2]

        deleted_string = ''
        for string in prescription_text.split('\n'):
            if string.startswith(drug_name):
                deleted_string = string
                break

        if deleted_string:
            prescription_text = prescription_text.replace(deleted_string, edited_string)
        else:
            prescription_text += f"\n{edited_string}"
        txt_prescription.delete(1.0, 'end')
        txt_prescription.insert(1.0, prescription_text.strip().replace('\n\n', '\n'))

    def open_drugs_root():
        if not data['examination'].get('is_drugs_root_open'):
            data['examination']['is_drugs_root_open'] = True
            drugs_root_main.grid()
        else:
            data['examination']['is_drugs_root_open'] = False
            drugs_root_main.grid_remove()

    def create_drugs_root():

        def create_recipe():
            drug_category, drug_name, marker_rp = selected_button.get().split('__')
            selected_button.set('')

            prescription_text = txt_prescription.get(1.0, 'end').strip().split('\n')
            edited_string = ''
            for string in prescription_text:
                if string.startswith(f"{drug_name}: "):
                    edited_string = string
            if not edited_string:
                messagebox.showerror("Ошибка!", "Перед созданием рецепта выберите препарат \n"
                                                "(форма/дозировка/способ применения)")
            elif (drug_category == 'ОРИ'
                  and drug_name in ('Парацетамол', 'Ибупрофен')
                  and data['examination']['selected_drugs'][drug_category][drug_name].get("Форма", '') == 'автоматически'):
                messagebox.showerror("Ошибка!", "Выберите определенную форму лекарства")

            else:

                d_t_d_n = '1 (одна упаковка)'
                drug_name_short = edited_string.split('--')[0].strip()


                if data['examination']['selected_drugs'][drug_category][drug_name].get("Форма", ''):
                    form = data['examination']['selected_drugs'][drug_category][drug_name].get("Форма", '')
                    if recipe_data.get(drug_category, dict()).get(drug_name, dict()).get(form):
                        d_t_d_n = recipe_data[drug_category][drug_name].get(form)

                signatura = edited_string.replace(drug_name_short, '').replace('--', '-').replace('  ', ' ')
                signatura = signatura.replace('выписан рецепт', '').replace('выписан льготный рецепт', '').strip()
                if signatura.startswith('-'):
                    signatura = signatura[1:]
                signatura = signatura.replace(' ,', '').strip()
                if 'суппозитории' in edited_string:
                    signatura = f"Ректально {signatura}"
                elif (drug_category != 'Бронхолитики'
                        and drug_category != 'Глазные капли'
                        and 'капли' not in drug_name
                        and 'спрей' not in drug_name
                        and 'Внутримышечно' not in signatura
                        and 'ингалляц' not in signatura):
                    signatura = f"Принимать внутрь {signatura}"

                render_data.clear()

                render_data['date'] = datetime.now().strftime("%d.%m.%Y")
                patient_name = ''
                for i in patient.get('name').strip().split():
                    if not patient_name:
                        patient_name += f"{i} "
                    else:
                        patient_name += f"{i[0]}."
                render_data['name_short'] = patient_name
                render_data['birth_date'] = patient.get('birth_date')
                render_data['doc_name'] = user.get('doctor_name')
                render_data['rp'] = f"{drug_name_short}\nD.t.d.n {d_t_d_n}\nS.: {signatura}"
                render_data['address'] = patient.get('address')
                render_data['drug_name'] = drug_name_short

                render_data['age'] = patient['age'].get('age_txt')

                doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}рецепт_{marker_rp}.docx")
                doc.render(render_data)
                doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]}_рецепт.docx"
                doc_name = save_document(doc=doc, doc_name=doc_name)
                run_document(doc_name)

                render_data.clear()
                data_base(command="statistic_write",
                          insert_data="Рецепт")

        def select_drugs_category():
            for drug_category in data['examination'].get("all_drug_frame"):
                if '__' not in drug_category:
                    data['examination']['all_drug_frame'][drug_category].pack_forget()
            all_drug_frame = data['examination']['all_drug_frame'].get(selected_button.get())
            all_drug_frame.pack(fill='both', expand=True)
            all_drug_frame.update_idletasks()
            data['examination']['canvas_frame_scrolled'].yview_moveto(0)

        def select_drugs_name():
            if data['examination']['all_drug_frame'].get(selected_button.get()):
                edit_frame, marker = data['examination']['all_drug_frame'].get(selected_button.get())
                if marker:
                    edit_frame.pack_forget()
                    data['examination']['all_drug_frame'][selected_button.get()][1] = False
                    edit_frame = data['examination']['all_drug_frame'][selected_button.get().split("__")[0]]
                    edit_frame.columnconfigure(index='all', minsize=40, weight=1)
                    edit_frame.rowconfigure(index='all', minsize=20)
                    for drug_category in data['examination'].get("all_drug_frame"):
                        if '__' not in drug_category:
                            data['examination']['all_drug_frame'][drug_category].rowconfigure(index='all', minsize=20)
                        else:
                            data['examination']['all_drug_frame'][drug_category][0].rowconfigure(index='all',
                                                                                                 minsize=20)



                else:
                    data['examination']['all_drug_frame'][selected_button.get()][1] = True
                    edit_frame.columnconfigure(index='all', minsize=40, weight=1)
                    edit_frame.rowconfigure(index='all', minsize=20)

                    edit_frame.pack(fill='both', expand=True)

        def create_scroller_frame(master_frame, func):
            def resize(event):
                region = canvas.bbox(tk.ALL)
                canvas.configure(scrollregion=region)

            def on_binds(event):
                canvas.idbind = canvas.bind_all("<MouseWheel>", on_mousewheel)

            def off_binds(event=None):
                canvas.unbind_all("<MouseWheel>")

            def on_mousewheel(event):

                region = canvas.bbox(tk.ALL)
                canvas.configure(scrollregion=region)

                if os.name == 'posix':
                    canvas.yview_scroll(int(-1 * event.delta), "units")
                else:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            scroll_x = tk.Scrollbar(master_frame, orient=tk.HORIZONTAL)
            scroll_y = tk.Scrollbar(master_frame, orient=tk.VERTICAL)

            canvas = tk.Canvas(master_frame,
                               xscrollcommand=scroll_x.set,
                               yscrollcommand=scroll_y.set)
            scroll_x.config(command=canvas.xview)
            scroll_y.config(command=canvas.yview)

            canvas_frame = Frame(canvas)

            data['examination']['canvas_frame_scrolled'] = canvas

            func(canvas_frame)
            #
            # canvas['width'] = int(canvas.winfo_geometry().split('x')[0])
            # canvas_frame['width'] = int(canvas.winfo_geometry().split('x')[0])

            canvas.grid(row=0, column=0, sticky="nsew")
            scroll_x.grid(row=1, column=0, sticky="we")
            scroll_y.grid(row=0, column=1, sticky="ns")

            master_frame.rowconfigure(0, weight=1)
            master_frame.columnconfigure(0, weight=1)

            master_frame.bind("<Configure>", resize)
            master_frame.update_idletasks()

            canvas.bind("<Enter>", on_binds)
            canvas.bind("<Leave>", off_binds)

            canvas.create_window((0, 0), window=canvas_frame, anchor="nw",
                                 width=canvas.winfo_width())

        def create_drugs_frame(frame):

            for drug_category in all_data_diagnosis.get("drugs"):
                all_drug_frame = Frame(frame, bg="#36566d")

                for drugs in all_data_diagnosis["drugs"].get(drug_category):
                    drug_name = drugs[0]
                    drug_frame = Frame(all_drug_frame)
                    drug_name_btn_text = drug_name
                    if drug_name == 'Амоксициллин + клавулановая кислота':
                        drug_name_btn_text = 'Амоксициллин\n+ клавулановая кислота'
                    elif drug_name == 'Бромгексин+Гвайфенезин+Сальбутамол+Ментол (Джосет)':
                        drug_name_btn_text = 'Бромгексин + Гвайфенезин \n+ Сальбутамол + Ментол \n(Джосет)'
                    elif '- капли' in drug_name_btn_text:
                        drug_name_btn_text = drug_name_btn_text.replace('- капли', '\n- капли')
                    elif '- мазь' in drug_name_btn_text:
                        drug_name_btn_text = drug_name_btn_text.replace('- мазь', '\n- мазь')


                    elif drug_name == 'Бромгексин+Гвайфенезин+Сальбутамол+Ментол (Джосет)':
                        drug_name_btn_text = 'Бромгексин + Гвайфенезин \n+ Сальбутамол + Ментол \n(Джосет)'

                    elif '(' in drug_name_btn_text:
                        drug_name_btn_text = drug_name_btn_text.replace('(', '\n(')

                    btn = Radiobutton(drug_frame, text=f'{drug_name_btn_text}',
                                      font=('Comic Sans MS', user.get('text_size')),
                                      value=f"{drug_category}__{drug_name}", variable=selected_button,
                                      command=select_drugs_name,
                                      indicatoron=False, selectcolor='#77f1ff')
                    btn.pack(fill='both', expand=True)

                    drug_frame_add = Frame(drug_frame)
                    mark_flag = ''
                    for mark in drugs[1:]:
                        if mark in ("Форма", "Дозировка", "Кратность", "Длительность", "Способ применения"):
                            mark_flag = mark
                            Label(drug_frame_add, text=f"{mark}",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  bg="#36566d", fg='white').pack(fill='both', expand=True)
                        elif mark.startswith('Инструкция'):
                            Label(drug_frame_add, text=f"{mark}",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  bg="#36566d", fg='white').pack(fill='both', expand=True, pady=2)


                        else:
                            btn_text = ''
                            for i in mark.split():
                                if len(btn_text.split('\n')[-1]) > 30:
                                    btn_text += '\n'
                                btn_text += f"{i} "
                            btn = Radiobutton(drug_frame_add, text=f'{btn_text}',
                                              font=('Comic Sans MS', user.get('text_size')),
                                              value=f"{drug_category}__{drug_name}__{mark_flag}__{mark}",
                                              variable=selected_button,
                                              command=select_drugs_item,
                                              indicatoron=False, selectcolor='#77f1ff',
                                              bg='#cdcdcd')
                            btn.pack(fill='both', expand=True)
                            data['examination']['all_drug_buttons'][f"{drug_category}__{drug_name}__{mark_flag}__" \
                                                                    f"{mark}"] = btn

                    Label(drug_frame_add, text="Рецепты:",
                          font=('Comic Sans MS', user.get('text_size')),
                          bg="#36566d", fg='white').pack(fill='both', expand=True)

                    Radiobutton(drug_frame_add, text=f'Выписать простой рецепт',
                                font=('Comic Sans MS', user.get('text_size')),
                                value=f"{drug_category}__{drug_name}__простой_а6",
                                variable=selected_button,
                                command=create_recipe,
                                indicatoron=False, selectcolor='#77f1ff',
                                bg='#cdcdcd').pack(fill='both', expand=True)

                    Radiobutton(drug_frame_add, text=f'Выписать льготный рецепт',
                                font=('Comic Sans MS', user.get('text_size')),
                                value=f"{drug_category}__{drug_name}__льготный_а6",
                                variable=selected_button,
                                command=create_recipe,
                                indicatoron=False, selectcolor='#77f1ff',
                                bg='#cdcdcd').pack(fill='both', expand=True)

                    data['examination']['all_drug_frame'][f"{drug_category}__{drug_name}"] = [drug_frame_add, False]

                    drug_frame_add.columnconfigure(index='all', minsize=40, weight=1)
                    drug_frame_add.rowconfigure(index='all', minsize=20)

                    drug_frame.columnconfigure(index='all', minsize=40, weight=1)
                    drug_frame.rowconfigure(index='all', minsize=20)

                    drug_frame.pack(fill='both', expand=True, pady=5)

                data['examination']['all_drug_frame'][drug_category] = all_drug_frame

                # if len(drugs[0]) > min_width:
                #     min_width = len(drugs[0])

                # all_drug_frame.pack(fill='both', expand=True)
            drug_category_frame.columnconfigure(index='all', minsize=40, weight=1)
            drug_category_frame.rowconfigure(index='all', minsize=20)

            drugs_root_main.columnconfigure(index='all', minsize=40, weight=1)
            drugs_root_main.rowconfigure(index='all', minsize=20)

        data['examination']['all_drug_frame'] = dict()

        drug_category_frame = Frame(drugs_root_main, bg="#36566d")
        all_drugs_frame_scrolled = Frame(drugs_root_main, bg="#36566d")

        Label(drug_category_frame, text="        Перечень лекарственных препаратов        ",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3)
        Button(drug_category_frame, text=f"Закрыть окно препаратов",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_drugs_root,
               bg='#f0fffe').pack(fill='both', expand=True)

        drugs_list = [[]]
        for drug_category in all_data_diagnosis.get("drugs"):
            if len(drugs_list[-1]) == 3:
                drugs_list.append([])
            drugs_list[-1].append(drug_category)

        for drug_category_list in drugs_list:
            frame = Frame(drug_category_frame)
            for drug_category in drug_category_list:
                Radiobutton(frame, text=f'{drug_category}',
                            font=('Comic Sans MS', user.get('text_size')),
                            value=drug_category, variable=selected_button,
                            command=select_drugs_category,
                            indicatoron=False, selectcolor='#77f1ff',
                            bg="#36566d", fg='white').pack(fill='x', expand=True, side='left', ipady=4, ipadx=8)
            frame.pack(fill='x', expand=True)



        # for drug_category in all_data_diagnosis.get("drugs"):
        #     btn = Radiobutton(drug_category_frame, text=f'{drug_category}',
        #                       font=('Comic Sans MS', user.get('text_size')),
        #                       value=drug_category, variable=selected_button,
        #                       command=select_drugs_category,
        #                       indicatoron=False, selectcolor='#77f1ff',
        #                       bg="#36566d", fg='white')
        #
        #     btn.pack(fill='x', expand=True)

        drug_category_frame.pack(fill='x', anchor='nw')
        all_drugs_frame_scrolled.pack(fill='both', expand=True)
        data['examination']['is_drugs_root_open'] = False
        data['examination']['all_drug_buttons'] = dict()



        drugs_root_main.grid(row=0, column=3, sticky="nwse", rowspan=3)
        create_scroller_frame(master_frame=all_drugs_frame_scrolled, func=create_drugs_frame)

        drugs_root_main.grid_remove()

    drugs_root_main = Frame(master=root_examination, padx=3, pady=3)
    drugs_root_main.update_idletasks()
    create_drugs_root()


    def open_dispanser_root():
        if not data['examination'].get('is_dispanser_root_open'):
            data['examination']['is_dispanser_root_open'] = True
            dispanser_root_main.grid()
        else:
            data['examination']['is_dispanser_root_open'] = False
            dispanser_root_main.grid_remove()

    def create_dispanser_root():
        def celect_dispanser():
            txt_prescription.insert('end', f"\nОбсленование и наблюдение согласно постановлению МЗ РБ № 1201:"
                                           f"\n{celected_code.get()}")
            open_dispanser_root()

        def search_mkb(event=None):
            def resize(event=None):
                region = canvas.bbox(tk.ALL)
                canvas.configure(scrollregion=region)

            def on_binds(event):
                canvas.idbind = canvas.bind_all("<MouseWheel>", on_mousewheel)

            def off_binds(event=None):
                canvas.unbind_all("<MouseWheel>")

            def on_mousewheel(event):

                region = canvas.bbox(tk.ALL)
                canvas.configure(scrollregion=region)

                if os.name == 'posix':
                    canvas.yview_scroll(int(-1 * event.delta), "units")
                else:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            if data['examination'].get('frame_found_data_dispanser'):
                frame_found_data_dispanser = data['examination'].get('frame_found_data_dispanser')
                frame_found_data_dispanser.destroy()
            master_frame = Frame(mkb_frame_scrolled)
            data['examination']['frame_found_data_dispanser'] = master_frame
            master_frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

            found_data = list()
            mkb_code_edit = ''
            mkb_name_edit = mkb_name.get()

            if mkb_code.get():
                word_list = ["qwertyuiopasdfghjkl;'zxcvbnm,.", "йцукенгшщзфывапролджэячсмитьбю"]

                for word in mkb_code.get().lower():
                    if word in word_list[1]:
                        mkb_code_edit += word_list[0][word_list[1].index(word)]
                    elif word == ',':
                        mkb_code_edit += '.'
                    else:
                        mkb_code_edit += word
                mkb_code_edit = mkb_code_edit.upper()

            if mkb_code_edit and mkb_name_edit:
                for dispanser_data in post_1201:
                    key = dispanser_data.get('mkb_key')
                    value = dispanser_data.get('Наименование заболевания')

                    if mkb_code_edit in key and mkb_name_edit.lower() in value.lower():
                        found_data.append(dispanser_data)
            elif mkb_code_edit:
                for dispanser_data in post_1201:
                    key = dispanser_data.get('mkb_key')
                    if mkb_code_edit in key:
                        found_data.append(dispanser_data)
            elif mkb_name_edit:
                for dispanser_data in post_1201:
                    value = dispanser_data.get('Наименование заболевания')
                    if mkb_name_edit.lower() in value.lower():
                        found_data.append(dispanser_data)

            if found_data:

                scroll_x = tk.Scrollbar(master_frame, orient=tk.HORIZONTAL)
                scroll_y = tk.Scrollbar(master_frame, orient=tk.VERTICAL)

                canvas = tk.Canvas(master_frame,
                                   xscrollcommand=scroll_x.set,
                                   yscrollcommand=scroll_y.set)
                scroll_x.config(command=canvas.xview)
                scroll_y.config(command=canvas.yview)

                canvas_frame = Frame(canvas)

                for dispanser_data in found_data:
                    dispanser_data = f"Наименование заболевания: " \
                                     f"{dispanser_data.get('Наименование заболевания')}\n" \
                                     f"Сроки и кратность медицинских обследований: " \
                                     f"{dispanser_data.get('Сроки и кратность медицинских обследований')}\n" \
                                     f"Сроки наблюдения за пациентом: " \
                                     f"{dispanser_data.get('Сроки наблюдения за пациентом')}"

                    but_text = ''
                    for i in dispanser_data.split(" "):
                        if len(but_text.split('\n')[-1]) > 60:
                            but_text += '\n'
                        but_text += i + ' '
                    Radiobutton(canvas_frame, text=but_text,
                                font=('Comic Sans MS', user.get('text_size')),
                                value=f"{dispanser_data}",
                                variable=celected_code,
                                command=celect_dispanser,
                                indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff'
                                ).pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

                # canvas_frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

                canvas['width'] = int(canvas.winfo_geometry().split('x')[0])
                canvas_frame['width'] = int(canvas.winfo_geometry().split('x')[0])
                canvas.grid(row=0, column=0, sticky="nsew")
                scroll_x.grid(row=1, column=0, sticky="we")
                scroll_y.grid(row=0, column=1, sticky="ns")

                master_frame.rowconfigure(0, weight=1)
                master_frame.columnconfigure(0, weight=1)

                master_frame.bind("<Configure>", resize)
                master_frame.update_idletasks()
                canvas_frame['height'] = int(dispanser_root_main.winfo_height() - frame_main_dispanser.winfo_height())

                canvas.bind("<Enter>", on_binds)
                canvas.bind("<Leave>", off_binds)

                canvas.create_window((0, 0), window=canvas_frame, anchor="nw",
                                     width=canvas.winfo_width())

            else:
                Label(master_frame, text="Поиск не дал результатов!",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')

        mkb_code = StringVar()
        mkb_name = StringVar()
        celected_code = StringVar()

        frame_main_dispanser = Frame(dispanser_root_main, bg="#36566d")
        Label(frame_main_dispanser, text="Поиск по постановлению 1201",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')
        Button(frame_main_dispanser, text=f"Закрыть окно",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_dispanser_root,
               bg='#f0fffe').pack(fill='x', expand=True, pady=3, padx=3, anchor='n')

        mkb_title_frame = Frame(frame_main_dispanser, bg="#36566d")
        Label(mkb_title_frame, text="Код (МКБ-10): ",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, side='left')
        txt_mkb = Entry(mkb_title_frame, width=10,
                        font=('Comic Sans MS', user.get('text_size')),
                        justify="center",
                        textvariable=mkb_code)
        txt_mkb.pack(fill='x', expand=True, pady=3, padx=3, side='left')
        txt_mkb.bind('<Return>', search_mkb)

        Label(mkb_title_frame, text="Нозология: ",
              font=('Comic Sans MS', user.get('text_size')),
              bg="#36566d", fg='white').pack(fill='x', expand=True, pady=3, padx=3, side='left')
        txt_mkb = Entry(mkb_title_frame, width=30,
                        font=('Comic Sans MS', user.get('text_size')),
                        textvariable=mkb_name)
        txt_mkb.pack(fill='x', expand=True, pady=3, padx=3, side='left')
        txt_mkb.bind('<Return>', search_mkb)

        mkb_title_frame.pack(fill='x', anchor='n')
        frame_main_dispanser.pack(fill='x', anchor='n')

        mkb_frame_scrolled = Frame(dispanser_root_main)
        mkb_frame_scrolled.pack(fill='both', expand=True)

        data['examination']['is_dispanser_root_open'] = False
        dispanser_root_main.grid(row=0, column=3, sticky="nwse", rowspan=3)

        dispanser_root_main.grid_remove()

    dispanser_root_main = Frame(master=root_examination, padx=3, pady=3, bg="#36566d")
    dispanser_root_main.update_idletasks()
    create_dispanser_root()

    def paste_prescription_kb():

        data['examination']['open_prescription_kb'] = 'open'
        data['examination']['prescription_frame'] = dict()
        data['examination']['prescription_buttons_color'] = dict()

        data['examination']['prescription_but_ab_value'] = dict()

        for mark_group_main in all_data_diagnosis.get('prescription'):
            frame_loc = Frame(frame_prescription_buttons, borderwidth=1)
            Radiobutton(frame_loc, text=f"{mark_group_main[0]}",
                        font=('Comic Sans MS', user.get('text_size')),
                        value=f"{mark_group_main[0]}",
                        variable=selected_prescription_frame,
                        command=select_prescription_frame,
                        indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff'
                        ).pack(fill='both', expand=True)
            row, col = 0, 0
            frame_loc_but = Frame(frame_loc, borderwidth=1)
            data['examination']['prescription_frame'][mark_group_main[0]] = frame_loc_but
            for mark_group in mark_group_main[1:]:
                frame = Frame(frame_loc_but)
                for mark_2 in mark_group:
                    mark_2_text = ""
                    for i in mark_2.split(' '):
                        if len(mark_2_text.split('\n')[-1]) > 30:
                            mark_2_text += '\n'
                        mark_2_text += f"{i} "
                    data['examination']['prescription_but'][f"{mark_group_main[0]}_{mark_2}"] = IntVar()
                    btn = Radiobutton(frame, text=mark_2_text,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      value=f"{mark_group_main[0]}_{mark_2}",
                                      variable=selected_button,
                                      command=select_prescription,
                                      indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
                    btn.pack(fill='both', expand=True, side='left')
                    data['examination']['prescription_buttons_color'][f"{mark_group_main[0]}_{mark_2}"] = btn
                frame.pack(fill='both', expand=True)

            # if mark[0] == 'Разрешена вакцинация':
            #     loc_vac_data_main = list()
            #     loc_vac_data = list()
            #     for mark_2 in mark[1:]:
            #         if mark_2 == '\n':
            #             loc_vac_data_main.append(loc_vac_data.copy())
            #             loc_vac_data.clear()
            #         else:
            #             loc_vac_data.append(mark_2)
            #     for mark_group in loc_vac_data_main:
            #         loc_vac_frame = Frame(frame_loc_but)
            #         for mark_2 in mark_group:
            #             btn = Radiobutton(loc_vac_frame, text=f"{mark_2}",
            #                               font=('Comic Sans MS', user.get('text_size')),
            #                               value=f"{mark[0]}_{mark_2}",
            #                               variable=selected_button,
            #                               command=select_prescription,
            #                               indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
            #
            #             btn.pack(fill='both', expand=True, side='left')
            #             data['examination']['prescription_buttons_color'][f"{mark[0]}_{mark_2}"] = btn
            #         loc_vac_frame.pack(fill='both', expand=True)
            # else:
            #     for mark_2 in mark[1:]:
            #         btn = Radiobutton(frame_loc_but, text=f"{mark_2}",
            #                           font=('Comic Sans MS', user.get('text_size')),
            #                           value=f"{mark[0]}_{mark_2}",
            #                           variable=selected_button,
            #                           command=select_prescription,
            #                           indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
            #
            #         btn.grid(row=row, column=col, sticky='ew')
            #         data['examination']['prescription_buttons_color'][f"{mark[0]}_{mark_2}"] = btn
            #
            #         col += 1
            #         if col == 6:
            #             col = 0
            #             row += 1

            frame_loc_but.columnconfigure(index='all', minsize=40, weight=1)
            frame_loc_but.rowconfigure(index='all', minsize=20)

            frame_loc.columnconfigure(index='all', minsize=40, weight=1)
            frame_loc.rowconfigure(index='all', minsize=20)
            frame_loc.pack(fill='both', expand=True)

        Button(frame_prescription_buttons, text=f"Анализы",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_analyzes_root,
               bg='#f0fffe').pack(fill='both', expand=True)

        Button(frame_prescription_buttons, text=f"Консультация",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_consultation_root,
               bg='#f0fffe').pack(fill='both', expand=True)

        Button(frame_prescription_buttons, text=f"Препараты",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_drugs_root,
               bg='#f0fffe').pack(fill='both', expand=True)

        Button(frame_prescription_buttons, text=f"Диспансеризация \n(пост. 1201)",
               font=('Comic Sans MS', user.get('text_size')),
               command=open_dispanser_root,
               bg='#f0fffe').pack(fill='both', expand=True)

        Button(frame_prescription_buttons, text=f"Справка",
               font=('Comic Sans MS', user.get('text_size')),
               command=fast_certificate,
               bg='#f0fffe').pack(fill='both', expand=True)

        # data['examination']['prescription_frame']['Препараты'] = frame_prescription_buttons_drugs_buttons

        frame_prescription_buttons.columnconfigure(index='all', minsize=40, weight=1)
        frame_prescription_buttons.rowconfigure(index='all', minsize=20)
        frame_prescription_buttons.pack(fill='both', expand=True, padx=2, pady=2)

        # frame_prescription_buttons_drugs_main.columnconfigure(index='all', minsize=40, weight=1)
        # frame_prescription_buttons_drugs_main.rowconfigure(index='all', minsize=20)
        # frame_prescription_buttons_drugs_main.pack(fill='both', expand=True, padx=2, pady=2)

    # def paste_prescription_kb():
    #
    #     data['examination']['open_prescription_kb'] = 'open'
    #     data['examination']['prescription_frame'] = dict()
    #     data['examination']['prescription_buttons_color'] = dict()
    #
    #     data['examination']['prescription_but_ab_value'] = dict()
    #
    #     for mark in all_data_diagnosis.get('prescription'):
    #         frame_loc = Frame(frame_prescription_buttons, borderwidth=1)
    #         btn = Radiobutton(frame_loc, text=f"{mark[0]}",
    #                           font=('Comic Sans MS', user.get('text_size')),
    #                           value=f"{mark[0]}", variable=selected_prescription_frame,
    #                           command=select_prescription_frame,
    #                           indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
    #         btn.pack(fill='both', expand=True)
    #         row, col = 0, 0
    #         frame_loc_but = Frame(frame_loc, borderwidth=1)
    #         data['examination']['prescription_frame'][mark[0]] = frame_loc_but
    #         if mark[0] == 'Разрешена вакцинация':
    #             loc_vac_data_main = list()
    #             loc_vac_data = list()
    #             for mark_2 in mark[1:]:
    #                 if mark_2 == '\n':
    #                     loc_vac_data_main.append(loc_vac_data.copy())
    #                     loc_vac_data.clear()
    #                 else:
    #                     loc_vac_data.append(mark_2)
    #             for mark_group in loc_vac_data_main:
    #                 loc_vac_frame = Frame(frame_loc_but)
    #                 for mark_2 in mark_group:
    #                     btn = Radiobutton(loc_vac_frame, text=f"{mark_2}",
    #                                       font=('Comic Sans MS', user.get('text_size')),
    #                                       value=f"{mark[0]}_{mark_2}",
    #                                       variable=selected_button,
    #                                       command=select_prescription,
    #                                       indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
    #
    #                     btn.pack(fill='both', expand=True, side='left')
    #                     data['examination']['prescription_buttons_color'][f"{mark[0]}_{mark_2}"] = btn
    #                 loc_vac_frame.pack(fill='both', expand=True)
    #         else:
    #             for mark_2 in mark[1:]:
    #                 btn = Radiobutton(frame_loc_but, text=f"{mark_2}",
    #                                   font=('Comic Sans MS', user.get('text_size')),
    #                                   value=f"{mark[0]}_{mark_2}",
    #                                   variable=selected_button,
    #                                   command=select_prescription,
    #                                   indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff')
    #
    #                 btn.grid(row=row, column=col, sticky='ew')
    #                 data['examination']['prescription_buttons_color'][f"{mark[0]}_{mark_2}"] = btn
    #
    #                 col += 1
    #                 if col == 6:
    #                     col = 0
    #                     row += 1
    #
    #         frame_loc_but.columnconfigure(index='all', minsize=40, weight=1)
    #         frame_loc_but.rowconfigure(index='all', minsize=20)
    #
    #         frame_loc.columnconfigure(index='all', minsize=40, weight=1)
    #         frame_loc.rowconfigure(index='all', minsize=20)
    #         frame_loc.pack(fill='both', expand=True)
    #
    #     Button(frame_prescription_buttons, text=f"Анализы",
    #            font=('Comic Sans MS', user.get('text_size')),
    #            command=open_analyzes_root,
    #            bg='#f0fffe').pack(fill='both', expand=True)
    #
    #     Button(frame_prescription_buttons, text=f"Консультация",
    #            font=('Comic Sans MS', user.get('text_size')),
    #            command=open_consultation_root,
    #            bg='#f0fffe').pack(fill='both', expand=True)
    #
    #
    #     Button(frame_prescription_buttons, text=f"Препараты",
    #            font=('Comic Sans MS', user.get('text_size')),
    #            command=open_drugs_root,
    #            bg='#f0fffe').pack(fill='both', expand=True)
    #
    #     Button(frame_prescription_buttons, text=f"Диспансеризация \n(пост. 1201)",
    #            font=('Comic Sans MS', user.get('text_size')),
    #            command=open_dispanser_root,
    #            bg='#f0fffe').pack(fill='both', expand=True)
    #
    #     Button(frame_prescription_buttons, text=f"Справка",
    #            font=('Comic Sans MS', user.get('text_size')),
    #            command=fast_certificate,
    #            bg='#f0fffe').pack(fill='both', expand=True)
    #
    #
    #
    #     # data['examination']['prescription_frame']['Препараты'] = frame_prescription_buttons_drugs_buttons
    #
    #     frame_prescription_buttons.columnconfigure(index='all', minsize=40, weight=1)
    #     frame_prescription_buttons.rowconfigure(index='all', minsize=20)
    #     frame_prescription_buttons.pack(fill='both', expand=True, padx=2, pady=2)
    #
    #     # frame_prescription_buttons_drugs_main.columnconfigure(index='all', minsize=40, weight=1)
    #     # frame_prescription_buttons_drugs_main.rowconfigure(index='all', minsize=20)
    #     # frame_prescription_buttons_drugs_main.pack(fill='both', expand=True, padx=2, pady=2)

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
    # frame_prescription_buttons_drugs_main = Frame(frame_prescription_buttons, padx=1, pady=1)
    # frame_prescription_buttons_drugs_buttons = Frame(frame_prescription_buttons_drugs_main, padx=1, pady=1)

    txt_prescription = ScrolledText(frame_prescription_main, width=15, height=16,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    wrap="word")
    change_prescription_kb_button = Button(frame_prescription_main, text='скрыть клавиатуру рекомендаций',
                                           command=change_prescription_kb_status,
                                           font=('Comic Sans MS', user.get('text_size')))

    paste_frame_prescription()

    def write_ln():
        data['examination']['LN_data']['type_doc'] = selected_button.get()

        def save():
            def check_input():
                error_flag = False

                for marker in data['examination']['LN_data'].get('current_data'):
                    if marker in ("Фамилия", "Имя", "Дата рождения", "Адрес места жительства",
                                  'Место работы (службы, учебы)') and not data['examination']['LN_data']['current_data'].get(marker).get():
                        messagebox.showerror('Ошибка', f"Ошибка!\nНе указан пункт\n'{marker}'")
                        return False
                    elif marker == "Дата рождения":
                        try:
                            if get_age(data['examination']['LN_data']['current_data'].get(marker).get()) < 0:
                                messagebox.showerror('Ошибка', f"Дата рождения не может быть больше текущей даты!")
                                return False
                        except Exception:
                            messagebox.showerror('Ошибка', f"Дата рождения должна быть в формате 'ДД.ММ.ГГ'")
                            return False
                    elif marker in ("Дата выдачи", "Дата начала ВН", "Дата окончания ВН"):
                        try:
                            get_age(data['examination']['LN_data']['current_data'].get(marker).get())
                        except Exception:
                            messagebox.showerror('Ошибка', f"{marker} должна быть в формате 'ДД.ММ.ГГ'")
                            return False

                return True


            if check_input():
                render_data.clear()
                txt_ln_from.delete(0, 'end')
                txt_ln_from.insert(0, data['examination']['LN_data']['current_data'].get("Дата начала ВН").get().strip())

                txt_ln_until.delete(0, 'end')
                txt_ln_until.insert(0, data['examination']['LN_data']['current_data'].get("Дата окончания ВН").get().strip())

                txt_second_examination.delete(0, 'end')
                txt_second_examination.insert(0, data['examination']['LN_data']['current_data'].get("Дата окончания ВН").get().strip())


                data['examination']['LN_data']['current_data']['save'] = True
                render_data['patient_info_1'] = \
                    data['examination']['LN_data']['current_data'].get('Информация про ребенка (в корешок)').get().strip()
                render_data['patient_info_2'] = \
                    data['examination']['LN_data']['current_data'].get('Особые отметки').get().strip()
                render_data['parent_name_full'] = \
                    f"{data['examination']['LN_data']['current_data'].get('Фамилия').get().strip()} " \
                    f"{data['examination']['LN_data']['current_data'].get('Имя').get().strip()} " \
                    f"{data['examination']['LN_data']['current_data'].get('Отчество').get().strip()}"
                render_data['address'] = \
                    data['examination']['LN_data']['current_data'].get('Адрес места жительства').get().strip()
                render_data['work'] = \
                    data['examination']['LN_data']['current_data'].get('Место работы (службы, учебы)').get().strip()
                render_data['doctor_name'] = \
                    user.get('doctor_name').split()[0]

                for marker_1, marker_2 in (('d_open', 'Дата выдачи'), ('d_from', 'Дата начала ВН'),
                                           ('d_until', 'Дата окончания ВН'),
                                           ('b_d_1', 'Дата рождения'), ('b_d_2', 'Дата рождения'),
                                           ('parent_name_1', 'Фамилия'), ('parent_name_2', 'Имя'),
                                           ('parent_name_3', 'Отчество')):
                    if marker_1 in ('d_open', 'd_from', 'd_until', 'b_d_1', 'b_d_2'):
                        date = ''
                        for word in data['examination']['LN_data']['current_data'].get(marker_2).get().strip():
                            if word.isdigit():
                                date += word
                            else:
                                date += '.'
                        date = date.split('.')
                        if len(date[-1]) == 4:
                            year = date.pop(-1)
                            date.append(f"{year[-2]}{year[-1]}")
                        date = ''.join(date)
                        text = list()
                        for word in date:
                            text.append(word)
                        render_data[marker_1] = '  '.join(text)
                    else:
                        text = list()
                        for word in data['examination']['LN_data']['current_data'].get(marker_2).get().strip():
                            text.append(word)
                        if marker_1 in ('parent_name_1', 'parent_name_2', 'parent_name_3'):
                            render_data[marker_1] = '  '.join(text)
                        else:
                            render_data[marker_1] = ' '.join(text)

                doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}"
                                   f"БЛАНК_ВН_{selected_type_ln.get().replace(' ', '_'.capitalize())}.docx")
                doc.render(render_data)
                doc_name = f".{os.sep}generated{os.sep}БЛАНК_ВН_{patient.get('name', '').split()[0]}.docx"
                doc_name = save_document(doc=doc, doc_name=doc_name)

                render_data.clear()
                run_document(doc_name)
                new_root.destroy()
                data_base(command="statistic_write",
                          insert_data="Документ ВН")

        def select_last_data():
            last_info = selected_button.get()
            for marker in data['examination']['LN_data']['last_patient_ln'].get(last_info, []):
                if data['examination']['LN_data']['current_data'].get(marker):
                    data['examination']['LN_data']['current_data'][marker].set(
                        data['examination']['LN_data']['last_patient_ln'][last_info].get(marker))

        def calendar_LN():
            text_field = selected_button.get()
            selected_button.set('')
            paste_calendar(text_field=text_field)


        if data['examination']['LN_data'].get('ln_root'):
            data['examination']['LN_data']['ln_root'].destroy()

        new_root = Toplevel()
        data['examination']['LN_data']['ln_root'] = new_root
        new_root.title(f"Генерация документа {selected_type_ln.get()} {data['examination']['LN_data'].get('type_doc')}")
        new_root.bind("<Control-KeyPress>", keypress)
        if not data['examination']['LN_data'].get('current_data'):
            data['examination']['LN_data']['current_data'] = {
                "Дата выдачи": StringVar(),
                "Дата начала ВН": StringVar(),
                "Дата окончания ВН": StringVar(),
                "Фамилия": StringVar(),
                "Имя": StringVar(),
                "Отчество": StringVar(),
                "Дата рождения": StringVar(),
                "Адрес места жительства": StringVar(),
                "Место работы (службы, учебы)": StringVar(),
                "Информация про ребенка (в корешок)": StringVar(),
                "Особые отметки": StringVar(),
            }

        data['examination']['LN_data']['current_data']['Дата выдачи'].set(datetime.now().strftime("%d.%m.%y"))
        if txt_ln_from.get().strip():
            data['examination']['LN_data']['current_data']['Дата начала ВН'].set(txt_ln_from.get().strip())
        else:
            data['examination']['LN_data']['current_data']['Дата начала ВН'].set(datetime.now().strftime("%d.%m.%y"))
        if txt_ln_until.get().strip():
            data['examination']['LN_data']['current_data']['Дата окончания ВН'].set(txt_ln_until.get().strip())
        data['examination']['LN_data']['current_data']['Адрес места жительства'].set(patient.get('address', ''))

        if 'по уходу' in data['examination']['LN_data'].get('type_doc'):
            try:
                data['examination']['LN_data']['current_data'][
                    'Информация про ребенка (в корешок)'].set(
                    f"{' '.join(patient.get('name', ' ').strip().split()[:-1])} {patient.get('birth_date', '')}")
                data['examination']['LN_data']['current_data'][
                    'Особые отметки'].set(
                    f"{patient.get('name', ' ').strip().split()[1]} {patient.get('birth_date', '')}")
            except IndexError:
                data['examination']['LN_data']['current_data'][
                    'Информация про ребенка (в корешок)'].set(
                    f"{patient.get('name', ' ')} {patient.get('birth_date', '')}")
                data['examination']['LN_data']['current_data'][
                    'Особые отметки'].set(
                    f"{patient.get('name', ' ')} {patient.get('birth_date', '')}")


        if 'по болезни' in data['examination']['LN_data'].get('type_doc'):
            data['examination']['LN_data']['current_data']['Дата рождения'].set(patient.get('birth_date', ''))
            if len(patient.get('name', ' ').strip().split()) == 3:
                data['examination']['LN_data']['current_data']['Фамилия'].set(
                    patient.get('name').strip().split()[0])
                data['examination']['LN_data']['current_data']['Имя'].set(
                    patient.get('name').strip().split()[1])
                data['examination']['LN_data']['current_data']['Отчество'].set(
                    patient.get('name').strip().split()[2])

            data['examination']['LN_data']['current_data']['Информация про ребенка (в корешок)'].set("")
            data['examination']['LN_data']['current_data']['Особые отметки'].set("")

        frame_title = Frame(new_root)
        for marker in ('Дата выдачи', 'Дата начала ВН', 'Дата окончания ВН'):
            frame = Frame(frame_title)
            Label(frame, text=f"{marker}:",
                  font=('Comic Sans MS', user.get('text_size')),
                  bg="#36566d", fg='white').grid(column=0, row=0, sticky='nwse', padx=2, pady=2, ipadx=3)
            Entry(frame, width=15, font=('Comic Sans MS', user.get('text_size')),
                      textvariable=data['examination']['LN_data']['current_data'].get(marker)
                      ).grid(column=1, row=0, sticky='nwse', ipadx=2, ipady=2)
            Radiobutton(frame, text="Календарь",
                        font=('Comic Sans MS', user.get('text_size')),
                        value=f"ln_root_{marker}__{marker}",
                        variable=selected_button,
                        command=calendar_LN,
                        indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff'
                        ).grid(column=0, row=1, sticky='nwse', ipadx=2, ipady=2, columnspan=2)

            frame.pack(fill='both', expand=True, padx=2, pady=2, side='left')
        frame_title.pack(fill='both', expand=True, padx=2, pady=2)

        row = 0
        frame = Frame(new_root)
        for marker in ('Фамилия', 'Имя', 'Отчество', 'Дата рождения',
                       'Адрес места жительства', 'Место работы (службы, учебы)',
                       'Информация про ребенка (в корешок)', 'Особые отметки'):
            Label(frame, text=marker,
                  font=('Comic Sans MS', user.get('text_size')),
                  bg="#36566d", fg='white').grid(column=0, row=row, sticky='nwse', padx=2, pady=2)
            Entry(frame, width=30, font=('Comic Sans MS', user.get('text_size')),
                      textvariable=data['examination']['LN_data']['current_data'].get(marker)
                      ).grid(column=1, row=row, sticky='nwse', ipadx=2, ipady=2)
            row += 1
        frame.pack(fill='both', expand=True, padx=2, pady=2)
        frame.columnconfigure(index='all', minsize=40, weight=1)

        Button(new_root, text='Создать документ', command=save,
               font=('Comic Sans MS', user.get('text_size'))
               ).pack(fill='both', expand=True, padx=2, pady=2)

        if data['examination']['LN_data'].get('last_patient_ln'):
            frame = Frame(new_root)
            Label(frame, text="Прошлые данные",
                  font=('Comic Sans MS', user.get('text_size')),
                  bg="#36566d", fg='white').pack(fill='both', expand=True, padx=2, pady=2)

            for key in data['examination']['LN_data'].get('last_patient_ln'):
                Radiobutton(frame, text=key,
                            font=('Comic Sans MS', user.get('text_size')),
                            value=f"{key}",
                            variable=selected_button,
                            command=select_last_data,
                            indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff'
                            ).pack(fill='both', expand=True, padx=2, pady=2)
            frame.pack(fill='both', expand=True, padx=2, pady=2)

        new_root.mainloop()

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
                last_visit = data['examination']['get_last_patient_ln'].get(type_ln)

                if last_visit:
                    ln_num = last_visit.split('__')[1].replace('_', '')
                    try:
                        date_from_cont = datetime.strptime(f"{last_visit.split('__')[3]}",
                                                           "%d.%m.%Y") + timedelta(days=1)
                        txt_ln_from.delete(0, 'end')
                        txt_ln_from.insert(0, date_from_cont.strftime("%d.%m.%Y"))

                    except Exception:
                        txt_ln_from.delete(0, 'end')
                        txt_ln_from.insert(0, datetime.now().strftime("%d.%m.%Y"))

                if not ln_num:
                    open_frame_ln_my_blanks()
                else:
                    txt_ln_num.delete(0, 'end')
                    if ln_num:
                        txt_ln_num.insert(0, ln_num)


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
        selected_type_ln.set('Уход обеспечен')
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

        Radiobutton(frame_ln_add, text="Создать документ по уходу",
                    font=('Comic Sans MS', user.get('text_size')),
                    value=f"по уходу",
                    variable=selected_button,
                    command=write_ln,
                    indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff'
                    ).grid(column=0, row=2, sticky='nwse', ipadx=2, ipady=2, columnspan=2)

        Radiobutton(frame_ln_add, text="Создать документ по болезни",
                    font=('Comic Sans MS', user.get('text_size')),
                    value=f"по болезни",
                    variable=selected_button,
                    command=write_ln,
                    indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff'
                    ).grid(column=2, row=2, sticky='nwse', ipadx=2, ipady=2, columnspan=4)



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
            lbl_ln_from.grid_configure(columnspan=3)
            lbl_ln_from.tkraise()
            lbl_ln_from['text'] = f"{selected_type_ln.get()} закрыт к труду c "
            but_ln_closed['text'] = "отменить закрытие"
            txt_ln_until.delete(0, 'end')
            txt_ln_until.insert(0, (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y"))


        else:
            data['examination']['ln_closed'] = False
            lbl_ln_from.grid_configure(columnspan=1)
            lbl_ln_from['text'] = " с "
            but_ln_closed['text'] = "закрыть к труду"
            txt_ln_until.delete(0, 'end')

    def open_frame_ln_my_blanks():
        def select_ln_num():
            txt_ln_num.delete(0, 'end')
            txt_ln_num.insert(0, selected_ln_num.get())

            txt_ln_from.delete(0, 'end')
            txt_ln_from.insert(0, datetime.now().strftime("%d.%m.%Y"))

        def add_my_new_ln():
            if not my_new_txt_ln_num.get():
                messagebox.showerror('Ошибка!', "Не указан номер первого ЛН")
            else:
                if type_ln == 'Лист ВН':
                    insert_data = f"{my_new_txt_ln_text.get()}__{my_new_txt_ln_num.get()}"
                else:
                    insert_data = f"__{my_new_txt_ln_num.get()}"

                data_base(command='examination__edit_doctor_LN',
                                       insert_data=[type_ln, insert_data])



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


            found_info = None

            if user.get('my_LN'):
                for ln_data in user.get('my_LN'):
                    if type_ln == ln_data[0]:
                        found_info = ln_data[1]

            row, col = 0, 0
            if found_info:
                found_info_past = data['examination']['get_last_doc_LN'].get(type_ln)

                frame_ln_my_blanks_local_1 = Frame(frame_ln_my_blanks_local, padx=1, pady=1)
                first_ln_num = int(found_info.split('__')[-1])
                first_ln_text = found_info.split('__')[0]
                for ln_num in range(first_ln_num, first_ln_num + 10, 1):
                    btn = Radiobutton(frame_ln_my_blanks_local_1, text=f"{first_ln_text} {first_ln_num}",
                                      font=('Comic Sans MS', user.get('text_size')),
                                      value=f"{first_ln_text} {first_ln_num}",
                                      variable=selected_ln_num, command=select_ln_num,
                                      indicatoron=False, selectcolor='#77f1ff')
                    btn.grid(row=row, column=col, sticky='ew')
                    if found_info_past:
                        for i in found_info_past:
                            if isinstance(i, tuple):
                                i = i[0]
                            if str(first_ln_num) in i:
                                btn['bg'] = '#cdcdcd'
                                break
                        else:
                            btn['bg'] = "#cefeed"
                            if not active_ln:
                                active_ln = True
                                txt_ln_num.delete(0, 'end')
                                txt_ln_num.insert(0, f"{first_ln_text} {first_ln_num}")

                                txt_ln_from.delete(0, 'end')
                                txt_ln_from.insert(0, datetime.now().strftime("%d.%m.%Y"))
                    else:
                        btn['bg'] = "#cefeed"



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

    def paste_frame_button_create():
        def create_examination_doc_a5():
            create_examination_doc('а5')

        def create_examination_doc_a5_rec():
            create_examination_doc('а5_рек')

        def create_examination_doc_a6_rec():
            create_examination_doc('а6_рек')

        def create_examination_doc_a5_disp():
            create_examination_doc('а5_child_disp')

        def create_examination_doc_a6():
            create_examination_doc('а6')

        def create_examination_doc_none():
            create_examination_doc()

        frame_button = Frame(examination_root, relief="solid", padx=1, pady=1, bg="#36566d")

        Button(frame_button, text='Печать А5',
               bg="#36566d", fg='white',
               command=create_examination_doc_a5,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=0, sticky='nswe')

        Button(frame_button, text='Печать А6',
               bg="#36566d", fg='white',
               command=create_examination_doc_a6,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=0, row=1, sticky='nswe')

        Button(frame_button, text='Печать А5 + рекомендации',
               bg="#36566d", fg='white',
               command=create_examination_doc_a5_rec,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=1, row=0, sticky='nswe')

        Button(frame_button, text='Печать А6 + рекомендации',
               bg="#36566d", fg='white',
               command=create_examination_doc_a6_rec,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=1, row=1, sticky='nswe')


        Button(frame_button, text='Сохранить\nбез печати',
               bg="#36566d", fg='white',
               command=create_examination_doc_none,
               font=('Comic Sans MS', user.get('text_size'))).grid(column=2, row=0, rowspan=2, sticky='nswe')


        if child_marker:
            Button(frame_button, text='Печать А5\nежемесячный',
                   bg="#36566d", fg='white',
                   command=create_examination_doc_a5_disp,
                   font=('Comic Sans MS', user.get('text_size'))).grid(column=3, row=0, rowspan=2, sticky='nswe')



        frame_button.columnconfigure(index='all', minsize=40, weight=1)
        frame_button.rowconfigure(index='all', minsize=20)
        frame_button.pack(fill='both', expand=True, side=tk.LEFT)

    paste_frame_button_create()


    def paste_calendar(text_field):
        command, marker = text_field.split('__')
        if data['examination'].get('calendar_root'):
            data['examination']['calendar_root'].destroy()

        calendar_root = Toplevel()
        data['examination']['calendar_root'] = calendar_root
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
            edit_day = list()
            for i in day.split('.'):
                if len(i) == 1:
                    i = f"0{i}"
                edit_day.append(i)
            answer = '.'.join(edit_day)
            if command.startswith('ln_root_'):
                data['examination']['LN_data']['current_data'][command.split('_')[-1]].set(answer)

            elif command == 'ln_from':
                txt_ln_from.delete(0, 'end')
                txt_ln_from.insert(0, answer)

            elif command == 'ln_until':
                txt_ln_until.delete(0, 'end')
                txt_ln_until.insert(0, answer)

                txt_second_examination.delete(0, 'end')
                txt_second_examination.insert(0, answer)

            elif command == 'second_examination':
                txt_second_examination.delete(0, 'end')
                txt_second_examination.insert(0, answer)



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
                                              value=f"{day}.{month}.{year}", variable=selected_day, command=select_day,
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

    start_action(upload_last_data)
