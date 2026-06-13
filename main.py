from fastapi import FastAPI
from database import engine
import models
from routers import router

#SQLalchemy revisa los modelos que existe y crea sus tablas en postgret si no existen, cada vez que comienza la API
# Llamamos a el motor de conexion
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Conectamos el router con los endpoints de usuarios
app.include_router(router)

@app.get("/ping")
def ping():
    return {"status": "ok", "mensaje": "La API está funcionando"}