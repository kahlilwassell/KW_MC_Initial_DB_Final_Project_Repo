import logging

from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import DriverError, Neo4jError


class Neo4jDb:

    def __init__(self, uri, user, password, database=None):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def find_movie(self, title):
        with self.driver.session() as session:
            movies = self._find_and_return_movie(title)
        return movies

    def _find_and_return_movie(self, title):
        query = (
            "MATCH (m:Movie {title: $title}) "
            "OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Director) "
            "OPTIONAL MATCH (m)<-[:FEATURED_IN]-(a:Actor)"
            "RETURN m.title AS title, m.year AS year, d.firstName+' '+d.lastName AS director, collect(a.firstName+' '+a.lastName) AS actors"
        )
        try:
            records = self.driver.execute_query(
                query, title=title,
                database_=self.database,routing=RoutingControl.READ,
                result_transformer_=lambda r: r.single().data("title","year","director","actors")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_movies(self):
        with self.driver.session() as session:
            movies = self._find_and_return_movies()
        return movies

    def _find_and_return_movies(self):
        query = (
            "MATCH (m:Movie) "
            "OPTIONAL MATCH (m)<-[:DIRECTED]-(d:Director) "
            "OPTIONAL MATCH (m)<-[:FEATURED_IN]-(a:Actor) "
            "WITH m, d, collect(a.firstName + ' ' + a.lastName) AS actors "
            "RETURN collect({title:m.title, year:m.year,"
            " director:COALESCE(d.firstName+' '+d.lastName,''),"
            " actors:actors}) AS movies"
        )
        try:
            records = self.driver.execute_query(
                query,
                database_=self.database,routing=RoutingControl.READ,
                result_transformer_=lambda r: r.data("movies")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_movie_reviews(self, title):
        with self.driver.session() as session:
            reviews = self._find_and_return_movies_reviews(title)
        return reviews

    def _find_and_return_movie_reviews(self, title):
        query = (
            "MATCH (m:Movie $title) -[:HAS_REVIEW]->(r:Review)<-[:GAVE_REVIEW]- (u:User)"
            "RETURN collect({ review:r.text, rating:r.stars user:u.username }) AS reviews"
        )
        try:
            records = self.driver.execute_query(
                query, first_name=first_name,last_name=last_name,
                database_=self.database,routing=RoutingControl.READ,
                result_transformer_=lambda r: r.data("reviews")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_movies_by_director(self, first_name, last_name):
        with self.driver.session() as session:
            movies = self._find_and_return_movies_by_director(first_name, last_name)
        return movies

    def _find_and_return_movies_by_director(self, first_name, last_name):
        query = (
            "MATCH (m:Movie)<-[:DIRECTED]-(d:Director {firstName:$first_name, lastName:$last_name}) "
            "RETURN collect({ title:m.title, year:m.year}) AS movies"
        )
        try:
            records = self.driver.execute_query(
                query, first_name=first_name,last_name=last_name,
                database_=self.database,routing=RoutingControl.READ,
                result_transformer_=lambda r: r.data("movies")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_movies_by_actor(self, first_name, last_name):
        with self.driver.session() as session:
            movies = self._find_and_return_movies_by_actor(first_name, last_name)
        return movies

    def _find_and_return_movies_by_actor(self, first_name, last_name):
        query = (
            "MATCH (m:Movie)<-[:FEATURED_IN]-(a:Actor {firstName:$first_name, lastName:$last_name}) "
            "RETURN collect({ title:m.title, year:m.year}) AS movies"
        )
        try:
            records = self.driver.execute_query(
                query, first_name=first_name,last_name=last_name,
                database_=self.database,routing=RoutingControl.READ,
                result_transformer_=lambda r: r.data("movies")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_movies_by_genre(self, genre):
        with self.driver.session() as session:
            movies = self._find_and_return_movies_by_genre(genre)
        return movies

    def _find_and_return_movies_by_genre(self, genre):
        query = (
            "MATCH (m:Movie)<-[:HAS_GENRE]-(g:Genre {type:$genre}) "
            "RETURN collect({ title:m.title, year:m.year}) AS movies"
        )
        try:
            records = self.driver.execute_query(
                query, genre=genre,
                database_=self.database,routing=RoutingControl.READ,
                result_transformer_=lambda r: r.data("movies")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_user(self, username):
        with self.driver.session() as session:
            user = self._find_and_return_user(username)
        return user

    def _find_and_return_user(self, username):
        query = (
            "MATCH (u:User {userName:$username}) "
            "RETURN u.firstName AS firstName, u.lastName AS lastName, u.userName AS userName, u.email AS email "
        )
        try:
            records = self.driver.execute_query(
                query, username=username,
                database_=self.database,routing=RoutingControl.READ,
                result_transformer_=lambda r: r.single(strict=True).data("firstName","lastName","userName","email")
            )
            return records
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_watchlist(self, username):
        pass

    def add_watchlist(self, username):
        pass

    def add_to_watchlist(self, username):
        pass

    def find_reviews_by_user(self, username):
        pass

    def add_reviews(self, username):
        pass

    def find_friends(self, username):
        friends = self._find_and_return_friends(username)
        for friend in friends:
            print(f"{username} is friends with {friend}")
        return friends

    def _find_and_return_friends(self, username):
        query = (
            "MATCH (:User {userName:$username})-[:FRIENDS_WITH]->(u:User) "
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

    def connect_friends(self, username1, username2):
        print(f"u1: {username1} u2: {username2}")
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and
            # transient errors
            result = self._create_and_return_friendship(
                username1, username2
            )
        return result

    def _create_and_return_friendship(self, username1, username2):
        print(f"Inside connection fn -> u1:{username1}, u2:{username2}")
        query = (
            "MATCH (u1:User { userName: $username1}) "
            "MATCH (u2:User { userName: $username2}) "
            "MERGE (u1)-[:FRIENDS_WITH]->(u2) "
            "MERGE (u2)-[:FRIENDS_WITH]->(u1) "
            "RETURN u1.firstName AS user1FirstName, u1.lastName AS user1LastName, u2.firstName AS user2FirstName, u2.lastName AS user2LastName"
        )
        try:
            record = self.driver.execute_query(
                query, username1=username1, username2=username2,
                database_=self.database,
                result_transformer_=lambda r: r.single(strict=True).data("user1FirstName", "user1LastName", "user2FirstName", "user2LastName")
            )
            return record
        # Capture any errors along with the query and data for traceability
        except (DriverError, Neo4jError) as exception:
            logging.error("%s raised an error: \n%s", query, exception)
            raise

    def find_friends_network(self, username):
        pass

    def find_movie_recommendations(self, username):
        pass
