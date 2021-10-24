from datetime import datetime

from flaskr.app.persistence.db import db_connect
from flaskr.app.models.forums import even_sort

def post_forum(id, key, form):
    try:
        connection = db_connect()

        timedate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with connection.cursor() as cursor:
            cursor.execute(
            """INSERT INTO Foro 
                (id, idUsuario, titulo, datos,
                publicacion, cerrado, estado) VALUES 
            (X%s, %s, %s, %s, %s, %s, %s);""",
            (key, id, form["titulo"], form["datos"], timedate, 0, 1))
        connection.commit()

        connection.close()
        return 0
    except Exception as e:
        print(e)
        return -1

def get_forums():
    try:
        connection = db_connect()

        men_matches = None
        non_men_matches = None

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT F.id, F.titulo 
                FROM Foro AS F
                INNER JOIN Usuario AS U ON F.idUsuario = U.id
                WHERE U.idGenero = 2
                ORDER BY publicacion DESC;""")
            men_matches = cursor.fetchall()

            cursor.execute(
                """SELECT F.id, F.titulo 
                FROM Foro AS F
                INNER JOIN Usuario AS U ON F.idUsuario = U.id
                WHERE U.idGenero != 2
                ORDER BY publicacion DESC;""")
            non_men_matches = cursor.fetchall()

        match = even_sort(men_matches, non_men_matches)

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
                SELECT 
                Foro.titulo, Foro.datos, Foro.publicacion, Foro.cerrado,
                Usuario.nombre, Usuario.apellido1, Usuario.apellido2
                FROM Foro 
                INNER JOIN Usuario ON Foro.idUsuario = Usuario.id
                WHERE Foro.id = %s;""", (id))
            match = cursor.fetchone()
        if match == None:
            connection.close()
            return -2

        connection.close()
        return match
    except Exception as e:
        print(e)
        return -1

def post_comment(text, idUser, datetime, idForum=None, idComment=None):
    if idForum == None and idComment == None:
        return -2

    try:
        connection = db_connect()

        if idForum != None:
            with connection.cursor() as cursor:
                cursor.execute(
                """INSERT INTO ComentarioForo 
                    (idUsuario, idForo, texto, publicacion,
                    votos, promedio, estado) VALUES 
                (%s, %s, %s, %s, %s, %s, %s);""",
                (idUser, idForum, text, datetime, 0, 0, 1))
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                """INSERT INTO ComentarioForo 
                    (idUsuario, idComentarioForo, texto, publicacion,
                    votos, promedio, estado) VALUES 
                (%s, %s, %s, %s, %s, %s, %s);""",
                (idUser, idComment, text, datetime, 0, 0, 1))
        connection.commit()

        connection.close()
        return 0
    except Exception as e:
        print(e)
        return -1

def get_comments(idForum): 
    try:
        connection = db_connect()

        responses = {}

        with connection.cursor() as cursor:
            cursor.execute(
            """SELECT Comm.id, Comm.texto, Comm.publicacion,
                Comm.votos, Comm.promedio,
                Us.nombre, Us.apellido1, Us.apellido2
                FROM ComentarioForo AS Comm
                INNER JOIN Usuario AS Us ON Comm.idUsuario = Us.id
                WHERE Comm.idForo = %s;""", (idForum))
            responses["comms"] = cursor.fetchall()
        
        replies = {}

        with connection.cursor() as cursor:
            for match in responses["comms"]:
                cursor.execute(
                """SELECT Comm.id, Comm.texto, Comm.publicacion,
                    Comm.votos, Comm.promedio,
                    Us.nombre, Us.apellido1, Us.apellido2
                    FROM ComentarioForo AS Comm
                    INNER JOIN Usuario AS Us ON Comm.idUsuario = Us.id
                    WHERE Comm.idComentarioForo = %s;""", (match[0]))
                replies[match[0]] = cursor.fetchall()
        responses["replies"] = replies

        connection.close()
        return responses
    except Exception as e:
        print(e)
        return -1

def save_forum(idUser, idForum):
    try:
        connection = db_connect()

        match = None
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT estado FROM ForoGuardar
                WHERE idForo = %s AND idUsuario = %s;""", 
                (idForum, idUser))
            match = cursor.fetchone()

        if match == None:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO ForoGuardar 
                    (idForo, idUsuario, estado) VALUES
                    (%s, %s, 1);""", (idForum, idUser))

        else:
            new_state = 1 if match[0] == 0 else 0
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE ForoGuardar SET estado = %s
                    WHERE idForo = %s AND idUsuario = %s;""", 
                    (new_state, idForum, idUser))

        connection.commit()

        connection.close()
        return 0
    except Exception as e:
        print(e)
        return -1

def check_saved(idUser, idForum):
    try:
        connection = db_connect()

        match = None
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT estado FROM ForoGuardar
                WHERE idForo = %s AND idUsuario = %s;""", 
                (idForum, idUser))
            match = cursor.fetchone()
        if match == None:
            match = 0
        
        connection.close()
        return match[0]

    except Exception as e:
        print(e)
        return -1

def get_saved_forums(idUser):
    try:
        connection = db_connect()

        match = None
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT F.id, F.titulo FROM Foro AS F
                INNER JOIN ForoGuardar AS G 
                    ON F.id = G.idForo
                WHERE G.idUsuario = %s AND G.estado = 1;""",
                (idUser,))
            match = cursor.fetchall()

        connection.close()
        return match
    except Exception as e:
        print(e)
        return -1