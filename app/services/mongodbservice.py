from utilities import ConfigLoader, ConfigException
from managers import MongoDBManager


class MongoDBService():
    def __init__(self):
        self._config = {}
        self._manager = None

    def _load_config(self):
        config = ConfigLoader().load("config.yaml").get("mongodb")

        scheme = config.get("scheme", "mongodb")
        host = config.get("host", None)
        port = config.get("port", 27017)
        username = config.get("username", None)
        password = config.get("password", None)
        database = config.get("database", None)
        options = config.get("options", {})

        if (host is None) or (username is None) or (password is None) or (database is None):
            raise ConfigException("%s %s %s %s configs are required to connect MongoDB" % (host, username, password, database))

        self._config = config

    def _connect(self):
        if self._manager is None:
            self._load_config()

            self._manager = MongoDBManager().connect(
                self._config.get("scheme"),
                self._config.get("host"),
                self._config.get("username"),
                self._config.get("password"),
                port= self._config.get("port"),
                database = self._config.get("database"),
                options = self._config.get("options")
            )

        return self

    def connect(self):
        return self._connect()

    def list_databases(self):
        self._connect()
        return self._manager.list_databases()

    def create_database(self, database):
        self._connect()
        if self._manager.create_database(database):
            return

        raise MongoDBServiceException("Failed to create MongoDB database %s" % (database))

    def drop_database(self, database):
        self._connect()
        if self._manager.drop_database(database):
            return

        raise MongoDBServiceException("Failed to drop MongoDB database %s" % (database))

    def create_user(self, database, user):
        self._connect()
        if self._manager.create_user(
            database,
            user.get("username"),
            user.get("password"),
            user.get("permission", "readWrite")
        ):
            return

        raise MongoDBServiceException("Failed to create user %s" % (user.get("username")))

    def update_user(self, database, user):
        self._connect()
        if self._manager.update_user(
            database,
            user.get("username"),
            user.get("password", None),
            user.get("permission", None)
        ):
            return

        raise MongoDBServiceException("Failed to update user %s" % (user.get("username")))

    def drop_user(self, database, username):
        self._connect()
        if self._manager.drop_user(database, username):
            return

        raise MongoDBServiceException("Failed to drop user %s" % (username))

class MongoDBServiceException(Exception): ...