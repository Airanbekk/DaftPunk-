import psycopg2
import csv
import os

# Подключение к базе
conn = psycopg2.connect(
    dbname="techno_events",
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
    "avg_bio_length_by_genre": """
        SELECT g.name AS genre_name, AVG(LENGTH(a.bio)) AS avg_bio_length
        FROM artists a
        LEFT JOIN genres g ON a.genreid = g.id
        WHERE a.bio IS NOT NULL
        GROUP BY g.name
        ORDER BY avg_bio_length DESC;
    """,
    "artists_with_long_names": """
        SELECT name, LENGTH(name) AS name_length
        FROM artists
        ORDER BY name_length DESC
        LIMIT 10;
    """,
    "artists_with_links_count": """
        SELECT COUNT(*) AS artists_with_links
        FROM artists
        WHERE spotify IS NOT NULL OR soundcloud IS NOT NULL OR youtube IS NOT NULL;
    """,
    "percent_artists_with_picture": """
        SELECT (COUNT(*) FILTER (WHERE pictureurl IS NOT NULL)/COUNT(*)::float)*100 AS percent_with_picture
        FROM artists;
    """,
    "top_5_genres_by_avg_bio_length": """
        SELECT g.name AS genre_name, AVG(LENGTH(a.bio)) AS avg_bio_length
        FROM artists a
        JOIN genres g ON a.genreid = g.id
        WHERE a.bio IS NOT NULL
        GROUP BY g.name
        ORDER BY avg_bio_length DESC
        LIMIT 5;
    """,
    "artists_with_all_platforms": """
        SELECT name
        FROM artists
        WHERE spotify IS NOT NULL AND soundcloud IS NOT NULL AND youtube IS NOT NULL
        ORDER BY name;
    """,
    "name_length_distribution": """
        SELECT CASE
                 WHEN LENGTH(name) <= 5 THEN '1-5 chars'
                 WHEN LENGTH(name) <= 10 THEN '6-10 chars'
                 WHEN LENGTH(name) <= 15 THEN '11-15 chars'
                 ELSE '16+ chars'
               END AS name_length_group,
               COUNT(*) AS artist_count
        FROM artists
        GROUP BY name_length_group
        ORDER BY name_length_group;
    """,
    "genres_by_no_links_percent": """
        SELECT g.name AS genre_name,
               COUNT(*) FILTER (WHERE spotify IS NULL AND soundcloud IS NULL AND youtube IS NULL) AS no_links,
               COUNT(a.id) AS total_artists,
               (COUNT(*) FILTER (WHERE spotify IS NULL AND soundcloud IS NULL AND youtube IS NULL)::float
                / NULLIF(COUNT(a.id),0))*100 AS percent_no_links
        FROM genres g
        LEFT JOIN artists a ON g.id = a.genreid
        GROUP BY g.name
        ORDER BY percent_no_links DESC
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

import psycopg2
import csv
import os

# Подключение к базе
conn = psycopg2.connect(
    dbname="techno_events",
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
    "avg_bio_length_by_genre": """
        SELECT g.name AS genre_name, AVG(LENGTH(a.bio)) AS avg_bio_length
        FROM artists a
        LEFT JOIN genres g ON a.genreid = g.id
        WHERE a.bio IS NOT NULL
        GROUP BY g.name
        ORDER BY avg_bio_length DESC;
    """,
    "artists_with_long_names": """
        SELECT name, LENGTH(name) AS name_length
        FROM artists
        ORDER BY name_length DESC
        LIMIT 10;
    """,
    "artists_with_links_count": """
        SELECT COUNT(*) AS artists_with_links
        FROM artists
        WHERE spotify IS NOT NULL OR soundcloud IS NOT NULL OR youtube IS NOT NULL;
    """,
    "percent_artists_with_picture": """
        SELECT (COUNT(*) FILTER (WHERE pictureurl IS NOT NULL)/COUNT(*)::float)*100 AS percent_with_picture
        FROM artists;
    """,
    "top_5_genres_by_avg_bio_length": """
        SELECT g.name AS genre_name, AVG(LENGTH(a.bio)) AS avg_bio_length
        FROM artists a
        JOIN genres g ON a.genreid = g.id
        WHERE a.bio IS NOT NULL
        GROUP BY g.name
        ORDER BY avg_bio_length DESC
        LIMIT 5;
    """,
    "artists_with_all_platforms": """
        SELECT name
        FROM artists
        WHERE spotify IS NOT NULL AND soundcloud IS NOT NULL AND youtube IS NOT NULL
        ORDER BY name;
    """,
    "name_length_distribution": """
        SELECT CASE
                 WHEN LENGTH(name) <= 5 THEN '1-5 chars'
                 WHEN LENGTH(name) <= 10 THEN '6-10 chars'
                 WHEN LENGTH(name) <= 15 THEN '11-15 chars'
                 ELSE '16+ chars'
               END AS name_length_group,
               COUNT(*) AS artist_count
        FROM artists
        GROUP BY name_length_group
        ORDER BY name_length_group;
    """,
    "genres_by_no_links_percent": """
        SELECT g.name AS genre_name,
               COUNT(*) FILTER (WHERE spotify IS NULL AND soundcloud IS NULL AND youtube IS NULL) AS no_links,
               COUNT(a.id) AS total_artists,
               (COUNT(*) FILTER (WHERE spotify IS NULL AND soundcloud IS NULL AND youtube IS NULL)::float
                / NULLIF(COUNT(a.id),0))*100 AS percent_no_links
        FROM genres g
        LEFT JOIN artists a ON g.id = a.genreid
        GROUP BY g.name
        ORDER BY percent_no_links DESC
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

