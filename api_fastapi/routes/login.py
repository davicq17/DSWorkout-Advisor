import datetime
from fastapi import APIRouter,HTTPException
from db import get_conn
import jwt
from config import SECRET_KEY


router = APIRouter(prefix="/Login", tags=["Login"]);

@router.get("/{username}")
def login(username: str):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, name, surname, password, rol, status
            FROM usuarios
            WHERE username = %s
        """, (username,))
        rv = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rv:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        payload_list = []

        for result in rv:
            id, username, name, surname, password, rol, status = result

            # Generar token JWT
            jpayload = {
                "id": id,
                "username": username,
                "name": name,
                "surname": surname,
                "rol": rol,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=6),
                "iat": datetime.datetime.now()
            }

            token = jwt.encode(jpayload, SECRET_KEY, algorithm="HS256") 

            content = {
                "id": id,
                "username": username,
                "name": name,
                "surname": surname,
                "password": password,
                "rol": rol,
                "status": status,
                "token": token
            }

            payload_list.append(content)

        return payload_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))