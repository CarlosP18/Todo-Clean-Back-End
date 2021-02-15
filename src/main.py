"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Trabajador
#from trabajador import db, Trabajador
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Miguel1989@localhost:3306/proyecto_final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/user/signup', methods=['POST'])
def create_user():
    id = request.json.get('id')
    email = request.json.get('email')
    rut = request.json.get('rut')
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    address = request.json.get('address')
    birth_date = request.json.get('birth_date')
    gender = request.json.get('gender')
    password = request.json.get('password')
    status = request.json.get('status')
    phone = request.json.get('phone')

    user = User()
    
    user.id = id
    user.email = email
    user.rut = rut
    user.name = name
    user.last_name = last_name
    user.address = address
    user.birth_date = birth_date
    user.gender = gender
    user.password = password
    user.status = status
    user.phone = phone

    user.save()
    print(user)

    return jsonify({"msg":"usuario creado"}), 200


@app.route('/new/trabajaconnosotros', methods=['POST'])
def create_trabajador():
    id = request.json.get('id')
    email = request.json.get('email')
    rut = request.json.get('rut')
    name = request.json.get('name')
    last_name = request.json.get('last_name')
    address = request.json.get('address')
    birth_date = request.json.get('birth_date')
    gender = request.json.get('gender')
    password = request.json.get('password')
    status = request.json.get('status')
    phone = request.json.get('phone')

    trabajador = Trabajador()
    trabajador.tra_id = id
    trabajador.tra_email = email
    trabajador.tra_rut = rut
    trabajador.tra_name = name
    trabajador.tra_last_name = last_name
    trabajador.tra_address = address
    trabajador.tra_birth_date = birth_date
    trabajador.tra_gender = gender
    trabajador.tra_password = password
    trabajador.tra_status = status
    trabajador.tra_phone = phone

    trabajador.save()

    return jsonify({"msg":"trabajador creado, bienvenido/a"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
