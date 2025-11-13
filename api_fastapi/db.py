import tomllib
import mysql.connector
from fastapi import HTTPException
import os

# 📦 Cargar configuración desde el archivo TOML
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    toml_path = os.path.join(base_dir,"pyproject.toml")
    with open(toml_path, "rb") as f:
        config = tomllib.load(f)
        db_conf = config["database"]
except Exception as e:
    raise RuntimeError(f"❌ No se pudo cargar la configuración de la base de datos: {e}")

# CONECCIÓN A LA BASE DE DATOS
def get_conn():
    """Crea y retorna una conexión a MySQL usando los datos del archivo TOML."""
    try:
        print("iniciando conexión")
        conn = mysql.connector.connect(
            host="",
            user="",
            password="",
            database="",
            port=,
             ssl_ca=os.path.join(os.path.dirname(__file__),"certs","ca.pem"),
        )
        print("conexión exitosa, se devolvera")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error conectando a MySQL: {err}")
        raise HTTPException(status_code=500, detail=f"Error conectando a la base de datos: {err}")
