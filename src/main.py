"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, url_for, redirect, render_template, flash
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Pedido
from dotenv import load_dotenv
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
#from trabajador import db, Trabajador
#from models import Person
load_dotenv()

ALLOWED_FILE_EXTENSIONS = {'pdf', 'doc', 'docx','png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = os.getenv('DEBUG')
app.config['ENV'] = os.getenv('FLASK_ENV')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Miguel1989@localhost:3306/proyecto_final_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'mimarchtt@gmail.com'
app.config['MAIL_PASSWORD'] = 'Piwi1989'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEBUG'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'luis'
MIGRATE = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
CORS(app)
setup_admin(app)
mail = Mail(app)

#s = URLSafeTimedSerializer('secret-key')

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['JWT_SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(config.key)
    try:
        email = serializer.loads(
            token,
            salt=config.salt,
            max_age=expiration
        )
    except:
        return False
    return email

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/clientes', methods=['GET'])

def vista_usersall():
    users = User.query.all()
    users = list(map(lambda user: user.trabajador_serialize(), users))
    return jsonify(users),200

@app.route('/cliente/<email>', methods=['GET'])
@jwt_required()
def vista_cliente(email=None):
    if email is not None:
        user = User.query.filter_by(email=email).first()
        if not user: return jsonify({"message":"no existe el usuario"}), 404
        return jsonify (user.serialize()), 200
           
@app.route('/user/signup', methods=['POST'])
def create_user():
    email = request.json.get('email')
    rut = request.json.get('rut')
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    
    phone = request.json.get('phone')
    password = request.json.get('password')
 
    user = User()
    user.email = email
    user.rut = rut
    user.name = name
    user.last_name = last_name
    
    user.phone = phone
    user.password = generate_password_hash(password)
    # 1 = cliente
    user.rol_id = 1
    user.is_active = True

    user.save()

    if user:
        access_token = create_access_token(identity=user.id)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"message":"Registration failed"}), 400


@app.route('/user/signin', methods=['POST'])
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            data = {
                "access_token": access_token,
                "user": user.serialize()
            }
            return jsonify(data), 200
        else:
            return jsonify({"message":"Usuario o contraseña invalida"}), 400
    else:
        return jsonify({"message":"Usuario o contraseña invalida"}), 400

@app.route('/user/signup-trabajador', methods=['POST'])
def create_trabajador():
    email = request.json.get('email')
    rut = request.json.get('rut')
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    
    phone = request.json.get('phone')
    password = request.json.get('password')
 
    user = User()
    user.email = email
    user.rut = rut
    user.name = name
    user.last_name = last_name
    
    user.phone = phone
    user.password = generate_password_hash(password)
    # 2 = Trabajador
    user.rol_id = 2
    user.is_active = True

    user.save()

    if user:
        access_token = create_access_token(identity=user.id)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"message":"Registration failed"}), 400

@app.route('/trabajador/formulario-inicio/<int:id>', methods=['PUT'])
def formulario_tra(id=None):
    name = request.json.get("name")
    last_name = request.json.get("last_name")
    phone = request.json.get("phone")
    email = request.json.get("email")
    #birth_date = request.json.get("birth_date")
    rut = request.json.get("rut")
    ciudad = request.json.get("ciudad")
    comuna = request.json.get("comuna")
    address = request.json.get("address")
    bank = request.json.get("bank")
    cuenta = request.json.get("cuenta")
    numero_cuenta = request.json.get("numero_cuenta")
    
    if not name: return jsonify({"msg": "nombre es requerido"}), 400
    if not last_name: return jsonify({"msg": "apellido es requerido"}), 400
    if not phone: return jsonify({"msg": "telefono es requerido"}), 400
    if not email: return jsonify({"msg": "email es requerido"}), 400
    if not rut: return jsonify({"msg": "rut es requerido"}), 400
    if not address: return jsonify({"msg": "direccion es requerido"}), 400
    if not ciudad: return jsonify({"msg": "ciudad es requerido"}), 400
    if not comuna: return jsonify({"msg": "comuna es requerido"}), 400
    user = User.query.filter_by(email=email).first()
    if user and user.id != id: return jsonify({"msg": "email ya existe "}), 400

    user = User.query.get(id)
    user.name = name
    user.last_name = last_name
    user.phone = phone
    user.email = email
    #user.birth_date = birth_date
    user.rut = rut
    user.address = address
    user.ciudad = ciudad
    user.comuna = comuna
    user.bank = bank
    user.cuenta = cuenta
    user.numero_cuenta = numero_cuenta
    user.update()

    return jsonify({"status": 200, "result": "User actualizado", "user": user.serialize()}), 200

