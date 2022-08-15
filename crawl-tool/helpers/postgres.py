import psycopg2


def connect_to_postgres(user, password, host, port, database):
    return psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )
