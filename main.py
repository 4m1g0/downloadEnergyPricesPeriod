from http.server import BaseHTTPRequestHandler, HTTPServer
import xmltodict
import requests
from datetime import timedelta, date
import time

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
start_date = date(2016, 9, 1)
end_date = date(2017, 9, 2)

precio1 = {}
for i in range(0, 25):
    precio1[i] = 0.0
precio2 = {}
for i in range(0, 25):
    precio2[i] = 0.0
cantidad = 0

for single_date in daterange(start_date, end_date):
    d = single_date.strftime("%d-%m-%Y")
    r = requests.get("https://api.esios.ree.es/archives/80/download?date=" + d)
    print(d)
    time.sleep(0.2)
    doc = xmltodict.parse(r.text)
    for tarifa in doc['PVPCDesgloseHorario']['SeriesTemporales']:
        if 'TipoPrecio' in tarifa and 'TerminoCosteHorario' in tarifa and tarifa['TipoPrecio']['@v'] == "Z01" and tarifa['TerminoCosteHorario']['@v'] =="FEU":
            n = 0
            cantidad += 1
            for i in tarifa['Periodo']['Intervalo']:
                precio1[n] += float(i['Ctd']['@v'])
                n += 1
        if 'TipoPrecio' in tarifa and 'TerminoCosteHorario' in tarifa and tarifa['TipoPrecio']['@v'] == "Z02" and tarifa['TerminoCosteHorario']['@v'] =="FEU":
            n = 0
            cantidad += 1
            for i in tarifa['Periodo']['Intervalo']:
                precio2[n] += float(i['Ctd']['@v'])
                n += 1
                
print(precio1)
print(precio2)
print(cantidad)
