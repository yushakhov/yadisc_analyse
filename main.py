from webdav3.client import Client
import os
import time
import random
import json
import logging

# Настройка логирования
logging.basicConfig(filename='scan_log.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Установите ваши учетные данные
WEBDAV_URL = "https://webdav.yandex.ru"
WEBDAV_LOGIN = "def-def"
WEBDAV_PASSWORD = "ugpgwyctogigizlx"

# Настройки клиента WebDAV
options = {
    'webdav_hostname': WEBDAV_URL,
    'webdav_login': WEBDAV_LOGIN,
    'webdav_password': WEBDAV_PASSWORD
}
client = Client(options)

# Проверка подключения
try:
    client.list()
    print("Успешно подключено к Яндекс Диску через WebDAV")
except Exception as e:
    print(f"Не удалось подключиться к Яндекс Диску через WebDAV: {e}")
    exit()


# Функция для рекурсивного сканирования каталогов
def scan_directory(path="/"):
    files_info = []
    consecutive_errors = 0
    for item in client.list(path):
        time.sleep(random.randint(50, 150) / 1000)
        full_path = os.path.join(path, item)
        print(full_path)
        retries = 0
        while retries < 3:
            try:
                if client.check(full_path):
                    if client.is_dir(full_path):
                        files_info.append({
                            "name": item,
                            "path": full_path,
                            "size": 0,  # Размер папки не имеет смысла
                            "checksum": None,  # Контрольная сумма для папки не имеет смысла
                            "type": "папка"
                        })
                        files_info.extend(scan_directory(full_path))
                    else:
                        file_info = {
                            "name": item,
                            "path": full_path,
                            "size": client.info(full_path)["size"],
                            "checksum": client.info(full_path).get("checksum", None),
                            "type": "файл"
                        }
                        files_info.append(file_info)
                        # Запись данных в JSON-файл
                        append_to_json("yandex_disk_files.json", file_info)
                    consecutive_errors = 0
                    break
                else:
                    consecutive_errors += 1
                    logging.error(f"Объект не найден: {full_path}")
            except Exception as e:
                retries += 1
                consecutive_errors += 1
                logging.error(f"Ошибка при считывании объекта {full_path}: {e}")
                time.sleep(2)

        if consecutive_errors >= 50:
            logging.error("Превышено количество последовательных ошибок. Завершение работы скрипта.")
            exit()

    return files_info


# Функция для добавления данных в JSON-файл
def append_to_json(filename, data):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)

    with open(filename, 'r+') as f:
        file_data = json.load(f)
        file_data.append(data)
        f.seek(0)
        json.dump(file_data, f, indent=4)


# Сканирование всего дерева каталогов
scan_directory()

print("Сканирование завершено и данные сохранены в yandex_disk_files.json")