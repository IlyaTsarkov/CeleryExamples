import celery
import random
import string
import datetime
import psycopg2
# Модуль для работы с исполнением задач по расписанию
from celery.schedules import crontab

# Конфигурация БД
connection = psycopg2.connect(
    host='127.0.0.1',
    database='celery_example_db',
    user='ilya',
    password='123654ZyF!',
    # Классический PostgreSQL порт
    port=5432,
)
# Автоматическое применение изменений
connection.autocommit = True

# Объект Celery с импортированными настройками конфигурации
app = celery.Celery('db_work')
app.config_from_object('simple_examples.celeryconfig')

# Конфигурация отправки по времени
app.conf.beat_schedule = {
    'add_note_to_db': {
        # Выполнение задачи раз в минуту
        'task': 'insert-into-table-task',
        'schedule': crontab(minute='*/2'),
    },
}


@app.task(name='create-table-task')
def create_table():
    """Задача на создание таблицы в БД"""

    # Вывод информации о версии postgreSQL и ПК
    with connection.cursor() as cursor:
        # Объект курсора устанавливает соединение с БД
        # Метод .execute() для SQL-запроса
        cursor.execute(
            "SELECT version();"
        )

        # Метод .fetchone() возвращает результат работы .execute()
        print(f'Версия - {cursor.fetchone()}')

    # Создание новой таблицы с полями id и log_info
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE results(
                id serial PRIMARY KEY,
                log_info text NOT NULL);"""
        )

        print('Таблица results создана')


@app.task(name='insert-into-table-task')
def insert_into_table():
    """Задача для добавления новой записи в таблицу"""

    # Генерация случайно строки из цифр и букв
    letters_and_digits = string.ascii_letters + string.digits
    some_string = ''.join(random.choice(letters_and_digits) for i in range(random.randint(30, 50)))

    # Добавление сгенерированной строки в таблицу results
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO results (log_info) VALUES(%s);", [some_string])

        print(f'Запись {some_string} добавлена в таблицу results')

    # Генерация результата, возвращаемого задачей
    res = f'{some_string} добавлена в {datetime.datetime.now()}'
    return res
