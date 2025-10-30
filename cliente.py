import requests
import json
from requests.auth import HTTPBasicAuth

url_api = "http://localhost:8000"  # o la URL donde corre tu API

def menu():
    usuario = input('Nombre de usuario: ')
    pwd = input('Contraseña: ')
    auth = HTTPBasicAuth(usuario, pwd)

    while True:
        print(
            '\nOpciones:\n'
            '=== Películas ===\n'
            '1. Obtener película\n'
            '2. Obtener peliculas de un actor\n'
            '3. Obtener la cantidad de películas\n'
            '4. Obtener la cantidad de películas según género\n'
            '5. Agregar película\n'
            '6. Modificar película\n'
            '7. Eliminar película\n'
            '=== Watchlist ===\n'
            '8. Obtener watchlist\n'
            '9. Agregar pelicula a la watchlist\n'
            '10. Eliminar pelicula de la watchlist\n'
            '11. Salir'
        )

        entrada = input('Elija una opción: ')

        if entrada.isdigit() == False:
            print('Debe ingresar un número')
            continue
       
        opcion = int(entrada)

        if opcion == 1:
            pelicula = input('Nombre de la película: ')
            r = requests.get(f"{url_api}/buscar_titulo", params={"nombre_buscado": pelicula})
            print(json.dumps(r.json(), indent=4, ensure_ascii=False))

        if opcion == 2:
            actor = input('Nombre del actor: ')
            r = requests.get(f"{url_api}/buscar_actor", params={"nombre_buscado": actor})
            print(r.json())

        if opcion == 3:
            r = requests.get(f"{url_api}/total")
            print(r.text)

        if opcion == 4:
            genero = input('Género de pelicula: ')
            r = requests.get(f"{url_api}/obtener_cantidad_segun_genero", params={"genero": genero})
            print(r.text)

        if opcion == 5:
            print("Ingrese los datos de la nueva película: ")
            title = input("Título: ")
            year = int(input("Año: "))
            cast_input = input("Actores (separados por coma): ")
            cast = [a.strip() for a in cast_input.split(",") if a.strip()]
            genres_input = input("Géneros (separados por coma): ")
            genres = [g.strip() for g in genres_input.split(",") if g.strip()]
            href = input("Href: ") or ""
            extract = input("Extract: ") or ""
            thumbnail = input("thumbnail: ")
            thumbnail_width = int(input("Ancho del thumbnail: ") or 0)
            thumbnail_height = int(input("Alto del thumbnail: ") or 0)

            pelicula = {
                "title": title,
                "year": year,
                "cast": cast,
                "genres": genres,
                "href": href,
                "extract": extract,
                "thumbnail": thumbnail,
                "thumbnail_width": thumbnail_width,
                "thumbnail_height": thumbnail_height
            }

            r = requests.post(f"{url_api}/agregar_pelicula", json=pelicula, auth=auth)
            print(r.text)

        if opcion == 6:
            nombre_pelicula = input('Ingrese el nombre de la pelicula: ')
            atributo = input('Ingrese el atributo de la pelicula a modificar: ')
            valor = input('Ingrese el valor: ')
            r = requests.put(f"{url_api}/modificar_pelicula", params={'nombre_pelicula': nombre_pelicula, 'atributo': atributo, 'valor': valor}, auth=auth)
            print(r.text)

        if opcion == 7:
            nombre_pelicula = input('Ingrese el nombre de la pelicula: ')
            r = requests.delete(f"{url_api}/eliminar_pelicula", params={'nombre_pelicula': nombre_pelicula}, auth=auth)
            print(r.text)
            
        if opcion == 8:
            r = requests.get(f"{url_api}/obtener_watchlist")
            print(r.text)

        if opcion == 9:
            nombre_pelicula = input('Ingrese el nombre de la pelicula: ')
            r = requests.post(f"{url_api}/agregar_watchlist", params={'nombre_buscado': nombre_pelicula})
            print(r.text)

        if opcion == 10:
            nombre_pelicula = input('Ingrese el nombre de la pelicula: ')
            r = requests.delete(f"{url_api}/eliminar_watchlist", params={'nombre_buscado': nombre_pelicula})
            print(r.text)

        elif opcion == 11:
            print("Saliendo...")
            break


menu()