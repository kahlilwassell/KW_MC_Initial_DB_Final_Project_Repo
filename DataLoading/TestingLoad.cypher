MATCH (m:Movie) RETURN count(m) AS movies;
MATCH (:Movie)-[:IN_GENRE]->(:Genre) RETURN count(*) AS movieGenreLinks;
MATCH (m:Movie)<-[:ABOUT]-(r:Review) RETURN m.title, count(r) AS numReviews ORDER BY numReviews DESC LIMIT 10;
RETURN avg(m.imdbRating) AS avgIMDB FROM (MATCH (m:Movie) RETURN m);
