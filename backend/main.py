import datetime
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

from models import db, Dueño, Mascota, TipoMascota

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:postgres@localhost:5432/tp2_granjeros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def hello_world():
    return 'Buenas buenas'

@app.route('/dueños', methods=['GET'])
def get_dueños():
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
        return jsonify(dueños_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'No hay ningun perfil disponible'}), 500
    
@app.route('/dueños/<nombre>', methods=['POST'])
def add_dueño(nombre):
    try:
        dinero = 100
        fecha_creacion = datetime.datetime.now()
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
    
@app.route("/dueños/<id_jugador>/mascotas", methods=['GET'])
def data_mascotas(id_jugador):
    try:
        mascotas = db.session.query(Mascota, TipoMascota                                    
        ).filter(Mascota.id_tipo_animal == TipoMascota.id
        ).filter(Mascota.id_dueño == id_jugador).all()

        mascotas_data = []
        for (mascota, tipo_animal) in mascotas:
            mascota_data = {
                'id': mascota.id,
                'tipo_animal': tipo_animal.animal,
                'nombre': mascota.nombre,
                'fecha_adopcion': mascota.fecha_adopcion,
                'hambre': mascota.hambre,
                'desperdicios': mascota.desperdicios,
                'felicidad': mascota.felicidad
            }
            mascotas_data.append(mascota_data)
        return jsonify(mascotas_data)
    except:
        return jsonify({"mensaje": "No hay mascotas."})
    
