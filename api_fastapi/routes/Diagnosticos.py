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