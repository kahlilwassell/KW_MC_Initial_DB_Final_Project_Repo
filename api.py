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

    # Checked
    @ver_bp.route("/movie/<title>")
    def get_movie(title):
        result = app.driver.find_movie(title)
        return result

    # Checked
    @ver_bp.route("/movies")
    def get_movies():
        result = app.driver.find_movies()
        return result

    @ver_bp.route("/movie/<title>/ratings")
    def get_movie_ratings(title):
        result = app.driver.find_movie_ratings(title)
        return result

    @ver_bp.route("/movie/<title>/reviews")
    def get_movie_reviews(title):
        result = app.driver.find_movie_reviews(title)
        return result

    def _format_names(fullname):
        names = fullname.strip().split(" ")
        if len(names)>= 2:
            first_name = names[0]
            last_name = names[-1]
        else:
            first_name = names[0]
            last_name = ""
        return (first_name, last_name)

    # Checked
    @ver_bp.route("movies/director/<fullname>")
    def get_movies_by_director(fullname):
        first_name, last_name = _format_names(fullname)
        result = app.driver.find_movies_by_director(first_name, last_name)
        return result

    # Checked
    @ver_bp.route("movies/actor/<fullname>")
    def get_movies_by_actor(fullname):
        first_name, last_name = _format_names(fullname)
        result = app.driver.find_movies_by_actor(first_name, last_name)
        return result

    # Checked
    @ver_bp.route("movies/genre/<genre>")
    def get_movies_by_genre(genre):
        first_name, last_name = _format_names(genre)
        result = app.driver.find_movies_by_genre(genre)
        return result
    
    # Checked
    @ver_bp.route("/user/<username>")
    def get_user(username):
        result = app.driver.find_user(username)
        return result

    @ver_bp.route("user/<username>/watchlist")
    def get_watchlist(username):
        result = app.driver.find_watchlist(username)
        return result

    @ver_bp.route("user/<username>/watchlist/new", methods=["POST"])
    def set_watchlist(username):
        data = request.get_json()
        result = app.driver.add_watchlist(data.get("username"))
        return result

    @ver_bp.route("user/<username>/watchlist", methods=["POST"])
    def set_to_watchlist(username):
        data = request.get_json()
        print(f"data: {data}")
        result = app.driver.add_to_watchlist(username, data.get("title"))
        return result

    @ver_bp.route("user/<username>/ratings")
    def get_ratings_by_user(username):
        result = app.driver.find_ratings_by_user(username)
        return result

    @ver_bp.route("user/<username>/ratings/new", methods=["POST"])
    def set_rating(username):
        data = request.get_json()
        print(f"data: {data}")
        result = app.driver.add_rating(username, data.get("title"), data.get("stars"))
        return result
    
    @ver_bp.route("user/<username>/reviews")
    def get_reviews(username):
        result = app.driver.find_reviews_by_user(username)
        return result

    @ver_bp.route("user/<username>/review/new", methods=["POST"])
    def set_review(username):
        data = request.get_json()
        print(f"data: {data}")
        result = app.driver.add_review(username, data.get("title"), data.get("content"))
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

    @ver_bp.route("user/<username>/friends/network")
    def get_friends_network(username):
        result = app.driver.find_friends_network(username)
        return result

    @ver_bp.route("user/<username>/movies/recommendations")
    def get_movie_recommendations(username):
        result = app.driver.find_movie_recommendations(username)
        return result

    return app


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    ver_bp = Blueprint(config["Flask"]["version"], __name__, url_prefix="/api/v1")
    app = create_app(config["Neo4jdb"])
    app.register_blueprint(ver_bp)
    app.run(debug=True)
