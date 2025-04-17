import psycopg2


def getConnection (): 
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"
    )
    return conn