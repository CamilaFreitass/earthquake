import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Earthquake, conn
import requests
import json
import googlemaps
from haversine import haversine
from decouple import config, Csv
from unidecode import unidecode
from datetime import datetime, timedelta

app = FastAPI()

DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


key = config('key')


def conectaBanco():
    engine = create_engine(conn, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


def is_valid_data(data_str):
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def verificar_limite_de_tempo(data_inicial, data_final):
    limite_de_anos = 2
    diferenca = data_final - data_inicial
    dois_anos = timedelta(days=limite_de_anos * 365.25)
    if diferenca <= dois_anos:
        return True
    else:
        return False


@app.get('/consulta')
def consulta(cidade_base: str, data_inicio: str, data_fim: str):
    session = conectaBanco()
    if not is_valid_data(data_inicio) or not is_valid_data(data_fim):
        raise HTTPException(status_code=400, detail="Formato da data inválido. Um exemplo de formato válido é '2022-04-02' (ano-mês-dia).")
    else:
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        if not verificar_limite_de_tempo(data_inicio, data_fim) == True:
            raise HTTPException(status_code=400,
                                detail="Intervalo de tempo muito grande entre 'data_inicio' e 'data_fim'. Intervalo máximo de 2 anos")
        else:
            cidade_base = unidecode(cidade_base).lower()
            registro = session.query(Earthquake).filter_by(cidade_base=cidade_base, data_inicio=data_inicio, data_fim=data_fim).all()
            if len(registro) == 0:
                response = requests.get(
                    f'https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime={data_inicio}&endtime={data_fim}&minmagnitude=5&orderby=time')
                dados = json.loads(response.content)

                gmaps = googlemaps.Client(key=key)

                geocode_result = gmaps.geocode(cidade_base)

                if geocode_result:
                    busca = geocode_result[0]['geometry']['location']

                    latitude = busca['lat']

                    longitude = busca['lng']

                    local = [latitude, longitude]

                    menor_distancia = 40075.0000

                    magnitude = 5

                    localizacao = None

                    data_evento = None

                    for item in dados['features']:
                        distancia = haversine(item['geometry']['coordinates'][-2::-1], local)
                        if distancia < menor_distancia:
                            menor_distancia = distancia
                            magnitude = item['properties']['mag']
                            localizacao = item['properties']['place']
                            resposta = requests.get(item['properties']['detail'])
                            date = json.loads(resposta.content)
                            data_evento = date['properties']['products']['origin'][0]['properties']['eventtime'][0:10]

                    data_evento = datetime.strptime(data_evento, "%Y-%m-%d").date()
                    x = Earthquake(cidade_base=cidade_base, data_inicio=data_inicio, data_fim=data_fim,
                                       magnitude=magnitude, distancia_km=menor_distancia, localizacao=localizacao,
                                       data_evento=data_evento)
                    session.add(x)
                    session.commit()
                    registro = session.query(Earthquake).filter_by(cidade_base=cidade_base, data_inicio=data_inicio,
                                                                       data_fim=data_fim).all()
                    return registro

                else:
                    raise HTTPException(status_code=400, detail="Cidade inválida. Digite uma cidade válida!")
            elif len(registro) > 0:
                return registro



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=81)
