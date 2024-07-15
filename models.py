import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dueño(db.Model):
    __tablename__ = 'dueños'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    dinero = db.Column(db.Integer, nullable=False)

class Mascota(db.Model):
    __tablename__ = 'mascotas'
    id = db.Column(db.Integer, primary_key=True)
    id_dueño = db.Column(db.Integer, db.ForeignKey('dueños.id'))
    id_tipo_animal = db.Column(db.Integer, db.ForeignKey('tipos_mascota.id'))
    fecha_adopcion = db.Column(db.DateTime, default=datetime.datetime.now())
    fecha_recoleccion = db.Column(db.DateTime, default=datetime.datetime.now())
    hambre = db.Column(db.Integer, nullable=False, default=100)
    desperdicios = db.Column(db.Integer, nullable=False, default=0)
    felicidad = db.Column(db.Integer, nullable=False, default=70)

class TipoMascota(db.Model):
    __tablename__ = 'tipos_mascota'
    id = db.Column(db.Integer, primary_key=True)
    animal = db.Column(db.String(100), nullable=False)
    tamaño_estomago = db.Column(db.Integer, nullable=False)
    frecuencia_desperdicios = db.Column(db.Integer, nullable=False)
    necesidad_atencion = db.Column(db.Integer, nullable=False)
