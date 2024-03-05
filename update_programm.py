import shutil
import time
import sqlite3 as sq
from datetime import datetime
import os
import zipfile


def update():
    path_srv = None
    print('Извлечение пути к серверу')
    with sq.connect(f"../генератор_справок{os.sep}data_base{os.sep}data_base.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT path_srv_data_base FROM app_data")
        path_srv = cur.fetchone()
        if isinstance(path_srv, tuple):
            path_srv = path_srv[0]
    if path_srv:
        print('Извлечение пути к серверу - успешно')
        edit_file = False
        for file in sorted(os.listdir(path_srv)):
            print(file)
            if file.startswith('генератор_справок') and file.endswith('.zip'):
                print("Обнаружен нужный файл:", file)
                edit_file = file
        if edit_file:
            print("Копирую локальную базу данных")
            if 'обновление' in os.listdir(f'..{os.sep}'):
                shutil.rmtree(f'..{os.sep}обновление')
            destination_dir = f'..{os.sep}обновление{os.sep}'
            if not os.path.exists(path=destination_dir):
                os.mkdir(path=destination_dir)
            if 'генератор_справок' in os.listdir(f"..{os.sep}"):
                if 'data_base' in os.listdir(f"..{os.sep}генератор_справок{os.sep}"):
                    if not os.path.exists(path=f"{destination_dir}data_base{os.sep}"):
                        os.mkdir(path=f"{destination_dir}data_base{os.sep}")

                    for file in os.listdir(f"..{os.sep}генератор_справок{os.sep}data_base{os.sep}"):
                        if '.db' in file:
                            shutil.copy2(f"..{os.sep}генератор_справок{os.sep}data_base{os.sep}{file}",
                                         f"{destination_dir}data_base{os.sep}{file}")

            print("Загружаю обновление")
            destination_dir = f'..{os.sep}обновление{os.sep}'

            shutil.copy2(f"{path_srv}{edit_file}",
                         f"..{os.sep}обновление{os.sep}генератор_справок.zip")

            if 'генератор_справок' in os.listdir(f"..{os.sep}"):
                print("Удаляю старую директорию")
                shutil.rmtree(f'..{os.sep}генератор_справок')
                # os.mkdir(path=f'..{os.sep}генератор_справок{os.sep}')

            archive = zipfile.ZipFile(f"..{os.sep}обновление{os.sep}генератор_справок.zip", 'r')
            archive.extractall(f"..{os.sep}")
            archive.close()
            print("Начинаю синхронизацию")
            if 'data_base' in os.listdir(f"..{os.sep}обновление{os.sep}"):

                for file in os.listdir(f"..{os.sep}обновление{os.sep}data_base"):
                    if '.db' in file:
                        shutil.copy2(f"..{os.sep}обновление{os.sep}data_base{os.sep}{file}",
                                     f"..{os.sep}генератор_справок{os.sep}data_base{os.sep}{file}")
                print('База данных синхронизирована')


if __name__ == '__main__':
    update()
    time.sleep(5)
    os.system(f"start ..{os.sep}генератор_справок{os.sep}генератор_справок.exe")


