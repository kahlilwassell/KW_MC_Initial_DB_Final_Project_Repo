from flask import Flask, g, Blueprint, request, jsonify
import neo4jconn
import configparser


def connect_db(config):
    if 'neo4j_conn' not in g:
        scheme = config["scheme"]
        host_name = config["host_name"]
        port = config["port"]
        g.neo4j_conn = neo4jconn.Neo4jDb(
            uri=f"{scheme}://{host_name}:{port}",
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
    return g.neo4j_conn


def create_app(config):
    app = Flask(__name__)

    with app.app_context():
        app.driver = connect_db(config)

    @app.teardown_appcontext
    def close_db(exception):
        """Close the Neo4j connection when the app context ends."""
        conn = g.pop('neo4j_conn', None)
        if conn is not None:
            conn.close()

    # checked but untested
    @ver_bp.route("/movie/<title>")
    def get_movie(title):
        result = app.driver.find_movie(title)
        return result

    # checked
    @ver_bp.route("/movie/new", methods=["POST"])
    def set_movie():
        data = request.get_json()
        movie_id = data.get("movieId")
        title = data.get("title")
        year = data.get("releaseYear")

        if not all([movie_id, title, year]):
            return {"error": "The movie_id, title, and year must not be empty."}

        result = app.driver.add_movie(movie_id, title, year)
        return result

    # checked
    @ver_bp.route("/movie/genres/new", methods=["POST"])
    def set_movie_genres():
        data = request.get_json()
        title = data.get("title")
        genres = data.get("genres", [])

        if len(genres) == 0:
            return {"error": "Include more than one genre."}

        result = app.driver.add_genres_to_movie(title, genres)
        return result

    # checked but untested
    @ver_bp.route("/movies")
    def get_movies():
        result = app.driver.find_movies()
        return result

    @ver_bp.route("/movie/<title>/reviews")
    def get_movie_reviews(title):
        result = app.driver.find_movie_reviews(title)
        return result

    # checked but untested
    @ver_bp.route("movies/director/<fullname>")
    def get_movies_by_director(fullname):
        result = app.driver.find_movies_by_director(fullname)
        return result

    # checked but untested
    @ver_bp.route("movies/actor/<fullname>")
    def get_movies_by_actor(fullname):
        result = app.driver.find_movies_by_actor(fullname)
        return result

    # checked but untested
    @ver_bp.route("movies/genre/<genre>")
    def get_movies_by_genre(genre):
        result = app.driver.find_movies_by_genre(genre)
        return result

    # checked but untested
    @ver_bp.route("user/<username>")
    def get_user(username):
        result = app.driver.find_user(username)
        return result

    # checked
    @ver_bp.route("user/<username>/watchlist")
    def get_watchlist(username):
        result = app.driver.find_watchlist(username)
        return result

    # checked
    @ver_bp.route("user/<username>/reviews")
    def get_reviews(username):
        result = app.driver.find_reviews_by_user(username)
        return result

    # checked
    @ver_bp.route("user/<username>/friends")
    def get_friends(username):
        result = app.driver.find_friends(username)
        return result

    # checked
    @ver_bp.route("/friends/new", methods=["POST"])
    def set_friends():
        data = request.get_json()
        print(f"data: {data}")
        result = app.driver.connect_friends(data.get("username1"), data.get("username2"))
        return result

    # Advanced queries
    # checked
    @ver_bp.route("user/<username>/friends/network/<degree>")
    def get_friends_network(username, degree):
        result = app.driver.find_friends_network(username, degree)
        return result

    # checked
    @ver_bp.route("user/<username>/movies/hottest")
    def get_hottest_movies(username):
        result = app.driver.find_hottest_movies(username)
        return result

    # checked
    @ver_bp.route("user/<username>/movies/recommendations")
    def get_movie_recommendations(username):
        result = app.driver.find_movie_recommendations(username)
        return result

    # checked
    @ver_bp.route("reviews/<keyword>")
    def get_reviews_with_keyword(keyword):
        result = app.driver.find_reviews_with_keyword(keyword)
        return result

    return app


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    ver_bp = Blueprint(config["Flask"]["version"], __name__, url_prefix="/api/v1")
    app = create_app(config["Neo4jdb"])
    app.register_blueprint(ver_bp)
    app.run(debug=True)
