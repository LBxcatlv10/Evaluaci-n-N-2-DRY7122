import requests
import urllib.parse
import time

route_url = "https://graphhopper.com/api/1/route?"

key = "668cae31-befc-4d51-a5d2-2c5833003cdf"


def geocoding(location, key):
    while location == "":
        location = input("Ingrese nuevamente la ubicación: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key, "locale": "es"})

    replydata   = requests.get(url)
    json_data   = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat   = json_data["hits"][0]["point"]["lat"]
        lng   = json_data["hits"][0]["point"]["lng"]
        name  = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0]["country"] if "country" in json_data["hits"][0] else ""
        state   = json_data["hits"][0]["state"]   if "state"   in json_data["hits"][0] else ""

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        #print("URL de la API de Geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
        
    else:
        lat     = "null"
        lng     = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])

    return json_status, lat, lng, new_loc


while True:
    opciones_vehiculo = {
        "1": {"api": "car", "texto": "auto", "frase": "en auto"},
        "2": {"api": "bike", "texto": "bicicleta", "frase": "en bicicleta"},
        "3": {"api": "foot", "texto": "a pie", "frase": "a pie"}
    }

    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Seleccione el tipo de medio de transporte:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. A pie")
    print("4. Salir")
    print("También puede ingresar 'q' para salir")    
    print("+++++++++++++++++++++++++++++++++++++++++++++")

    opcion = input("Ingrese una opción del 1 al 4: ")

    if opcion == "4" or opcion == "q":
        print("Saliendo del programa...")
        break
    elif opcion in opciones_vehiculo:
        vehicle = opciones_vehiculo[opcion]["api"]
        vehicle_texto = opciones_vehiculo[opcion]["texto"]
        vehicle_frase = opciones_vehiculo[opcion]["frase"]
    else:
        print("Opción no válida. Intente nuevamente.")
        continue

    loc1 = input("Ciudad de Origen (o 'q' para salir): ")

    if loc1 == "quit" or loc1 == "s" or loc1 == "salir" or loc1 == "q":
        break

    orig = geocoding(loc1, key)

    loc2 = input("Destino (o 'q' para salir): ")

    if loc2 == "quit" or loc2 == "s" or loc2 == "salir" or loc2 == "q":
        break

    dest = geocoding(loc2, key)

    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])

        paths_url    = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data   = requests.get(paths_url).json()

        #print("Estado de la API de Enrutamiento: " + str(paths_status) + "\nURL de la API de Enrutamiento:\n" + paths_url)
        print("=================================================")
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3] + " " + vehicle_frase)
        print("=================================================")

        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km    = (paths_data["paths"][0]["distance"]) / 1000
            sec   = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min   = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr    = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)

            print("Distancia recorrida {0:.2f} millas / {1:.2f} km".format(miles, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path     = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]

                print("{0} ( {1:.2f} km / {2:.2f} millas )".format(
                    path, distance / 1000, distance / 1000 / 1.61))

            print("Recorrido finalizado desde " + orig[3] + " hasta " + dest[3] + " " + vehicle_frase + ".")
            print("=================================================")
            time.sleep(2)
        else:
            print("Mensaje de error: " + paths_data["message"])            
            print("*************************************************")

