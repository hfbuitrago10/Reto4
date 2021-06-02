﻿"""
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
import haversine as hs
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim as pm
from DISClib.Algorithms.Graphs import bellmanford as bf
assert cf

"""
Se define la estructura del analizador de conexiones
"""

# Construcción del modelo

def newAnalyzer():
    """
    Inicializa el analizador de conexiones
    """
    analyzer = {'connections': None,
                'cablesbylandingpoint': None,
                'connectedlandingpoints': None,
                'landingpointscoords': None,
                'landingpointsnames': None,
                'countries': None,
                'landingpointsbycountry': None,
                'sccomponents': None,
                'minimumcostpaths': None}
    
    analyzer['connections'] = gr.newGraph('ADJ_LIST',
                                           True,
                                           100000)
    
    analyzer['cablesbylandingpoint'] = mp.newMap()
    analyzer['connectedlandingpoints'] = mp.newMap()
    analyzer['landingpointscoords'] = mp.newMap()
    analyzer['landingpointsnames'] = mp.newMap()
    analyzer['countries'] = mp.newMap()
    analyzer['landingpointsbycountry'] = mp.newMap()

    return analyzer

# Funciones para agregar información al analizador

def addLandingPointConnection(analyzer, connection):
    """
    Adiciona los puntos de conexión como vértices del grafo, además
    crea un arco entre cada vértice adyacente con su distancia
    en kilometros como peso
    """
    origin = vertexOrigin(connection)
    destination = vertexDestination(connection)
    distance = haversineDistance(analyzer, connection)
    addLandingPoint(analyzer, origin)
    addLandingPoint(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
    addConnection(analyzer, destination, origin, distance)
    addCablesByLandingPoint(analyzer, connection, 'origin')
    addCablesByLandingPoint(analyzer, connection, 'destination')

def addLandingPoint(analyzer, landingpoint):
    """
    Adiciona un punto de conexión como vértice al grafo
    """
    graph = analyzer['connections']
    if not gr.containsVertex(graph, landingpoint):
        gr.insertVertex(graph, landingpoint)
    return analyzer

def addConnection(analyzer, origin, destination, weight):
    """
    Adiciona un arco entre dos vértices del grafo
    """
    graph = analyzer['connections']
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, weight)
    return analyzer

def addCablesByLandingPoint(analyzer, connection, landingpoint):
    """
    Adiciona un cable a la lista de cables de un punto de
    conexión específico
    """
    map = analyzer['cablesbylandingpoint']
    entry = mp.get(map, connection[landingpoint])
    if entry is None:
        lstcables = lt.newList('ARRAY_LIST')
        lt.addLast(lstcables, connection['cable_id'])
        mp.put(map, connection[landingpoint], lstcables)
    else:
        lstcables = entry['value']
        if not lt.isPresent(lstcables, connection['cable_id']):
            lt.addLast(lstcables, connection['cable_id'])
    return analyzer

def addConnectedLandingPoints(analyzer, connection):
    """
    Adiciona la lista de puntos de conexión conectados con un
    punto de conexión específico
    """
    map = analyzer['connectedlandingpoints']
    entry = mp.get(map, connection['origin'])
    if entry is None:
        lstconnections = lt.newList('ARRAY_LIST')
        lt.addLast(lstconnections, connection['destination'])
        mp.put(map, connection['origin'], lstconnections)
    else:
        lstconnections = entry['value']
        if not lt.isPresent(lstconnections, connection['destination']):
            lt.addLast(lstconnections, connection['destination'])
    return analyzer

def addLandingPointsCoords(analyzer, landingpoint):
    """
    Adiciona las coordenadas geográficas de un punto de
    conexión específico
    """
    map = analyzer['landingpointscoords']
    key = landingpoint['landing_point_id']
    latitude = float(landingpoint['latitude'])
    longitude = float(landingpoint['longitude'])
    name = str(landingpoint['name'])
    mp.put(map, key, (latitude, longitude, name))

def addLandingPointsNames(analyzer, landingpoint):
    """
    Adiciona el nombre de un punto de conexión
    específico
    """
    map = analyzer['landingpointsnames']
    name = str(landingpoint['name'])
    key = name.split(', ')[0]
    value = landingpoint['landing_point_id']
    mp.put(map, key, value)

def addLocalConnections(analyzer):
    """
    Adiciona un arco entre cada vértice de un punto de conexión
    específico
    """
    map = analyzer['cablesbylandingpoint']
    lstlandingpoints = mp.keySet(map)
    for landingpoint in lt.iterator(lstlandingpoints):
        entry = mp.get(map, landingpoint)
        lstcables = me.getValue(entry)
        fstcable =  None
        for cable in lt.iterator(lstcables):
            nxtcable = landingpoint + '-' + cable
            if fstcable is not None:
                addConnection(analyzer, fstcable, nxtcable, 0.10)
                addConnection(analyzer, nxtcable, fstcable, 0.10)
            fstcable = nxtcable

def addCountries(analyzer, country):
    """
    Adiciona la capital, la poblacion y el número de
    usuarios de cada país
    """
    map = analyzer['countries']
    key = str(country['CountryName'])
    capital = str(country['CapitalName'])
    population = float(country['Population'])
    users = float(country['Internet users'])
    mp.put(map, key, (capital, population, users))

def addLandingPointsByCountry(analyzer, country):
    """
    Adiciona los puntos de conexión de un país
    específico
    """
    map = analyzer['landingpointsbycountry']
    key = str(country['CountryName'])
    value = getLandingPointsByCountry(analyzer, key)
    mp.put(map, key, value)

def addCapitalLandingPoints(analyzer, country):
    """
    Adiciona los puntos de conexión de la capital de un país como
    vértices del grafo, además crea un arco entre cada vértice
    capital y los puntos de conexión de ese país
    """
    countries = analyzer['landingpointsbycountry']
    name = country['CountryName']
    lstlandingpoints = me.getValue(mp.get(countries, str(name)))
    for landingpoint in lt.iterator(lstlandingpoints):
        cables = analyzer['cablesbylandingpoint']
        lstcables = me.getValue(mp.get(cables, landingpoint))
        for cable in lt.iterator(lstcables):
            coords = analyzer['landingpointscoords']
            origin = str(country['CapitalName']) + '-' + cable
            destination = landingpoint + '-' + cable
            originlat = float(country['CapitalLatitude'])
            originlon = float(country['CapitalLongitude'])
            destlat = me.getValue(mp.get(coords, landingpoint))[0]
            destlon = me.getValue(mp.get(coords, landingpoint))[1]
            distance = hs.haversine((originlat, originlon), (destlat, destlon))
            if lt.isEmpty(lstcables) == False:
                addLandingPoint(analyzer, origin)
                addConnection(analyzer, origin, destination, distance)
                addConnection(analyzer, destination, origin, distance)

# Funciones para creación de datos

def vertexOrigin(connection):
    """
    Crea la estructura del vértice de
    origen
    """
    vertex = connection['origin'] + '-'
    vertex = vertex + connection['cable_id']
    return vertex

def vertexDestination(connection):
    """
    Crea la estructura del vértice de
    destino
    """
    vertex = connection['destination'] + '-'
    vertex = vertex + connection['cable_id']
    return vertex

def haversineDistance(analyzer, connection):
    """
    Calcula la distancia en kilometros entre dos puntos
    de conexión
    """
    map = analyzer['landingpointscoords']
    origin = connection['origin']
    destination = connection['destination']
    originlat = me.getValue(mp.get(map, origin))[0]
    originlon = me.getValue(mp.get(map, origin))[1]
    destlat = me.getValue(mp.get(map, destination))[0]
    destlon = me.getValue(mp.get(map, destination))[1]
    distance = hs.haversine((originlat, originlon), (destlat, destlon))
    return distance

# Funciones de consulta

def getLandingPoint(analyzer, landingpointname):
    """
    Retorna el identificador de un punto de conexión
    específico
    """
    map = analyzer['landingpointsnames']
    landingpoint = me.getValue(mp.get(map, landingpointname))
    return landingpoint

def getVertexByLandingPoint(analyzer, landingpoint):
    """
    Retorna un vértice de un punto de conexión
    específico
    """
    map = analyzer['cablesbylandingpoint']
    lstcables = me.getValue(mp.get(map, landingpoint))
    cable = lt.firstElement(lstcables)
    vertex = landingpoint + '-' + cable
    return vertex

def getCountryByLandingPoint(analyzer, landingpoint):
    """
    Retorna el país de un punto de conexión
    específico
    """
    map = analyzer['landingpointscoords']
    location = me.getValue(mp.get(map, landingpoint))[2]
    lstlocation = location.split(', ')
    if len(lstlocation) == 3:
        country = lstlocation[2]
    else:
        country = lstlocation[1]
    return country

def getCapitalByCountry(analyzer, country):
    """
    Retorna la capital de un país específico
    """
    map = analyzer['countries']
    capital = me.getValue(mp.get(map, country))[0]
    return capital

def getCapitalVertexByCountry(analyzer, country):
    """
    Retorna un vértice del punto de conexión de la capital
    de un país específico
    """
    map = analyzer['landingpointsbycountry']
    lstlandingpoints = me.getValue(mp.get(map, country))
    landingpoint = lt.firstElement(lstlandingpoints)
    cables = analyzer['cablesbylandingpoint']
    lstcables = me.getValue(mp.get(cables, landingpoint))
    cable = lt.firstElement(lstcables)
    capital = getCapitalByCountry(analyzer, country)
    vertex = capital + '-' + cable
    return vertex

def getHarvesineDistance(analyzer, origin, destination):
    """
    Retorna la distancia en kilometros entre dos puntos
    de conexión
    """
    map = analyzer['landingpointscoords']
    originlat = me.getValue(mp.get(map, origin))[0]
    originlon = me.getValue(mp.get(map, origin))[1]
    destlat = me.getValue(mp.get(map, destination))[0]
    destlon = me.getValue(mp.get(map, destination))[1]
    distance = hs.haversine((originlat, originlon), (destlat, destlon))
    return distance

def getLandingPointsByCountry(analyzer, country):
    """
    Retorna una lista con los puntos de conexión de un país
    específico
    """
    map = analyzer['landingpointscoords']
    lstlandingpoints = mp.keySet(map)
    lstlandingsbycountry = lt.newList('ARRAY_LIST')
    for landingpoint in lt.iterator(lstlandingpoints):
        entry = mp.get(map, landingpoint)
        value = me.getValue(entry)[2]
        if country in value:
            lt.addLast(lstlandingsbycountry, landingpoint)
    return lstlandingsbycountry

def stronglyConnectedComponents(analyzer):
    """
    Retorna el número de componentes fuertemente
    conectados del grafo
    """
    graph = analyzer['connections']
    analyzer['sccomponents'] = scc.KosarajuSCC(graph)
    return scc.connectedComponents(analyzer['sccomponents'])

def stronglyConnectedVertexs(analyzer, vertexa, vertexb):
    """
    Retorna si dos vértices están fuertemente
    conectados o no
    """
    sccomponents = analyzer['sccomponents']
    return scc.stronglyConnected(sccomponents, vertexa, vertexb)

def mostConnectedLandingPoint(analyzer):
    """
    Retorna el punto de conexión con mayor número de
    cables conectados
    """
    map = analyzer['cablesbylandingpoint']
    lstlandingpoints = mp.keySet(map)
    maxlandingpoint = None
    maxconnections = 0
    for landingpoint in lt.iterator(lstlandingpoints):
        entry = mp.get(map, landingpoint)
        lstcables = me.getValue(entry)
        connections = lt.size(lstcables)
        if connections > maxconnections:
            maxlandingpoint = landingpoint
            maxconnections = connections
    return maxlandingpoint, maxconnections

def minimumCostPaths(analyzer, vertexa):
    """
    Retorna los caminos de costo mínimo desde un punto de conexión
    inicial a todos los demás puntos de conexión
    """
    graph = analyzer['connections']
    analyzer['minimumcostpaths'] = djk.Dijkstra(graph, vertexa)
    return analyzer

def hasPathTo(analyzer, vertexb):
    """
    Retorna si existe un camino entre el punto de conexión
    inicial y un punto de conexión específico
    """
    paths = analyzer['minimumcostpaths']
    return djk.hasPathTo(paths, vertexb)

def minimumCostPath(analyzer, vertexb):
    """
    Retorna el camino de costo mínimo entre el punto de conexión
    inicial y un punto de conexión específico
    """
    paths = analyzer['minimumcostpaths']
    return djk.pathTo(paths, vertexb)

def getConnectedCountries(analyzer, landingpoint):
    """
    Retorna un árbol tipo 'RBT' de paises conectados a un
    punto de conexión específico
    """
    map = analyzer['connectedlandingpoints']
    ordmap = om.newMap('RBT', compareValuesDescOrder)
    lstlandingpoints = me.getValue(mp.get(map, landingpoint))
    for connection in lt.iterator(lstlandingpoints):
        country = getCountryByLandingPoint(analyzer, connection)
        distance = getHarvesineDistance(analyzer, landingpoint, connection)
        om.put(ordmap, distance, country)
    return ordmap

# Funciones de comparación

def compareValuesDescOrder(value1, value2):
    """
    Compara los valores de una característica
    de dos eventos en orden descendente
    """
    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return -1
    else:
        return 1