"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from dotenv import load_dotenv
#from trabajador import db, Trabajador
#from models import Person
load_dotenv()

ALLOWED_FILE_EXTENSIONS = {'pdf', 'doc', 'docx','png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = os.getenv('DEBUG')
app.config['ENV'] = os.getenv('FLASK_ENV')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost:3306/proyecto_final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['JWT_SECRET_KEY'] = 'super-secret'
MIGRATE = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/clientes', methods=['GET'])
@jwt_required()
def vista_usersall():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
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
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)