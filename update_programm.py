import shutil
from tkinter import *
from tkinter import messagebox, Label, Frame

import os
import zipfile

destination_dir = f'.{os.sep}Archive{os.sep}Загрузка_обновлений_БД{os.sep}' \
                  f'{datetime.strftime(datetime.now(), "%d_%m_%y__%H_%M_%S")}{os.sep}'

if not os.path.exists(path=destination_dir):
    os.mkdir(path=destination_dir)

destination_file = f'{destination_dir}' \
                   f'Архив_{datetime.strftime(datetime.now(), "%d_%m_%y__%H_%M_%S")}.zip'

if document := message.document:
    await edit_message_text(message=message,
                            text="Файл получен! Загружаю...")
    for num in range(1, 4):
        await edit_message_text(message=message,
                                text=f"Попытка загрузки файла {num}")
        try:
            await document.download(destination_file=destination_file)
        except Exception:
            await edit_message_text(message=message,
                                    text="Ошибка загрузки файла!")
        else:
            await edit_message_text(message=message,
                                    text="Файл загружен! Открываю архив...")

            archive = zipfile.ZipFile(destination_file, 'r')

            archive.extractall(destination_dir)
            await edit_message_text(message=message,
                                    text="Архив успешно извлечен")

            archive.close()
            await edit_message_text(message=message,
                                    text="Архив закрыт. Прохожусь по файлам")

            await search_in_dir(message=message,
                                path=destination_dir)
            text = '<b>Прививки:</b>'
            for file in vaccination_file_list:
                text += f"\n{file.replace(f'.{os.sep}Archive{os.sep}Загрузка_обновлений_БД{os.sep}', '')}"
            text += '\n\n<b>Картотека:</b>'
            for file in card_file_list:
                text += f"\n{file}.replace(f'.{os.sep}Archive{os.sep}Загрузка_обновлений_БД{os.sep}', '')"
            await message.answer(text)

