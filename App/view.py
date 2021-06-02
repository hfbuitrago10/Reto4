"""
 * Copyright 2021, Departamento de Sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program. If not, see <http://www.gnu.org/licenses/>.
"""

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import stack as st
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
assert cf

sys.setrecursionlimit(1000000*10)

"""
La vista se encarga de la interacción con el usuario
"""

# Funciones para la impresión de resultados

def printFirstLandingPoint(analyzer):
    """
    Imprime la información del primer punto de conexión
    cargado
    """
    map = analyzer['landingpointscoords']
    lstlandingpoints = mp.keySet(map)
    key = lt.firstElement(lstlandingpoints)
    value = me.getValue(mp.get(map, key))
    print("---------- Primer punto de conexión cargado ----------")
    print("Nombre: " + str(value[2]) + "  Identificador: " + str(key) + "  Latitud: " + str(value[0]) +
    "  Longitud: " + str(value[1]) + "\n")

def printLastCountry(analyzer):
    """
    Imprime la información del último país cargado
    """
    map = analyzer['countries']
    lstcountries = mp.keySet(map)
    key = lt.lastElement(lstcountries)
    value = me.getValue(mp.get(map, key))
    print("---------- Último país cargado ----------")
    print("País: " + str(key) + "  Población: " + str(value[1]) + "  Usuarios: " + str(value[2]) + "\n")

def printStronglyConnectedVertexs(analyzer, vertexa, vertexb):
    """
    Imprime si dos vértices están fuertemente
    conectados
    """
    scvertexs = controller.stronglyConnectedVertexs(analyzer, vertexa, vertexb)
    if scvertexs == True:
        print("Los puntos de conexión " + str(vertexa) + " y " + str(vertexb) + " se encuntran en" +
        " el mismo cluster de conexiones\n")
    else:
        print("Los puntos de conexión " + str(vertexa) + " y " + str(vertexb) + " no se encuntran en" +
        " el mismo cluster de conexiones\n")

def printMostConnectedLandingPoint(analyzer, landingpoint, cables):
    """
    Imprime el punto de conexión con mayor número de cables
    conectados
    """
    map = analyzer['landingpointscoords']
    key = landingpoint
    value = me.getValue(mp.get(map, key))
    print("---------- Punto de conexión crítico ----------")
    print("Nombre: " + str(value[2].split(', ')[0]) + "  País: " + str(value[2].split(', ')[1]) +
    "  Identificador: " + str(landingpoint))
    print("Total cables conectados: " + str(cables) + "\n")

def printMinimumCostPath(analyzer, vertexb):
    """
    Imprime el camino de costo mínimo entre un punto de conexión
    inicial y un punto de conexión específico
    """
    haspath = controller.hasPathTo(analyzer, vertexb)
    if haspath == True:
        minimuncostpath = controller.minimumCostPath(analyzer, vertexb)
        distance = 0
        size = lt.size(minimuncostpath)
        index = 1
        print("\n---------- Camino de costo mínimo ----------")
        while index <= size:
            connection = lt.getElement(minimuncostpath, index)
            print("\n---------- Conexión " + str(index) + "----------")
            print("Origen: " + str(connection['vertexA']) + "\nDestino: " + str(connection['vertexB']) +
            "\nDistancia: " + str(connection['weight']) + " km")
            distance += connection['weight']
            index += 1
        print("\nTotal distancia: " + str(distance) + " km")
        print()
    else:
        print("\nNo existe camino entre los puntos de conexión")
        print()

def printConnectedCountries(analyzer, landingpoint):
    """
    Imprime los países conectados a un punto de conexión
    específico en orden descendente de distancia
    """
    ordmap = controller.getConnectedCountries(analyzer, landingpoint)
    keys = om.keySet(ordmap)
    values = om.valueSet(ordmap)
    size = om.size(ordmap)
    index = 1
    print("\n---------- Países afectados ----------")
    while index <= size:
        country = lt.getElement(values, index)
        distance = lt.getElement(keys, index)
        print(str(index) + ". " + str(country) + "  Distancia: " + str(distance) + " km")
        index += 1
    print()
    print("Total países afectados: " + str(size) + "\n")

# Menú de opciones

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información de las conexiones")
    print("3- Consultar clusters de conexión")
    print("4- Consultar puntos de conexión críticos")
    print("5- Consultar ruta mínima entre dos países")
    print("6- Consultar red de expansión mínima")
    print("7- Consultar falla en punto de conexión")
    print("8- Consultar red con máximo ancho de banda")
    print("9- Consultar ruta mínima entre dos direcciones IP")
    print("0- Salir")

# Funciones de inicialización

def initAnalyzer():
    """
    Inicializa el analizador de conexiones
    """
    return controller.initAnalyzer()

def loadData(analyzer):
    """
    Carga la información de las conexiones al analizador
    """
    return controller.loadData(analyzer)

analyzer = None

"""
Menú principal
"""
while True:
    printMenu()
    inputs = input("Seleccione una opción para continuar\n")
    if int(inputs[0]) == 1:
        print()
        print("Inicializando....\n")
        analyzer = initAnalyzer()

    elif int(inputs[0]) == 2:
        print()
        print("Cargando información de las conexiones....\n")
        data = loadData(analyzer)
        print("Total puntos de conexión: " + str(gr.numVertices(analyzer['connections'])))
        print("Total conexiones: " + str(gr.numEdges(analyzer['connections'])))
        print("Total países: " + str(mp.size(analyzer['countries']))+ "\n")
        printFirstLandingPoint(analyzer)
        printLastCountry(analyzer)
    
    elif int(inputs[0]) == 3:
        print()
        vertexa = str(input("Ingrese punto de conexión: "))
        vertexb = str(input("Ingrese punto de conexión: "))
        print("\n---------- Clusters de conexión ----------")
        print("Total clusters: " + str(controller.stronglyConnectedComponents(analyzer)))
        printStronglyConnectedVertexs(analyzer, vertexa, vertexb)

    elif int(inputs[0]) == 4:
        print()
        landingpoint = controller.mostConnectedLandingPoint(analyzer)[0]
        cables = controller.mostConnectedLandingPoint(analyzer)[1]
        printMostConnectedLandingPoint(analyzer, landingpoint, cables)

    elif int(inputs[0]) == 5:
        print()
        vertexa = str(input("Ingrese punto de conexión: "))
        vertexb = str(input("Ingrese punto de conexión: "))
        controller.minimumCostPaths(analyzer, vertexa)
        printMinimumCostPath(analyzer, vertexb)

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        print()
        landingpointname = str(input("Ingrese punto de conexión: "))
        landingpoint = controller.getLandingPoint(analyzer, landingpointname)
        printConnectedCountries(analyzer, landingpoint)

    elif int(inputs[0]) == 8:
        pass

    elif int(inputs[0]) == 9:
        pass

    else:
        sys.exit(0)
sys.exit(0)