import mysql.connector
import toml
print("🚀 Iniciando prueba de conexión...")

try:
    config = toml.load("api_fastapi/pyproject.toml")["database"]
    print("antes de la conexión")
    conn = mysql.connector.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        connection_timeout=5
    )
    print("✅ Conexión exitosa a la base de datos")
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    print("🕒 Fecha/hora del servidor:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Error de conexión:", e)

print("🏁 Prueba terminada.")
