from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types


class PreparacionModel(base_de_datos.Model):
    __tablename__ = "preparaciones"
    preparacionID = Column(name='id', type_=types.Integer,
                           primary_key=True, unique=True, autoincrement=True)

    preparacionOrden = Column(
        name='orden', nullable=False, type_=types.Integer)

    preparacionDescripcion = Column(
        name="descripcion", type_=types.Text, nullable=False)
    # asi se crean las relacion entre un modelo y otro
    postre = Column(ForeignKey(column='postres.id', ondelete='CASCADE'),
                    name="postre_id", type_=types.Integer, nullable=False)

    def __init__(self, orden, descripcion, postre_id):
        self.preparacionOrden = orden
        self.preparacionDescripcion = descripcion
        self.postre = postre_id

    def save(self):
        base_de_datos.session.add(self)
        base_de_datos.session.commit()

    def json(self):
        return {
            "id": self.preparacionID,
            "orden": self.preparacionOrden,
            "descripcion": self.preparacionDescripcion,
            "postre": self.postre
        }
