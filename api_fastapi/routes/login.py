import time
import jwt
from fastapi import APIRouter, HTTPException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from api_fastapi.db import get_conn

from ..config import SECRET_KEY, ALGORITHM



router = APIRouter(prefix="/Login", tags=["Login"])

##LOGIN
@router.get("/User/{username}")
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
            now = int(time.time())
            jpayload = {
                "id": id,
                "username": username,
                "name": name,
                "surname": surname,
                "rol": rol,
                "exp": now + 60*60*6,
                "iat": now
            }

            token = jwt.encode(jpayload, SECRET_KEY, algorithm=ALGORITHM)

            content = {"id": id,"username": username,"name": name,"surname": surname,"password": password,"rol": rol, "status": status,"token": token}

            payload_list.append(content)

        return payload_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## VERIFICAR EL TOKEN#
@router.get("/verify_token/{token}")
def verify_token(token: str):
    try:
        if not token:
            raise HTTPException(status_code=401, detail="No se envio el token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token invalido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## VRIFICAR LA EXIXSTENCIA DE UN USUARIO
@router.get("/VerifyUser/{username}")
def VerifyUser(username:str):
    try:
        conn=get_conn()
        cur=conn.cursor()
        cur.execute('SELECT count(*) as Existe FROM usuarios WHERE username = %s', (username,))
        rv = cur.fetchone()
        cur.close()
        conn.close()
        payload={"Existe":rv[0]}
        print(payload)
        return payload
    except Exception as e:
        print("Error en la verificacion: {e}")
        raise HTTPException(status_code=500, detail="Error verificando usuario")
