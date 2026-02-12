# API REST de Gestión de Películas (Cliente-Servidor)

Este proyecto implementa una arquitectura Cliente-Servidor utilizando el protocolo HTTP para la gestión de una base de datos de películas.

El sistema permite realizar operaciones CRUD (Crear, Leer, Actualizar, Borrar) a través de una API RESTful, comunicando un cliente basado en consola con un servidor que procesa las peticiones y administra la persistencia de datos.

## Arquitectura del Sistema

### Servidor (`main.py`)
Implementa la lógica de negocio y expone los endpoints de la API utilizando FastAPI.
* **Protocolo:** HTTP sobre TCP/IP.
* **Formato de Intercambio:** JSON.
* **Persistencia:** Gestión de datos en memoria (lista de diccionarios).
* **Endpoints Principales:**
    * `GET /peliculas`: Listado completo o filtrado por género/título.
    * `GET /peliculas/{id}`: Detalle de una película específica.
    * `POST /peliculas`: Alta de nueva película.
    * `PUT /peliculas/{id}`: Modificación de datos existentes.
    * `DELETE /peliculas/{id}`: Baja del registro.

### Cliente (`cliente.py`)
Aplicación de consola que actúa como interfaz de usuario.
* Menú interactivo para seleccionar operaciones.
* Generación de requests HTTP mediante la librería `requests`.
* Formateo y visualización de las respuestas JSON recibidas del servidor.
* Manejo de códigos de estado HTTP (200 OK, 201 Created, 404 Not Found) para feedback al usuario.

## Tecnologías Utilizadas
* Python 3.9+
* FastAPI (Framework de API)
* Uvicorn (Servidor ASGI)
* Requests (Cliente HTTP)
* Pydantic (Validación de datos)

## Instrucciones de Ejecución

### 1. Instalación de dependencias
Se requiere instalar las librerías del servidor y del cliente:

    pip install fastapi uvicorn requests

### 2. Iniciar el Servidor
Ejecutar el siguiente comando para levantar la API en el puerto 8000 (localhost):

    python main.py

*Nota: El servidor debe mantenerse en ejecución para que el cliente pueda conectarse.*

### 3. Iniciar el Cliente
En una nueva terminal, ejecutar la interfaz de consola:

    python cliente.py

## Documentación
Para detalles sobre el diseño del protocolo, el diagrama de flujo y los códigos de estado HTTP utilizados, consultar el archivo `Accurso-Mancini - Informe.pdf` incluido en este repositorio.

---
*Proyecto desarrollado para la asignatura Redes de Datos - Tecnicatura Universitaria en IA (UNR), en colaboración con Mancini.*
