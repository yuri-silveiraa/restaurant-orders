from sqlalchemy import Column, Integer, String, DateTime
from configs.database import Base
from datetime import datetime


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    item = Column(String, nullable=False)
    qtd = Column(Integer, nullable=False)
    estado = Column(String, nullable=False, default="recebido")
    hora_recebido = Column(DateTime, default=datetime.utcnow)
    hora_preparo = Column(DateTime, nullable=True)
    hora_finalizado = Column(DateTime, nullable=True)
