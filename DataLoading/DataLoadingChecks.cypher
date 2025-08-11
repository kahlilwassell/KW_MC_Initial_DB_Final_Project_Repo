\\check counts of loaded data
MATCH (:movie)  RETURN count(*) AS movies;
MATCH (:review) RETURN count(*) AS reviews;
MATCH (:actor)  RETURN count(*) AS actors;
MATCH (:director) RETURN count(*) AS directors;
MATCH (:genre)  RETURN count(*) AS genres;
MATCH (:user)   RETURN count(*) AS users;

MATCH (:movie)-[:inGenre]->(:genre) RETURN count(*) AS movieGenreLinks;
MATCH (:director)-[:directs]->(:movie) RETURN count(*) AS directsLinks;
MATCH (:actor)-[:actsIn]->(:movie) RETURN count(*) AS actsInLinks;
MATCH (:movie)-[:hasReview]->(:review) RETURN count(*) AS movieReviewLinks;
MATCH (:user)-[:gaveReview]->(:review) RETURN count(*) AS gaveReviewLinks;
MATCH (:user)-[:wantsToWatch]->(:movie) RETURN count(*) AS wantsToWatchLinks;
MATCH (:user)-[:isFriendsWith]->(:user) RETURN count(*) AS friendLinks;


\\sample movies + genres
MATCH (m:movie)-[:inGenre]->(g:genre)
RETURN m.title, collect(g.name) AS genres
LIMIT 5;


\\sample reviews for a movie
MATCH (m:movie {title: "Inception"})<-[:hasReview]-(rev:review)
RETURN rev.reviewId, rev.rating, left(rev.text, 80) AS snippet
LIMIT 5;


\\who reviewed what
MATCH (u:user)-[gr:gaveReview]->(r:review)<-[:hasReview]-(m:movie)
RETURN u.userName, m.title, r.rating, gr.reviewDate
ORDER BY gr.reviewDate DESC
LIMIT 10;


\\friends check
MATCH (u:user)-[:isFriendsWith]->(f:user)
RETURN u.userName AS user, collect(f.userName) AS friends
LIMIT 5;


\\most reviewed films
MATCH (m:movie)<-[:hasReview]-(:review)
RETURN m.title, count(*) AS reviewCount
ORDER BY reviewCount DESC
LIMIT 10;


\\friend degree check
MATCH (u:user)-[:isFriendsWith]->()
RETURN u.userName, count(*) AS friendCount
ORDER BY friendCount DESC
LIMIT 10;


\\ actor => movie => genre
MATCH (a:actor)-[:actsIn]->(m:movie)-[:inGenre]->(g:genre)
RETURN a.name, collect(DISTINCT m.title) AS movies, collect(DISTINCT g.name) AS genres
LIMIT 5;
