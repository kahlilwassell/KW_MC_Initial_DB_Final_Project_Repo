LOAD CSV WITH HEADERS FROM 'file:///imdb_reviews.csv' AS row
WITH
  trim(row.imdb_id)       AS imdbId,
  trim(row.`review title`) AS rtitle,
  toInteger(row.review_rating) AS rr,
  trim(row.review)        AS rtext
WHERE imdbId IS NOT NULL AND imdbId <> ''

MATCH (m:Movie {imdbId: imdbId})
WITH m, rtitle, rr, rtext,
     // deterministic key for MERGE
     (m.imdbId + '|' + coalesce(left(rtitle,80),'') + '|' + coalesce(left(rtext,120),'')) AS reviewKey
MERGE (r:Review {reviewKey: reviewKey})
  ON CREATE SET r.title = rtitle, r.text = rtext, r.rating = rr, r.source = 'IMDB'
  ON MATCH  SET r.title = coalesce(r.title, rtitle),
               r.text = coalesce(r.text, rtext),
               r.rating = coalesce(r.rating, rr)
MERGE (r)-[:ABOUT]->(m);
