from flask import Flask, jsonify, g
import json
import neo4jconn


def connect_db():
    if 'neo4j_conn' not in g:
        scheme = "neo4j"
        host_name = "127.0.0.1"
        port = 7687
        g.neo4j_conn = neo4jconn.App(
            uri=f"{scheme}://{host_name}:{port}",
            user="neo4j",
            password="<password>",
            database="neo4j"
        )
    return g.neo4j_conn


def create_app():
    app = Flask(__name__)

    with app.app_context():
        app.driver = connect_db()

    @app.teardown_appcontext
    def close_db(exception):
        """Close the Neo4j connection when the app context ends."""
        conn = g.pop('neo4j_conn', None)
        if conn is not None:
            conn.close()


    @app.route("/movie/<title>")
    def get_movie(title):
        result = app.driver.find_movie(title)
        return jsonify(result)


    @app.route("/user/<username>")
    def get_username(username):
        print(f"username0: {username}")
        result = app.driver.find_user(username)
        return jsonify(result)

    @app.route("/friends/<username>")
    def get_friends(username):
        print(f"username0: {username}")
        result = app.driver.find_friends(username)
        return jsonify(result)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
