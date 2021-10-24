from hashlib import md5

from flaskr.app.persistence.db import db_connect

def create_user(form):
    try:
        connection = db_connect()

        password = md5(form["contrasena"].encode()).hexdigest()[0:20]

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT id FROM Genero WHERE genero = %s;""", (form["genero"], ))
            id_genero = cursor.fetchone()[0]

            cursor.execute(
            """INSERT INTO Usuario 
                (idRol, correo, nombre, apellido1, apellido2, 
                nacimiento, idGenero, nacionalidad, residencia, 
                contrasena, estado) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            (form["idRol"], form["correo"], form["nombre"], form["apellido1"], 
            form["apellido2"], form["fecha"], id_genero, form["nacionalidad"], 
            form["residencia"], password, 1))
        connection.commit()

        connection.close()
        return 0
    except Exception as e:
        print(e)
        return -1

def login_user(form):
    try:
        connection = db_connect()

        password = md5(form["contrasena"].encode()).hexdigest()[0:20]

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT id FROM Usuario 
                WHERE correo = %s AND contrasena = %s;""",
                (form["correo"], password))
            match = cursor.fetchone()
        if match == None:
            connection.close()
            return -2

        connection.close()
        return match
    except Exception as e:
        print(e)
        return -1

def get_user_for_session(id):
    try:
        connection = db_connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT id, correo, contrasena, estado 
                FROM Usuario WHERE id = %s;""", (id))
            match = cursor.fetchone()
        if match == None:
            connection.close()
            return -2

        connection.close()
        return match
    except Exception as e:
        print(e)
        return -1

def get_user_data(key):
    try:
        connection = db_connect()

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT U.correo, U.nombre, U.apellido1, U.apellido2, 
                    U.nacimiento, G.genero, U.nacionalidad, U.residencia, 
                    U.estado, R.rol
                FROM Usuario AS U
                INNER JOIN Rol AS R ON U.idRol = R.id
                INNER JOIN Genero AS G ON U.idGenero = G.id
                WHERE U.id = %s;""", (key))

                # Needed for final product
                # 
                # INNER JOIN ActividadUsuario AS AU ON U.id = AU.idUsuario
                # INNER JOIN Actividad AS A ON AU.idActividad = A.id

            match = cursor.fetchone()

        connection.close()
        return match
    except Exception as e:
        print(e)
        return -1