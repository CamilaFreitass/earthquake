from sqlalchemy import Column, Integer, String, Float, Text, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Earthquake(Base):
    __tablename__ = 'Earthquake'
    id = Column(Integer, primary_key=True)
    cidade_base = Column(String(100))
    data_inicio = Column(Date)
    data_fim = Column(Date)
    magnitude = Column(Float)
    distancia_km = Column(Float)
    localizacao = Column(Text)
    data_evento = Column(Date)
