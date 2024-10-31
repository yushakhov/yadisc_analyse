import time
import yadisk
# import pandas as pd
# from collections import defaultdict
import logging

# Настройка логирования
logging.basicConfig(
    filename='log.log',  # Имя файла, в который будут записываться логи
    level=logging.DEBUG,     # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
    datefmt='%Y-%m-%d %H:%M:%S'  # Формат времени
)

# Создание логгера
logger = logging.getLogger('my_logger')

# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Установите ваши токены доступа
y = yadisk.YaDisk(token="y0_AgAAAAAAVtKZAAykGAAAAAEVS4ljAADxRJXH2c9ISbj80DIgMYXg-8Zhxg")

# Проверка, авторизован ли пользователь
if y.check_token():
    logger.info("Успешная авторизация")
else:
    logger.error("Ошибка авторизации")
    exit()


# Функция для проверки существования пути
def path_exists(path):
    try:
        y.get_meta(path)
        return True
    except yadisk.exceptions.PathNotFoundError:
        return False

# Рекурсивная функция для сканирования всех файлов
def scan_folder(exclude, path="/"):
    
    if not path_exists(path):
        logger.error(f"Путь не найден: {path}")
        return

    # Словарь для хранения информации о файлах
    # file_info = defaultdict(list)
    file_info = []

    for item in y.listdir(path):
        full_path = f"{path if path != '/' else ''}/{item['name']}"
        if item['type'] == 'dir':
            print(full_path)
            for ex_path in exclude:
                if ex_path in full_path:
                    break
                else:
                    time.sleep(2)
                    scan_folder(exclude, full_path)
                    break
        elif item['type'] == 'file':
            file_name = item['name']
            # full_path = item['path']
            file_size = item['size']
            # modified = item['modified']
            # resource_id = item['resource_id']
            # gps_longitude = dict(item['exif'])['gps_longitude']
            # gps_latitude = dict(item['exif'])['gps_latitude']
            file_info.append([file_name, file_size, path])
            logger.info(f"обработан: {(file_size, file_name)}")
    # Запись информации о файлах в файл
    with open('data.txt', 'a') as f:
        for i in file_info:
            f.write(f"{i[0]},{i[1]},{i[2]}\n")

exclude = ['Дистрибутивы','Архив переписок', ':::',]
# Начать сканирование с корневой папки
scan_folder(exclude=exclude)
# scan_folder(exclude, '/Записки')