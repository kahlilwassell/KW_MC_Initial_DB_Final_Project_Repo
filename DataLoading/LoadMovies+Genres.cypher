LOAD CSV WITH HEADERS FROM 'file:///imdb_list.csv' AS row
WITH
  trim(row.id)      AS imdbId,
  trim(row.title)   AS title,
  toFloat(row.rating) AS imdbRating,
  toInteger(row.year) AS year,
  // split genres on comma
  [g IN split(coalesce(row.genre,''), ',') | trim(g)] AS genres
WHERE imdbId IS NOT NULL AND imdbId <> ''

MERGE (m:Movie {imdbId: imdbId})
  ON CREATE SET m.title = title, m.releaseYear = year, m.imdbRating = imdbRating
  ON MATCH  SET m.title = coalesce(m.title, title),
               m.releaseYear = coalesce(m.releaseYear, year),
               m.imdbRating = coalesce(m.imdbRating, imdbRating)

WITH m, [g IN genres WHERE g <> '' AND g <> 'N/A'] AS genres
FOREACH (g IN genres |
  MERGE (gg:Genre {type: g})
  MERGE (m)-[:IN_GENRE]->(gg)
);
