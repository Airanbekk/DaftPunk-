<<<<<<< HEAD
import psycopg2
import csv
import os

# Папка с CSV файлами
csv_folder = r"C:\Users\Admin\Downloads\archive"

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="techno_events",
    user="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Получаем все CSV в папке
for filename in os.listdir(csv_folder):
    if filename.lower().endswith(".csv"):
        table_name = os.path.splitext(filename)[0].lower()  # имя таблицы из имени файла
        file_path = os.path.join(csv_folder, filename)
        print(f"Импортируем {filename} в таблицу {table_name}...")

        # Открываем CSV и очищаем заголовки
        with open(file_path, newline='', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [f.strip() for f in reader.fieldnames]

            # Создаём таблицу с колонками на основе заголовков CSV
            columns = ", ".join([f"{f.lower()} TEXT" for f in reader.fieldnames if f.lower() != 'id'])
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                {columns}
            )
            """
            cur.execute(create_sql)
            conn.commit()

            # Вставка данных
            for row in reader:
                fields = [f.lower() for f in reader.fieldnames if f.lower() != 'id']
                values = [row[f] for f in reader.fieldnames if f.lower() != 'id']
                placeholders = ", ".join(["%s"] * len(values))
                insert_sql = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
                cur.execute(insert_sql, values)

        conn.commit()
        print(f"{filename} импортирован!")

cur.close()
conn.close()
print("Все CSV импортированы!")
=======
import psycopg2
import csv
import os

# Папка с CSV файлами
csv_folder = r"C:\Users\Admin\Downloads\archive"

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="techno_events",
    user="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Получаем все CSV в папке
for filename in os.listdir(csv_folder):
    if filename.lower().endswith(".csv"):
        table_name = os.path.splitext(filename)[0].lower()  # имя таблицы из имени файла
        file_path = os.path.join(csv_folder, filename)
        print(f"Импортируем {filename} в таблицу {table_name}...")

        # Открываем CSV и очищаем заголовки
        with open(file_path, newline='', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [f.strip() for f in reader.fieldnames]

            # Создаём таблицу с колонками на основе заголовков CSV
            columns = ", ".join([f"{f.lower()} TEXT" for f in reader.fieldnames if f.lower() != 'id'])
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                {columns}
            )
            """
            cur.execute(create_sql)
            conn.commit()

            # Вставка данных
            for row in reader:
                fields = [f.lower() for f in reader.fieldnames if f.lower() != 'id']
                values = [row[f] for f in reader.fieldnames if f.lower() != 'id']
                placeholders = ", ".join(["%s"] * len(values))
                insert_sql = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
                cur.execute(insert_sql, values)

        conn.commit()
        print(f"{filename} импортирован!")

cur.close()
conn.close()
print("Все CSV импортированы!")
>>>>>>> 4837fc428ddd766658469d4e0d8c321d0d478aaf
