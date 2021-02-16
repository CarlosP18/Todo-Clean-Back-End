from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rut = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(180), nullable=False, default="")
    phone = db.Column(db.String(15), unique=True, nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.String(10), nullable=False, default="")
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=True, default=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    

    #def __repr__(self):
    #    return '<User %r>' % self.username

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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    rut = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(180), nullable=False, default="")
    phone = db.Column(db.String(15), unique=True, nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.String(10), nullable=False, default="")
    password = db.Column(db.String(80))
    status = db.Column(db.Boolean, nullable=True, default=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<Trabajador %r>' % self.username

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
            "status" : self.status
            
            # do not serialize the password, its a security breach
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Servicios(db.Model):
    tablename = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    serv_nombre = db.Column(db.String(120), unique=False, nullable=False)
    serv_detalle = db.Column(db.String(120), unique=False, nullable=False)
    serv_precio = db.Column(db.Integer, unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "serv_nombre": self.serv_nombre,
            "serv_detalle": self.serv_detalle,
            "serv_precio": self.serv_precio,
        }


class TipoVivienda(db.Model):
    __tablename__ = 'tipovivienda'
    id= db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(15), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
        }


class Comunas(db.Model):
    __tablename__ = 'comunas'
    id= db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
