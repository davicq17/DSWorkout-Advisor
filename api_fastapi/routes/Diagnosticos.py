from fastapi import APIRouter, HTTPException, Depends
from api_fastapi.db import get_conn
from .login import verify_token
from pydantic import BaseModel

router = APIRouter(prefix="/Diagnosticos", tags=["Diagnosticos"])

@router.get("/GetDiagnostico/{id}")
def GetDiagnostico(id: int):
    try:
        conn = get_conn()
        cur = conn.cursor()
        query = '''
            SELECT ur.id_cliente, ur.id_instructor, ur.fecha_evaluación, ur.diagnostico,
                   r.id_routine, r.nombre, r.nivel, r.descripcion
            FROM user_routine ur
            JOIN routine r ON ur.id_routine = r.id_routine
            WHERE ur.id_cliente = %s
            ORDER BY ur.fecha_evaluación DESC
            LIMIT 1
        '''
        cur.execute(query, (id,))
        rv = cur.fetchone()

        cur.close()
        conn.close()

        if rv:
            content = {
                "id_cliente": rv[0],
                "id_prof": rv[1],
                "fech_evaluation": rv[2],
                "diagnostico": rv[3],
                "idR": rv[4],
                "nombreR": rv[5],
                "nivelR": rv[6],
                "descripcion": rv[7]
            }
            return content
        return {"informacion": "SinDiagnostico"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class FisicState(BaseModel):
    id: int
    age: int
    gender: str
    height: float
    weight: float
    fr_train: str
    goal: str
    restrictions: str

@router.post("/regisFisicState")
def regisFisicState(FisicState: FisicState):
    try:
        conn = get_conn()
        cur = conn.cursor()
        query = '''
            INSERT INTO evaluacion (id_cliente,age,gender,height,weight,fr_train,goal,restrictions,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        cur.execute(query, (FisicState.id, FisicState.age, FisicState.gender, FisicState.height, FisicState.weight, FisicState.fr_train, FisicState.goal, FisicState.restrictions,1))
        conn.commit()
        cur.close()
        conn.close()
        return {"informacion": "Registro de estado fisico Exitoso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#Saber si el usuario ya ha realizado el formulario de estado fisico con el estado positivo
@router.get("/GetFisicState/{id}")
def GetFisicState(id: int):
    try:
        conn = get_conn()
        cur = conn.cursor()
        query = '''
            SELECT * FROM evaluacion WHERE id_cliente = %s AND status = 1
        '''
        cur.execute(query, (id,))
        rv = cur.fetchone()

        cur.close()
        conn.close()

        if rv:
            return True
        return False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# VER ESTADO FISICO MÁS DETALLADO SEGÚN EL ID
@router.get("/FisicById/{id}")
def fisic_by_id(id:int):
    try:
        conn = get_conn()
        cur = conn.cursor()
        query = '''
            SELECT usuarios.id ,usuarios.name, usuarios.surname,evaluacion.age ,
            evaluacion.gender, evaluacion.height, evaluacion.weight, evaluacion.fr_train, 
            evaluacion.restrictions, evaluacion.goal 
            FROM (defaultdb.usuarios JOIN defaultdb.evaluacion 
            ON(usuarios.id = evaluacion.id_cliente AND usuarios.status = 1 AND id = %s))
        '''
        cur.execute(query, (id))
        rv = cur.fetchone()
        cur.close()
        conn.close()

        if rv:
            content = {
                "id": rv[0],"name": rv[1],
                "surname": rv[2],"age": rv[3],
                "gender": rv[4],"height": rv[5],
                "weight": rv[6],"fr_train": rv[7],
                "restrictions": rv[8],"goal": rv[9]
            }
            return content
        return{"informacion":"Sin evaluación"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# REGISTRO DEL DIAGNOSTICO DeL PROFESIONAL
class DiagnosticoCreate(BaseModel):
    id_cliente: int
    rutina: int
    instructor: int 
    fecha: str
    diagnostico: str


@router.post("/AddDiagnostico")
def add_diagnostico(data: DiagnosticoCreate):
    try:
        conn = get_conn()
        cur = conn.cursor()

        query = """INSERT INTO defaultdb.user_routine (id_cliente,id_routine,id_instructor, fecha_evaluación, diagnostico) VALUES (%s,%s,%s,%s,%s)"""
        values = (data.id_cliente,data.rutina,data.instructor,data.fecha,data.diagnostico)

        cur.execute(query, values)
        conn.commit()
        cur.close()

        return {"informacion": "Registro exitoso"}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
