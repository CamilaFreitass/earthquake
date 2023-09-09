from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config
import pymysql


USUARIO = config('USUARIO')
SENHA = config('SENHA')
HOST = config('HOST')
BANCO = config('BANCO')
PORT = config('PORT')

CONN = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{BANCO}"


engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
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

Base.metadata.create_all(engine)