from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    rut = db.Column(db.String(15), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(180), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=True)
    birth_date = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(10), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Boolean(), unique=False, nullable=True)
    

    def __repr__(self):
       return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name" : self.last_name,
            "address": self.address,
            "phone" : self.phone,
            "birth_date" : self.birth_date,
            "gender" : self.gender,
            "status" : self.status,
            "rut" : self.rut
            
            # do not serialize the password, its a security breach
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()



class Trabajador(db.Model):
    __tablename__ = 'trabajadores'
    tra_id = db.Column(db.Integer, primary_key=True)
    tra_email = db.Column(db.String(120), unique=False, nullable=True)
    tra_rut = db.Column(db.String(15), unique=False, nullable=False)
    tra_name = db.Column(db.String(120), unique=False, nullable=False)
    tra_last_name = db.Column(db.String(120), unique=False, nullable=False)
    tra_address = db.Column(db.String(180), unique=False, nullable=False)
    tra_phone = db.Column(db.String(15), unique=False, nullable=True)
    tra_birth_date = db.Column(db.String(15), unique=False, nullable=False)
    tra_gender = db.Column(db.String(10), unique=False, nullable=False)
    tra_password = db.Column(db.String(80), unique=False, nullable=False)
    tra_status = db.Column(db.Boolean(), unique=False, nullable=True)
    

    def __repr__(self):
        return '<Trabajador %r>' % self.username

    def serialize(self):
        return {
            "tra_id": self.tra_id,
            "tra_email": self.tra_email,
            "tra_name": self.tra_name,
            "tra_last_name" : self.tra_last_name,
            "tra_address": self.tra_address,
            "tra_phone" : self.tra_phone,
            "tra_birth_date" : self.tra_birth_date,
            "tra_gender" : self.tra_gender,
            "tra_status" : self.tra_status
            
            # do not serialize the password, its a security breach
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()