from app import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def to_dict(self):
        # criamos um dicionário do objeto
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }