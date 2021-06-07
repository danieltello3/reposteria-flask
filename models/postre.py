from sqlalchemy.sql import base
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm


class PostreModel(base_de_datos.Model):
    __tablename__ = "postres"
    postreID = Column(name='id', primary_key=True,
                      autoincrement=True, unique=True, type_=types.Integer)

    postreNombre = Column(name='nombre', type_=types.String(length=45))
    postrePorcion = Column(name='porcion', type_=types.String(length=25))

    # el relationship sirve para indicar todos los hijos que puede tener ese modelo (todas sus FK) que puedan existir en determinado modelo
    # el backref creara un atributo virtual en el model del hijo (preparacion) para que pueda acceder a todo el objeto de PostreModel sin la necesidad de hacer una sub consulta (creara un join cuando sea necesario)
    # lazy => define cuando sqlAlchemy va a cargar la data adyacente de la base de datos
    preparaciones = orm.relationship(
        'PreparacionModel', backref='preparacionPostre', lazy=True)

    recetas = orm.relationship('RecetaModel', backref='recetaPostre')

    def __init__(self, nombre, porcion):
        self.postreNombre = nombre
        self.postrePorcion = porcion

    def __str__(self):
        return "El postre es {}".format(self.postreNombre)

    def save(self):
        # agrega un registro a la bd, pero todavia no lo guarda porque esta trabajandose mediante transacciones, entonces esperara a que se guarde de manera permanente haciendo un commit, o rechazando todos los cambios realizados mediante un rollback
        # la informacion ya existira en la bd pero en un stage (etapa) volatil
        base_de_datos.session.add(self)

        # ahora si todos los pasos de escritura, actualizacion y eliminacion de la bd fueron exitosos entonces se guardaran todos los cambios de manera permanente
        # todas las sesiones dentro de la misma instancia o entorno que esten pendientes de guardar PERMANENTE sus cambios en la bd al usar el commit se guardara de forma permanente

        base_de_datos.session.commit()

        # metodo que sirve para cerrar la sesion de la bd
        # base_de_datos.session.close()

    def json(self):
        return {
            "postreID": self.postreID,
            "postreNombre": self.postreNombre,
            "postrePorcion": self.postrePorcion
        }

    def delete(self):
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()
