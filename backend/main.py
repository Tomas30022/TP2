from flask import Flask, request, jsonify
from models import db, Dueño, Mascota, TipoMascota

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:postgres@localhost:5432/tp2_granjeros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def hello_world():
    return 'Buenas buenas'

@app.route('/dueños', methods=['GET'])
def get_authors():
    try:
        dueños = Dueño.query.all()
        dueños_data = []
        for dueño in dueños:
            dueño_data = {
                'id': dueño.id,
                'nombre': dueño.nombre,
                'dinero': dueño.dinero
            }
            dueños_data.append(dueño_data)
        return jsonify({'dueños': dueños_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'No hay ningun perfil disponible'}), 500
    
@app.route('/dueños', methods=['POST'])
def add_dueño():
    try:
        data = request.json
        nombre = data.get('nombre')
        dinero = data.get('dinero')
        fecha_creacion = data.get('fecha_creacion')
        if not nombre or not dinero:
            return jsonify({'message': 'Bad request, no se encontro el nombre o la cantidad de dinero'}), 400
        nuevo_dueño = Dueño(nombre=nombre, dinero=dinero, fecha_creacion=fecha_creacion)
        db.session.add(nuevo_dueño)
        db.session.commit()
        return jsonify({'dueño': {'id': nuevo_dueño.id, 'nombre': nuevo_dueño.nombre, 'dinero': nuevo_dueño.dinero, 'fecha_creacion': nuevo_dueño.fecha_creacion}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Error al crear el perfil'}), 500
    
@app.route("/dueños/<id_jugador>", methods=['GET'])
def data(id_jugador):
    try:
        dueño = Dueño.query.get(id_jugador)
        print('Dueño:', dueño.nombre)
        dueño_data = {
            'id': dueño.id,
            'nombre': dueño.nombre,
            'dinero': dueño.dinero
        }
        return jsonify(dueño_data)
    except:
        return jsonify({"ERROR": "ID DEL DUEÑO NO ENCONTRADO"}), 204
    
@app.route('/dueños', methods=['POST'])
def add_mascota():
    try:
        data = request.json
        nombre = data.get('nombre')
        dinero = data.get('dinero')
        fecha_creacion = data.get('fecha_creacion')
        if not nombre or not dinero:
            return jsonify({'message': 'Bad request, no se encontro el nombre o la cantidad de dinero'}), 400
        nuevo_dueño = Dueño(nombre=nombre, dinero=dinero, fecha_creacion=fecha_creacion)
        db.session.add(nuevo_dueño)
        db.session.commit()
        return jsonify({'dueño': {'id': nuevo_dueño.id, 'nombre': nuevo_dueño.nombre, 'dinero': nuevo_dueño.dinero, 'fecha_creacion': nuevo_dueño.fecha_creacion}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Error al crear el perfil'}), 500

if __name__ == '__main__':
    print('Starting server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print('Started.')
    app.run(host='0.0.0.0', debug=True, port=port)