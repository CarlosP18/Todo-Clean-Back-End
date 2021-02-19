from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()
#SACAR DE SERIALIZE PASSWORD
class Rol(db.Model):
    __tablename__= 'roles'
    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(120), nullable=False)
    user = db.relationship('User', backref='rol')
    
    def serialize(self):
        return {
            "id": self.id,
            "rol": self.rol,
            "user": self.user,
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
    password = db.Column(db.String(1000), nullable=False)
    is_active = db.Column(db.Boolean, nullable=True, default=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    cliente_pedidos = db.relationship('Pedido', backref='user')
    trab_pedidos = db.relationship('Pedido', backref='trabajador')
    membresia = db.relationship('Membresia', backref='user')
    documentos = db.relationship('DocumentoTrabajador', backref='user', cascade="all,delete")
    #def __repr__(self):
    #    return '<User %r>' % self.username
    def serialize(self):
        return {
            "id": self.id,
            "rol_id": self.rol_id,
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
            "cliente_pedidos": self.cliente_pedidos,
            "trab_pedidos": self.trab_pedidos,
            "membresia": self.membresia,
            "documentos": self.documentos
        }      
    def save(self):
        db.session.add(self)
        db.session.commit()

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=False, nullable=False)
    precio = db.Column(db.Integer, unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
        }

class Plan(db.Model):
    __tablename__ = 'planes'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(15), unique=False, nullable=True)
    horas = db.Column(db.Integer, unique=False)
    vecesx_mes = db.Column(db.Integer, unique=False)
    precio = db.Column(db.Integer, unique=False, nullable=False)
    membresia = db.relationship('Membresia', backref='plan')
    def serialize(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "horas": self.horas,
            "vecesx_mes": self.vecesx_mes,
            "precio": self.precio
        }

class Membresia(db.Model):
    __tablename__ = 'membresias'
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('planes.id', ondelete='CASCADE'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    fecha_compra = db.Column(db.DateTime, default=db.func.current_timestamp())
    fecha_termino = db.Column(db.DateTime)

    def serialize(self):
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "users_id": self.users_id,
            "fecha_compra": self.fecha_compra,
            "fecha_termino": self.fecha_termino
        }
    
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.DateTime, default=db.func.current_timestamp())
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    trab_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id', ondelete='CASCADE'), nullable=False)
    valor = db.Column(db.Integer, unique=False, nullable=False)
    id_comuna = db.Column(db.Integer, db.ForeignKey('comunas.id', ondelete='CASCADE'), nullable=False)
    #vivienda_id = db.Column(db.Integer, db.ForeignKey('tipoviviendas.id', ondelete='CASCADE'), nullable=False)
    #serv_adicional = db.Column(db.Integer, db.ForeignKey('servicios.id', ondelete='CASCADE'), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "fecha_pedido": self.fecha_pedido,
            "users_id": self.users_id,
            "trab_id": self.trab_id,
            "servicio_id": self.servicio_id,
            "serv_adicional": self.serv_adicional,
            "valor": self.valor,
            "id_comuna": self.id_comuna,
        }

class DocumentoTrabajador (db.Model):
    __tablename__ = 'documentos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    cert_antecedentes = db.Column(db.String(100), nullable=False)
    foto_cedula = db.Column(db.String(100), nullable=False)
    cert_domicilio = db.Column(db.String(100), nullable=False)
    cert_prevision = db.Column(db.String(100), nullable=False)
    cert_cotizacion = db.Column(db.String(100), nullable=False)
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "cert_antecedentes": self.cert_antecedentes,
            "foto_cedula": self.foto_cedula,
            "cert_domicilio": self.cert_domicilio,
            "cert_prevision": self.cert_prevision,
            "cert_cotizacion": self.cert_cotizacion
        }

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
        