from flask_restful import reqparse, Resource
from models.ingrediente import IngredienteModel
from config.conexion_bd import base_de_datos

# POST todos / ingredientes
# GET todos /ingredientes
# PUT ID /ingredientes/<int:ID>
# GET ID /ingredientes/<int:ID>

serializerIngredientes = reqparse.RequestParser(bundle_errors=True)
serializerIngredientes.add_argument(
    'nombre',
    type=str,
    required=True,
    help="Falta el nombre",
    location='json'
)


class IngredientesController(Resource):
    def post(self):
        data = serializerIngredientes.parse_args()
        nuevoIngrediente = IngredienteModel(nombre=data.get('nombre'))
        nuevoIngrediente.save()
        return {
            'success': True,
            'content': nuevoIngrediente.json(),
            'message': 'Ingrediente creado exitosamente'
        }, 201

    def get(self):
        ingredientes = base_de_datos.session.query(IngredienteModel).all()
        resultado = []
        for ingrediente in ingredientes:
            resultado.append(ingrediente.json())
        return {
            'success': True,
            'content': resultado,
            'message': None
        }


class IngredienteController(Resource):
    def put(self, id):
        ingrediente = base_de_datos.session.query(
            IngredienteModel).filter_by(ingredienteId=id).first()
        if ingrediente:
            data = serializerIngredientes.parse_args()
            ingrediente.ingredienteNombre = data.get('nombre')
            ingrediente.save()

            return {
                'success': True,
                'content': ingrediente.json(),
                'message': 'Ingrediente actualizado correctamente'
            }, 201
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Ingrediente no encontrado'
            }, 404

    def get(self, id):
        ingrediente = base_de_datos.session.query(
            IngredienteModel).filter_by(ingredienteId=id).first()
        print(ingrediente.json())
        return ({
            'success': True,
            'content': ingrediente.json(),
            'message': None
        }, 200) if ingrediente else ({
            'success': True,
            'content': None,
            'message': 'Ingrediente no encontrado'
        }, 404)
