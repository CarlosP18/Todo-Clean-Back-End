from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()
#SACAR DE SERIALIZE PASSWORD
class Rol(db.Model):
    __tablename__= 'roles'
    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(120), nullable=False)
    user = db.relationship('User', backref='rol')
    trabajador = db.relationship('Trabajador', backref='rol')

    def serialize(self):
        return {
            "id": self.id,
            "rol": self.rol,
            "user": self.user,
            "trabajador": self.trabajador
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
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
    membership = db.Column(db.Boolean, nullable=True, default=False)
    pedidos = db.relationship('Pedido', backref='user')
    membresia = db.relationship('Membresia', backref='user')
    #def __repr__(self):
    #    return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "rut" : self.rut,
            "name": self.name,
            "last_name" : self.last_name,
            "address": self.address,
            "phone" : self.phone,
            "birth_date" : self.birth_date,
            "gender" : self.gender,
            "is_active" : self.is_active,
            "fecha_registro": self.fecha_registro,
            "membership": self.membership,
            "pedidos": self.pedidos,
            "rol_id": self.rol_id
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Trabajador(db.Model):
    __tablename__ = 'trabajadores'
    id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    rut = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(180), nullable=False, default="")
    phone = db.Column(db.String(15), unique=True, nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.String(10), nullable=False, default="")
    password = db.Column(db.String(80))
    is_active = db.Column(db.Boolean, nullable=True, default=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    pedidos = db.relationship('Pedido', backref='trabajador')
    documentos = db.relationship('DocumentoTrabajador', backref='trabajador', cascade="all,delete")
    #def __repr__(self):
    #    return '<Trabajador %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "rut": self.rut,
            "name": self.name,
            "last_name" : self.last_name,
            "address": self.address,
            "phone" : self.phone,
            "birth_date" : self.birth_date,
            "gender" : self.gender,
            "is_active" : self.is_active,
            "fecha_registro": self.fecha_registro,
            "pedidos": self.pedidos,
            "rol_id": self.rol_id,
            "documentos": self.documentos
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=False, nullable=False)
    detalle = db.Column(db.String(120), unique=False, nullable=False)
    precio = db.Column(db.Integer, unique=False, nullable=False)
    pedidos = db.relationship('Pedido', backref='servicio')

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "detalle": self.detalle,
            "precio": self.precio,
            "pedidos": self.pedidos
        }

class Membresia(db.Model):
    __tablename__ = 'membresias'
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('planes.id', ondelete='CASCADE'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    fecha_compra = db.Column(db.DateTime, default=db.func.current_timestamp())

    def serialize(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "users_id": self.users_id,
            "fecha_compra": self.fecha_compra,
        }
    
class Plan(db.Model):
    __tablename__ = 'planes'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(15), unique=False, nullable=True)
    detalle = db.Column(db.String(120), unique=False, nullable=True)
    precio = db.Column(db.Integer, unique=False)
    membresia = db.relationship('Membresia', backref='plan')
    def serialize(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "detalle": self.detalle,
            "precio": self.precio,
            "membresia": self.membresia
        }

#class TipoVivienda(db.Model):
#    __tablename__ = 'tipoviviendas'
#    id= db.Column(db.Integer, primary_key=True)
#    tipo = db.Column(db.String(15), unique=False, nullable=False)
#    pedidos = db.relationship('Pedido', backref='tipovivienda')

#    def serialize(self):
#        return {
#            "id": self.id,
#            "tipo": self.tipo,
#            "pedidos": self.pedidos
#        }

class Comuna(db.Model):
    __tablename__ = 'comunas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)
    pedidos = db.relationship('Pedido', backref='comuna')

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "pedidos": self.pedidos
        }

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.DateTime, default=db.func.current_timestamp())
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    trabajador_id = db.Column(db.Integer, db.ForeignKey('trabajadores.id', ondelete='CASCADE'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id', ondelete='CASCADE'), nullable=False)
    habitacion_adicional = db.Column(db.Integer, unique=False, nullable=True)
    banio_adicional = db.Column(db.Integer, unique=False, nullable=True) 
    valor = db.Column(db.Integer, unique=False, nullable=False)
    id_comuna = db.Column(db.Integer, db.ForeignKey('comunas.id', ondelete='CASCADE'), nullable=False)
    #vivienda_id = db.Column(db.Integer, db.ForeignKey('tipoviviendas.id', ondelete='CASCADE'), nullable=False)
    #serv_adicional = db.Column(db.Integer, db.ForeignKey('servicios.id', ondelete='CASCADE'), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "fecha_pedido": self.fecha_pedido,
            "users_id": self.users_id,
            "trabajador_id": self.trabajador_id,
            "servicio_id": self.servicio_id,
            "habitacion_adicional": self.habitacion_adicional,
            "banio_adicional": self.banio_adicional,
            "serv_adicional": self.serv_adicional,
            "valor": self.valor,
            "id_comuna": self.id_comuna,

        }

class DocumentoTrabajador (db.Model):
    __tablename__ = 'documentos'
    trabajador_id = db.Column(db.Integer, db.ForeignKey('trabajadores.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    cert_antecedentes = db.Column(db.String(100), nullable=False)
    foto_cedula = db.Column(db.String(100), nullable=False)
    cert_domicilio = db.Column(db.String(100), nullable=False)
    cert_prevision = db.Column(db.String(100), nullable=False)
    cert_cotizacion = db.Column(db.String(100), nullable=False)
    
    def serialize(self):
        return {
            "trabajador_id": self.trabajador_id,
            "data": self.data,
            "cert_antecedentes": self.cert_antecedentes,
            "foto_cedula": self.foto_cedula,
            "cert_domicilio": self.cert_domicilio,
            "cert_prevision": self.cert_prevision,
            "cert_cotizacion": self.cert_cotizacion
        }
        