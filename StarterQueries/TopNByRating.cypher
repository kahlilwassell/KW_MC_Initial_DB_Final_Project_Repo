WITH 10 AS N
MATCH (m:Movie)
WHERE m.imdbRating IS NOT NULL
RETURN m.title, m.releaseYear, m.imdbRating
ORDER BY m.imdbRating DESC, m.title ASC
LIMIT N;
