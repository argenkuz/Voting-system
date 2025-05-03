import sqlite3

def clear_all_tables(db_path):
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Список всех таблиц, из которых нужно удалить данные и сбросить автоинкремент
    tables = ['Users', 'Elections', 'Candidates', 'Votes']  # Добавьте сюда остальные таблицы

    # Удаляем все данные из таблиц
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")

    # Сброс значения автоинкремента для каждой таблицы
    for table in tables:
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")

    # Выполняем изменения и закрываем соединение
    conn.commit()
    conn.close()

# Вызов функции для очистки таблиц и сброса автоинкремента
clear_all_tables("/Users/argenkulzhanov/Desktop/Designer/nursezim/vote.sqlite")
