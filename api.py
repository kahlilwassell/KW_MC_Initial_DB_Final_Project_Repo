from flask import Flask, g, Blueprint, request
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


    @ver_bp.route("/movie/<title>")
    def get_movie(title):
        result = app.driver.find_movie(title)
        return result


    @ver_bp.route("/user/<username>")
    def get_username(username):
        result = app.driver.find_user(username)
        return result

    @ver_bp.route("/friends/<username>")
    def get_friends(username):
        result = app.driver.find_friends(username)
        return result

    @ver_bp.route("/friends/connection", methods=["POST"])
    def set_friends():
        data = request.get_json()
        print(f"data: {data}")
        result = app.driver.connect_friends(data.get("username1"), data.get("username2"))
        return result

    return app


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    ver_bp = Blueprint(config["Flask"]["version"], __name__, url_prefix="/api/v1")
    app = create_app(config["Neo4jdb"])
    app.register_blueprint(ver_bp)
    app.run(debug=True)
