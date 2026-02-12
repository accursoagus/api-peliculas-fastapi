# API REST de Gestión de Películas (Cliente-Servidor)

Este proyecto implementa una arquitectura Cliente-Servidor utilizando el protocolo HTTP para la gestión de una base de datos de películas.

El sistema permite realizar operaciones CRUD (Crear, Leer, Actualizar, Borrar) a través de una API RESTful, comunicando un cliente basado en consola con un servidor que procesa las peticiones y administra la persistencia de datos.

## Arquitectura del Sistema

### Servidor (`main.py`)
Implementa la lógica de negocio y expone los endpoints de la API.
* Protocolo: HTTP sobre TCP/IP.
* Formato de Intercambio: JSON.
* Persistencia: Gestión de datos en memoria/archivo local.
* Endpoints Principales:
    * GET /peliculas: Listado completo o filtrado por género/título.
    * GET /peliculas/{id}: Detalle de una película específica.
    * POST /peliculas: Alta de nueva película.
    * PUT /peliculas/{id}: Modificación de datos existentes.
    * DELETE /peliculas/{id}: Baja lógica o física del registro.

### Cliente (`cliente.py`)
Aplicación de consola que actúa como interfaz de usuario.
* Menú interactivo para seleccionar operaciones.
* Generación de requests HTTP mediante la librería `requests`.
* Formateo y visualización de las respuestas JSON recibidas del servidor.

## Tecnologías Utilizadas
* Python 3
* FastAPI / Uvicorn (Servidor)
* Requests (Cliente)
* JSON (Serialización de datos)

## Instrucciones de Ejecución

1. Iniciar el Servidor:
```bash
python main.py
