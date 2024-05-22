import psycopg2

def dbConnect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='RGZ_PAD',
        user='pader',
        password='rgzpas')

    return conn