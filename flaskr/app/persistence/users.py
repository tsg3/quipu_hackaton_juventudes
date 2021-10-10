from flaskr.app.persistence.db import db_connect

def get_roles():
    connection = db_connect()
    roles = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM quipu_db.Rol")
        roles = cursor.fetchall()
    connection.close()
    return roles