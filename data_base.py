import sqlite3 as sq
import os
from datetime import datetime


def create_data_base():
    with sq.connect(r"\\SRV2\data_base\data_base.db") as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS certificate_camp (
                district TEXT, num TEXT, date TEXT, 
                name TEXT, birth_date TEXT, gender TEXT, address TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS certificate_ped_div (
                        ped_div TEXT, district TEXT, num TEXT, date TEXT, 
                        name TEXT, birth_date TEXT, address TEXT, type_cert TEXT, doctor_name TEXT)''')


def save_certificate_ped_div(district_pd, data, type_table):
    try:
        create_data_base()

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
                data[2] = number
                cur.execute(f"INSERT INTO certificate_ped_div VALUES({'?, ' * 8}?)", data)

            elif type_table == 'certificate_camp':
                data[1] = number
                cur.execute(f"INSERT INTO certificate_camp VALUES({'?, ' * 6}?)", data)
    except Exception:
        return '__________'
    return number


def get_certificate_for_district(district, type_table):
    create_data_base()
    with sq.connect(r"\\SRV2\data_base\data_base.db") as conn:
        cur = conn.cursor()

        if type_table == 'certificate_ped_div':
            cur.execute(f"SELECT *"
                        f" FROM {type_table} WHERE ped_div LIKE '{district}';")
        elif type_table == 'certificate_camp':
            cur.execute(f"SELECT *"
                        f" FROM {type_table} WHERE district LIKE '{district}';")

        data = list()
        for info in cur.fetchall():
            data.append(info)
        return data


def get_max_number_and_write(district_pd, type_table):

    create_data_base()
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

        return max(numbers) + 1


def statistic_write(user_id, info):
    date_now, time_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S").split()
    try:
        with sq.connect(r"\\SRV2\data_base\data_base.db") as conn:
            cur = conn.cursor()
            type_info, _, district = info.split('_')
            cur.execute(f"INSERT INTO statistic_DOC_db VALUES('{date_now}', '{time_now}', '{user_id}', '{type_info}', '{district}')")
    except Exception:
        pass
