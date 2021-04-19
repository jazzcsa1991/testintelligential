from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

ma = Marshmallow()
db = SQLAlchemy()


class Pago(db.Model,SerializerMixin):
    __tablename__ = 'pago'
    id = db.Column(db.Integer, primary_key=True)
    id_contrato = db.Column(db.Integer)
    id_cliente = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    monto = db.Column(db.Float)
    activo = db.Column(db.Boolean)
    fecha_registro = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self,id_contrato, id_cliente, fecha, monto, activo):
        self.id_contrato = id_contrato
        self.id_cliente = id_cliente
        self.fecha = fecha
        self.monto = monto
        self.activo = activo
        
class PagoSchema(ma.Schema):
    id = fields.Integer()
    id_contrato = fields.Integer(required=True)
    id_cliente = fields.Integer(required=True)
    fecha = fields.Date(required=True)
    monto = fields.Float(required=True)
    activo =fields.Boolean(required=True)
    fecha_registro = fields.DateTime()

    


