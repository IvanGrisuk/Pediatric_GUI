


def fast_certificate():

    def start_action(func=None):
        def check_thread(thread):
            if thread.is_alive():
                animation.set(animation.get()[-1] + animation.get()[:-1])
                # root.update()
                certificate_main_root.after(200, lambda: check_thread(thread))
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

    data['certificate'] = {
        'main_label': StringVar(),
        'all_roots': dict(),
        'type_cert_frames': dict(),
        'type_cert_info': dict(),
    }

    age = patient.get('age')

    certificate_main_root = Toplevel()
    certificate_main_root.bind("<Control-KeyPress>", keypress)
    certificate_main_root.config(bg='white')
    certificate_main_root.title(f'Cоздание справки')


    selected_button = StringVar()

    data['certificate']['main_label'].set(f"Данные пациента:    "
                                           f"Участок: {patient.get('patient_district')};    "
                                           f"№ амб: {patient.get('amb_cart')};    "
                                          f"Возраст: {patient['age'].get('age_txt')};\n"
                                           f"ФИО: {patient.get('name')};    "
                                           f"{patient.get('birth_date')};    "
                                           f"пол: {patient.get('gender')};\n"
                                           f"Адрес: {patient.get('address')};")

    Label(master=certificate_main_root,
          textvariable=data['certificate'].get('main_label'),
          font=('Comic Sans MS', user.get('text_size')),
          bg="#36566d",
          fg='white',
          padx=4, pady=4
          ).pack(fill='both', expand=True)
    animation = StringVar()

    Label(master=certificate_main_root,
          textvariable=animation,
          bg="#36566d",
          fg='white',
          ).pack(fill='both', expand=True)


    selected_place = StringVar()
    label_place_text = StringVar()
    label_place_text.set("Место требования справки: ")

    selected_button = StringVar()
    hobby_txt = StringVar()
    new_hobby_txt = StringVar()
    job_txt = StringVar()
    selected_diagnosis_ori = StringVar()

    ori_from = StringVar()
    ori_until = StringVar()
    ori_home_regime = StringVar()
    ori_add_to_childhood = StringVar()
    ori_fizra_days = StringVar()

    selected_chickenpox = StringVar()
    selected_allergy = StringVar()
    allergy_txt = StringVar()
    selected_injury_operation = StringVar()
    injury_operation_txt = StringVar()

    height = StringVar()
    weight = StringVar()
    vision = StringVar()

    patient_anthropometry = StringVar()

    selected_health_group = StringVar()
    selected_fiz_group = StringVar()
    selected_diet = StringVar()

    patient_temp = StringVar()
    patient_br = StringVar()
    patient_hr = StringVar()
    patient_bp = StringVar()

    posture = StringVar()
    dispanser_card = StringVar()
    dispanser_card.set('Да')
    examination_blank = StringVar()
    examination_blank.set("Да")

    work_place = StringVar()
    dispensary_observation = StringVar()
    registered_from = StringVar()
    registered_from = StringVar()
    registered_from = StringVar()
    registered_from = StringVar()
    registered_from = StringVar()
    registered_from = StringVar()
    registered_from = StringVar()
    registered_from = StringVar()
    registered_from = StringVar()





    date_of_issue = StringVar()
    date_of_issue.set(datetime.now().strftime('%d.%m.%Y'))

    regime_vars = dict()
    for mark in all_data_certificate.get('health').get('regime'):
        regime_vars[mark] = IntVar()
    desk_vars = dict()
    for mark in all_data_certificate.get('health').get('desk'):
        desk_vars[mark] = IntVar()


    def pack_frame_type_cert():
        def select_type_cert():
            if data['certificate']['type_cert_frames'].get('selected_cert'):
                data['certificate']['type_cert_frames']['selected_cert'].pack_forget()

            canvas = data['certificate'].get('canvas')
            type_cert_frame = data['certificate']['type_cert_frames'].get(selected_button.get())
            data['certificate']['type_cert_frames']['selected_cert'] = type_cert_frame
            scrolled_frame = data['certificate'].get('scrolled_frame')

            certificate_main_root.update_idletasks()
            type_cert_frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

            scrolled_frame.configure(height=type_cert_frame.winfo_height())
            region = canvas.bbox(tk.ALL)
            canvas.configure(scrollregion=region)
            canvas.create_window((0, 0), window=scrolled_frame, anchor="nw",
                                 width=canvas.winfo_width())
            canvas.yview_moveto(0)
            certificate_main_root.update()

        frame_type_cert = Frame(certificate_main_root)
        Label(master=certificate_main_root,
              text="Тип справки:",
              font=('Comic Sans MS', user.get('text_size')),
              ).pack(fill='both', expand=True)
        frame_type_cert_but = Frame(frame_type_cert)
        all_type_cert = [[]]
        for type_cert in all_data_certificate.get('type'):
            if len(all_type_cert[-1]) == 4:
                all_type_cert.append(list())
            all_type_cert[-1].append(type_cert)
        for type_cert_data in all_type_cert:
            frame = Frame(frame_type_cert_but)
            for type_cert in type_cert_data:
                Radiobutton(master=frame,
                            text=type_cert,
                            font=('Comic Sans MS', user.get('text_size')),
                            value=type_cert,
                            variable=selected_button,
                            command=select_type_cert,
                            indicatoron=False, bg='#f0fffe', selectcolor='#77f1ff'
                            ).pack(fill='both', expand=True, padx=1, pady=1, side='left')
            frame.pack(fill='both', expand=True)
        # frame_type_cert_but.columnconfigure(index='all', minsize=40, weight=1)
        # frame_type_cert_but.rowconfigure(index='all', minsize=20)
        data['certificate']['frame_type_cert_but'] = frame_type_cert_but
        # frame_type_cert_but.pack(fill='both', expand=True, padx=2, pady=2)
        frame_type_cert.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

    pack_frame_type_cert()

    def pack_scrolled_frame():
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

        certificate_main_root.update_idletasks()
        height = (certificate_main_root.winfo_screenheight() - certificate_main_root.winfo_height() - 200)
        width = certificate_main_root.winfo_screenheight()
        if certificate_main_root.winfo_screenwidth() < width:
            width = certificate_main_root.winfo_screenwidth()

        # print(f"height - {certificate_main_root.winfo_screenheight()}\n"
        #       f"width - {width}\n"
        #       f"{certificate_main_root.winfo_screenwidth()}")

        master_frame = Frame(certificate_main_root)
        master_frame.pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

        scroll_x = tk.Scrollbar(master_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(master_frame, orient=tk.VERTICAL, width=user.get('text_size', 10) * 2)

        canvas = tk.Canvas(master_frame,
                           xscrollcommand=scroll_x.set,
                           yscrollcommand=scroll_y.set, height=height, width=width)
        scroll_x.config(command=canvas.xview)
        scroll_y.config(command=canvas.yview)

        canvas_frame = Frame(canvas)
        data['certificate']['scrolled_frame'] = canvas_frame
        data['certificate']['canvas'] = canvas
        data['certificate']['scroll_x'] = scroll_x


        # canvas['width'] = int(canvas.winfo_geometry().split('x')[0])
        # canvas_frame['width'] = int(canvas.winfo_geometry().split('x')[0])
        canvas.grid(row=0, column=0, sticky="nsew")
        scroll_x.grid(row=1, column=0, sticky="we")
        scroll_y.grid(row=0, column=1, sticky="ns")

        master_frame.rowconfigure(0, weight=1)
        master_frame.columnconfigure(0, weight=1)

        master_frame.bind("<Configure>", resize)
        master_frame.update_idletasks()
        canvas_frame['height'] = height
        canvas_frame['height'] = canvas.winfo_width()

        canvas.bind("<Enter>", on_binds)
        canvas.bind("<Leave>", off_binds)
        certificate_main_root.update_idletasks()

        # canvas.create_window((0, 0), window=canvas_frame, anchor="nw",
        #                      width=canvas.winfo_width())

    pack_scrolled_frame()

    def create_type_cert_frames():
        canvas_frame = data['certificate']['scrolled_frame']

        sanatorium_profile = dict()

        def create_certificate():
            def certificate__create_doc():

                if not (type_certificate == "Оформление в ДДУ / СШ / ВУЗ"
                        and place_of_requirement in ('ВУЗ (колледж)', 'Кадетское училище')):
                    doctor_name, district, pediatric_division = (user.get('doctor_name'),
                                                                 user.get('doctor_district'),
                                                                 user.get('ped_div'))

                    active_examination = f"Выдана справка: {type_certificate}\n" \
                                         f"Цель выдачи справки: {render_data.get('place_of_requirement')}\n" \
                                         f"Перенесенные заболевания: {render_data.get('past_illnesses')}\n" \
                                         f"Дополнительные медицинские сведения: " \
                                         f"{render_data.get('additional_medical_information')}\n" \
                                         f"Заключение: {render_data.get('diagnosis')}\n" \
                                         f"Рекомендации: {render_data.get('recommendation')}"

                    if type_certificate in ('ЦКРОиР', 'Бесплатное питание'):
                        type_cert = '7.9 (выписка)'
                    else:
                        type_cert = '7.6 (справка)'
                    info = [pediatric_division,
                            district,
                            None,
                            datetime.now().strftime("%d.%m.%Y -- %H:%M:%S"),
                            render_data.get('name'),
                            render_data.get('birth_date'),
                            render_data.get('address'),
                            type_cert,
                            doctor_name,
                            active_examination]

                    number = data_base(command='save_certificate_single_window',
                                       insert_data=info)

                    render_data['number_cert'] = f"№ {number}"
                else:
                    render_data['number_cert'] = '№ ______'

                if (type_certificate == "Оформление в ДДУ / СШ / ВУЗ"
                    and place_of_requirement in ("Средняя школа (гимназия)", "Кадетское училище")) \
                        or type_certificate == 'Об усыновлении (удочерении)':
                    doc_name = ""
                    if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':
                        doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]}_справка_Оформление.docx"
                        if not render_data.get('number_cert'):
                            render_data['number_cert'] = '№ ______'
                    elif type_certificate == 'Об усыновлении (удочерении)':
                        doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]}_справка_Об_усыновлении.docx"

                    render_data['manager'] = user.get('manager', '______________________')

                    doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}справка а4 годовая.docx")
                    doc.render(render_data)
                    doc_name = save_document(doc=doc, doc_name=doc_name)

                    file_name_vac = create_vaccination(user_id=patient.get('amb_cart'), size=4)
                    if file_name_vac:
                        master = Document(doc_name)
                        master.add_page_break()
                        composer = Composer(master)
                        doc_temp = Document(file_name_vac)
                        composer.append(doc_temp)
                        doc_name = save_document(doc=composer, doc_name=doc_name)

                        # composer.save(doc_name)

                    run_document(doc_name)

                    doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}осмотр.docx")
                    doc.render(render_data)
                    doc_name_exam = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]}_осмотр.docx"
                    doc_name_exam = save_document(doc=doc, doc_name=doc_name_exam)
                    run_document(doc_name_exam)

                else:
                    if type_certificate in ('ЦКРОиР', 'Бесплатное питание'):
                        doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}Выписка.docx")
                        render_data['manager'] = '______________________'
                        if type_certificate == 'Бесплатное питание':
                            render_data['manager'] = user.get('manager', '______________________')

                        doc.render(render_data)
                        doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]}_" \
                                   f"Выписка_{type_certificate}.docx".replace(' ', '_')
                        doc_name = save_document(doc=doc, doc_name=doc_name)

                    elif type_certificate in ('Годовой медосмотр', 'В детский лагерь', "Оформление в ДДУ / СШ / ВУЗ"):
                        render_data['manager'] = '______________________'
                        if type_certificate.startswith('Оформление в ДДУ / СШ / ВУЗ'):
                            render_data['manager'] = user.get('manager', '______________________')

                        doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]}_" \
                                   f"справка_{type_certificate}.docx".replace(' в ДДУ / СШ / ВУЗ', '').replace(' ', '_')

                        if type_certificate == "Оформление в ДДУ / СШ / ВУЗ" \
                                and data['certificate'].get('place_of_requirement') == 'ВУЗ (колледж)':
                            master = Document(f".{os.sep}example{os.sep}certificate{os.sep}справка а5_вуз.docx")
                        else:
                            master = Document(f".{os.sep}example{os.sep}certificate{os.sep}справка а5.docx")

                        master.add_page_break()
                        composer = Composer(master)

                        if type_certificate in ('В детский лагерь', "Оформление в ДДУ / СШ / ВУЗ"):
                            file_name_vac = create_vaccination(user_id=patient.get('amb_cart'), size=5)
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

                        if type_certificate == 'Годовой медосмотр' and dispanser_card.get() == 'Да':
                            render_data['year'] = datetime.now().strftime("%Y")
                            render_data['date'] = datetime.now().strftime("%d.%m")

                            render_data['disp_visus'] = f"{render_data.get('date')} - {vision.get()}"
                            render_data['disp_posture'] = f"{render_data.get('date')} - {posture.get()}"
                            diagnosis_txt = data['certificate']['type_cert_info'][type_certificate].get(
                                'diagnosis_txt').get(1.0, 'end').strip() + \
                                            f"\nФизическое развитие: " \
                                            f"{patient_anthropometry.get().split('--')[-1].strip()}"
                            render_data['disp_diagnosis'] = diagnosis_txt
                            render_data['disp_health'] = selected_health_group.get()
                            render_data['disp_group'] = selected_fiz_group.get()


                            doc_temp = Document(f".{os.sep}example{os.sep}certificate{os.sep}диспансеризация.docx")
                            master.add_page_break()
                            composer.append(doc_temp)

                        doc_name = save_document(doc=composer, doc_name=doc_name)



                        doc = DocxTemplate(doc_name)
                        doc.render(render_data)

                        doc_name = save_document(doc=doc, doc_name=doc_name)

                    else:
                        render_data['manager'] = '______________________'
                        if type_certificate == 'О нуждаемости в сан-кур лечении':
                            render_data['manager'] = user.get('manager', '______________________')

                        doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}справка а5.docx")
                        doc.render(render_data)
                        doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]} " \
                                   f"справка {type_certificate}.docx".replace(' ', '_')
                        doc_name = save_document(doc=doc, doc_name=doc_name)


                        if (type_certificate in ('В детский лагерь', 'Может работать по специальности...')
                                or(type_certificate == 'Об отсутствии контактов'
                                   and data['certificate'].get('place_of_requirement') == 'В стационар')):
                            file_name_vac = create_vaccination(user_id=patient.get('amb_cart'), size=5)
                            if file_name_vac:
                                master = Document(doc_name)
                                master.add_page_break()
                                composer = Composer(master)
                                doc_temp = Document(file_name_vac)
                                composer.append(doc_temp)
                                doc_name = save_document(doc=composer, doc_name=doc_name)

                                # composer.save(doc_name)

                    run_document(doc_name)
                    if type_certificate in ("На кружки и секции", "ЦКРОиР", "Об отсутствии контактов",
                                            "О нуждаемости в сан-кур лечении", "Может работать по специальности...",
                                            "Бесплатное питание") and examination_blank.get() == 'Да':
                        diagnosis_txt = ''
                        if type_certificate in ('На кружки и секции', 'О нуждаемости в сан-кур лечении',
                                                'Может работать по специальности...'):
                            diagnosis_txt = data['certificate']['type_cert_info'][type_certificate].get(
                                'diagnosis_txt').get(1.0, 'end').strip()

                        local_data = {
                            "Об отсутствии контактов": "Осмотрен на чесотку, педикулез, микроспорию\n"
                                                       "Согласие на простое медицинское вмешательство получено\n"
                                                       "В контакте с инфекционными больными в течение 35 дней не был\n"
                                                       "На приеме: с мамой\n"
                                                       "Жалоб нет. Состояние удовлетворительное. "
                                                       "Кожа чистая, зев не гиперемирован. "
                                                       "Pulm: везикулярное дыхание, хрипов нет. "
                                                       "Cor: тоны громкие, ритмичные. "
                                                       "Периферические лимфоузлы не увеличены. "
                                                       "Живот мягкий, безболезненный. "
                                                       "Стул и диурез без особенностей.\n"
                                                       "Перенесенные заболевания: \n"
                                                       f"{render_data.get('past_illnesses')}\n"
                                                       "Заключение: на момент осмотра соматически здоров. "
                                                       "Может находиться в детском коллективе\n"
                                                       "Выдана справка: Об отсутствии контактов в "
                                                       f"{render_data.get('place_of_requirement')}",
                            "На кружки и секции": "Диагноз: "
                                                  f"{diagnosis_txt}\n"
                                                  f"Заключение: {render_data.get('diagnosis')}\n"
                                                  "Выдана справка: На кружки и секции",
                            "ЦКРОиР": "Дополнительные медицинские сведения: "
                                      f"{render_data.get('additional_medical_information')}\n"
                                      f"Заключение: {render_data.get('diagnosis')}\n"
                                      "Выписка дана для предоставления в "
                                      f"{render_data.get('place_of_requirement')}",
                            "О нуждаемости в сан-кур лечении": "Перенесенные заболевания: \n"
                                                               f"{render_data.get('past_illnesses')}\n"
                                                               "Диагноз: "
                                                               f"{diagnosis_txt}\n"
                                                               f"Заключение: {render_data.get('diagnosis')}\n"
                                                               "Выдана справка: О нуждаемости в "
                                                               "санаторно-курортном лечении",
                            "Может работать по специальности...": "Диагноз: "
                                                                  f"{diagnosis_txt}\n"
                                                                  f"Заключение: {render_data.get('diagnosis')}\n"
                                                                  "Группа здоровья: "
                                                                  f"{data['certificate'].get('health_group', '')};  "
                                                                  "Группа по физкультуре: "
                                                                  f"{data['certificate'].get('physical', '')};\n"
                                                                  "Выдана справка о годности к работе",

                            "Бесплатное питание": "Перенесенные заболевания: \n"
                                                  f"{render_data.get('past_illnesses')}\n"
                                                  "Дополнительные медицинские сведения: "
                                                  f"{render_data.get('additional_medical_information')}\n"
                                                  f"Заключение: {render_data.get('diagnosis')}\n"
                                                  "Рекомендации: "
                                                  f"{render_data.get('recommendation')}\n"
                                                  "Выписка дана для предоставления в "
                                                  f"{render_data.get('place_of_requirement')}"

                        }

                        examination_text = f"ФИО: {patient.get('name')}  " \
                                           f"Дата рождения: {patient.get('birth_date')}  " \
                                           f"Участок: {patient.get('patient_district')}\n" \
                                           f"Дата и время: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n" \
                                           f"{local_data.get(type_certificate)}\n" \
                                           f"Врач-педиатр: {user.get('doctor_name')}"
                        render_data['patient_info'] = examination_text

                        doc = DocxTemplate(f".{os.sep}example{os.sep}certificate{os.sep}Вкладыш_справка.docx")
                        doc.render(render_data)
                        doc_name = f".{os.sep}generated{os.sep}{patient.get('name').split()[0]} " \
                                   f"Вкладыш_осмотра.docx".replace(' ', '_')
                        doc_name = save_document(doc=doc, doc_name=doc_name)
                        run_document(doc_name)

                        # document = Document()
                        # paragraph = document.add_paragraph()
                        # p = paragraph.add_run(examination_text)
                        # r_fmt = p.font
                        # r_fmt.name = 'Times New Roman'
                        # r_fmt.size = Pt(10)
                        # if type_certificate in ('ЦКРОиР', 'Об отсутствии контактов'):
                        #     r_fmt.size = Pt(9)
                        # sections = document.sections
                        # for section in sections:
                        #     section.top_margin = Cm(1.5)
                        #     section.bottom_margin = Cm(1.5)
                        #     section.left_margin = Cm(1.5)
                        #     section.right_margin = Cm(1.5)
                        #     section.page_height = Cm(10.5)
                        #     section.page_width = Cm(14.8)
                        # doc_name = save_document(doc=document, doc_name=f"Вкладыш_осмотра_"
                        #                                                 f"{patient.get('name').split()[0]}.docx")
                        # run_document(doc_name)

                data_base(command="statistic_write",
                          insert_data="Справка")
                def save_info_examination():

                    active_examination = f"Выдана справка: {type_certificate}\n" \
                                         f"Цель выдачи справки: {render_data.get('place_of_requirement')}\n" \
                                         f"Перенесенные заболевания: {render_data.get('past_illnesses')}\n" \
                                         f"Дополнительные медицинские сведения: " \
                                         f"{render_data.get('additional_medical_information')}\n" \
                                         f"Заключение: {render_data.get('diagnosis')}\n" \
                                         f"Рекомендации: {render_data.get('recommendation')}"

                    active_but = f"type_examination:____certificate__<end!>__\n" \
                                 f"type_certificate:____{type_certificate}__<end!>__\n"
                    if type_certificate in ('Годовой медосмотр',
                                            'Оформление в ДДУ / СШ / ВУЗ',
                                            'В детский лагерь',
                                            'Об усыновлении (удочерении)',
                                            'Об отсутствии контактов',
                                            'Бесплатное питание',
                                            'О нуждаемости в сан-кур лечении'):
                        active_but += f"chickenpox_allergy_injury:____" \
                                      f"chickenpox__{data['certificate'].get('chickenpox', '')}____" \
                                      f"allergy__{data['certificate'].get('allergy', '')}____" \
                                      f"allergy_txt__{allergy_txt.get()}____" \
                                      f"injury_operation__{data['certificate'].get('injury_operation', '')}____" \
                                      f"injury_txt__{injury_operation_txt.get()}__<end!>__\n"

                    if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ',
                                            'В детский лагерь', 'Об усыновлении (удочерении)'):
                        active_but += f"health_physical_group:____" \
                                      f"health_group__{data['certificate'].get('health_group', '')}____" \
                                      f"physical__{data['certificate'].get('physical', '')}____" \
                                      f"diet__{data['certificate'].get('diet', '')}____"
                        for var in data['certificate'].get('regime', []):
                            active_but += f"regime__{var}____"
                        for var in data['certificate'].get('desk', []):
                            active_but += f"desk__{var}____"
                        active_but += f"posture__{posture.get()}____"

                        active_but += "__<end!>__\n"

                    if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ', 'ЦКРОиР',
                                            'В детский лагерь', 'Об усыновлении (удочерении)',
                                            'О нуждаемости в сан-кур лечении', 'На кружки и секции',
                                                'Может работать по специальности...'):
                        diagnosis_txt = data['certificate']['type_cert_info'][type_certificate].get('diagnosis_txt').get(1.0, 'end').strip()
                        if diagnosis_txt:
                            active_but += f"diagnosis_txt:____{diagnosis_txt}__<end!>__\n"

                    if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ', 'В детский лагерь'):
                        active_but += f"patient_anthro:____" \
                                      f"height__{height.get()}____" \
                                      f"weight__{weight.get()}____" \
                                      f"vision__{vision.get()}____" \
                                      f"__<end!>__\n"

                        if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ' \
                                and data['certificate'].get('place_of_requirement') == 'ВУЗ (колледж)':
                            specialties = data['certificate'].get('specialties_txt').get(1.0, 'end').strip()
                            if specialties:
                                active_but += f"last_patient_specialties:____{specialties}__<end!>__\n"

                    if type_certificate == 'ЦКРОиР':
                        add_med_info = data['certificate']['type_cert_info']['ЦКРОиР'].get('ЦКРОиР_add_med_info')
                        active_but += f"ЦКРОиР_add_med_info:____{add_med_info.get(1.0, 'end').strip()}__<end!>__\n"
                        active_but += f"ЦКРОиР_add_med_info_doctors:____"
                        for doctors in ('Невролог', 'Офтальмолог', 'ЛОР', 'Логопед'):
                            active_but += f"{doctors}____" \
                                      f"{data['certificate']['type_cert_info']['ЦКРОиР'][f'{doctors}_txt'].get()}" \
                                          f"__!__"
                        active_but += "__<end!>__\n"
                    'certificate__upload_last_data'
                    save_info = [
                        f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}",
                        f"{user.get('doctor_name')}",
                        'loc',
                        '',
                        f"{patient.get('name').strip()}__{patient.get('birth_date').strip()}",
                        active_examination,
                        active_but,
                        'certificate']
                    answer, message = data_base(command='examination__save',
                                                insert_data=save_info)
                save_info_examination()
                data['certificate'].clear()
                render_data.clear()

            type_certificate = selected_button.get()
            render_data.clear()
            data['certificate']['type_cert_frames']['selected_cert'].pack_forget()

            try:
                for marker in all_data_certificate['all_info'].get(type_certificate):
                    render_data[marker] = all_data_certificate['all_info'][type_certificate].get(marker)

                render_data['time'] = datetime.now().strftime("%H:%M")

                render_data['number_cert'] = ''
                render_data['doctor_name'] = user.get('doctor_name')

                render_data['name'] = patient.get('name')
                render_data['birth_date'] = patient.get('birth_date')
                render_data['gender'] = patient.get('gender')
                render_data['address'] = patient.get('address')
                render_data['amb_cart'] = patient.get('amb_cart')
                render_data['type'] = type_certificate
                render_data['examination_left'] = ''
                render_data['examination_main'] = ''


                render_data['date_of_issue'] = date_of_issue.get()
                render_data['validity_period'] = \
                    data['certificate']['type_cert_info'][type_certificate]['validity_period'].get()

                diagnosis_txt = data['certificate']['type_cert_info'][type_certificate].get('diagnosis_txt')
                if diagnosis_txt:
                    data['certificate']['diagnosis_text'] = diagnosis_txt.get(1.0, 'end').strip()

                if not render_data.get('place_of_requirement'):
                    if not data['certificate'].get('place_of_requirement'):
                        messagebox.showinfo('Ошибка!', 'Не выбрано место требования справки!')
                        raise ValueError
                    render_data['place_of_requirement'] = data['certificate'].get('place_of_requirement')
                place_of_requirement = render_data.get('place_of_requirement')

                if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':
                    if place_of_requirement == 'Детское Дошкольное Учреждение':
                        render_data['place_of_requirement'] = "Оформление в детское дошкольное учреждение"
                        render_data['type'] = 'Оформление в Детское Дошкольное Учреждение'
                        render_data['recommendation'] = \
                            render_data.get('recommendation').replace('Режим _',
                                                                      'Режим щадящий 1 мес, затем Режим _')
                    if place_of_requirement == 'Средняя школа (гимназия)':
                        render_data['place_of_requirement'] = "Оформление в учреждение общего среднего образования"
                        render_data['type'] = 'Оформление в Среднюю школу (гимназию)'
                        if patient.get('gender', '') == 'женский':
                            render_data['diagnosis'] += f'\nГотова к обучению в ' \
                                                        f"учреждении общего среднего образования"
                        else:
                            render_data['diagnosis'] += '\nГотов к обучению в учреждении общего среднего образования'

                    if place_of_requirement == 'ВУЗ (колледж)':
                        render_data['type'] = 'Оформление в ВУЗ'
                        render_data['additional_medical_information'] = "_____________________________________________"
                        render_data['recommendation'] = "_____________________________________________"
                        render_data['place_of_requirement'] = 'Для поступления в учреждения высшего, ' \
                                                              'среднего специального и ' \
                                                              'профессионально-технического образования '
                        render_data['diagnosis'] += "\nОтсутствуют медицинские противопоказания " \
                                                    f"к обучению по специальности: \n" \
                                                    f"{data['certificate'].get('specialties_txt').get(1.0, 'end')}" \
                                                    "(пункт 2 приложения к постановлению " \
                                                    "МЗ РБ от 25.07.2022г. №71)"

                    if place_of_requirement == 'Кадетское училище':
                        render_data['type'] = 'Оформление в Кадетское училище'
                        render_data['place_of_requirement'] = 'Для обучения в кадетском училище / ' \
                                                              'специализированном лицее Министерства внутренних дел / ' \
                                                              'специализированном лицее Министерства по чрезвычайным ситуациям»'

                        render_data['additional_medical_information'] = \
                            render_data.get('additional_medical_information') + \
                            '\nОфтальмолог: ________________________________________________________' \
                            '\nНевролог: ___________________________________________________________' \
                            '\nОториноларинголог : _________________________________________________' \
                            '\nСтоматолог: _________________________________________________________' \
                            '\nХирург: _____________________________________________________________' \
                            '\nПедиатр: ____________________________________________________________' \
                            '\nОАК: __________ – WBC: ____ *10^12; RBC: ____ * 10^9; PLT ____ * 10^9; ' \
                            'HGB: ____ г/л; HCT ____ %; MCV: ____ фл; MCH: ____ пг; MCHC: ____ г/л; ' \
                            'Нейтрофилы: ____ %; Лимфоциты: ____ %;  Моноциты: ____ %;  Базофилы: ____ %;  ' \
                            'Эозинофилы: ____ %;  СОЭ ____ мм/ч' \
                            '\nГлюкоза: __________ - _____ ммоль/л' \
                            '\nОАМ: __________ - Цвет: соломенный; Прозрачность: прозрачный; Реакция ____ ; ' \
                            'Удельный вес: ______ ; Белок: не обнаруж.; Глюкоза: не обнаруж.; ' \
                            'Кетоновые тела: не обнаруж.; Билирубин: не обнаруж.; Лейкоциты: не обнаруж.; ' \
                            'Эритроциты: не обнаруж.; Бактерии: не обнаруж.; ' \
                            'Сперматазоиды: не обнаруж.; Слизь: не обнаруж.;' \
                            '\nУЗИ сердца: _________________________________________________________' \
                            '\nЭлектрокардиограмма: ________________________________________________' \
                            '\nУЗИ щитовидной  железы : ____________________________________________'
                        render_data['diagnosis'] += \
                            '\n' \
                            'Врачебное профессионально-консультативное заключение: ' \
                            'отсутствуют медицинские противопоказания к обучению  в ГУО ' \
                            '«Минском городском  кадетском училище».'

                if type_certificate == 'По выздоровлении':
                    selected_diagnosis = data['certificate']['combo_diagnosis'].get()
                    if ori_from.get() and ori_until.get():
                        render_data['diagnosis'] = f"{selected_diagnosis} c {ori_from.get()} по {ori_until.get()}"
                    elif ori_from.get():
                        render_data['diagnosis'] = f"{selected_diagnosis} от {ori_from.get()}"
                    elif ori_until.get():
                        render_data['diagnosis'] = f"{selected_diagnosis}  {ori_until.get()}"
                    else:
                        render_data['diagnosis'] = f"{selected_diagnosis} "

                    if ori_home_regime.get():
                        if render_data.get('recommendation'):
                            render_data['recommendation'] = f"{render_data.get('recommendation')}\n"
                        render_data['recommendation'] = f"{render_data.get('recommendation')}" \
                                                        f"Домашний режим до {ori_home_regime.get()} включительно"
                    if ori_add_to_childhood.get():
                        if render_data.get('recommendation'):
                            render_data['recommendation'] = f"{render_data.get('recommendation')}\n"
                        render_data['recommendation'] = f"{render_data.get('recommendation')}" \
                                                        f"Допуск в детский коллектив с {ori_add_to_childhood.get()}"

                    if ori_fizra_days.get():
                        if render_data.get('recommendation'):
                            render_data['recommendation'] = f"{render_data.get('recommendation')}\n"
                        render_data['recommendation'] = f"{render_data.get('recommendation')}" \
                                                        f"Освобождение от занятий физкультурой и плаванием \n" \
                                                        f"в бассейне на {ori_fizra_days.get()} дней"

                if type_certificate == 'На кружки и секции':
                    render_data['place_of_requirement'] = \
                        f"{render_data.get('place_of_requirement')}{hobby_txt.get()}" \
                        f"".replace('участия в соревнованиях по ', '').replace(' и участия в соревнованиях', '').replace(' , ', '')

                    render_data['diagnosis'] = f"{render_data.get('diagnosis')}{hobby_txt.get()}"

                    if data['certificate'].get('health_group'):
                        render_data['diagnosis'] = \
                            f"{render_data.get('diagnosis')}\n" \
                            f"Группа здоровья: {data['certificate'].get('health_group')};"

                    if data['certificate'].get('physical'):
                        render_data['diagnosis'] = \
                            f"{render_data.get('diagnosis')}" \
                            f"  Группа по физкультуре: {data['certificate'].get('physical')};"

                if type_certificate == 'Может работать по специальности...':
                    render_data['diagnosis'] = \
                        f"{render_data.get('diagnosis')} {job_txt.get()}"

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

                    if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':

                        render_data['injury'] = data['certificate'].get('injury_operation', '')
                        if data['certificate'].get('injury_operation', '') == '-':
                            text_past_illnesses += '\nТравм и операций не было; '
                            render_data['injury'] = '-'
                        if data['certificate'].get('injury_operation', '') == '+':
                            text_past_illnesses += '\nТравмы и операции: '
                            if len(injury_operation_txt.get()) > 1:
                                text_past_illnesses += f'{injury_operation_txt.get()}'
                                data['certificate']['injury'] = f"+\n{injury_operation_txt.get()}"
                                render_data['injury'] = f"{render_data.get('injury')}\n{injury_operation_txt.get()}"

                    if render_data.get('past_illnesses'):
                        render_data['past_illnesses'] = f"{render_data.get('past_illnesses', '').strip()}" \
                                                        f"\n{text_past_illnesses}"
                    else:
                        render_data['past_illnesses'] = text_past_illnesses

                    if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ' \
                        and data['certificate'].get('place_of_requirement') == "ВУЗ (колледж)":
                        render_data['past_illnesses'] = "_____________________________________________"

                if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ', 'В детский лагерь', 'Об усыновлении (удочерении)'):

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
                                if (type_certificate == 'Оформление в ДДУ / СШ / ВУЗ'
                                        and render_data.get('type', '') == 'Оформление в ВУЗ'):
                                    continue
                                messagebox.showerror('Ошибка!', 'Не указана рассадка!')
                            raise ValueError
                    if not weight.get():
                        messagebox.showerror('Ошибка!', 'Не указан вес!')
                        raise ValueError

                    if not height.get():
                        messagebox.showerror('Ошибка!', 'Не указан рост!')
                        raise ValueError

                    if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ', 'В детский лагерь'):
                        render_data['visus'] = f"VIS OD/OS\n= {vision.get()}\n"
                    else:
                        render_data['visus'] = ''

                    render_data["add_diagnosis"] = diagnosis_txt.get(1.0, 'end').strip()
                    render_data['height'] = height.get().replace(',', '.')
                    render_data['weight'] = weight.get().replace(',', '.')
                    render_data['group'] = selected_health_group.get()
                    render_data['physical'] = selected_fiz_group.get()

                    add_med_info = render_data.get('additional_medical_information', '')
                    add_med_info = add_med_info.replace('Рост _____ см', f'Рост {height.get()} см')
                    add_med_info = add_med_info.replace('Вес _____ кг', f'Вес {weight.get()} кг')
                    add_med_info = add_med_info.replace('Vis OD/OS = __________', f"Vis OD/OS = {vision.get()}")
                    add_med_info = add_med_info.replace('АД ________', f'АД {patient_bp.get()} мм.рт.ст.')

                    render_data['additional_medical_information'] = add_med_info

                    render_data['temp'] = patient_temp.get()
                    render_data['br'] = patient_br.get()
                    render_data['hr'] = patient_hr.get()
                    render_data['bp'] = patient_bp.get()


                    diagnosis_cert = render_data.get('diagnosis', '')
                    if type_certificate in ('В детский лагерь',
                                            'Об усыновлении (удочерении)',
                                            'О нуждаемости в сан-кур лечении') \
                            or type_certificate == 'Оформление в ДДУ / СШ / ВУЗ' \
                            and place_of_requirement == 'Кадетское училище':

                        diagnosis_cert = f"{diagnosis_txt.get(1.0, 'end').strip()}\n{diagnosis_cert}"

                    diagnosis_cert = diagnosis_cert.replace('Группа здоровья: _',
                                                            f'Группа здоровья: {selected_health_group.get()}')
                    diagnosis_cert = diagnosis_cert.replace('Группа по физкультуре: _',
                                                            f'Группа по физкультуре: {selected_fiz_group.get()}')
                    render_data['diagnosis'] = diagnosis_cert

                    recommendation = render_data.get('recommendation', '')
                    recommendation = recommendation.replace('Режим _',
                                                            f"Режим {', '.join(data['certificate'].get('regime'))}")
                    render_data['regime'] = ', '.join(data['certificate'].get('regime'))

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

                        if 'Детское Дошкольное Учреждение' in data['certificate'].get('place_of_requirement'):
                            recommendation = recommendation.replace('Парта _', f" Мебель {result}")
                            render_data['desk'] = f"Мебель {result}"
                        else:
                            recommendation = recommendation.replace('Парта _', f" Парта {result}")
                            render_data['desk'] = f"Парта {result}"

                        if render_data.get('place_of_requirement') in ('Средняя школа (гимназия)',
                                                                       'Детское Дошкольное Учреждение'):
                            recommendation = f"{recommendation} Разрешены занятия в бассейне"

                    render_data['recommendation'] = recommendation

                    if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ' or age.get('year') >= 11:
                        render_data['hearing'] = '\nСлух в норме.'
                    else:
                        render_data['hearing'] = ''

                    if age.get('year') >= 4:
                        render_data['posture'] = f"\nОсанка: {posture.get()}."
                    else:
                        render_data['posture'] = ''

                    if 'Физическое развитие (выше- ниже-) среднее, (дис-) гармоничное' in render_data.get(
                            'diagnosis', ''):
                        render_data['diagnosis'] = render_data.get('diagnosis', '').replace(
                                'Физическое развитие (выше- ниже-) среднее, (дис-) гармоничное',
                                f"Физическое развитие: {patient_anthropometry.get().split('--')[-1].strip()}")
                    render_data['anthro'] = patient_anthropometry.get()

                    render_data['imt'] = round(float(render_data.get('weight')) /
                                               (float(render_data.get('height')) / 100) ** 2, 1)

                if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ', 'В детский лагерь'):
                    if age.get('year') < 14:
                        render_data['recommendation'] = render_data.get('recommendation', '') + \
                                "\nНа основании ст. 44 Закона Республики Беларусь от 18.06.1993 №2435-XII  " \
                                "'О здравоохранении' от законного представителя несовершеннолетнего получено устное" \
                                "  предварительное информированное добровольное согласие на оказание медицинской помощи"


                if type_certificate == 'О нуждаемости в сан-кур лечении':
                    render_data['diagnosis'] = f"Имеются медицинские показания и отсутствуют медицинские противопоказания " \
                                               f"к санаторно-курортному лечению по профилю: \n"  + \
                                  '\n'.join(data['certificate'].get('sanatorium_profile'))
                    # render_data['diagnosis'] = diagnosis_txt.get(1.0, 'end').strip()


                if type_certificate == 'ЦКРОиР':

                    result = data['certificate']['type_cert_info'][type_certificate]['ЦКРОиР_add_med_info'].get(1.0, 'end').strip()
                    for doctors in ('Невролог', 'Офтальмолог',  'ЛОР',  'Логопед'):
                        result += f"\n{doctors}: " \
                                  f"{data['certificate']['type_cert_info'][type_certificate][f'{doctors}_txt'].get()}"
                    render_data['additional_medical_information'] = result
                    render_data['diagnosis'] = diagnosis_txt.get(1.0, 'end').strip()



                if not render_data.get('additional_medical_information'):
                    render_data['additional_medical_information'] = '_' * 60
                if not render_data.get('past_illnesses'):
                    render_data['past_illnesses'] = '_' * 60
                if not render_data.get('recommendation'):
                    render_data['recommendation'] = '_' * 50



            except ValueError:
                data['certificate']['type_cert_frames']['selected_cert'].pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)
                canvas_frame.focus()
            else:

                certificate__create_doc()
                certificate_main_root.destroy()

        def diagnosis_healthy():
            for type_cert in data['certificate'].get('type_cert_info'):
                if data['certificate']['type_cert_info'][type_cert].get('diagnosis_txt'):
                    diagnosis = data['certificate']['type_cert_info'][type_cert].get('diagnosis_txt')
                    diagnosis.delete(1.0, 'end')
                    if patient.get('gender', '') == 'женский':
                        diagnosis.insert(INSERT, 'Соматически здорова. ')
                    else:
                        diagnosis.insert(INSERT, 'Соматически здоров. ')
            selected_health_group.set('1')
            selected_fiz_group.set('Основная')
            selected_diet.set('Б')
            for marker in regime_vars:
                if marker == 'общий':
                    regime_vars[marker].set(1)
                else:
                    regime_vars[marker].set(0)
            for marker in desk_vars:
                if marker == 'по росту':
                    desk_vars[marker].set(1)
                else:
                    desk_vars[marker].set(0)

            data['certificate']['health_group'] = selected_health_group.get()
            data['certificate']['physical'] = selected_fiz_group.get()
            data['certificate']['regime'] = ["общий"]
            data['certificate']['diet'] = selected_diet.get()
            data['certificate']['desk'] = ["по росту"]

        def select_health():
            for mark, var in (('health_group', selected_health_group),
                              ('physical', selected_fiz_group),
                              ('diet', selected_diet)):
                if var.get():
                    data['certificate'][mark] = var.get()


            for mark, var in (('regime', regime_vars),
                              ('desk', desk_vars),):
                result = list()
                for marker in all_data_certificate.get('health').get(mark):
                    if var.get(marker).get() == 1:
                        result.append(marker)
                data['certificate'][mark] = result

        def diagnosis_kb():
            def select_diagnosis():
                for type_cert in data['certificate'].get('type_cert_info'):
                    if data['certificate']['type_cert_info'][type_cert].get('diagnosis_txt'):
                        diagnosis_txt = data['certificate']['type_cert_info'][type_cert].get('diagnosis_txt')
                        diagnosis_txt.insert(INSERT, f" {selected_button.get()}")

            if data['certificate'].get('is_diagnosis_kb_open'):
                data['certificate']['is_diagnosis_kb_open'] = False
                for type_cert in data['certificate'].get('type_cert_info'):
                    if data['certificate']['type_cert_info'][type_cert].get('diagnosis_kb_frame'):
                        but = data['certificate']['type_cert_info'][type_cert].get('diagnosis_main_but')
                        but['text'] = "Открыть клавиатуру диагнозов"

                        frame = data['certificate']['type_cert_info'][type_cert].get('diagnosis_kb_frame')
                        frame.pack_forget()
                        frame.destroy()
            else:
                data['certificate']['is_diagnosis_kb_open'] = True
                for type_cert in data['certificate'].get('type_cert_info'):
                    if data['certificate']['type_cert_info'][type_cert].get('diagnosis_frame'):
                        but = data['certificate']['type_cert_info'][type_cert].get('diagnosis_main_but')
                        but['text'] = "Закрыть клавиатуру диагнозов"

                        diagnosis_frame = data['certificate']['type_cert_info'][type_cert].get('diagnosis_frame')
                        diagnosis_kb_frame = Frame(diagnosis_frame, bg="#36566d")
                        diagnosis_kb_frame.pack(fill='both', expand=True, padx=3, pady=3)
                        data['certificate']['type_cert_info'][type_cert]['diagnosis_kb_frame'] = diagnosis_kb_frame
                        for tuple_diagnosis in all_data_certificate.get('diagnosis'):
                            Label(diagnosis_kb_frame, text=tuple_diagnosis[0],
                                  font=('Comic Sans MS', user.get('text_size')),
                                  bg='white'
                                  ).pack(fill='both', expand=True)
                            frame = Frame(diagnosis_kb_frame)

                            for diagnosis_name in tuple_diagnosis[1:]:
                                if diagnosis_name == '_':
                                    frame.pack(fill='both', expand=True)
                                    frame = Frame(diagnosis_kb_frame)
                                else:
                                    Radiobutton(frame, text=diagnosis_name,
                                                font=('Comic Sans MS', user.get('text_size')),
                                                value=diagnosis_name,
                                                variable=selected_button,
                                                command=select_diagnosis,
                                                indicatoron=False, selectcolor='#77f1ff'
                                                ).pack(fill='both', expand=True, side='left')

        def paste_calendar():
            if data['certificate'].get('calendar_root'):
                data['certificate']['calendar_root'].destroy()


            command, marker = selected_button.get().split('__')

            calendar_root = Toplevel()
            data['certificate']['calendar_root'] = calendar_root
            calendar_root.title(f'Календарь {marker}')
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
                data['certificate']['calendar_root'] = None
                day = selected_day.get()
                edit_day = list()
                for i in day.split('.'):
                    if len(i) == 1:
                        i = f"0{i}"
                    edit_day.append(i)
                answer = '.'.join(edit_day)
                if command == 'ori_from':
                    ori_from.set(answer)

                elif command == 'ori_until':
                    ori_until.set(answer)

                elif command == 'ori_home_regime':
                    ori_home_regime.set(answer)

                elif command == 'ori_add_to_childhood':
                    ori_add_to_childhood.set(answer)

                elif command == 'date_of_issue':
                    date_of_issue.set(answer)

                elif command.startswith('validity_period'):
                    type_cert = command.split('-')[-1]
                    var = data['certificate']['type_cert_info'][type_cert].get('validity_period')
                    var.set(answer)


                elif command.startswith('ЦКРОиР'):
                    marker = command.split('-')[-1]
                    var = data['certificate']['type_cert_info']["ЦКРОиР"].get(marker)
                    var.set(f"{answer} - {var.get()}")

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

        def paste_bp():

            indicators = {
                '0-3': {
                    'br': (24, 28),
                    'hr': (90, 100),
                    'bp': (90, 100, 60, 70)},
                '3-6': {
                    'br': (22, 28),
                    'hr': (80, 90),
                    'bp': (96, 110, 60, 70)},
                '6-12': {
                    'br': (20, 24),
                    'hr': (70, 90),
                    'bp': (100, 110, 60, 75)},
                '>12': {
                    'br': (18, 22),
                    'hr': (70, 80),
                    'bp': (110, 120, 70, 78)},
            }

            if age.get('year') <= 3:
                indicator = indicators['0-3']
            elif age.get('year') <= 6:
                indicator = indicators['3-6']
            elif age.get('year') <= 12:
                indicator = indicators['6-12']
            else:
                indicator = indicators['>12']

            patient_temp.set(random.choice(['36,6', '36,7', '36,5']))
            patient_br.set(random.randrange(start=indicator['br'][0], stop=indicator['br'][1], step=2))
            patient_hr.set(random.randrange(start=indicator['hr'][0], stop=indicator['hr'][1], step=2))
            patient_bp.set(f"{random.randrange(start=indicator['bp'][0], stop=indicator['bp'][1], step=1)}/"
                           f"{random.randrange(start=indicator['bp'][2], stop=indicator['bp'][3], step=1)}")

        def check_anthro(num, marker):
            if num:
                num = num.replace(',', '.')
                try:
                    float(num)
                except ValueError:
                    return False
            height_var, weight_var = None, None
            if marker == 'height':
                height_var, weight_var = num.replace(',', '.'), weight.get().replace(',', '.')
            elif marker == 'weight':
                weight_var, height_var = num.replace(',', '.'), height.get().replace(',', '.')
            if weight_var:
                weight_var = float(weight_var)
            if height_var:
                height_var = float(height_var)

            patient_anthropometry.set(
                patient_anthro(marker_age_y='после года',
                               marker_age=age.get('year'),
                               height=height_var,
                               weight=weight_var)
            )
            return True

        def select_chickenpox():
            data['certificate']['chickenpox'] = selected_chickenpox.get()

        def select_allergy():
            data['certificate']['allergy'] = selected_allergy.get()
            if selected_allergy.get() == '+':
                if not data['certificate'].get('is_frame_allergy_open'):
                    data['certificate']['is_frame_allergy_open'] = True
                    for type_cert in data['certificate'].get('type_cert_info'):
                        if data['certificate']['type_cert_info'][type_cert].get('frame_allergy'):
                            frame_allergy = data['certificate']['type_cert_info'][type_cert].get(
                                'frame_allergy')
                            frame = Frame(frame_allergy, borderwidth=1, relief="solid", padx=2, pady=2)
                            Label(frame, text="Аллергия на:",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  bg='white').pack(fill='both', expand=True, side='left')
                            Entry(frame, width=60, textvariable=allergy_txt,
                                  font=('Comic Sans MS', user.get('text_size'))
                                  ).pack(fill='both', expand=True, side='left')
                            frame.pack(fill='both', expand=True)
                            data['certificate']['type_cert_info'][type_cert]['frame_allergy_txt'] = frame


            else:
                if data['certificate'].get('is_frame_allergy_open'):
                    data['certificate']['is_frame_allergy_open'] = False
                    for type_cert in data['certificate'].get('type_cert_info'):
                        if data['certificate']['type_cert_info'][type_cert].get('frame_allergy_txt'):
                            frame = data['certificate']['type_cert_info'][type_cert].get('frame_allergy_txt')
                            frame.pack_forget()
                            frame.destroy()
                            data['certificate']['type_cert_info'][type_cert]['frame_allergy_txt'] = False

        def select_injury_operation():
            data['certificate']['injury_operation'] = selected_injury_operation.get()
            if selected_injury_operation.get() == '+':
                if not data['certificate'].get('is_frame_injury_open'):
                    data['certificate']['is_frame_injury_open'] = True
                    for type_cert in data['certificate'].get('type_cert_info'):
                        if data['certificate']['type_cert_info'][type_cert].get('frame_injury'):
                            frame_allergy = data['certificate']['type_cert_info'][type_cert].get(
                                'frame_injury')
                            frame = Frame(frame_allergy, borderwidth=1, relief="solid", padx=2, pady=2)
                            Label(frame, text="Травмы и операции:",
                                  font=('Comic Sans MS', user.get('text_size')),
                                  bg='white').pack(fill='both', expand=True, side='left')
                            Entry(frame, width=60, textvariable=injury_operation_txt,
                                  font=('Comic Sans MS', user.get('text_size'))
                                  ).pack(fill='both', expand=True, side='left')
                            frame.pack(fill='both', expand=True)
                            data['certificate']['type_cert_info'][type_cert]['frame_injury_txt'] = frame


            else:
                if data['certificate'].get('is_frame_injury_open'):
                    data['certificate']['is_frame_injury_open'] = False
                    for type_cert in data['certificate'].get('type_cert_info'):
                        if data['certificate']['type_cert_info'][type_cert].get('frame_injury_txt'):
                            frame = data['certificate']['type_cert_info'][type_cert].get('frame_injury_txt')
                            frame.pack_forget()
                            frame.destroy()
                            data['certificate']['type_cert_info'][type_cert]['frame_injury_txt'] = False

        def select_posture():
            data['certificate']['posture'] = posture.get()


        def upload_last_data():
            found_info = data_base(command='certificate__upload_last_data')
            local_info = {
                'select_past_examination': list(),
                'get_last_anthro_data': dict(),

            }
            flags = {
                'chickenpox_allergy_injury': False,
                'health_physical_group': False,
                'diagnosis_txt': False,
                'patient_anthro': False,
                'ЦКРОиР_add_med_info': False,
                'ЦКРОиР_add_med_info_doctors': False,
                'last_patient_specialties': False,
                'break': False
            }
            variables = {
                'chickenpox_allergy_injury': {
                    'chickenpox': selected_chickenpox,
                    'allergy': selected_allergy,
                    'injury_operation': selected_injury_operation,
                    'allergy_txt': allergy_txt,
                    'injury_txt': injury_operation_txt},
                'health_physical_group': {
                    'health_group': selected_health_group,
                    'physical': selected_fiz_group,
                    'diet': selected_diet,
                    'regime': regime_vars,
                    'desk': desk_vars},
                'patient_anthro': {
                    'height': height,
                    'weight': weight,
                    'vision': vision
                }

            }

            if found_info.get('select_past_examination'):
                for rowid, examination_key in sorted(found_info.get('select_past_examination'),
                                                     key=lambda i: (datetime.now() -
                                                                    datetime.strptime(f"{i[0]}",
                                                                                      "%d.%m.%Y %H:%M:%S")).total_seconds()):

                    for string in examination_key.split('__<end!>__\n'):
                        if string.startswith('chickenpox_allergy_injury:____'):
                            if not flags.get('chickenpox_allergy_injury'):
                                flags['chickenpox_allergy_injury'] = True
                                string = string.replace('chickenpox_allergy_injury:____', '').split('____')
                                for marker in string:
                                    if len(marker.split('__')) == 2:
                                        var_name, info = marker.split('__')
                                        if variables['chickenpox_allergy_injury'].get(var_name):
                                            variable = variables['chickenpox_allergy_injury'].get(var_name)
                                            variable.set(info)
                                select_chickenpox()
                                select_allergy()
                                select_injury_operation()

                        elif string.startswith('health_physical_group:____'):
                            if not flags.get('health_physical_group'):
                                flags['health_physical_group'] = True
                                for marker in string.replace('health_physical_group:____', '').split('____'):
                                    if len(marker.split('__')) == 2:
                                        var_name, info = marker.split('__')
                                        if var_name in ('health_group', 'physical', 'diet'):
                                            if variables['health_physical_group'].get(var_name):
                                                variable = variables['health_physical_group'].get(var_name)
                                                variable.set(info)

                                        elif var_name in ('regime', 'desk'):
                                            variable = variables['health_physical_group'].get(var_name)
                                            if variable.get(info):
                                                variable[info].set(1)

                                        elif var_name == 'posture':
                                            posture.set(info)







                                select_health()

                        elif string.startswith('diagnosis_txt:____'):
                            if not flags.get('diagnosis_txt'):
                                flags['diagnosis_txt'] = True
                                text = string.replace('diagnosis_txt:____', '')
                                for type_certificate in data['certificate'].get('type_cert_info'):
                                    if data['certificate']['type_cert_info'][type_certificate].get('diagnosis_txt'):
                                        diagnosis_txt = data['certificate']['type_cert_info'][type_certificate].get(
                                            'diagnosis_txt')
                                        diagnosis_txt.insert(1.0, text)

                        elif string.startswith('last_patient_specialties:____'):
                            if not flags.get('last_patient_specialties'):
                                flags['last_patient_specialties'] = True
                                text = string.replace('last_patient_specialties:____', '')
                                data['certificate']['last_patient_specialties'] = text


                        elif string.startswith('patient_anthro:____'):
                            if not flags.get('patient_anthro'):
                                flags['patient_anthro'] = True
                                chickenpox_variables = ()

                                for marker in string.replace('patient_anthro:____', '').split('____'):
                                    if len(marker.split('__')) == 2:
                                        var_name, info = marker.split('__')
                                        if variables['patient_anthro'].get(var_name):
                                            variable = variables['patient_anthro'].get(var_name)
                                            variable.set(info)

                        elif string.startswith('ЦКРОиР_add_med_info'):

                            if string.startswith('ЦКРОиР_add_med_info:____'):
                                if not flags.get('ЦКРОиР_add_med_info'):
                                    flags['ЦКРОиР_add_med_info'] = True
                                    text = string.replace('ЦКРОиР_add_med_info:____', '')
                                    add_med_info = data['certificate']['type_cert_info']['ЦКРОиР'].get(
                                        'ЦКРОиР_add_med_info')
                                    add_med_info.delete(1.0, 'end')
                                    add_med_info.insert(1.0, text)

                            elif string.startswith('ЦКРОиР_add_med_info_doctors:____'):
                                if not flags.get('ЦКРОиР_add_med_info_doctors'):
                                    flags['ЦКРОиР_add_med_info_doctors'] = True
                                    for marker in string.replace('ЦКРОиР_add_med_info_doctors:____', '').split(
                                            '__!__'):
                                        if len(marker.split('____')) == 2:
                                            var_name, info = marker.split('____')
                                            data['certificate']['type_cert_info']['ЦКРОиР'][f'{var_name}_txt'].set(
                                                info)

                    flags['break'] = True
                    for flag in flags:
                        if not flags.get(flag):
                            flags['break'] = False
                    if flags.get('break'):
                        break

        paste_bp()
        for type_certificate in all_data_certificate.get('type'):
            def paste_diagnosis_frame():
                frame_diagnosis = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                frame = Frame(frame_diagnosis)
                Label(frame, text="Диагноз:",
                      font=('Comic Sans MS', user.get('text_size')), bg='white'
                      ).pack(fill='both', expand=True, side='left')
                Button(frame, text='Здоров', command=diagnosis_healthy,
                       font=('Comic Sans MS', user.get('text_size'))
                       ).pack(fill='both', expand=True, side='left')
                but = Button(frame, text='Открыть клавиатуру диагнозов', command=diagnosis_kb,
                           font=('Comic Sans MS', user.get('text_size')))
                data['certificate']['type_cert_info'][type_certificate]['diagnosis_main_but'] = but
                but.pack(fill='both', expand=True, side='left')
                frame.pack(fill='both', expand=True, padx=2, pady=2)

                frame = Frame(frame_diagnosis)
                diagnosis = ScrolledText(frame, width=80, height=4,
                                         font=('Comic Sans MS', user.get('text_size')), wrap="word")
                diagnosis.pack(fill='both', expand=True)
                data['certificate']['type_cert_info'][type_certificate]['diagnosis_txt'] = diagnosis
                data['certificate']['type_cert_info'][type_certificate]['diagnosis_frame'] = frame

                frame.pack(fill='both', expand=True, padx=2, pady=2)
                frame_diagnosis.pack(fill='both', expand=True, padx=2, pady=2)

            data['certificate']['type_cert_info'][type_certificate] = dict()

            master_frame = Frame(canvas_frame, bg="#36566d")
            data['certificate']['type_cert_frames'][type_certificate] = master_frame

            Label(master=master_frame,
                  text=type_certificate,
                  font=('Comic Sans MS', user.get('text_size')),
                  bg="#36566d",
                  fg='white'
                  ).pack(fill='both', expand=True, padx=2, pady=2, ipadx=2, ipady=2)

            if not all_data_certificate['all_info'].get(type_certificate).get('place_of_requirement'):
                def select_place():
                    type_cert, place = selected_place.get().split('__')
                    data['certificate']['place_of_requirement'] = place
                    label_place_text.set(f"Место требования справки: {place}")

                    if type_cert == "Оформление в ДДУ / СШ / ВУЗ" and place == 'ВУЗ (колледж)':
                        data['certificate']['type_cert_info'][type_cert]['validity_period'].set('1 год')

                        if not data['certificate'].get('frame_specialties'):
                            frame_place = data['certificate']['type_cert_info'][type_cert].get("frame_place")
                            frame_specialties = Frame(master=frame_place,
                                          borderwidth=1, relief="solid", padx=4, pady=4)
                            data['certificate']['frame_specialties'] = frame_specialties
                            frame = Frame(frame_specialties)
                            specialties_txt = ScrolledText(frame, width=80, height=4,
                                                           font=('Comic Sans MS', user.get('text_size')),
                                                           wrap="word")
                            if data['certificate'].get('last_patient_specialties'):
                                specialties_txt.insert(1.0, data['certificate'].get('last_patient_specialties'))
                            data['certificate']['specialties_txt'] = specialties_txt
                            Label(frame, text="Специальности для поступления:",
                                  font=('Comic Sans MS', user.get('text_size')), bg='white'
                                  ).pack(fill='both', expand=True, padx=2, pady=2)
                            specialties_txt.pack(fill='both', expand=True, padx=2, pady=2)
                            frame.pack(fill='both', expand=True, padx=2, pady=2)
                            frame_specialties.pack(fill='both', expand=True, padx=2, pady=2)

                    else:
                        if data['certificate'].get('frame_specialties'):
                            data['certificate']['last_patient_specialties'] = \
                                data['certificate']['specialties_txt'].get(1.0, 'end').strip()
                            data['certificate']['frame_specialties'].pack_forget()
                            data['certificate']['frame_specialties'] = None
                        if type_cert == "Оформление в ДДУ / СШ / ВУЗ":
                            if place == 'Кадетское училище':
                                data['certificate']['type_cert_info'][type_cert]['validity_period'].set('3 месяца')
                            else:
                                    data['certificate']['type_cert_info'][type_cert]['validity_period'].set('1 год')



                frame_place = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                data['certificate']['type_cert_info'][type_certificate]['frame_place'] = frame_place

                place = all_data_certificate.get('place')
                if type_certificate == 'Оформление в ДДУ / СШ / ВУЗ':
                    place = ('Детское Дошкольное Учреждение',
                             'Средняя школа (гимназия)',
                             'ВУЗ (колледж)', 'Кадетское училище')
                if type_certificate == 'ЦКРОиР':
                    place = ('Для логопедической комиссии (ЦКРОиР)',
                             'Ресурсный центр раннего вмешательства')

                Label(frame_place, textvariable=label_place_text,
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white').pack(fill='both', expand=True, padx=2, pady=2)


                frame_place_1 = Frame(frame_place, padx=4, pady=4)

                row, col = 0, 0
                for mark in place:
                    btn = Radiobutton(frame_place_1, text=mark,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      value=f"{type_certificate}__{mark}",
                                      variable=selected_place, command=select_place,
                                      indicatoron=False, selectcolor='#77f1ff')
                    btn.grid(row=row, column=col, sticky='ew')
                    col += 1
                    if col == 3:
                        row += 1
                        col = 0

                    frame_place_1.columnconfigure(index='all', minsize=40, weight=1)
                    frame_place_1.rowconfigure(index='all', minsize=20)
                    frame_place_1.pack(fill='both', expand=True, padx=2, pady=2)

                frame_place.columnconfigure(index='all', minsize=40, weight=1)
                frame_place.rowconfigure(index='all', minsize=20)
                frame_place.pack(fill='both', expand=True, padx=2, pady=2)

            if type_certificate in ('На кружки и секции', 'Может работать по специальности...'):
                def save_new_hobby():
                    if not new_hobby_txt.get():
                        messagebox.showerror('Ошибка', "Не указан кружок / секция для сохранения")
                    else:
                        if data_base(command='save_new_hobby',
                                     insert_data=[user.get('doctor_name'), new_hobby_txt.get()]):

                            messagebox.showinfo('Инфо', "Секция сохранена в избранное\n")
                            certificate_main_root.destroy()
                        else:
                            messagebox.showinfo('Инфо', "Ошибка при сохранении")

                def append_hobby():
                    if selected_button.get() == '+ СОРЕВНОВАНИЯ':
                        if hobby_txt.get():
                            hobby_txt.set(f"{hobby_txt.get()} и участия в соревнованиях")
                        else:
                            hobby_txt.set("участия в соревнованиях по ")
                    else:
                        if hobby_txt.get():
                            hobby_txt.set(f"{hobby_txt.get()}, {selected_button.get()}")
                        else:
                            hobby_txt.set(f"{selected_button.get()}")

                def delete_new_hobby():
                    if not user.get('my_sport_section'):
                        messagebox.showinfo('Инфо', "Нет сохраненных данных")

                    else:
                        def delete_sport_section():
                            if data_base(command='delete_sport_section',
                                         delete_data=selected_delete_sport_section.get()):
                                messagebox.showinfo("Инфо", "Запись удалена")
                                delete_new_hobby_root.destroy()
                                delete_new_hobby()
                            else:
                                messagebox.showerror("Ошибка", "Запись не удалена")

                        delete_new_hobby_root = Toplevel()
                        delete_new_hobby_root.title('Удаление секций')
                        delete_new_hobby_root.config(bg='white')

                        selected_delete_sport_section = StringVar()

                        Label(delete_new_hobby_root, text="Выберите секцию для удаления",
                              font=('Comic Sans MS', user.get('text_size')),
                              bg='white').pack(fill='both', expand=True, padx=2, pady=2)
                        frame_delete_new_hobby = Frame(delete_new_hobby_root, borderwidth=1,
                                                       relief="solid", padx=4, pady=4)

                        col_, row_ = 0, 0
                        for sport_section in user.get('my_sport_section'):
                            if not isinstance(sport_section, str):
                                sport_section = sport_section[0]

                            Radiobutton(frame_delete_new_hobby, text=sport_section,
                                        font=('Comic Sans MS', user.get('text_size')),
                                        value=f"{sport_section}", variable=selected_delete_sport_section,
                                        command=delete_sport_section, indicatoron=False,
                                        selectcolor='#77f1ff').grid(row=row_, column=col_, sticky='ew')
                            col_ += 1
                            if col_ == 5:
                                col_ = 0
                                row_ += 1
                        frame_delete_new_hobby.columnconfigure(index='all', minsize=40, weight=1)
                        frame_delete_new_hobby.rowconfigure(index='all', minsize=20)
                        frame_delete_new_hobby.pack(fill='both', expand=True, padx=2, pady=2)

                if type_certificate == 'На кружки и секции':
                    frame_section = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)

                    frame = Frame(frame_section, borderwidth=1, relief="solid")
                    Label(frame, text='Не имеется медицинских противопоказаний для занятия:',
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').pack(fill='both', expand=True)
                    Entry(frame, textvariable=hobby_txt,
                          width=150, font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True)
                    frame.pack(fill='both', expand=True, padx=2, pady=2)



                    if user.get('my_sport_section'):
                        row, col = 0, 0
                        frame = Frame(frame_section, borderwidth=1, relief="solid")
                        Label(frame, text='Мои кружки и секции',
                              font=('Comic Sans MS', user.get('text_size')),
                              bg='white').grid(row=0, column=0, sticky='ew')

                        col += 1
                        for mark in user.get('my_sport_section'):
                            mark = mark[0]
                            btn = Radiobutton(frame, text=mark,
                                              font=('Comic Sans MS', user.get('text_size')),
                                              value=f"{mark}",
                                              variable=selected_button, command=append_hobby,
                                              indicatoron=False, selectcolor='#77f1ff')
                            btn.grid(ipadx=2, ipady=2, padx=2, pady=2, sticky='ew', row=row, column=col)

                            col += 1
                            if col == 5:
                                col = 0
                                row += 1

                        Button(frame, text='Редактировать мой список',
                               command=delete_new_hobby,
                               font=('Comic Sans MS', user.get('text_size'))
                               ).grid(padx=2, pady=2, sticky='ew', row=row, column=col)

                        frame.columnconfigure(index='all', minsize=40, weight=1)
                        frame.rowconfigure(index='all', minsize=20)
                        frame.pack(fill='both', expand=True, padx=2, pady=2)

                    frame_but = Frame(frame_section, borderwidth=1, relief="solid")

                    for mark_group in all_data_certificate.get('sport_section'):
                        frame = Frame(frame_but)
                        for mark in mark_group:

                            Radiobutton(frame, text=mark,
                                      font=('Comic Sans MS', user.get('text_size')),
                                      value=f"{mark}",
                                      variable=selected_button, command=append_hobby,
                                      indicatoron=False, selectcolor='#77f1ff'
                                        ).pack(fill='both', expand=True, side='left')

                        frame.columnconfigure(index='all', minsize=40, weight=1)
                        frame.rowconfigure(index='all', minsize=20)
                        frame.pack(fill='both', expand=True, padx=2, pady=2)
                    frame_but.pack(fill='both', expand=True, padx=2, pady=2)

                    frame = Frame(frame_section, borderwidth=1, relief="solid")
                    Label(frame, text="Добавить кружок в избранное: ",
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').pack(fill='both', expand=True, side='left')
                    Entry(frame, textvariable=new_hobby_txt,
                          width=50, font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True, side='left')
                    Button(frame, text='Сохранить', command=save_new_hobby,
                           font=('Comic Sans MS', user.get('text_size'))
                           ).pack(fill='both', expand=True, side='left')
                    frame.pack(fill='both', expand=True, padx=2, pady=2)

                    frame_section.pack(fill='both', expand=True, padx=2, pady=2)

                    paste_diagnosis_frame()
                    for txt, marker, variable in (('Группа здоровья', 'group', selected_health_group),
                                                  ('Группа по физ-ре', 'physical', selected_fiz_group)):
                        frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)

                        Label(frame, text=f"{txt}:",
                              font=('Comic Sans MS', user.get('text_size')), bg='white'
                              ).pack(fill='both', expand=True, side='left')

                        for mark in all_data_certificate.get('health').get(marker):
                            Radiobutton(frame, text=mark,
                                        font=('Comic Sans MS', user.get('text_size')),
                                        value=mark, variable=variable,
                                        command=select_health, indicatoron=False, selectcolor='#77f1ff'
                                        ).pack(fill='both', expand=True, side='left')
                        frame.pack(fill='both', expand=True, padx=2, pady=2)


                else:
                    frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                    Label(frame, text='Может работать по специальности:',
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').pack(fill='both', expand=True, side='left')

                    Entry(frame, textvariable=job_txt, width=70,
                          font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True, side='left')
                    frame.pack(fill='both', expand=True, padx=2, pady=2)

                    paste_diagnosis_frame()
                    for txt, marker, variable in (('Группа здоровья', 'group', selected_health_group),
                                                  ('Группа по физ-ре', 'physical', selected_fiz_group)):
                        frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)

                        Label(frame, text=f"{txt}:",
                              font=('Comic Sans MS', user.get('text_size')), bg='white'
                              ).pack(fill='both', expand=True, side='left')

                        for mark in all_data_certificate.get('health').get(marker):
                            Radiobutton(frame, text=mark,
                                        font=('Comic Sans MS', user.get('text_size')),
                                        value=mark, variable=variable,
                                        command=select_health, indicatoron=False, selectcolor='#77f1ff'
                                        ).pack(fill='both', expand=True, side='left')
                        frame.pack(fill='both', expand=True, padx=2, pady=2)

            if type_certificate == 'По выздоровлении':
                def selected_combo_diagnosis(event=None):
                    if combo_diagnosis.get() == 'ребенок был в поликлинике на приеме у педиатра':
                        ori_until.set(datetime.now().strftime('%d.%m.%Y до %H:%M'))
                    else:
                        ori_until.set(datetime.now().strftime('%d.%m.%Y'))


                frame_ori = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)

                frame = Frame(frame_ori)
                Label(frame, text="Диагноз:", font=('Comic Sans MS', user.get('text_size')),
                      bg='white').pack(fill='both', expand=True, padx=2, pady=2, side='left')

                combo_diagnosis = Combobox(frame, width=40,
                                           font=('Comic Sans MS', user.get('text_size')))
                combo_diagnosis['values'] = ['ОРИ', "ФРК", "Ветряная оспа",
                                             "ребенок был в поликлинике на приеме у педиатра",
                                             "ребенок был в поликлинике для вакцинации",
                                             "лечение в стационаре"]
                combo_diagnosis.current(0)
                data['certificate']['combo_diagnosis'] = combo_diagnosis
                combo_diagnosis.bind("<<ComboboxSelected>>", selected_combo_diagnosis)

                combo_diagnosis.pack(fill='both', expand=True, padx=2, pady=2, side='left')
                frame.pack(fill='both', expand=True, padx=2, pady=2)

                frame = Frame(frame_ori)

                Label(frame, text="c",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white').pack(fill='both', expand=True, padx=2, pady=2, side='left')
                Entry(frame, width=15, textvariable=ori_from,
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True, padx=2, pady=2, side='left')
                # Label(frame,
                #       text='',
                #       image=user.get('сalendar_img'),
                #       compound='bottom'
                #       ).pack(fill='both', expand=True, side='left')

                Radiobutton(frame, image=user.get('сalendar_img'),
                            font=('Comic Sans MS', user.get('text_size')),
                            value="ori_from__Болеет с ...",
                            variable=selected_button,
                            command=paste_calendar,
                            indicatoron=False, selectcolor='#77f1ff'
                            ).pack(side='left')

                Label(frame, text="по",
                      font=('Comic Sans MS', user.get('text_size')), bg='white',
                      compound="center").pack(fill='both', expand=True, padx=2, pady=2, side='left')
                Entry(frame, width=15, textvariable=ori_until,
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True, padx=2, pady=2, side='left')
                ori_until.set(datetime.now().strftime("%d.%m.%Y"))

                Radiobutton(frame, image=user.get('сalendar_img'),
                            font=('Comic Sans MS', user.get('text_size')),
                            value="ori_until__Болеет по ...",
                            variable=selected_button,
                            command=paste_calendar,
                            indicatoron=False, selectcolor='#77f1ff'
                            ).pack(side='left')
                frame.pack(fill='both', expand=True, padx=2, pady=2)

                frame = Frame(frame_ori)
                Label(frame, text="Домашний режим до (включительно):",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white', compound="center").pack(fill='both', expand=True, padx=2, pady=2, side='left')
                Entry(frame, width=15, textvariable=ori_home_regime,
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True, padx=2, pady=2, side='left')
                Radiobutton(frame, image=user.get('сalendar_img'),
                            font=('Comic Sans MS', user.get('text_size')),
                            value="ori_home_regime__Домашний режим до ...",
                            variable=selected_button,
                            command=paste_calendar,
                            indicatoron=False, selectcolor='#77f1ff'
                            ).pack(side='left')

                frame.pack(fill='both', expand=True, padx=2, pady=2)

                frame = Frame(frame_ori)

                Label(frame, text="Допуск в детский коллектив с",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white', compound="center").pack(fill='both', expand=True, padx=2, pady=2, side='left')
                Entry(frame, width=15, textvariable=ori_add_to_childhood,
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True, padx=2, pady=2, side='left')
                Radiobutton(frame, image=user.get('сalendar_img'),
                            font=('Comic Sans MS', user.get('text_size')),
                            value="ori_add_to_childhood__Допуск в детский коллектив с ...",
                            variable=selected_button,
                            command=paste_calendar,
                            indicatoron=False, selectcolor='#77f1ff'
                            ).pack(side='left')

                frame.pack(fill='both', expand=True, padx=2, pady=2)

                frame = Frame(frame_ori)
                Label(frame, text="Освобождение от физкультуры на (дней):",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white', compound="center").pack(fill='both', expand=True, padx=2, pady=2, side='left')


                Entry(frame, width=15, textvariable=ori_fizra_days,
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True, padx=2, pady=2, side='left')
                ori_fizra_days.set('семь')

                frame.pack(fill='both', expand=True, padx=2, pady=2)


                frame_ori.columnconfigure(index='all', minsize=40, weight=1)
                frame_ori.rowconfigure(index='all', minsize=20)
                frame_ori.pack(fill='both', expand=True, padx=2, pady=2)

            if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ', 'В детский лагерь',
                                    'Об усыновлении (удочерении)', 'Об отсутствии контактов', 'Бесплатное питание',
                                    'О нуждаемости в сан-кур лечении', 'Эпикриз 15 лет', 'Эпикриз 18 лет'):


                frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                Label(frame, text="Ветрянка:",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white').pack(fill='both', expand=True, side='left')


                for mark in ["+", "-", "привит"]:
                    Radiobutton(frame, text=mark,
                                font=('Comic Sans MS', user.get('text_size')),
                                value=mark, variable=selected_chickenpox, command=select_chickenpox,
                                indicatoron=False, selectcolor='#77f1ff'
                                ).pack(fill='both', expand=True, side='left')

                frame.pack(fill='both', expand=True, padx=2, pady=2)

                frame_allergy = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                frame = Frame(frame_allergy)
                data['certificate']['type_cert_info'][type_certificate]['frame_allergy'] = frame_allergy
                data['certificate']['type_cert_info'][type_certificate]['frame_allergy_txt'] = False

                Label(frame, text="Аллергия:", font=('Comic Sans MS', user.get('text_size')),
                      bg='white').pack(fill='both', expand=True, side='left')

                for mark in ["-", "+"]:
                    Radiobutton(frame, text=mark,
                                font=('Comic Sans MS', user.get('text_size')),
                                value=f"{mark}",
                                variable=selected_allergy, command=select_allergy,
                                indicatoron=False, selectcolor='#77f1ff'
                                ).pack(fill='both', expand=True, side='left')
                frame.pack(fill='both', expand=True)
                frame_allergy.pack(fill='both', expand=True, padx=2, pady=2)

                if type_certificate in ('Оформление в ДДУ / СШ / ВУЗ', 'Эпикриз 15 лет', 'Эпикриз 18 лет'):

                    frame_injury_operation = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                    data['certificate']['type_cert_info'][type_certificate]['frame_injury'] = frame_injury_operation
                    data['certificate']['type_cert_info'][type_certificate]['frame_injury_txt'] = False

                    frame = Frame(frame_injury_operation, borderwidth=1, relief="solid", padx=2, pady=2)
                    Label(frame, text="Травмы и операции:",
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').pack(fill='both', expand=True, side='left')
                    for mark in ("-", "+"):
                        Radiobutton(frame, text=mark,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    value=f"{mark}",
                                    variable=selected_injury_operation,
                                    command=select_injury_operation,
                                    indicatoron=False, selectcolor='#77f1ff'
                                    ).pack(fill='both', expand=True, side='left')

                    frame.pack(fill='both', expand=True, padx=2, pady=2)
                    frame_injury_operation.pack(fill='both', expand=True, padx=2, pady=2)

                if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ',
                                        'В детский лагерь', 'Об усыновлении (удочерении)'):

                    frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                    Label(frame, text="Осанка:",
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').pack(fill='both', expand=True, side='left')


                    for mark in ["в норме", "нарушена", "ГПС"]:
                        Radiobutton(frame, text=mark,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    value=mark, variable=posture, command=select_posture,
                                    indicatoron=False, selectcolor='#77f1ff'
                                    ).pack(fill='both', expand=True, side='left')

                    frame.pack(fill='both', expand=True, padx=2, pady=2)

            if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ', 'В детский лагерь',
                                    'Об усыновлении (удочерении)', 'Эпикриз 15 лет', 'Эпикриз 18 лет'):

                frame_body = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                frame = Frame(frame_body, borderwidth=1, relief="solid", padx=2, pady=2)
                for text, var in (('ЧД:', patient_br),
                                          ('    ЧСС:', patient_hr),
                                          ('    Температура:', patient_temp)):
                    Label(frame, text=text, bg='white',
                          font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True, side='left')

                    Entry(frame, width=10, textvariable=var,
                          font=('Comic Sans MS', user.get('text_size')),
                          justify="center",
                          ).pack(fill='both', expand=True, side='left')

                frame.pack(fill='both', expand=True, padx=2, pady=2)

                frame = Frame(frame_body, borderwidth=1, relief="solid", padx=2, pady=2)

                for text, marker, var in (('Рост (см):', 'height', height),
                                          ('    Вес (кг):', 'weight', weight)):
                    check = (certificate_main_root.register(check_anthro), "%P", f"{marker}")

                    Label(frame, text=text, bg='white',
                          font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True, side='left')

                    Entry(frame, width=10, textvariable=var,
                          font=('Comic Sans MS', user.get('text_size')),
                          justify="center",
                          validate="key",
                          validatecommand=check
                          ).pack(fill='both', expand=True, side='left')

                if type_certificate in ('Годовой медосмотр', 'Оформление в ДДУ / СШ / ВУЗ', 'В детский лагерь',
                                        'Эпикриз 15 лет', 'Эпикриз 18 лет'):
                    Label(frame, text="    Зрение:",
                          font=('Comic Sans MS', user.get('text_size')), bg='white'
                          ).pack(fill='both', expand=True, side='left')
                    Entry(frame, width=10, textvariable=vision, justify="center",
                          font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True, side='left')
                    if age.get('year') >= 4:
                        vision.set('1.0/1.0')
                    else:
                        vision.set('предметное')

                    Label(frame, text="    АД:",
                          font=('Comic Sans MS', user.get('text_size')), bg='white'
                          ).pack(fill='both', expand=True, side='left')
                    Entry(frame, width=10, textvariable=patient_bp, justify="center",
                          font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True, side='left')

                frame.pack(fill='both', expand=True, padx=2, pady=2)
                frame_body.pack(fill='both', expand=True, padx=2, pady=2)

                frame = Frame(frame_body, borderwidth=1, relief="solid", padx=2, pady=2)
                Label(frame, text="Физическое развитие: ",
                      font=('Comic Sans MS', user.get('text_size')), bg='white'
                      ).pack(fill='both', expand=True)
                Entry(frame, width=100, textvariable=patient_anthropometry,
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True)

                frame.pack(fill='both', expand=True, padx=2, pady=2)
                if type_certificate not in ('Эпикриз 15 лет', 'Эпикриз 18 лет'):
                    paste_diagnosis_frame()

                    for txt, marker, variable in (('Группа здоровья', 'group', selected_health_group),
                                                  ('Группа по физ-ре', 'physical', selected_fiz_group),
                                                  ('Режим', 'regime', regime_vars),
                                                  ('Стол', 'diet', selected_diet),
                                                  ('Парта', 'desk', desk_vars)):
                        frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)

                        Label(frame, text=f"{txt}:",
                              font=('Comic Sans MS', user.get('text_size')), bg='white'
                                ).pack(fill='both', expand=True, side='left')

                        for mark in all_data_certificate.get('health').get(marker):
                            if marker in ('group', 'physical', 'diet'):
                                Radiobutton(frame, text=mark,
                                            font=('Comic Sans MS', user.get('text_size')),
                                            value=mark, variable=variable,
                                            command=select_health, indicatoron=False, selectcolor='#77f1ff'
                                            ).pack(fill='both', expand=True, side='left')
                            else:
                                Checkbutton(frame, text=mark,
                                            font=('Comic Sans MS', user.get('text_size')),
                                            variable=variable.get(mark), command=select_health,
                                            onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff'
                                            ).pack(fill='both', expand=True, side='left')

                        frame.pack(fill='both', expand=True, padx=2, pady=2)

                if type_certificate == 'Годовой медосмотр':
                    frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                    Label(frame, text="Печатать карту диспансеризации",
                          font=('Comic Sans MS', user.get('text_size')),
                          bg='white').pack(fill='both', expand=True, side='left')


                    for mark in ["Да", "Нет"]:
                        Radiobutton(frame, text=mark,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    value=mark, variable=dispanser_card,
                                    indicatoron=False, selectcolor='#77f1ff'
                                    ).pack(fill='both', expand=True, side='left')
                    frame.pack(fill='both', expand=True, padx=2, pady=2)

            if type_certificate == 'О нуждаемости в сан-кур лечении':
                def select_profile():
                    result = list()
                    for regime in sanatorium_profile:
                        if sanatorium_profile.get(regime).get() == 1:
                            result.append(regime)
                    data['certificate']['sanatorium_profile'] = result

                paste_diagnosis_frame()
                frame_profiles = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)

                Label(frame_profiles, text="Профиль санатория:",
                      font=('Comic Sans MS', user.get('text_size')), bg='white'
                      ).pack(fill='both', expand=True)


                for profiles in (('Болезни органов дыхания', 'Болезни органов пищеварения'),
                                ('Болезни нервной системы', 'Болезни костно-мышечной системы и соединительной ткани'),
                                ('Болезни мочеполовой системы', 'Болезни системы кровообращения', 'Болезни эндокринной системы, нарушения обмена веществ'),
                                ('Болезни кожи и подкожной клетчатки', 'Болезни глаза и его придаточного аппарата')):
                    frame = Frame(frame_profiles)
                    for profile in profiles:
                        sanatorium_profile[profile] = IntVar()
                        Checkbutton(frame, text=profile,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    variable=sanatorium_profile.get(profile),
                                    command=select_profile,
                                    onvalue=1, offvalue=0, indicatoron=False, selectcolor='#77f1ff'
                                    ).pack(fill='both', expand=True, side='left')
                    frame.pack(fill='both', expand=True)
                frame_profiles.pack(fill='both', expand=True)

            if type_certificate == 'ЦКРОиР':
                def set_default():
                    diagnosis = data['certificate']['type_cert_info']["ЦКРОиР"].get('ЦКРОиР_add_med_info')
                    diagnosis.delete(1.0, 'end')
                    diagnosis.insert(1.0, all_data_certificate['all_info']['ЦКРОиР'].get('additional_medical_information'))
                    for doctors, diagnosis in (('Невролог', 'Без очаговой патологии'),
                                               ('Офтальмолог', 'Без патологии'),
                                               ('ЛОР', 'Без патологии'),
                                               ('Логопед', 'ОНР ( __ ур. р. р.)')):
                        data['certificate']['type_cert_info']['ЦКРОиР'][f"{doctors}_txt"].set(diagnosis)

                "Для логопедической комиссии (ЦКРОиР)"
                frame_add_info = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                frame = Frame(frame_add_info)
                Label(frame, text="Данные о развитии:",
                      font=('Comic Sans MS', user.get('text_size')), bg='white'
                      ).pack(fill='both', expand=True, side='left')
                Button(frame, text='Вернуть данные по умолчанию',
                       command=set_default,
                       font=('Comic Sans MS', user.get('text_size'))
                       ).pack(fill='both', expand=True, side='left')

                frame.pack(fill='both', expand=True, padx=2, pady=2)

                frame = Frame(frame_add_info)

                diagnosis = ScrolledText(frame, width=80, height=8,
                                         font=('Comic Sans MS', user.get('text_size')), wrap="word")
                diagnosis.pack(fill='both', expand=True)
                diagnosis.insert(1.0, all_data_certificate['all_info']['ЦКРОиР'].get('additional_medical_information'))
                data['certificate']['type_cert_info'][type_certificate]['ЦКРОиР_add_med_info'] = diagnosis
                frame.pack(fill='both', expand=True, padx=2, pady=2)
                frame_add_info.pack(fill='both', expand=True, padx=2, pady=2)

                for doctors, diagnosis in (('Невролог', 'Без очаговой патологии'),
                                           ('Офтальмолог', 'Без патологии'),
                                           ('ЛОР', 'Без патологии'),
                                           ('Логопед', 'ОНР ( __ ур. р. р.)')):
                    frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                    Label(frame, text=f"{doctors}:",
                          font=('Comic Sans MS', user.get('text_size')), bg='white'
                          ).pack(fill='both', expand=True, side='left')
                    data['certificate']['type_cert_info'][type_certificate][f"{doctors}_txt"] = StringVar()
                    data['certificate']['type_cert_info'][type_certificate][f"{doctors}_txt"].set(diagnosis)
                    Radiobutton(frame, image=user.get('сalendar_img'),
                                font=('Comic Sans MS', user.get('text_size')),
                                value=f"{type_certificate}-{doctors}_txt__{type_certificate} - {doctors}",
                                variable=selected_button,
                                command=paste_calendar,
                                indicatoron=False, selectcolor='#77f1ff'
                                ).pack(side='left')

                    Entry(frame, width=50,
                          textvariable=data['certificate']['type_cert_info'][type_certificate].get(f"{doctors}_txt"),
                          font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True, side='left')
                    frame.pack(fill='both', expand=True, padx=2, pady=2)

                paste_diagnosis_frame()

            if type_certificate in ("На кружки и секции", "ЦКРОиР", "Об отсутствии контактов",
                                    "О нуждаемости в сан-кур лечении", "Может работать по специальности...",
                                    "Бесплатное питание"):
                frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                Label(frame, text="Печатать вкладыш в карту",
                      font=('Comic Sans MS', user.get('text_size')),
                      bg='white').pack(fill='both', expand=True, side='left')

                for mark in ["Да", "Нет"]:
                    Radiobutton(frame, text=mark,
                                font=('Comic Sans MS', user.get('text_size')),
                                value=mark, variable=examination_blank,
                                indicatoron=False, selectcolor='#77f1ff'
                                ).pack(fill='both', expand=True, side='left')
                frame.pack(fill='both', expand=True, padx=2, pady=2)

            if type_certificate in ('Эпикриз 15 лет', 'Эпикриз 18 лет'):
                frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                Label(frame, text="Место учебы (работы):",
                      font=('Comic Sans MS', user.get('text_size')), bg='white'
                      ).pack(fill='both', expand=True, side='left')
                Entry(frame, width=30,
                      textvariable=work_place,
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True, side='left')
                frame.pack(fill='both', expand=True, padx=2, pady=2)

                # frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                # Label(frame, text="Диспансерное наблюдение:",
                #       font=('Comic Sans MS', user.get('text_size')), bg='white'
                #       ).pack(fill='both', expand=True, side='left')
                # Entry(frame, width=30,
                #       textvariable=dispensary_observation,
                #       font=('Comic Sans MS', user.get('text_size'))
                #       ).pack(fill='both', expand=True, side='left')
                # frame.pack(fill='both', expand=True, padx=2, pady=2)

                if type_certificate == "Эпикриз 15 лет":
                    for doctors in ("Диспансерное наблюдение",
                                    'УЗИ сердца', 'УЗИ шитовидной железы', 'УЗИ органов брюшной полости',
                                    'Электрокардиограмма', 'OAK', 'Глюкоза', 'OAM'):
                        frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                        Label(frame, text=f"{doctors}:",
                              font=('Comic Sans MS', user.get('text_size')), bg='white'
                              ).pack(fill='both', expand=True)

                        scrolled_text = ScrolledText(frame, width=80, height=3,
                                                     font=('Comic Sans MS', user.get('text_size')),
                                                     wrap="word")
                        data['certificate']['type_cert_info'][type_certificate][f"{doctors}_scrolled_txt"] = scrolled_text

                        scrolled_text.pack(fill='both', expand=True)
                        frame.pack(fill='both', expand=True, padx=2, pady=2)

                if type_certificate == "Эпикриз 18 лет":
                    frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                    Label(frame, text="Состоит на учете поликлиники с:",
                          font=('Comic Sans MS', user.get('text_size')), bg='white'
                          ).pack(fill='both', expand=True, side='left')
                    Entry(frame, width=30,
                          textvariable=registered_from,
                          font=('Comic Sans MS', user.get('text_size'))
                          ).pack(fill='both', expand=True, side='left')
                    frame.pack(fill='both', expand=True, padx=2, pady=2)

                    for doctors in ("Диспансерное наблюдение", "Педиатр", "Хирург", "Офтальмолог", "Невролог",
                                    "Стоматолог", "Гинеколог", "Другие врачи-специалисты",
                                    'УЗИ сердца', 'УЗИ шитовидной железы',
                                    'УЗИ органов брюшной полости', "УЗИ мочеполовой системы",
                                    'Электрокардиограмма', 'OAK', 'OAM',
                                    'Глюкоза', "Слух", "Флюорография", "Половое развитие"):
                        frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                        Label(frame, text=f"{doctors}:",
                              font=('Comic Sans MS', user.get('text_size')), bg='white'
                              ).pack(fill='both', expand=True)

                        scrolled_text = ScrolledText(frame, width=80, height=3,
                                                     font=('Comic Sans MS', user.get('text_size')),
                                                     wrap="word")
                        data['certificate']['type_cert_info'][type_certificate][f"{doctors}_txt"] = scrolled_text

                        scrolled_text.pack(fill='both', expand=True)
                        frame.pack(fill='both', expand=True, padx=2, pady=2)

                paste_diagnosis_frame()
                for txt, marker, variable in (('Группа здоровья', 'group', selected_health_group),
                                              ('Группа по физ-ре', 'physical', selected_fiz_group)):
                    frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)

                    Label(frame, text=f"{txt}:",
                          font=('Comic Sans MS', user.get('text_size')), bg='white'
                          ).pack(fill='both', expand=True, side='left')

                    for mark in all_data_certificate.get('health').get(marker):
                        Radiobutton(frame, text=mark,
                                    font=('Comic Sans MS', user.get('text_size')),
                                    value=mark, variable=variable,
                                    command=select_health, indicatoron=False, selectcolor='#77f1ff'
                                    ).pack(fill='both', expand=True, side='left')
                    frame.pack(fill='both', expand=True, padx=2, pady=2)

            def paste_validaty_period():
                frame = Frame(master_frame, borderwidth=1, relief="solid", padx=4, pady=4)
                Label(frame, text="Дата выдачи:",
                      font=('Comic Sans MS', user.get('text_size')), bg='white'
                      ).pack(fill='both', expand=True, side='left')
                Entry(frame, width=15,
                      textvariable=date_of_issue,
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True, side='left')
                Radiobutton(frame, image=user.get('сalendar_img'),
                            font=('Comic Sans MS', user.get('text_size')),
                            value="date_of_issue__Дата выдачи справки...",
                            variable=selected_button,
                            command=paste_calendar,
                            indicatoron=False, selectcolor='#77f1ff'
                            ).pack(side='left')
                data['certificate']['type_cert_info'][type_certificate]['validity_period'] = StringVar()
                if all_data_certificate['all_info'].get(type_certificate).get('validity_period'):
                    data['certificate']['type_cert_info'][type_certificate]['validity_period'].set(
                        all_data_certificate['all_info'].get(type_certificate).get('validity_period'))
                else:
                    try:
                        date = patient.get('birth_date')
                        day, month, year = date.split('.')
                        date = datetime.strptime(f"{day}.{month}.{datetime.now().year}", "%d.%m.%Y")
                        if date < datetime.now():
                            day, month, year = date.strftime("%d.%m.%Y").split('.')
                            year = int(year) + 1
                            date = datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y")

                        if (date - datetime.now()).total_seconds() < 5356800:
                            day, month, year = date.strftime("%d.%m.%Y").split('.')
                            year = int(year) + 1
                            date = datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y")
                        date = (date - timedelta(days=1)).strftime("%d.%m.%Y")

                        data['certificate']['type_cert_info'][type_certificate]['validity_period'].set(f"до {date}")
                    except Exception:
                        data['certificate']['type_cert_info'][type_certificate]['validity_period'].set('1 год')

                Label(frame, text="    Срок действия:",
                      font=('Comic Sans MS', user.get('text_size')), bg='white'
                      ).pack(fill='both', expand=True, side='left')
                Entry(frame, width=30,
                      textvariable=data['certificate']['type_cert_info'][type_certificate].get('validity_period'),
                      font=('Comic Sans MS', user.get('text_size'))
                      ).pack(fill='both', expand=True, side='left')
                frame.pack(fill='both', expand=True, padx=2, pady=2)

            paste_validaty_period()
            Radiobutton(master_frame, text="\n< < < Создать справку > > >\n",
                        font=('Comic Sans MS', user.get('text_size')),
                        value=type_certificate,
                        variable=selected_button,
                        command=create_certificate,
                        indicatoron=False, selectcolor='#36566d',
                        bg="#36566d",
                        fg='white',
                        ).pack(fill='both', expand=True)
            frame.pack(fill='both', expand=True)

        certificate_main_root.update_idletasks()
        certificate_main_root.geometry('+0+0')

        start_action(upload_last_data)
        selected_button.set('')
        data['certificate']['frame_type_cert_but'].pack(fill='both', expand=True, padx=2, pady=2)


    create_type_cert_frames()
