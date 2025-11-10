import mysql.connector

print("🚀 Iniciando prueba de conexión...")

try:
    print("antes de la conexión")
    conn = mysql.connector.connect(
        host="",
        port=,
        user="",
        password="",
        database="",
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
