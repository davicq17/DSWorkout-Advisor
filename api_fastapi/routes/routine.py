from fastapi import APIRouter, HTTPException, Depends
from api_fastapi.db import get_conn
from api_fastapi.routes.login import verify_token
from pydantic import BaseModel

router = APIRouter(prefix="/Routine", tags=["Routine"])


#REGISTRAR RUTINA
class RoutineRegist(BaseModel):
    creador:int
    nombre:str
    descripcion:str
    duracion:int
    nivel:str
    ejercicios: str 

@router.post("/regisRutina")
def regis_rutina(routine:RoutineRegist):
    try:
         conn = get_conn()
         cur = conn.cursor()

         # Insertar la rutina
         sql_routine = """
             INSERT INTO routine (id_prof, nombre, descripcion, duration, nivel,status)
             VALUES (%s, %s, %s, %s, %s,%s)
         """
         cur.execute(sql_routine, (
             routine.creador,
             routine.nombre,
             routine.descripcion,
             routine.duracion,
             routine.nivel,
             1
         ))

         # Obtener el ID de la rutina recién creada
         #cur.execute("SELECT LAST_INSERT_ID()")
         conn.commit()
         id_routine = cur.lastrowid;

         # Construir el query para insertar los ejercicios
         ejercicios = routine.ejercicios.split(',')
         sql="""INSERT INTO routine_workout (id_routine, id_workout, orden,status) VALUES(%s,%s,%s,%s)"""
         

         for i, ejercicio in enumerate(ejercicios, start=1):
             cur.execute(sql,(id_routine,int(ejercicio),i,1))


         conn.commit()
         cur.close()
         conn.close()

         return {"informacion": "Registro de rutina Exitoso"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error e regis_routina: {e}")
        raise HTTPException(status_code=500, detail=str(e))
 

#TABLA DE RUTINAS
@router.get("/getRoutines")
def routines():#token: dict= Depends(verify_token)
    try:
        conn = get_conn()
        cur = conn.cursor()
        sql = """
            SELECT 
                CONCAT(usuarios.name, ' ', usuarios.surname) AS profesional,
                routine.id_routine,
                routine.nombre,
                routine.descripcion,
                routine.duration,
                routine.nivel
            FROM routine
            JOIN usuarios ON routine.id_prof = usuarios.id
        """
        cur.execute(sql)
        rv = cur.fetchall()
        cur.close()
        conn.close()

        payload = []
        for result in rv:
            content = {
                "Autor": result[0],
                "id_routine": result[1],
                "nombre": result[2],
                "descripcion": result[3],
                "duracion": result[4],
                "nivel": result[5]
            }
            payload.append(content)
        return payload
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en routines: {e}")
        raise HTTPException(status_code=500, detail=str(e))

