import time
from urllib import parse as URLParse
from pymongo import MongoClient
from pymongo.helpers import OperationFailure


class MongoDBManager():
    def __init__(self):
        self._client = None
        self._config = None

    def connect(self, scheme, host, username, password, port = 27017, database = "admin", options = {}):
        if scheme == "mongodb":
            connection_string = "mongodb://{}:{}@{}:{}/{}?{}".format(
                URLParse.quote_plus(username),
                URLParse.quote_plus(password),
                host,
                port,
                database,
                self._get_connection_query_string(options)
            )
        elif scheme == "mongodb+srv":
            connection_string = "mongodb+srv://{}:{}@{}/{}?{}".format(
                URLParse.quote_plus(username),
                URLParse.quote_plus(password),
                host,
                database,
                self._get_connection_query_string(options)
            )
        else:
            raise SchemeNotSupportedException("Scheme %s not supported!" % (scheme))

        self._client = MongoClient(connection_string)

        return self

    def _get_connection_query_string(self, options):
        if type(options) == str:
            return options

        if type(options) == list:
            return "&".join(options)

        if type(options) == dict:
            items = []
            for key, value in options.items():
                items.append("%s=%s" % (key, value))

            return "&".join(items)

    def _get_client(self):
        if self._client is None:
            self._connect()

        return self._client

    def list_databases(self):
        return self._get_client().list_database_names()

    def create_database(self, database):
        collection = self._get_client().get_database(database).get_collection("operation_logs")
        collection.insert_one(
                {
                    "created_by": __name__,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            )

        if collection.find({"created_by": __name__}).count() > 0:
            return True

        return False

    def drop_database(self, database):
        self._get_client().get_database(database).command("dropAllUsersFromDatabase", 1)
        self._get_client().drop_database(database)
        return True

    def create_user(self, database, username, password, permission = "readWrite"):
        try:
            self._get_client().get_database(database).command(
                "createUser",
                username,
                pwd=password,
                roles=[permission]
            )
        except OperationFailure as e:
            if e.code == 51003:
                raise UserAlreadyExistsException("User {}@{} alerady exists!".format(username, database))

            raise e

        self._get_client().get_database(database).command("usersInfo", username)
        return True

    def update_user(self, database, username, password = None, permission = None):
        if password is not None:
            self._get_client().get_database(database).command(
                "updateUser",
                username,
                pwd=password
            )

        if permission is not None:
            self._get_client().get_database(database).command(
                "updateUser",
                username,
                roles=[permission]
            )

        return True

    def drop_user(self, database, username):
        self._get_client().get_database(database).command(
            "dropUser",
            username
        )
        return True

class UserAlreadyExistsException(Exception): ...
class SchemeNotSupportedException(Exception): ...