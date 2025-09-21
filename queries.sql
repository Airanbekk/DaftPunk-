-- 1. Топ-10 жанров с наибольшим количеством артистов
SELECT g.name AS genre_name, COUNT(a.id) AS artist_count
FROM genres g
LEFT JOIN artists a ON g.id = a.genreid
GROUP BY g.name
ORDER BY artist_count DESC
LIMIT 10;

-- 2. Артисты без биографии (Bio) – потенциально нуждаются в заполнении
SELECT name, genreid
FROM artists
WHERE bio IS NULL OR bio = ''
ORDER BY genreid;

-- 3. Средняя длина биографии артистов по жанрам
SELECT g.name AS genre_name, AVG(LENGTH(a.bio)) AS avg_bio_length
FROM artists a
LEFT JOIN genres g ON a.genreid = g.id
WHERE a.bio IS NOT NULL
GROUP BY g.name
ORDER BY avg_bio_length DESC;

-- 4. Артисты с самыми длинными именами (топ-10)
SELECT name, LENGTH(name) AS name_length
FROM artists
ORDER BY name_length DESC
LIMIT 10;

-- 5. Количество артистов с хотя бы одной ссылкой на соцсети (Spotify, SoundCloud или YouTube)
SELECT COUNT(*) AS artists_with_links
FROM artists
WHERE spotify IS NOT NULL OR soundcloud IS NOT NULL OR youtube IS NOT NULL;

-- 6. Процент артистов с изображением (PictureUrl)
SELECT (COUNT(*) FILTER (WHERE pictureurl IS NOT NULL)/COUNT(*)::float)*100 AS percent_with_picture
FROM artists;

-- 7. Топ-5 жанров с самой длинной средней биографией
SELECT g.name AS genre_name, AVG(LENGTH(a.bio)) AS avg_bio_length
FROM artists a
JOIN genres g ON a.genreid = g.id
WHERE a.bio IS NOT NULL
GROUP BY g.name
ORDER BY avg_bio_length DESC
LIMIT 5;

-- 8. Артисты с активными профилями на всех платформах (Spotify, SoundCloud, YouTube)
SELECT name
FROM artists
WHERE spotify IS NOT NULL AND soundcloud IS NOT NULL AND youtube IS NOT NULL
ORDER BY name;

-- 9. Распределение артистов по длине имени (группировка)
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

-- 10. Список жанров с наибольшим процентом артистов без ссылок на соцсети
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

