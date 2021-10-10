from flask_login import UserMixin

class User(UserMixin):
    def __init__(self):
        self.id = None
        self.username = None
        self.contrasena = None
        self.estado = None

    def is_active(self):
        return self.estado

    def get_id(self):
        try:
            return str(self.id)
        except:
            return None

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False