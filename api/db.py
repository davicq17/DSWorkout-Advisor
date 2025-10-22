import mysql.connector
import tomllib

# Cargar la configuración desde el archivo TOML
with open("api/pyproject.toml", "rb") as f:
    config = tomllib.load(f)
db_conf = config["database"]

def get_conn():
    """Crea y retorna una conexión a la base de datos MySQL usando datos del TOML."""
    try:
        conn = mysql.connector.connect(
            host=db_conf["host"],
            user=db_conf["user"],
            password=db_conf["password"],
            database=db_conf["database"],
            port=db_conf["port"]
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error conectando a MySQL: {err}")
        return None
