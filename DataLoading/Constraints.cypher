// Movies
CREATE CONSTRAINT movie_imdbid IF NOT EXISTS
FOR (m:Movie) REQUIRE m.imdbId IS UNIQUE;

// Genres
CREATE CONSTRAINT genre_type IF NOT EXISTS
FOR (g:Genre) REQUIRE g.type IS UNIQUE;

// Reviews (synthetic deterministic key)
CREATE CONSTRAINT review_key IF NOT EXISTS
FOR (r:Review) REQUIRE r.reviewKey IS UNIQUE;
