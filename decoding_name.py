from tkinter import messagebox


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
                            for _ in range(3):
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
                            for i_ in info[info.index('г'):]:
                                if len(i_) == 10 and '.' in i_:
                                    break
                                else:
                                    user['address'] += f'{i_} '
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
                        for i_ in info[info.index('Минск'):]:
                            if i_.isdigit():
                                user['address'] += f'{i_} - '
                            else:
                                user['address'] += f'{i_} '
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
