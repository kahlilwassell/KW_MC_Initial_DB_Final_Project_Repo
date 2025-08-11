:param {
  // Define the file path root and the individual file names required for loading.
  // https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
  file_path_root: 'file:///', // Change this to the folder your script can access the files at.
  file_0: 'movieReviews.csv',
  file_1: 'movies.csv',
  file_2: 'directors.csv',
  file_3: 'actors.csv',
  file_4: 'genres.csv',
  file_5: 'users.csv',
  file_6: 'hasReview.csv',
  file_7: 'directs.csv',
  file_8: 'inGenre.csv',
  file_9: 'actsIn.csv',
  file_10: 'gaveReview.csv',
  file_11: 'wantsToWatch.csv',
  file_12: 'isFriendsWith.csv'
};

// CONSTRAINT creation
// -------------------
//
// Create node uniqueness constraints, ensuring no duplicates for the given node label and ID property exist in the database. This also ensures no duplicates are introduced in future.
//
// NOTE: The following constraint creation syntax is generated based on the current connected database version 2025.7.1.
CREATE CONSTRAINT `movieId_movie_uniq` IF NOT EXISTS
FOR (n: `movie`)
REQUIRE (n.`movieId`) IS UNIQUE;
CREATE CONSTRAINT `reviewId_review_uniq` IF NOT EXISTS
FOR (n: `review`)
REQUIRE (n.`reviewId`) IS UNIQUE;
CREATE CONSTRAINT `actorId_actor_uniq` IF NOT EXISTS
FOR (n: `actor`)
REQUIRE (n.`actorId`) IS UNIQUE;
CREATE CONSTRAINT `directorId_director_uniq` IF NOT EXISTS
FOR (n: `director`)
REQUIRE (n.`directorId`) IS UNIQUE;
CREATE CONSTRAINT `genreId_genre_uniq` IF NOT EXISTS
FOR (n: `genre`)
REQUIRE (n.`genreId`) IS UNIQUE;
CREATE CONSTRAINT `userId_user_uniq` IF NOT EXISTS
FOR (n: `user`)
REQUIRE (n.`userId`) IS UNIQUE;

:param {
  idsToSkip: []
};

// NODE load
// ---------
//
// Load nodes in batches, one node label at a time. Nodes will be created using a MERGE statement to ensure a node with the same label and ID property remains unique. Pre-existing nodes found by a MERGE statement will have their other properties set to the latest values encountered in a load file.
//
// NOTE: Any nodes with IDs in the 'idsToSkip' list parameter will not be loaded.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row
WHERE NOT row.`movieId` IN $idsToSkip AND NOT row.`movieId` IS NULL
CALL {
  WITH row
  MERGE (n: `movie` { `movieId`: row.`movieId` })
  SET n.`movieId` = row.`movieId`
  SET n.`title` = row.`title`
  SET n.`genre` = row.`genre`
  SET n.`releaseYear` = toInteger(trim(row.`year`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`reviewId` IN $idsToSkip AND NOT toInteger(trim(row.`reviewId`)) IS NULL
CALL {
  WITH row
  MERGE (n: `review` { `reviewId`: toInteger(trim(row.`reviewId`)) })
  SET n.`reviewId` = toInteger(trim(row.`reviewId`))
  SET n.`title` = row.`title`
  SET n.`rating` = toInteger(trim(row.`rating`))
  SET n.`text` = row.`text`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_3) AS row
WITH row
WHERE NOT row.`actorId` IN $idsToSkip AND NOT toInteger(trim(row.`actorId`)) IS NULL
CALL {
  WITH row
  MERGE (n: `actor` { `actorId`: toInteger(trim(row.`actorId`)) })
  SET n.`actorId` = toInteger(trim(row.`actorId`))
  SET n.`name` = row.`name`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
WITH row
WHERE NOT row.`directorId` IN $idsToSkip AND NOT toInteger(trim(row.`directorId`)) IS NULL
CALL {
  WITH row
  MERGE (n: `director` { `directorId`: toInteger(trim(row.`directorId`)) })
  SET n.`directorId` = toInteger(trim(row.`directorId`))
  SET n.`name` = row.`name`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_4) AS row
WITH row
WHERE NOT row.`genreId` IN $idsToSkip AND NOT toInteger(trim(row.`genreId`)) IS NULL
CALL {
  WITH row
  MERGE (n: `genre` { `genreId`: toInteger(trim(row.`genreId`)) })
  SET n.`genreId` = toInteger(trim(row.`genreId`))
  SET n.`name` = row.`name`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_5) AS row
WITH row
WHERE NOT row.`userId` IN $idsToSkip AND NOT toInteger(trim(row.`userId`)) IS NULL
CALL {
  WITH row
  MERGE (n: `user` { `userId`: toInteger(trim(row.`userId`)) })
  SET n.`userId` = toInteger(trim(row.`userId`))
  SET n.`name` = row.`name`
  SET n.`userName` = row.`userName`
  SET n.`email` = row.`email`
} IN TRANSACTIONS OF 10000 ROWS;


// RELATIONSHIP load
// -----------------
//
// Load relationships in batches, one relationship type at a time. Relationships are created using a MERGE statement, meaning only one relationship of a given type will ever be created between a pair of nodes.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_7) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `director` { `directorId`: toInteger(trim(row.`directorId`)) })
  MATCH (target: `movie` { `movieId`: row.`movieId` })
  MERGE (source)-[r: `directs`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_9) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `actor` { `actorId`: toInteger(trim(row.`actorId`)) })
  MATCH (target: `movie` { `movieId`: row.`movieId` })
  MERGE (source)-[r: `actsIn`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `movie` { `movieId`: row.`movieId` })
  MATCH (target: `review` { `reviewId`: toInteger(trim(row.`reviewId`)) })
  MERGE (source)-[r: `hasReview`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_8) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `movie` { `movieId`: row.`imdbId` })
  MATCH (target: `genre` { `genreId`: toInteger(trim(row.`genreId`)) })
  MERGE (source)-[r: `inGenre`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_11) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `user` { `userId`: toInteger(trim(row.`userId`)) })
  MATCH (target: `movie` { `movieId`: row.`movieId` })
  MERGE (source)-[r: `wantsToWatch`]->(target)
  SET r.`addedOn` = row.`addedOn`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_12) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `user` { `userId`: toInteger(trim(row.`userAId`)) })
  MATCH (target: `user` { `userId`: toInteger(trim(row.`userBId`)) })
  MERGE (source)-[r: `isFriendsWith`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_10) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `user` { `userId`: toInteger(trim(row.`userId`)) })
  MATCH (target: `review` { `reviewId`: toInteger(trim(row.`reviewId`)) })
  MERGE (source)-[r: `gaveReview`]->(target)
  SET r.`reviewDate` = row.`reviewDate`
} IN TRANSACTIONS OF 10000 ROWS;
