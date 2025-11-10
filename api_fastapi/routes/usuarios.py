from fastapi import APIRouter, HTTPException
from api_fastapi.db import get_conn

router = APIRouter(prefix="/Usuarios", tags=["Login"])


@router.get("/TableUser")

def TableUser():
    print("entrando a la ruta de la tabla")
    try: 
        conn = get_conn()
        print("conexion establecida con MySQL")
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios WHERE status = 1')
        rv = cur.fetchall()
        cur.close()
        conn.close()
        payload = []
        content = {}
        for result in rv:
            content  = {
                "id": result[0],
                "username": result[1],
                "name": result[2],
                "surname": result[3],
                "email": result[4],
                "password": result[5],
                "cell": result[6],
                "rol": result[7]
            }
            payload.append(content)
        print( "Datos obtenidos")
        return payload 
    except Exception as e:
        print("❌ Error en TableUser:", e)
        print(e)
        raise HTTPException(status_code=500, detail=str(e))