import pymongo
import sys
import os


# Añadir el directorio del archivo que quieres importar
# NOTE: Es para poder importar el archivo config.py fuera de este directorio.
""" directorio = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(directorio) """
from config import MONGODB_TRYCLOUD_URL

def connect_to_mongo():
    # Conexión a la base de datos MongoDB (asegúrate de tener MongoDB ejecutándose localmente o cambia la URL)
    return pymongo.MongoClient(MONGODB_TRYCLOUD_URL)


def close_mongo_connection(client):
    client.close()