@app.route('/dueños/<id_jugador>/nueva_mascota/<id_tipo_mascota>/<nombre>', methods=['POST'])
def agregar_mascota(id_jugador, id_tipo_mascota, nombre):
    try:
        fecha_adopcion = datetime.datetime.now()

        if not nombre:
            return jsonify({'message': 'Bad request, no se encontro el nombre'}), 400
        nueva_mascota = Mascota(id_dueño=id_jugador, id_tipo_animal=id_tipo_mascota, nombre=nombre, fecha_adopcion=fecha_adopcion)
        db.session.add(nueva_mascota)
        db.session.commit()
        return jsonify({'dueño': {'id': nueva_mascota.id}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Error al crear la mascota'}), 500
    
@app.route("/dueños/mascotas/<id_mascota>", methods=['GET'])
def recibir_mascota(id_mascota):
    try:
        mascotas = db.session.query(Mascota, TipoMascota, Dueño                                    
        ).filter(Mascota.id_tipo_animal == TipoMascota.id
        ).filter(Mascota.id == id_mascota).filter(Mascota.id_dueño == Dueño.id).all()
        print(mascotas)
        mascotas_data = []
        for (mascota, tipo_animal, dueño) in mascotas:
            mascota_data = {
                'id': mascota.id,
                'tipo_animal': tipo_animal.animal,
                'tamaño_estomago': tipo_animal.tamaño_estomago,
                'frecuencia_desperdicios': tipo_animal.frecuencia_desperdicios,
                'necesidad_atencion': tipo_animal.necesidad_atencion,
                'dueño_id': dueño.id,
                'dinero': dueño.dinero,
                'nombre': mascota.nombre,
                'fecha_adopcion': mascota.fecha_adopcion,
                'hambre': mascota.hambre,
                'desperdicios': mascota.desperdicios,
                'felicidad': mascota.felicidad
            }
            mascotas_data.append(mascota_data)
        return jsonify(mascotas_data)
    except:
        return jsonify({"ERROR": "ID DE LA MASCOTA NO ENCONTRADO"}), 204
    
@app.route("/alimentar/<id_mascota>", methods=["POST"])
def alimentar_mascota(id_mascota):
    try:
        mascota = Mascota.query.get(id_mascota)
        dueño = Dueño.query.get(mascota.id_dueño)
        tipo_mascota = TipoMascota.query.get(mascota.id_tipo_animal)   

        if mascota.hambre < tipo_mascota.tamaño_estomago and (mascota.hambre + 10) > tipo_mascota.tamaño_estomago:
            dueño.dinero -= 10
            mascota.hambre = tipo_mascota.tamaño_estomago
            mascota.desperdicios += tipo_mascota.frecuencia_desperdicios/2
            mascota.felicidad += tipo_mascota.necesidad_atencion/6
        elif mascota.hambre < tipo_mascota.tamaño_estomago:
            dueño.dinero -= 10
            mascota.hambre += tipo_mascota.tamaño_estomago/10
            mascota.desperdicios += tipo_mascota.frecuencia_desperdicios/2
            mascota.felicidad += tipo_mascota.necesidad_atencion/6
        else:
            print("Mascota llena")

        db.session.add(mascota)
        db.session.add(dueño)
        db.session.commit()

        return jsonify({'nuevo_dinero': dueño.dinero, 'nueva_hambre': mascota.hambre, 'nuevo_desperdicios': mascota.desperdicios, 'nueva_felicidad': mascota.felicidad}), 201
    except Exception as error:
        print(error)
        return jsonify({"ERROR": "ID DE LA MASCOTA NO ENCONTRADO"}), 500
    
@app.route("/limpiar/<id_mascota>", methods=["POST"])
def limpiar_mascota(id_mascota):
    try:
        mascota = Mascota.query.get(id_mascota)
        dueño = Dueño.query.get(mascota.id_dueño)
        tipo_mascota = TipoMascota.query.get(mascota.id_tipo_animal)   

        if mascota.desperdicios > 0 and (mascota.desperdicios - 15) < 0:
            dueño.dinero -= 5
            mascota.desperdicios = 0
            mascota.felicidad -= tipo_mascota.necesidad_atencion/1.6
        elif mascota.desperdicios > 0:
            dueño.dinero -= 5
            mascota.desperdicios -= 15
            mascota.felicidad -= tipo_mascota.necesidad_atencion/1.6
            mascota.hambre -= 5
        else:
            print("No hay desperdicios.")
            

        db.session.add(mascota)
        db.session.add(dueño)
        db.session.commit()

        return jsonify({'nuevo_dinero': dueño.dinero, 'nueva_hambre': mascota.hambre, 'nuevo_desperdicios': mascota.desperdicios, 'nueva_felicidad': mascota.felicidad}), 201
    except Exception as error:
        print(error)
        return jsonify({"ERROR": "ID DE LA MASCOTA NO ENCONTRADO"}), 500
    
@app.route("/jugar/<id_mascota>", methods=["POST"])
def jugar_mascota(id_mascota):
    try:
        mascota = Mascota.query.get(id_mascota)
        dueño = Dueño.query.get(mascota.id_dueño)
        tipo_mascota = TipoMascota.query.get(mascota.id_tipo_animal)   

        if mascota.desperdicios < 100 and (mascota.desperdicios + tipo_mascota.frecuencia_desperdicios/1.4) < 100:
            mascota.desperdicios += tipo_mascota.frecuencia_desperdicios/1.4
        elif mascota.desperdicios < 100:
            mascota.desperdicios = 100
        else: 
            print("desperdicios al maximo")

        if mascota.hambre > 0 and (mascota.hambre - 5) > 0:
            mascota.hambre -= 5
        elif mascota.hambre > 0:
            mascota.hambre = 0
        else: 
            print("estomago vacio")

        if mascota.felicidad < 100 and (mascota.felicidad + tipo_mascota.necesidad_atencion/1.6) < 100:
            mascota.felicidad += 5
        elif mascota.felicidad < 100:
            mascota.felicidad = 100
        else:
            print ("tu mascota ya esta muy feliz!")

        dueño.dinero += 15

        db.session.add(mascota)
        db.session.add(dueño)
        db.session.commit()

        return jsonify({'nuevo_dinero': dueño.dinero, 'nueva_hambre': mascota.hambre, 'nuevo_desperdicios': mascota.desperdicios, 'nueva_felicidad': mascota.felicidad}), 201
    except Exception as error:
        print(error)
        return jsonify({"ERROR": "ID DE LA MASCOTA NO ENCONTRADO"}), 500
    
@app.route("/liberar/<id_mascota>", methods=["POST"])
def liberar_mascota(id_mascota):
    try:
        mascota = Mascota.query.get(id_mascota)
        dueño = Dueño.query.get(mascota.id_dueño) 
            

        db.session.delete(mascota)
        db.session.commit()

        return jsonify({'id': dueño.id}), 201
    except Exception as error:
        print(error)
        return jsonify({"ERROR": "ID DE LA MASCOTA NO ENCONTRADO"}), 500


if __name__ == '__main__':
    print('Starting server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print('Started.')
    app.run(host='0.0.0.0', debug=True, port=port)