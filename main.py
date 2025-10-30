from fastapi import FastAPI, Depends, HTTPException, status, Body, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from typing import Deque, Dict
import secrets
import uvicorn
import requests

# Crear la API
app = FastAPI()

# Seguridad
security = HTTPBasic()
USUARIOS = {"nico": "nico123"}

def verificar_credenciales(credenciales: HTTPBasicCredentials = Depends(security)) -> str:
    pwd_correcta = USUARIOS.get(credenciales.username)
    if not pwd_correcta or not secrets.compare_digest(credenciales.password, pwd_correcta):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas", headers={"WWW-Authenticate": "Basic"},)
    return credenciales.username

# Clase para definir los atributos de una película
class Pelicula(BaseModel):
    title: str
    year: int
    cast: List[str] = []
    genres: List[str] = []
    href: Optional[str] = ""
    extract: Optional[str] = ""
    tumbnail: str = ""
    thumbnail_width: Optional[int] = 0
    thumbnail_height: Optional[int] = 0

# Datos en memoria
datos_en_memoria: List[dict] = []
watchlist: list[str] = []

@app.on_event("startup")
def cargar_datos():
    global datos_en_memoria
    try:
        url = 'https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json'
        datos_en_memoria = requests.get(url).json()
    except Exception:
        datos_en_memoria = []

# Buscar por título
@app.get("/buscar_titulo")
def buscar_por_titulo(nombre_buscado: str):
    for obj in datos_en_memoria:
        if obj.get("title", "").lower() == nombre_buscado.lower():
            return obj
    return {"error": "No encontrado"}

# Buscar por actor
@app.get("/buscar_actor")
def buscar_por_actor(nombre_buscado: str):
    resultados = []
    for obj in datos_en_memoria:
        if any(nombre_buscado.lower() == actor.lower() for actor in obj.get("cast", [])):
            resultados.append(obj["title"])
    return resultados

# Obtener el número total de películas
@app.get("/total")
def obtener_cantidad():
    return len(datos_en_memoria)

# Obtener el número total de películas según el género
@app.get("/obtener_cantidad_segun_genero")
def obtener_cantidad_segun_genero(genero:str=None):
    cant_genero = 0

    if genero == None:
        return {"error": "No encontrado"}

    for pelicula in datos_en_memoria:
        generos = pelicula.get("genres", [])
        if isinstance(generos, list):
            if genero.lower() in [g.lower() for g in generos]:
                cant_genero += 1
    
    return f'Hay {cant_genero} peliculas de {genero}'

# Obtener la Watchlist 
@app.get("/obtener_watchlist")
def obtener_watchlist():
    return watchlist

#Agregar a la Watchlist
@app.post("/agregar_watchlist")
def agregar_pelicula_watchlist(nombre_buscado: str):
    if watchlist != []:
        for titulo in watchlist:
            if titulo.lower() == nombre_buscado.lower():
                return f"{nombre_buscado} ya está en la watchlist"

    for pelicula in datos_en_memoria:
        if pelicula.get("title", "").lower() == nombre_buscado.lower():
            watchlist.append(pelicula["title"])
            return f"Película '{nombre_buscado}' agregada a la watchlist."
    
    return "Película no encontrada"

#Eliminar de la Watchlist
@app.delete("/eliminar_watchlist")
def eliminar_pelicula_watchlist(nombre_buscado: str):

    for titulo in watchlist:
        if titulo.lower() == nombre_buscado.lower():
            watchlist.remove(titulo)
            return f"Película '{nombre_buscado}' eliminada de la watchlist."
    return f"{nombre_buscado} no estaba en la watchlist"

#Agregar pelicula en memoria
@app.post("/agregar_pelicula")
def agregar_pelicula(pelicula: Pelicula = Body(...), usuario: str = Depends(verificar_credenciales)):
    datos_en_memoria.append(pelicula.dict())
    return {"mensaje": f"Película '{pelicula.title}' agregada temporalmente."}

#Modificar pelicula en memoria
@app.put("/modificar_pelicula")
def modificar_pelicula(nombre_pelicula: str, atributo: str, valor: str, usuario: str = Depends(verificar_credenciales)):
    for pelicula in datos_en_memoria:
        if pelicula["title"] == nombre_pelicula:
            pelicula[atributo] = valor
            return {"mensaje": f"Pelicula '{nombre_pelicula}' modificada temporalmente."}
    return {"error": "Película no encontrada"}

#Eliminar pelicula en memoria
@app.delete("/eliminar_pelicula")
def eliminar_pelicula(nombre_pelicula: str, usuario: str = Depends(verificar_credenciales)):
    for pelicula in datos_en_memoria:
        if pelicula.get("title", "").lower() == nombre_pelicula.lower():
            datos_en_memoria.remove(pelicula)
            return {"mensaje": f"Película '{nombre_pelicula}' eliminada temporalmente."}
    
    raise HTTPException(status_code=404, detail="Película no encontrada.")

#Limitador
VENTANA = timedelta(seconds=1)   # Ventana de tiempo
MAX_PETICIONES = 10             # Máximo de peticiones dentro de la ventana

cubos_ip: Dict[str, Deque[datetime]] = {}

@app.middleware("http")
async def limitador(request: Request, call_next):
    ip = request.client.host
    ahora = datetime.utcnow()

    cubo = cubos_ip.setdefault(ip, Deque())

    # Eliminar timestamps fuera de la ventana
    while cubo and (ahora - cubo[0]) > VENTANA:
        cubo.popleft()

    if len(cubo) >= MAX_PETICIONES:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiadas solicitudes: límite 10 req/s",
        )

    cubo.append(ahora)
    respuesta = await call_next(request)
    return respuesta

# Ejecutar servidor
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)