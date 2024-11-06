import re
import json
from collections import defaultdict, Counter

# Patrón de expresión regular para analizar cada línea de registro
patron_log = re.compile(
    r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<fecha>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\] '
    r'"(?P<metodo>\w+) (?P<recurso>/\S*) HTTP/\d\.\d" (?P<estado>\d{3}) \d+ "(?P<user_agent>[^"]+)"'
)

# Inicializar listas y contadores
datos_log = []
contador_ip = Counter()
contador_recursos = Counter()
errores_http = []

# Procesar archivo de log y extraer datos
with open("log.txt", "r") as archivo:
    for linea in archivo:
        resultado = patron_log.search(linea)
        if resultado:
            datos = resultado.groupdict()
            datos_log.append(datos)
            contador_ip[datos["ip"]] += 1
            contador_recursos[datos["recurso"]] += 1
            if datos["estado"].startswith("4") or datos["estado"].startswith("5"):
                errores_http.append(datos)

# Guardar datos de registro en formato JSON
with open("datos_log.json", "w") as archivo_json:
    json.dump(datos_log, archivo_json, indent=4)

# Guardar conteo de solicitudes por IP
with open("conteo_por_ip.txt", "w") as archivo_ip:
    for ip, conteo in contador_ip.items():
        archivo_ip.write(f"{ip}: {conteo}\n")

# Guardar errores HTTP en un archivo
with open("errores_http.txt", "w") as archivo_errores:
    for error in errores_http:
        archivo_errores.write(json.dumps(error) + "\n")

# Guardar conteo de solicitudes por recurso
with open("conteo_por_recurso.txt", "w") as archivo_recursos:
    for recurso, conteo in contador_recursos.items():
        archivo_recursos.write(f"{recurso}: {conteo}\n")
