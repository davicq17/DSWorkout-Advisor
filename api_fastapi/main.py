from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import usuarios

from api_fastapi.db import get_conn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173","*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#RUTAS
app.include_router(usuarios.router);

@app.get("/")
def read_root():
    return {"mensaje": "API FastAPI funcionando correctamente 🚀"}
