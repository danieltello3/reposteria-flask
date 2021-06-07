from controllers.ingrediente import IngredienteController, IngredientesController
from controllers.preparacion import PreparacionesController
from controllers.postre import BusquedaPostre, PostreController, PostresController
from flask import Flask, request
from flask_restful import Api
from dotenv import load_dotenv
from os import environ
from config.conexion_bd import base_de_datos
from flask_swagger_ui import get_swaggerui_blueprint
from models.receta import RecetaModel


load_dotenv()

# configurar SWAGGER en FLASK

# esta variable sirve para indicar en que ruta (endpoint) se encontrara la documentacion
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"  # indicar la ubicacion del archivo json
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={
        'app_name': "Reposteria Flask - Swagger Documentation"
    }
)

app = Flask(__name__)
# sirve para registrar en el caso que nosotros tengamos un proyecto interno para agregarlo a un proyecto principal
app.register_blueprint(swagger_blueprint)
api = Api(app)
# dialect://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
# si se establece en TRUE, Flask-SQLAlchemy rastreara las modificaciones de los objetos y lanzara señales. su valor predeterminado es None, igual habilita el tracking pero emite una advertencia que se deshabilitara de manera prederminada en futuras versiones. esto consume memoria adicional y si no se va a utilzar es mejor desactivarlo (false)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
base_de_datos.init_app(app)

# base_de_datos.drop_all(app=app)       para eliminar las tablas
# crea todas las tablas defininads en los modelos del proyecto
base_de_datos.create_all(app=app)

app.route("/")


def initial_controller():
    return {
        "message": "Bienvenido a mi API de recetas de postres 🎂"
    }


# defino las rutas usando Flask restful
api.add_resource(PostresController, "/postres")
api.add_resource(PostreController, "/postres/<int:id>")
api.add_resource(BusquedaPostre, "/busqueda_postre")
api.add_resource(PreparacionesController, "/preparaciones",
                 "/preparaciones/<int:postre_id>")
api.add_resource(IngredientesController, "/ingredientes")
api.add_resource(IngredienteController, "/ingredientes/<int:id>")

# POST todos / ingredientes
# GET todos /ingredientes
# PUT ID /ingredientes/<int:ID>
# GET ID /ingredientes/<int:ID>


if __name__ == '__main__':
    app.run(debug=True)
