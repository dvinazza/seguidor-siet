#!/usr/bin/python

from pickle import dump, load
from sys import exit

archivo_pickle = "tramites.pickle"

try:
    tramites = load(open(archivo_pickle, 'rb'))
    for t in tramites.keys():
        print "%s: %s" % (t, tramites[t])
except:
    print "No se pudo leer el archivo de tramites."
    tramites = {}


try:
    cuig = int(raw_input("cuig:"))
except ValueError:
    exit()

desc = raw_input("desc:")
mail = raw_input("mail:")

tramites.update({cuig: {'desc': desc, 'mail': mail, 'paso': ""}})
dump(tramites, open(archivo_pickle, 'wb'))
