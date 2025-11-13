import datetime
from fastapi import APIRouter, HTTPException, Header
from api_fastapi.db import get_conn
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from ..config import SECRET_KEY, ALGORITHM


router = APIRouter(prefix="/Login", tags=["Login"]);

##LOGIN
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

            token = jwt.encode(jpayload, SECRET_KEY, ALGORITHM)

            content = {"id": id,"username": username,"name": name,"surname": surname,"password": password,"rol": rol, "status": status,"token": token}

            payload_list.append(content)

        return payload_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## VERIFICAR EL TOKEN#
@router.get("/verify_token")
def verify_token(Authorization: str = Header(...)):
    try:
        if not Authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Formato de token invalido")
        token = Authorization.split("")[1]
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token invalido")

## VRIFICAR LA EXIXSTENCIA DE UN USUARIO
@router.get("/VerifyUser/{username}")
def VerifyUser(username:str):
    try:
        conn=get_conn()
        cur=conn.cursor()
        cur.execute('SELECT username FROM usuarios WHERE username = %s', (username,))
        rv = cur.fetchall()
        cur.close()
        conn.close()
        payload = []
        content = {}

        for result in rv:
            content = {"username":result[0]}
            payload.append(content)
        return payload
    except Exception as e:
        print("Error en la verificacion: {e}")
        raise HTTPException(status_code=500, detail="Error verificando usuario")
