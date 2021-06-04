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
import folium
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
    cargado al analizador
    """
    map = analyzer['landingpointscoords']
    lstlandingpoints = mp.keySet(map)
    key = lt.firstElement(lstlandingpoints)
    value = me.getValue(mp.get(map, key))
    print("---------- Primer punto de conexión cargado ----------")
    print("Nombre: " + str(value[2].split(', ')[0]) + "  Identificador: " + str(key) + "  Latitud: " +
    str(value[0]) + "  Longitud: " + str(value[1]) + "\n")

def printLastCountry(analyzer):
    """
    Imprime la información del último país cargado al
    analizador
    """
    map = analyzer['countries']
    lstcountries = mp.keySet(map)
    key = lt.lastElement(lstcountries)
    value = me.getValue(mp.get(map, key))
    print("---------- Último país cargado ----------")
    print("País: " + str(key) + "  Población: " + str(value[1]) + "  Usuarios: " + str(value[2]) + "\n")

def printStronglyConnectedLandingPoints(scvertexs, landingpointnamea, landingpointnameb):
    """
    Imprime si dos puntos de conexión están en el mismo componente
    fuertemente conectado o no
    """
    if scvertexs == True:
        print("Los puntos " + str(landingpointnamea) + " y " + str(landingpointnameb) + " están en el" +
        " mismo cluster? Sí")
    else:
        print("Los puntos " + str(landingpointnamea) + " y " + str(landingpointnameb) + " están en el" +
        " mismo cluster? No")

def printMostConnectedLandingPoint(analyzer):
    """
    Imprime el punto de conexión con mayor número de
    conexiones
    """
    ordmap = controller.mostConnectedLandingPoint(analyzer)
    keys = om.keySet(ordmap)
    index = 1
    print("---------- Puntos de conexión críticos ----------")
    while index <= 5:
        key = lt.getElement(keys, index)
        value = me.getValue(om.get(ordmap, key))
        name = value.split('-')[0]
        country = value.split('-')[1]
        print(str(index) + ". Nombre: " + str(name) + "  País: " + str(country) + "  Identificador: " +
        str(value))
        print("   Total cables conectados: " + str(key))
        index += 1
    print()

def printMinimumCostPath(analyzer, vertexb):
    """
    Imprime la ruta de costo mínimo entre un punto de conexión
    origen y un punto de conexión destino
    """
    haspath = controller.hasPathTo(analyzer, vertexb)
    if haspath == True:
        minimuncostpath = controller.minimumCostPath(analyzer, vertexb)
        distance = 0
        size = lt.size(minimuncostpath)
        index = 1
        print("\n---------- Ruta de costo mínimo ----------\n")
        while index <= size:
            connection = lt.getElement(minimuncostpath, index)
            print("---------- Conexión " + str(index) + "----------")
            print("Origen: " + str(connection['vertexA']) + "\nDestino: " + str(connection['vertexB']) +
            "\nDistancia: " + str(connection['weight']) + " km\n")
            distance += connection['weight']
            index += 1
        print("Total distancia: " + str(distance) + " km\n")
    else:
        print("No existe ruta entre los puntos de conexión\n")

def printConnectedCountries(analyzer, landingpoint):
    """
    Imprime los países conectados a un punto de conexión específico
    en orden descendente por distancia en km
    """
    ordmap = controller.getConnectedCountries(analyzer, landingpoint)
    lstcountries = lt.newList('ARRAY_LIST')
    keys = om.keySet(ordmap)
    values = om.valueSet(ordmap)
    size = om.size(ordmap)
    index = 1
    count = 1
    print("\n---------- Países afectados ----------")
    while index <= size:
        country = lt.getElement(values, index)
        distance = lt.getElement(keys, index)
        if not lt.isPresent(lstcountries, country):
            print(str(count) + ". " + str(country) + "  Distancia: " + str(distance) + " km")
            lt.addLast(lstcountries, country)
            index += 1
            count += 1
        else:
            index += 1
    print()
    print("Total países afectados: " + str(lt.size(lstcountries)) + "\n")

def printMaximumBandwidthByCountry(analyzer, countrya, cable):
    """
    Imprime los países conectados a un cable específico con su máximo
    ancho de banda en mbps
    """
    map = controller.maximumBandwidthByCountry(analyzer, cable)
    lstcountries = mp.keySet(map)
    print("\n---------- Países conectados a " + str(cable) + " ----------")
    for country in lt.iterator(lstcountries):
        if country is not None and country != countrya:
            entry = mp.get(map, country)
            maxbandwidth = me.getValue(entry)
            print("País: " + str(country) + "   Máximo ancho de banda: " + str(f"{maxbandwidth:.3f}") +
            " mbps")
    print()

def printMinimumJumpsPath(analyzer, vertexb):
    """
    Imprime la ruta de saltos mínima entre un punto de conexión
    origen y un punto de conexión destino
    """
    haspath = controller.hasJumpsPathTo(analyzer, vertexb)
    if haspath == True:
        minimumjumpspath = controller.minimumJumpsPath(analyzer, vertexb)
        size = lt.size(minimumjumpspath)
        index = 1
        print("\n---------- Ruta de saltos mínima ----------")
        while index <= size:
            jump = lt.getElement(minimumjumpspath, index)
            print(str(index) + ". " + str(jump))
            index += 1
        print("\nTotal saltos: " + str(size + 1) + "\n")
    else:
        print("\nNo existe ruta entre los puntos de conexión\n")

# Funciones para la creación de mapas

def plotStronglyConnectedComponentsMap(analyzer, vertexa, vertexb, namea, nameb):
    """
    Crea un mapa html de los componentes fuertemente
    conectados del grafo
    """
    vertexacoords = controller.getVertexCoordinates(analyzer, vertexa)
    vertexbcoords = controller.getVertexCoordinates(analyzer, vertexb)
    lstcomponenta = controller.getStronglyConnectedComponent(analyzer, 1)
    lstcomponentb = controller.getStronglyConnectedComponent(analyzer, 2)
    lstcoordinatesa = controller.getVertexsCoordinates(analyzer, lstcomponenta)
    lstcoordinatesb = controller.getVertexsCoordinates(analyzer, lstcomponentb)
    map = folium.Map()
    folium.PolyLine(lstcoordinatesa['elements'], color="green", weight=2.5, opacity=0.35).add_to(map)
    folium.PolyLine(lstcoordinatesb['elements'], color="blue", weight=2.5, opacity=0.35).add_to(map)
    folium.Marker(vertexacoords, str(namea)).add_to(map)
    folium.Marker(vertexbcoords, str(nameb)).add_to(map)
    map.save("map1.html")

def plotMostConnectedLandingPointMap(analyzer):
    """
    Crea un mapa html del punto de conexión con mayor número
    de cables conectados
    """
    ordmap = controller.mostConnectedLandingPoint(analyzer)
    key = om.minKey(ordmap)
    vertex = me.getValue(om.get(ordmap, key))
    city = vertex.split('-')[0]
    country = vertex.split('-')[1]
    vertexcoords = me.getValue(mp.get(analyzer['vertexscoords'], vertex))
    lstvertexs = controller.getAdjacentVertexs(analyzer, vertex)
    lstcoordinates = controller.getVertexsCoordinates(analyzer, lstvertexs)
    map = folium.Map(vertexcoords)
    folium.Marker(vertexcoords, str(city)).add_to(map)
    for location in lt.iterator(lstcoordinates):
        folium.Marker(location).add_to(map)
        folium.PolyLine([vertexcoords, location], color="blue", weight=2.5, opacity=0.35).add_to(map)
    map.save("map2.html")

def plotMinimumCostPathMap(analyzer, vertexb):
    """
    Crea un mapa html de la ruta de costo mínimo entre dos
    puntos de conexión
    """
    lstvertexs = controller.getMinimumCostPathVertexs(analyzer, vertexb)
    lstcoordinates = controller.getPathCoordinates(analyzer, lstvertexs)
    map = folium.Map()
    for location in lt.iterator(lstcoordinates):
        folium.Marker(location).add_to(map)
        folium.PolyLine(lstcoordinates['elements'], color="blue", weight=2.5, opacity=0.35).add_to(map)
    map.save("map3.html")

def plotConnectedCountriesMap(analyzer, landingpoint, landingpointname):
    """
    Crea un mapa html de los países conectados a un punto 
    de conexión
    """
    origincoords = controller.getLandingPointCoordinates(analyzer, landingpoint)
    lstlandingpoints = controller.getConnectedLandingPoints(analyzer, landingpoint)
    lstcoordinates = controller.getLandingPointsCoordinates(analyzer, lstlandingpoints)
    map = folium.Map(origincoords)
    folium.Marker(origincoords, str(landingpointname)).add_to(map)
    for location in lt.iterator(lstcoordinates):
        folium.Marker(location).add_to(map)
        folium.PolyLine([origincoords, location], color="blue", weight=2.5, opacity=0.35).add_to(map)
    map.save("map5.html")

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
        landingpointnamea = str(input("Ingrese punto de conexión: "))
        landingpointnameb = str(input("Ingrese punto de conexión: "))
        landingpointa = controller.getLandingPoint(analyzer, landingpointnamea)
        landingpointb = controller.getLandingPoint(analyzer, landingpointnameb)
        vertexa = controller.getVertexByLandingPoint(analyzer, landingpointa)
        vertexb = controller.getVertexByLandingPoint(analyzer, landingpointb)
        sccomponents = controller.stronglyConnectedComponents(analyzer)
        scvertexs = controller.stronglyConnectedVertexs(analyzer, vertexa, vertexb)
        print("\n---------- Clusters de conexión ----------")
        printStronglyConnectedLandingPoints(scvertexs, landingpointnamea, landingpointnameb)
        print("Total clusters: " + str(sccomponents) + "\n")
        plotStronglyConnectedComponentsMap(analyzer, vertexa, vertexb, landingpointnamea, landingpointnameb)

    elif int(inputs[0]) == 4:
        print()
        printMostConnectedLandingPoint(analyzer)
        plotMostConnectedLandingPointMap(analyzer)

    elif int(inputs[0]) == 5:
        print()
        countrya = str(input("Ingrese país: "))
        countryb = str(input("Ingrese país: "))
        vertexa = controller.getCapitalVertexByCountry(analyzer, countrya)
        vertexb = controller.getCapitalVertexByCountry(analyzer, countryb)
        controller.minimumCostPaths(analyzer, vertexa)
        printMinimumCostPath(analyzer, vertexb)
        plotMinimumCostPathMap(analyzer, vertexb)

    elif int(inputs[0]) == 6:
        controller.minimumSpanningTrees(analyzer)
        minspanningtree = controller.minimumSpanningTree(analyzer)
        print("\n---------- Red de expansión mínima ----------")
        print("Total nodos conectados: " + str(minspanningtree[0]))
        print("Costo total: " + str(minspanningtree[1]) + " km\n")

    elif int(inputs[0]) == 7:
        print()
        landingpointname = str(input("Ingrese punto de conexión: "))
        landingpoint = controller.getLandingPoint(analyzer, landingpointname)
        printConnectedCountries(analyzer, landingpoint)
        plotConnectedCountriesMap(analyzer, landingpoint, landingpointname)

    elif int(inputs[0]) == 8:
        print()
        countrya = str(input("Ingrese país: "))
        cable = str(input("Ingrese cable: "))
        printMaximumBandwidthByCountry(analyzer, countrya, cable)

    elif int(inputs[0]) == 9:
        print()
        ipaddressa = str(input("Ingrese dirección IP: "))
        ipaddressb = str(input("Ingrese dirección IP: "))
        coordinatesa = controller.getCoordinatesByIPAddress(ipaddressa)
        coordinatesb = controller.getCoordinatesByIPAddress(ipaddressb)
        clstlandingpointa = controller.getClosestLandingPoint(analyzer, coordinatesa)[0]
        clstlandingpointb = controller.getClosestLandingPoint(analyzer, coordinatesb)[0]
        vertexa = controller.getVertexByLandingPoint(analyzer, clstlandingpointa)
        vertexb = controller.getVertexByLandingPoint(analyzer, clstlandingpointb)
        controller.minimumJumpsPaths(analyzer, vertexa)
        printMinimumJumpsPath(analyzer, vertexb)

    else:
        sys.exit(0)
sys.exit(0)