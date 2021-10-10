from flaskr.app.persistence.db import db_connect
from hashlib import md5

def create_user(form):
    try:
        connection = db_connect()

        idRol = 1 if form["idRol"] == "1" else 4 # Check with HTML
        password = md5(form["contrasena"].encode()).hexdigest()[0:20]
        birth_date = "%s-%s-%s" % (form["ano"], form["mes"], form["dia"])

        with connection.cursor() as cursor:
            cursor.execute(
            """INSERT INTO Usuario 
                (idRol, username, nombre, apellido1, apellido2, 
                nacimiento, genero, nacionalidad, residencia, 
                actividad, contrasena, estado) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            (idRol, form["nombre"], form["username"], form["apellido1"], 
            form["apellido2"], birth_date, form["genero"], form["nacionalidad"], 
            form["residencia"], form["actividad"], password, 1))
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
                WHERE username = %s AND contrasena = %s;""",
                (form["username"], password))
            match = cursor.fetchone()
        if match == None:
            return -2

        connection.close()
        return 0
    except Exception as e:
        print(e)
        return -1