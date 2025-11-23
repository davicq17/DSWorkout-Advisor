from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import usuarios, login, routine, workout,Diagnosticos


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173","*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#RUTAS
app.include_router(usuarios.router)
app.include_router(login.router)
app.include_router(routine.router)
app.include_router(workout.router)
app.include_router(Diagnosticos.router)

@app.get("/")
def read_root():
    return {"mensaje": "API FastAPI funcionando correctamente 🚀"}
