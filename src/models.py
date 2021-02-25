from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

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
    ciudad = db.Column(db.String(180), nullable=False, default="")
    comuna = db.Column(db.String(180), nullable=False, default="")
    address = db.Column(db.String(180), nullable=False, default="")
    phone = db.Column(db.String(15), unique=True, nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    
    password = db.Column(db.String(1000), nullable=False)
    is_active = db.Column(db.Boolean, nullable=True, default=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())  
    bank = db.Column(db.String(180), nullable=False, default="")
    cuenta = db.Column(db.String(180), nullable=False, default="")
    numero_cuenta = db.Column(db.String(180), nullable=False, default="")
    cliente_pedidos = db.relationship("Pedido", primaryjoin="and_(User.id==Pedido.users_id)")
    trab_pedidos = db.relationship("Pedido", primaryjoin="and_(User.id==Pedido.trab_id)")     
    membresia = db.relationship('Membresia', backref='user')
    documentos = db.relationship('DocumentoTrabajador', backref='user', cascade="all,delete")
    #def __repr__(self):
    #    return '<User %r>' % self.username
    def get_reset_token(self, expires_sec=30):
        s = Serializer(os.getenv('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.getenv('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def trabajador_serialize(self):
        return {
            "id": self.id,
            "rol_id" : self.rol_id,
            "comuna" : self.comuna,
            "name": self.name,
            "last_name": self.last_name
        }


    def serialize(self):
        return {
            "id": self.id,
            "rol_id": self.rol_id,
            "email": self.email,
            "rut" : self.rut,
            "name": self.name,
            "last_name" : self.last_name,
            "ciudad": self.ciudad,
            "comuna": self.comuna,
            "address": self.address,
            "phone" : self.phone,
            "birth_date" : self.birth_date,
            
            "is_active" : self.is_active,
            "fecha_registro": self.fecha_registro,
            "bank": self.bank,
            "cuenta": self.cuenta,
            "numero_cuenta": self.numero_cuenta,
            "cliente_pedidos": self.get_cliente_pedidos(),
            "trab_pedidos": self.get_trabajador_pedidos(),
            "membresia": self.membresia
            
        } 
    def get_trabajador_pedidos(self):
        return list(map(lambda pedido: pedido.serialize(), self.trab_pedidos))

    def get_cliente_pedidos(self):
        return list(map(lambda pedido: pedido.serialize(), self.cliente_pedidos))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
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
    tipo_servicio = db.Column(db.String(50), unique=False, nullable=False)
    num_habitaciones = db.Column(db.Integer, unique=False, nullable=False)
    num_banios = db.Column(db.Integer, unique=False, nullable=False)
    fecha_parareserva = db.Column(db.String(50), unique=False, nullable=False)
    fecha_pedido = db.Column(db.DateTime, default=db.func.current_timestamp())
    valor = db.Column(db.Integer, unique=False, nullable=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    trab_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id', ondelete='CASCADE'), nullable=True)
    #id_comuna = db.Column(db.Integer, db.ForeignKey('comunas.id', ondelete='CASCADE'), nullable=True)
    ciudad = db.Column(db.String(180), nullable=False, default="")
    comuna = db.Column(db.String(180), nullable=False, default="")
    address = db.Column(db.String(180), nullable=False, default="")
    #vivienda_id = db.Column(db.Integer, db.ForeignKey('tipoviviendas.id', ondelete='CASCADE'), nullable=False)
    #serv_adicional = db.Column(db.Integer, db.ForeignKey('servicios.id', ondelete='CASCADE'), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "tipo_servicio": self.tipo_servicio,
            "num_habitaciones": self.num_habitaciones,
            "num_banios": self.num_banios,
            "fecha_parareserva": self.fecha_parareserva,
            "fecha_pedido": self.fecha_pedido,
            "valor": self.valor,
            "users_id": self.users_id,
            "trab_id": self.trab_id,
            "servicio_id": self.servicio_id,
            "ciudad": self.ciudad,
            "comuna": self.comuna,
            "address": self.address

        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

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
    #pedidos = db.relationship('Pedido', backref='comuna')

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
        

