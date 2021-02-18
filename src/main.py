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
from models import db, User, Trabajador
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
def vista_usersall():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users),200

@app.route('/cliente/<email>', methods=['GET'])
def vista_cliente(email=None):
    if email is not None:
        user = User.query.filter_by(email=email).first()
        if not user: return jsonify({"msg":"no existe el usuario"}), 404
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
    user.rol_id = 1

    user.save()

    if user:
        access_token = create_access_token(identity=user.id)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200

    else:
        return jsonify({"msg":"Registration failed"}), 400

@app.route('/new/trabajaconnosotros', methods=['POST'])
def create_trabajador():
    email = request.json.get('email')
    rut = request.json.get('rut')
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    address = request.json.get('address')
    phone = request.json.get('phone')
    password = request.json.get('password')
    
    trabajador = Trabajador()
    trabajador.email = email
    trabajador.rut = rut
    trabajador.name = name
    trabajador.last_name = last_name
    trabajador.address = address
    trabajador.phone = phone
    trabajador.password = password
    trabajador.rol_id = 2
    
    trabajador.save()
    return jsonify({"msg":"trabajador creado, bienvenido/a"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)