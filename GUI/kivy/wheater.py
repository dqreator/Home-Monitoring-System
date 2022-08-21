import requests, json
# ingresamos la API KEY
# 
api_key = "effb9e3b99e8f5c2f03e529c11754950"

# direccion web desde donde solicitaremos la informacion
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# ciudad (se lo mas especifico posible en el nombre)
city_name = "Krakow"

# esta es la URL completa con la informacion concatenada para realizar la petición correcta
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
# Ejecutamos la consulta
response = requests.get(complete_url)

# Obtenemos la respuesta en formato JSON
x = response.json()
print(x)
if x["cod"] == "200":
    # En “main” se encuentra la informacion principal del estado del tiempo
    y = x["main"]

    # Almacenamos la temperatura
    current_temperature = y["temp"]

    # presion atmosferica
    current_pressure = y["pressure"]

    # humedad
    current_humidity = y["humidity"]

    print("temperature"+current_temperature)