from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rut = db.Column(db.String(15), unique=True, nullable=False, default="")
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(180), unique=False, nullable=False, default="")
    phone = db.Column(db.String(15), unique=True, nullable=True)
    birth_date = db.Column(db.String(15), unique=False, nullable=False, default="")
    gender = db.Column(db.String(10), unique=False, nullable=False, default="")
    password = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Boolean(), unique=False, nullable=True )
    

    #def __repr__(self):
    #   return '<User %r>' % self.username
    
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
    tra_email = db.Column(db.String(120), unique=True, nullable=False)
    tra_rut = db.Column(db.String(15), unique=True, nullable=False, default="")
    tra_name = db.Column(db.String(120), unique=False, nullable=False)
    tra_last_name = db.Column(db.String(120), unique=False, nullable=False)
    tra_address = db.Column(db.String(180), unique=False, nullable=False, default="")
    tra_phone = db.Column(db.String(15), unique=True, nullable=True)
    tra_birth_date = db.Column(db.String(15), unique=False, nullable=False, default="")
    tra_gender = db.Column(db.String(10), unique=False, nullable=False, default="")
    tra_password = db.Column(db.String(80), unique=False, nullable=False)
    tra_status = db.Column(db.Boolean, nullable=True, default=False)
    

    #def __repr__(self):
    #    return '<Trabajador %r>' % self.username

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

class Servicios(db.Model):
    __tablename__ = 'servicios'
    serv_id = db.Column(db.Integer, primary_key=True)
    serv_nombre = db.Column(db.String(120), unique=False, nullable=False)
    serv_detalle = db.Column(db.String(120), unique=False, nullable=False)
    serv_precio = db.Column(db.String(120), unique=False, nullable=False)

    def serialize(self):
        return {
            "serv_id": self.serv_id,
            "serv_nombre": self.serv_nombre,
            "serv_detalle": self.serv_detalle,
            "serv_precio": self.serv_precio,
        }

class TipoVivienda(db.Model):
    __tablename__ = 'tipovivienda'
    vivienda_id= db.Column(db.Integer, primary_key=True)
    vivienda_tipo = db.Column(db.String(120), unique=False, nullable=False)

    def serialize(self):
        return {
            "vivienda_id": self.vivienda_id,
            "vivienda_tipo": self.vivienda_tipo,
        }

class Comunas(db.Model):
    __tablename__ = 'comunas'
    comuna_id= db.Column(db.Integer, primary_key=True)
    comuna_nombre = db.Column(db.String(30), unique=False, nullable=False)

    def serialize(self):
        return {
            "comuna_id": self. comuna_id,
            "comuna_nombre": self.comuna_nombre,
        }
