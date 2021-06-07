
from sqlalchemy.sql.schema import ForeignKey
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types


class RecetaModel(base_de_datos.Model):
    __tablename__ = "recetas"
    recetaId = Column(name="id", type_=types.Integer,
                      primary_key=True, unique=True, autoincrement=True)
    recetaCantidad = Column(name="cantidad", type_=types.Integer)
    recetaUnidadMedida = Column(
        name="unidad_medida", type_=types.String(length=25))
    postre = Column(ForeignKey(column="postres.id",
                    ondelete="CASCADE"), name="postre_id", type_=types.Integer)
    ingrediente = Column(ForeignKey(column="ingredientes.id",
                         ondelete="CASCADE"), name="ingrediente_id", type_=types.Integer)

    def __init__(self, cantidad, unidad_medida, postre, ingrediente):
        self.recetaCantidad = cantidad
        self.recetaUnidadMedida = unidad_medida
        self.postre = postre
        self.ingrediente = ingrediente
