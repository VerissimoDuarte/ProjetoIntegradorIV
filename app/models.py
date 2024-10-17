from app import db, UserMixin

class RegisterNF(db.Model):
    __tablename__ = 'register_NF'
    id = db.Column(db.Integer, primary_key=True)
    NFId = db.Column(db.BigInteger, nullable=True, unique=True)
    NFDate = db.Column(db.DateTime, nullable=True)
    NFValue = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f"<RegisterNF (Id={self.id}, Numero Nota={self.NFId})>"
    
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True, unique=True)
    password = db.Column(db.String, nullable=True)
    role = db.Column(db.String, nullable=True, default='user')
    
    
    def __repr__(self):
        return f"<User(Nome={self.name}, email={self.email})>"
    
    
