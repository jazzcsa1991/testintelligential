from flask import request
import json
from flask_restful import Resource
from Model import db, Pago,PagoSchema
import asyncio
import time

pagos_schema = PagoSchema(many=True)
pago_schema = PagoSchema()


# funcion que verifica si existen pagos posteriores
def check_fecha(fecha):
    pagos = Pago.query.order_by(Pago.fecha).filter_by(activo=True)
    renovar_pagos = []
    fecha_pago = time.strptime(fecha.strftime("%m/%d/%Y"),"%m/%d/%Y")
    for i in pagos:
        temp_fecha = time.strptime(i.fecha.strftime("%m/%d/%Y"),"%m/%d/%Y")
        if (fecha_pago<temp_fecha):
            pago = Pago.query.filter_by(id=i.id).first()
            pago.activo = False
            db.session.add(pago)
            db.session.commit()
            renovar_pagos.append(i)
    return renovar_pagos

#endpoint para pagos
class PagoResource(Resource):
    def get(self,id=None):
        '''request para obtener pago por id o general'''
        id = request.args.get('id')
        if id:
            pago = Pago.query.get(id)
            pago = pago_schema.dump(pago).data
            return {'status': 'success', 'data': pago}, 200
        else:
            pagos = Pago.query.all()
            pagos = pagos_schema.dump(pagos).data
            return {'status': 'success', 'data': pagos}, 200

    def put(self):
        ''' request put para la edicion de un pago, se necesitan todos los parametros'''
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = pago_schema.load(json_data)
        if errors:
            return errors, 422
        pago = Pago.query.filter_by(id=data['id']).first()
        if not pago:
            return {'message': 'pago does not exist'}, 400
        
        pago.id_contrato = data['id_contrato'],
        pago.id_cliente = data['id_cliente']
        pago.fecha = data['fecha'],
        pago.monto = data['monto'],
        pago.activo = data['activo']
        db.session.add(pago)
        db.session.commit()
        result = pago_schema.dump(pago).data
        return { "status": 'success', 'data': result}, 201

    def post(self):
        '''request post para la creacion de un nuevo pago, se necesitan todos los argumentos'''
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = pago_schema.load(json_data)
        if errors:
            return errors, 422
        #revisa si exiten pagos posteriorer
        new_pagos = check_fecha(data['fecha'])
        pago = Pago(
                id_contrato=data['id_contrato'],
                id_cliente=data['id_cliente'],
                fecha=data['fecha'],
                monto=data['monto'],
                activo=data['activo']
            )
        db.session.add(pago)
        db.session.commit()
        result = pago_schema.dump(pago).data
        #si exiten pagos posteriore los vuelve a crear
        if len(new_pagos) != 0:
            for pago in new_pagos:
                pago = Pago(
                id_contrato=pago.id_contrato,
                id_cliente=pago.id_cliente,
                fecha=pago.fecha,
                monto=pago.monto,
                activo=True
                )
                db.session.add(pago)
                db.session.commit()
            
        return { "status": 'success', 'data': result }, 201

    def delete(self):
        '''request para eliminar un pago por id'''
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = pago_schema.load(json_data)
        if errors:
            return errors, 422
        pago = Pago.query.filter_by(id=data['id']).first()
        if not pago:
            return {'message': 'pago does not exist'}, 400
        pago = pago.query.filter_by(id=data['id']).delete()
        db.session.commit()
        result = pago_schema.dump(pago).data
        return { "status": 'success', 'data': pago}, 201
        

    
