from fastapi import APIRouter, HTTPException, Depends
from api_fastapi.db import get_conn
from api_fastapi.routes.login import verify_token
from pydantic import BaseModel

router = APIRouter(prefix="/Workout", tags=["Workout"])

##TABLA DE EJERCICIOS
@router.get("/ejercicioTabla")
def ejercicio_tabla(token: dict = Depends(verify_token)):
    try:
        conn = get_conn()
        cur= conn.cursor()
        cur.execute("SELECT * FROM workout")
        resultados = cur.fetchall()
        cur.close
        conn.close()

        payload = []
        for result in resultados:
            rating = result[9] if len(result) > 9 and result[9] is not None else 0
            content = {
                "id": result[0],
                "nombre": result[1],
                "guia": result[2],
                "tipo": result[3],
                "equipo": result[4],
                "nivel": result[5],
                "repeticiones": result[6],
                "series": result[7],
                "duracion": result[8],
                "rating": rating
            }
            payload.append(content)
        return payload
    except Exception as e:
        print(f"Error en ejercicio_tabla: {e}")
        raise HTTPException(status_code=500, detail=str(e))

##REGISTRAR UN EJERCICIO
class RegistroWorkout(BaseModel):
    nombre:str
    guia:str
    tipo:str
    equipo:str
    nivel:str
    repeticiones:int
    series:int
    duracion:str
@router.post("/registroEjercicio")
def registro_ejercicio(workout: RegistroWorkout, tor: dir = Depends(verify_token)):
    try:
        conn= get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO workout( nombre, guide, tipo, equipo, nivel, repetitions, series, duration) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (workout.nombre, workout.guia, workout.tipo, workout.equipo, workout.nivel, workout.repeticiones, workout.series, workout.duracion))
        conn.commit()
        cur.close()
        conn.close()
        return{"informacion":"Registro exitoso"}
    except Exception as e:
        print(f"Error:{e}")
        raise HTTPException(status_code=500, detail=str(e))
    
#PEDIR INFORMACION DEL EJERCICIO
@router.get("/WorkoutById/{id}")
def workout_by_id(id:int, toke: dict= Depends(verify_token)):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(" SELECT nombre, guide, tipo, equipo, nivel, duration FROM workout WHERE id_workout = %s", (id,))
        rv = cur.fetchone()
        cur.close()
        conn.close()

        if not rv:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
        
        content = {"nombre": rv[0],"desc": rv[1],"type": rv[2],"equipment": rv[3],"level": rv[4],"duration": rv[5]}
        return content
    except HTTPException as e:
        raise
    except Exception as e:
        print(f"Error en workout by id: {e}")
        raise HTTPException(status_code=500, detail=str(e))