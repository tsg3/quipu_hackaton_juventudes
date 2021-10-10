from datetime import datetime

from flaskr.app.persistence.db import db_connect

def post_forum(id, form):
    try:
        connection = db_connect()

        timedate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with connection.cursor() as cursor:
            cursor.execute(
            """INSERT INTO Foro 
                (idUsuario, titulo, datos,
                publicacion, cerrado, estado) VALUES 
            (%s, %s, %s, %s, %s, %s);""",
            (id, form["titulo"], form["datos"], timedate, 0, 1))
        connection.commit()

        connection.close()
        return 0
    except Exception as e:
        print(e)
        return -1

def get_forums():
    try:
        connection = db_connect()

        match = None
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id, titulo FROM Foro;""")
            match = cursor.fetchall()

        connection.close()
        return match
    except Exception as e:
        print(e)
        return -1

def get_forum(id):
    try:
        connection = db_connect()

        match = None
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT titulo, datos FROM Foro WHERE id = %s;""", (id))
            match = cursor.fetchone()
        if match == None:
            return -2

        connection.close()
        return match
    except Exception as e:
        print(e)
        return -1