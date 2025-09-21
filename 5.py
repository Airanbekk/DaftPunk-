import psycopg2
import csv
import os

# Подключение к базе
conn = psycopg2.connect(
    dbname="techno events",
    user="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Папка для сохранения результатов
output_folder = r"C:\Users\Admin\Documents\DaftPunk_Project"
os.makedirs(output_folder, exist_ok=True)

# Несколько SQL-запросов
queries = {
    "top_10_genres_by_artists": """
        SELECT g.name AS genre_name, COUNT(a.id) AS artist_count
        FROM genres g
        LEFT JOIN artists a ON g.id = a.genreid
        GROUP BY g.name
        ORDER BY artist_count DESC
        LIMIT 10;
    """,
    "artists_without_bio": """
        SELECT name, genreid
        FROM artists
        WHERE bio IS NULL OR bio = ''
        ORDER BY genreid;
    """,
    "artists_with_long_names": """
        SELECT name, LENGTH(name) AS name_length
        FROM artists
        ORDER BY name_length DESC
        LIMIT 10;
    """
}

# Выполнение запросов и сохранение результатов
for name, query in queries.items():
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    # Вывод в терминал
    print(f"\n=== Результат запроса: {name} ===")
    print(columns)
    for row in rows:
        print(row)

    # Сохранение в CSV в указанной папке
    csv_file = os.path.join(output_folder, f"{name}.csv")
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    print(f"Сохранено в {csv_file}")

cur.close()
conn.close()
print("\nВсе выбранные запросы выполнены и сохранены.")
