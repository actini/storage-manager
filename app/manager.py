from flask import Flask, request, jsonify

from services import MongoDBService

app = Flask(__name__)

@app.route("/")
def root():
    return "Welcome to Storage Manager!"

@app.route("/health")
def health():
    return "ok"

@app.route("/databases", methods=["GET"])
def all_databases():
    databases = MongoDBService().list_databases()
    return jsonify(databases)

@app.route("/databases", methods=["POST"])
def create_database():
    database = request.json.get("database", None)

    if database is None:
        return {
            "status": "error",
            "message": "Database name is required!"
        }, 400

    mongodb = MongoDBService().connect()

    try:
        mongodb.create_database(database)
    except Exception as e:
        return {
            "status": "error",
            "message": "%s" % (e)
        }, 500

    user = request.json.get("user", None)

    if user is None:
        return {
            "status": "ok",
            "database": database
        }

    username = user.get("username", None)
    password = user.get("password", None)
    permission = user.get("permission", "readWrite")

    if (username is None) or (password is None):
        return {
            "status": "error",
            "message": "Username and password are required to create database with a user!"
        }, 400

    try:
        mongodb.create_user(
            database,
            {
                "username": username,
                "password": password,
                "permission": permission
            }
        )
    except Exception as e:
        return {
            "status": "error",
            "message": "%s" % (e)
        }, 500

    return {
        "status": "ok",
        "database": database,
        "username": username
    }

@app.route("/databases/<database>", methods=["DELETE"])
def drop_database(database):
    try:
        MongoDBService().drop_database(database)
    except Exception as e:
        return {
            "status": "error",
            "message": "%s" % (e)
        }, 500

    return {
        "status": "ok"
    }

@app.route("/users", methods=["POST"])
def create_user():
    database = request.json.get("database", None)
    user = request.json.get("user", {})
    username = user.get("username", None)
    password = user.get("password", None)
    permission = user.get("permission", "readWrite")

    if (database is None) or (username is None) or (password is None):
        return {
            "status": "error",
            "message": "Username, password, database are required to create a user!"
        }, 400

    try:
        MongoDBService().create_user(
            database,
            {
                "username": username,
                "password": password,
                "permission": permission
            }
        )
    except Exception as e:
        return {
            "status": "error",
            "message": "%s" % (e)
        }, 500

    return {
        "status": "ok",
        "database": database,
        "username": username
    }

@app.route("/users/<username>", methods=["PUT", "PATCH"])
def update_user(username):
    database = request.json.get("database", None)
    user = request.json.get("user", {})
    password = user.get("password", None)
    permission = user.get("permission", None)

    if database is None:
        return {
            "status": "error",
            "message": "Database name is required to update a user!"
        }, 400

    if (password is None) and (permission is None):
        return {
            "status": "error",
            "message": "Password or permission is required to update a user!"
        }, 400

    try:
        MongoDBService().update_user(
            database,
            {
                "username": username,
                "password": password,
                "permission": permission
            }
        )
    except Exception as e:
        return {
            "status": "error",
            "message": "%s" % (e)
        }, 500

    return {
        "status": "ok",
        "database": database,
        "username": username
    }


@app.route("/users/<username>", methods=["DELETE"])
def drop_user(username):
    database = request.json.get("database", None)

    if database is None:
        return {
            "status": "error",
            "message": "Database name is required to drop a user!"
        }, 400

    try:
        MongoDBService().drop_user(database, username)
    except Exception as e:
        return {
            "status": "error",
            "message": "%s" % (e)
        }, 500

    return {
        "status": "ok"
    }

if __name__ == "__main__":
    app.run()
