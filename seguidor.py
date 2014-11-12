#!/usr/bin/python

from urllib3 import connection_from_url
from bs4 import BeautifulSoup
from pickle import dump, load
from sys import exit

from mail import enviarNotificacion

archivo_pickle = "tramites.pickle"

estados = {
    "imagenes/MapaA1.gif": "Inicio del tramite",
    "imagenes/MapaA2.gif": "Certificacion CBC",
    "imagenes/MapaA3.gif": "Recepcion del tramite (Dpto. de titulos)",
    "imagenes/MapaA4.gif": "Control final del Dpto. de titulos",
    "imagenes/MapaA5.gif": "Verificacion DNI/Firma y entrega de LU (1)",
    "imagenes/MapaA6.gif": "Verificacion DNI/Firma y entrega de LU (2)",
    "imagenes/MapaA7.gif": "Confeccion del diploma",
    "imagenes/MapaA8.gif": "Verificacion de diploma",
    "imagenes/MapaA9.gif": "Facultad",
    "imagenes/MapaA10.gif": "Firma de Autoridades del Rectorado",
    "imagenes/MapaA12.gif": "Final del tramite",
}


def cuigToURL(cuig):
    url = '%s/siet/mapa.asp?cuig=%s' % (base_url, cuig)
    return url

def notificar(tramite):
    print tramite

base_url = 'http://www.academica.rec.uba.ar'
http = connection_from_url(base_url, maxsize=2)


try:
    tramites = load(open("tramites.pickle", 'rb'))
except:
    exit("No se pudo leer el archivo de tramites")


hubo_cambios = 0
for cuig in tramites.keys():
    print "Investigando el estado de %s" % cuig
    html = http.request('GET', cuigToURL(cuig))
    soup = BeautifulSoup(html.data)

    for img in soup.findAll('img'):
        if img.has_attr("src") and "Mapa" in img['src']:
            if img['src'] != tramites[cuig]['paso']:
                hubo_cambios = 1
                tramites[cuig]['paso'] = img['src']
                tramites[cuig]['estado'] = estados[img['src']]

                print "Avanzo %s! (%s)" % (tramites[cuig]['desc'],
                                           estados[img['src']])

                enviarNotificacion(tramites[cuig], html.data)

if hubo_cambios:
    dump(tramites, open(archivo_pickle, 'wb'))
