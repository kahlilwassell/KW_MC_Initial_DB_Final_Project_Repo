WITH 'nostalgic' AS q
MATCH (m:Movie)<-[:ABOUT]-(r:Review)
WHERE toLower(r.text) CONTAINS toLower(q) OR toLower(r.title) CONTAINS toLower(q)
RETURN m.title, r.title, r.rating
ORDER BY m.title, r.rating DESC
LIMIT 50;
