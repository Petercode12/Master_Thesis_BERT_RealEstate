from pymongo import MongoClient


def connect_to_mongodb(user, password, host, port, database):
    client = MongoClient(
        "%s:%d" % (host, port),
        username=user,
        password=password,
        authSource="admin",
        authMechanism="SCRAM-SHA-1",
    )
    return client.get_database(database)
