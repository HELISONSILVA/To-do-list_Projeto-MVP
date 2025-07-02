from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base
from model.comentario import Comentario

class Produto(Base):
    __tablename__ = 'produto'

    id = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    urgencia = Column(String(50))
    data = Column(DateTime)
    data_insercao = Column(DateTime, default=datetime.now)

    comentarios = relationship("Comentario")

    def __init__(self, nome: str, urgencia: str, data: Union[DateTime, None] = None,
                 data_insercao: Union[DateTime, None] = None):
        self.nome = nome
        self.urgencia = urgencia
        self.data = data if data else datetime.now()
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario: Comentario):
        self.comentarios.append(comentario)
