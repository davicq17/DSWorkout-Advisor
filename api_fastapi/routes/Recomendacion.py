from fastapi import APIRouter
from pydantic import BaseModel
from api_fastapi.db import get_conn
from pymysql import Error
import requests


router = APIRouter(prefix="/Recomendacion", tags=["Recomendacion"])

# =========================
# Conexión a MySQL - Se abre/cierra por petición
# =========================
# Ya no usamos conexión global para evitar saturar la BD

# =========================
# Hugging Face API - OpenAI-Compatible Router
# =========================

# Using Hugging Face Router API with OpenAI-compatible format
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"    
HF_MODEL = "Qwen/Qwen2.5-72B-Instruct:fastest"  # Fast, capable model
HF_API_TOKEN = "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"
HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

# =========================
# Modelos para request
# =========================
class AssignRoutineRequest(BaseModel):
    user_id: int
    routine_id: int
    trainer_id: int
    notes: str = ""

# =========================
# Endpoints
# =========================

# -------------------------
# Recomendación para entrenador
# -------------------------
@router.post("/recomendacionAI/{user_id}")
def recomendacionAI(user_id: int):
    # Abrir conexión a la BD
    db = get_conn()
    cursor = db.cursor()
    
    try:
        # Usuario
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            return {"error": "Usuario no encontrado"}

        # Convertir tupla a diccionario
        columns = [col[0] for col in cursor.description]
        user = dict(zip(columns, row))

        # Última evaluación
        cursor.execute("""
            SELECT * FROM evaluacion 
            WHERE id_cliente = %s 
            ORDER BY id_evaluación DESC 
            LIMIT 1
        """, (user_id,))
        row = cursor.fetchone()
        ultima_eval = dict(zip([col[0] for col in cursor.description], row)) if row else None

        # Historial de evaluaciones
        cursor.execute("""
            SELECT * FROM evaluacion
            WHERE id_cliente = %s
            ORDER BY id_evaluación ASC
        """, (user_id,))
        historial_eval = [dict(zip([col[0] for col in cursor.description], r)) for r in cursor.fetchall()]

        # Rutinas asignadas
        cursor.execute("""
            SELECT * FROM user_routine
            WHERE id_cliente = %s
            ORDER BY fecha_evaluación DESC
        """, (user_id,))
        rutinas_asignadas = [dict(zip([col[0] for col in cursor.description], r)) for r in cursor.fetchall()]

        # Ejercicios de cada rutina
        ejercicios_por_rutina = {}
        for r in rutinas_asignadas:
            cursor.execute("""
                SELECT w.* FROM routine_workout rw
                JOIN workout w ON rw.id_workout = w.id_workout
                WHERE rw.id_routine = %s
                ORDER BY rw.orden ASC
            """, (r['id_routine'],))
            ejercicios_por_rutina[r['id_routine']] = [dict(zip([col[0] for col in cursor.description], e)) for e in cursor.fetchall()]

        # Prompt optimizado
        prompt = f"""
            Usuario: {user['name']} {user['surname']}
            Última evaluación: {ultima_eval}
            Historial de evaluaciones: {historial_eval}
            Rutinas asignadas: {rutinas_asignadas}
            Ejercicios por rutina: {ejercicios_por_rutina}

            Genera una recomendación de rutina de ejercicios personalizada para el entrenador, incluyendo:
            - Series y repeticiones
            - Orden de ejercicios
            - Explicación de progresión
            - Ajustes según restricciones y objetivos
            - No uses negritas, itálicas, subrayado

            LIMITA LA RESPUESTA A UN MAXIMO DE 1000 TOKENS, SÉ CONCISO
            """

        # Llamada Hugging Face con formato OpenAI-compatible
        try:
            payload = {
                "model": HF_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            response = requests.post(
                HF_API_URL,
                headers=HF_HEADERS,
                json=payload,
                timeout=60  # Increased timeout for model loading
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text[:500]}")  # Print first 500 chars
            
            if response.status_code != 200:
                return {
                    "usuario": user,
                    "ultima_evaluacion": ultima_eval,
                    "rutinas_asignadas": rutinas_asignadas,
                    "recomendacion_IA": f"Error API ({response.status_code}): {response.text}"
                }
            
            data = response.json()
            # OpenAI format returns choices[0].message.content
            recomendacion_ia = data['choices'][0]['message']['content'] if 'choices' in data else str(data)
        except requests.exceptions.JSONDecodeError as e:
            recomendacion_ia = f"Error decodificando JSON: {e}. Response: {response.text[:200]}"
        except Exception as e:
            recomendacion_ia = f"Error llamando a Hugging Face: {e}"

        return {
            "usuario": user,
            "ultima_evaluacion": ultima_eval,
            "rutinas_asignadas": rutinas_asignadas,
            "recomendacion_IA": recomendacion_ia
        }
    
    finally:
        # Cerrar cursor y conexión siempre
        cursor.close()
        db.close()
        print("Conexión BD cerrada correctamente")


# -------------------------
# Asignar rutina por entrenador
# -------------------------
@router.post("/assign-routine")
def assign_routine(req: AssignRoutineRequest):
    # Abrir conexión a la BD
    db = get_conn()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO user_routine (id_cliente, id_routine, id_instructor, fecha_evaluación, diagnostico, status)
            VALUES (%s, %s, %s, NOW(), %s, 1)
        """, (req.user_id, req.routine_id, req.trainer_id, req.notes))
        db.commit()
        return {"status": "Rutina asignada correctamente"}
    
    except Exception as e:
        db.rollback()
        return {"error": f"Error al asignar rutina: {str(e)}"}
    
    finally:
        # Cerrar cursor y conexión siempre
        cursor.close()
        db.close()
        print("Conexión BD cerrada correctamente")