@app.route('/cliente/formulario-inicio/<int:id>', methods=['PUT'])
def formulario_cliente(id=None):
    name = request.json.get("name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    phone = request.json.get("phone")
    ciudad = request.json.get("ciudad")
    comuna = request.json.get("comuna")
    address = request.json.get("address")

    if not name: return jsonify({"msg": "nombre es requerido"}), 400
    if not last_name: return jsonify({"msg": "apellido es requerido"}), 400
    if not email: return jsonify({"msg": "email es requerido"}), 400
    if not phone: return jsonify({"msg": "telefono es requerido"}), 400
    if not ciudad: return jsonify({"msg": "ciudad es requerido"}), 400
    if not comuna: return jsonify({"msg": "comuna es requerido"}), 400
    if not address: return jsonify({"msg": "direccion es requerido"}), 400
    user = User.query.filter_by(email=email).first()
    if user and user.id != id: return jsonify({"msg": "email ya existe "}), 400

    user = User.query.get(id)
    user.name = name
    user.last_name = last_name
    user.email = email
    user.phone = phone
    user.ciudad = ciudad
    user.comuna = comuna
    user.address = address
    user.update()

    return jsonify({"status": 200, "result": "User actualizado", "user": user.serialize()}), 200

@app.route('/user/reserva', methods=['POST'])
def create_reserva():    
    tipo_servicio = request.json.get('tipo_servicio')
    num_habitaciones = request.json.get('num_habitaciones')
    num_banios = request.json.get('num_banios')
    fecha_parareserva = request.json.get('fecha_parareserva')
    valor = request.json.get('valor')
    users_id = request.json.get('users_id')
    ciudad = request.json.get('ciudad')
    address = request.json.get('address')
    comuna = request.json.get('comuna')

    pedido = Pedido()
    pedido.tipo_servicio = tipo_servicio
    pedido.num_habitaciones = num_habitaciones
    pedido.num_banios = num_banios
    pedido.fecha_parareserva = fecha_parareserva
    pedido.valor = valor
    pedido.users_id = users_id
    pedido.ciudad = ciudad
    pedido.address = address
    pedido.comuna = comuna
    pedido.save() 
    
    print(request.get_json())
    return jsonify({"result": pedido.serialize() }), 201
    #print(request.get_json())
    #return jsonify({"result": request.get_json()}), 201


    
    



@app.route('/reset-password-request', methods=['POST'])
def reset_request():
    
    email = request.json.get('correo')
    if not email:
        return jsonify({"msg":"Email inválido"})
    user = User.query.filter_by(email=email).first()
    token = generate_confirmation_token(user.id)
    url = 'http://localhost:3000/reset-password/' + token
    msg = Message('Recuperación de contraseña', sender='mimarchtt@gmail.com', recipients=[email])
    msg.body = f'''Para restablecer su contraseña, haga click en el link a continuación:
{url}
Si usted no hizo esta solicitud, ignore este mensaje. 
'''
    mail.send(msg)
    
    return jsonify({'msg' : 'Correo enviado'})





@app.route('/reset-password/<token>', methods=['GET','POST'])
def reset_token(token):
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('login_user'))
    user.password = generate_password_hash(password)
    db.session.commit()
    return jsonify({"msg":"contraseña actualizada"})



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)