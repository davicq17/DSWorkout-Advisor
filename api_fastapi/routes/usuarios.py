from fastapi import APIRouter, HTTPException, Depends
from api_fastapi.db import get_conn
from .login import verify_token
from pydantic import BaseModel

router = APIRouter(prefix="/Usuarios", tags=["Usuarios"])

## tabla usuarios
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
        print(" Error en TableUser:", e)
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

##REGISTAR USUARIO
class RegistroUser(BaseModel):
    username:str
    name:str
    surname:str
    email:str
    password: str
    cell:str
    rol: int
    status:int
    especialidad: str | None = None
@router.post("/registro")
def registro(data: RegistroUser):
    try:
        conn = get_conn()
        cur= conn.cursor()
        #iniciamos la tansacción
        cur.execute("START TRANSACTION")
        print("transacción iciada")

        #inserción en la tabla usuarios
        cur.execute("INSERT INTO usuarios (username,name,surname,email,password,cell,rol,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (data.username, data.name, data.surname, data.email, data.password, data.cell, data.rol,1))
        print("insercion de usuario realizada")
        #obtengo el ultimo ID insertado
        #cur.execute("SELECT LAST_INSERT_ID()")
        id_usuario = cur.lastrowid

        #verifica que el usuario es porfecsional
        if data.rol == 3 and data.especialidad:
            cur.execute("INSERT INTO Atributo (Descripción) VALUES (%s)",(data.especialidad,))
            print("inserccón de especialidad realizada")
            #obtengo el ultimo atrubuto ingresado 
            id_atributo= cur.lastrowid
            cur.execute("INSERT INTO usuario_atributo (id_user, id_atributo,status) VALUES (%s,%s,%s)",(id_usuario,id_atributo,1))
            print("inserccón de profesional realizada")
        # confirma la transaccion
        conn.commit()
        print("Transacción confirmada")
        cur.close()
        return{"informacion: Registro exitoso"}
    except Exception as e:
        conn.rollback()
        print(f"Error:{e}")
        raise HTTPException(status_code=500, detail=str(e))

## EDITAR USUARIOS DESDE ADMIN
class UserUpdate(BaseModel):
    username:str
    name:str
    surname:str
    email:str
    password: str
    cell: str
    rol: int

@router.put("/editUser/{id}")
def editUser(id:int, user:UserUpdate):
    try:
      conn = get_conn()
      cur = conn.cursor()
      sql = """UPDATE usuarios SET username=%s, name=%s, surname=%s, email=%s, password=%s, cell=%s, rol=%s WHERE id=%s"""
      values = ( user.username, user.name,user.surname, user.email,user.password,user.cell,user.rol,id)
      cur.execute(sql, values)
      conn.commit()
      cur.close()
      conn.close()
      return {"informacion": "Actualización realizada con éxito "}
    except Exception as e:
     print(f"Error en edit_user: {e}")
     raise HTTPException(status_code=500, detail=str(e))

## ELIMINAR USUARIO
@router.put("/delete/{id}")
def deleteUser(id:int):
    try:
        conn= get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE usuarios SET status = %s WHERE id = %s", (0, id))
        conn.commit()
        
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        cur.close()
        conn.close()
        return{"información":"Registro eliminado"}
    except Exception as e:
        print(f"Error eliminando usuario: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# tabla de estados fisicos
@router.get("/TableFisic")
def TableFisc():
    print("inciando ruta")
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT usuarios.id ,usuarios.name, usuarios.surname, evaluacion.age ,evaluacion.gender, evaluacion.height, evaluacion.weight, evaluacion.fr_train, evaluacion.restrictions, evaluacion.goal FROM (defaultdb.usuarios JOIN defaultdb.evaluacion ON(usuarios.id = evaluacion.id_cliente AND usuarios.status = 1))')
        rv = cur.fetchall()
        cur.close()
        conn.close()
        payload = []
        content= {}
        for result in rv:
            content = {
                "id":result[0],
                "name":result[1],
                "surname":result[2],
                "age":result[3],
                "gender":result[4],
                "height":result[5],
                "weight":result[6],
                "fr_train":result[7]
            }
            payload.append(content)
        print("datos obtenidos")
        return payload
    except Exception as e:
        print("Error en TablaFisic:",e)
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
