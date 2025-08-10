import logging

from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import DriverError, Neo4jError


class Neo4jDb:

    def __init__(self, uri, user, password, database=None):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def connect_friends(self, username1, username2):
        print(f"u1: {username1} u2: {username2}")
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and
            # transient errors
            result = self._create_and_return_friendship(
                username1, username2
            )
            print("Created friendship between: "
                  f"{result['username1']}, {result['username2']}")
        return result

    def _create_and_return_friendship(self, username1, username2):
        print(f"Inside connection fn -> u1:{username1}, u2:{username2}")
        query = (
            "MATCH (u1:User { userName: $username1}) "
            "MATCH (u2:User { userName: $username2}) "
            "MERGE (u1)-[:FRIENDS_WITH]->(u2) "
            "MERGE (u2)-[:FRIENDS_WITH]->(u1) "
            "RETURN u1.firstName AS username1, u2.firstName AS username2"
        )
        try:
            record = self.driver.execute_query(
                query, username1=username1, username2=username2,
                database_=self.database,
                result_transformer_=lambda r: r.single(strict=True)
            )
            return {"username1": record["username1"], "username2": record["username2"]}
        # Capture any errors along with the query and data for traceability
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_friends(self, username):
        friends = self._find_and_return_friends(username)
        for friend in friends:
            print(f"{username} is friends with {friend}")
        return friends

    def _find_and_return_friends(self, username):
        query = (
            "MATCH (:User {name:$username})-[:FRIENDS_WITH]->(u:User) "
            "RETURN u.firstName AS firstName, u.lastName AS lastName, u.email AS email"
        )
        try:
            records = self.driver.execute_query(
                query, username=username,
                database_=self.database, routing_=RoutingControl.READ,
                result_transformer_=lambda r: r.data("firstName","lastName","email")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_movie(self, title):
        with self.driver.session() as session:
            movies = self._find_and_return_movie(title)
        return movies

    def _find_and_return_movie(self, title):
        query = (
            "MATCH (m:Movie {title: $title})<-[:DIRECTED]-(d:Director) "
            "RETURN m.title AS title, m.year AS year, d.name AS director"
        )
        try:
            records = self.driver.execute_query(
                query, title=title,
                database_=self.database,routing=RoutingControl.READ,
                result_transformer_=lambda r: r.data("title","year","director")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise


    def find_movie_by_genre(self, genre):
        movies = self._find_and_return_movies_by_genre(genre)
        print(movies)
        for movie in movies:
            print(movie)
            for x in movie:
                print(x)

    def _find_and_return_movies_by_genre(self, genre):
        query = (
            "MATCH (m:Movie {genre: $genre})"
            "RETURN m.title AS title, m.genre AS genre, m.year AS year"
        )
        results = self.driver.execute_query(
            query, genre=genre,
            database_=self.database, routing=RoutingControl.READ,
            result_transformer_=lambda r: r.values("title", "genre", "year")
        )

        return results

# TODO: Remove after testing
if __name__ == "__main__":
    scheme = "neo4j"
    host_name = "127.0.0.1"
    port = 7687
    uri = f"{scheme}://{host_name}:{port}"
    user = "neo4j"
    password = "your_password"
    database = "neo4j"
    app = Neo4jDb(uri, user, password, database)
    try:
        app.find_movie("The Godfather")
        app.find_movie_by_genre("Sci-Fi")
    finally:
        app.close()
