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
from geoip import geolite2 as geo
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim as pm
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
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
                'landingpointsbycable': None,
                'bandwidthbycable': None,
                'landingpointscoords': None,
                'landingpointsnames': None,
                'countries': None,
                'landingpointsbycountry': None,
                'vertexscoords': None,
                'sccomponents': None,
                'minimumcostpaths': None,
                'minimumspanningtrees': None,
                'minimumjumpspaths': None}
    
    analyzer['connections'] = gr.newGraph('ADJ_LIST',
                                           False,
                                           100000)
    
    analyzer['cablesbylandingpoint'] = mp.newMap(maptype='PROBING')
    analyzer['connectedlandingpoints'] = mp.newMap(maptype='PROBING')
    analyzer['landingpointsbycable'] = mp.newMap(maptype='PROBING')
    analyzer['bandwidthbycable'] = mp.newMap(maptype='PROBING')
    analyzer['landingpointscoords'] = mp.newMap(maptype='PROBING')
    analyzer['landingpointsnames'] = mp.newMap(maptype='PROBING')
    analyzer['countries'] = mp.newMap(maptype='PROBING')
    analyzer['landingpointsbycountry'] = mp.newMap(maptype='PROBING')
    analyzer['vertexscoords'] = mp.newMap(maptype='PROBING')

    return analyzer

# Funciones para agregar información al analizador

def addLandingPointConnection(analyzer, connection):
    """
    Adiciona los puntos de conexión como vértices del grafo, adicionalmente
    crea un arco entre cada vértice adyacente con su distancia en km
    como peso del arco
    """
    origin = vertexOrigin(connection)
    destination = vertexDestination(connection)
    distance = haversineDistance(analyzer, connection)
    addLandingPoint(analyzer, origin)
    addVertexsCoords(analyzer, origin)
    addLandingPoint(analyzer, destination)
    addVertexsCoords(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
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
    Adiciona un punto de conexión a la lista de puntos de conexión
    conectados con un punto de conexión específico
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

def addLandingPointsByCable(analyzer, connection):
    """
    Adiciona un punto de conexión a la lista de puntos de conexión
    conectados por un cable específico
    """
    map = analyzer['landingpointsbycable']
    entry = mp.get(map, connection['cable_id'])
    if entry is None:
        lstlandingpoints = lt.newList('ARRAY_LIST')
        lt.addLast(lstlandingpoints, connection['origin'])
        mp.put(map, connection['cable_id'], lstlandingpoints)
    else:
        lstlandingpoints = entry['value']
        if not lt.isPresent(lstlandingpoints, connection['origin']):
            lt.addLast(lstlandingpoints, connection['origin'])
    return analyzer

def addBandwidthByCable(analyzer, connection):
    """
    Adiciona la capacidad de transferencia en tbps de
    cada cable
    """
    map = analyzer['bandwidthbycable']
    entry = mp.get(map, connection['cable_id'])
    if entry is None:
        lstbandwidth = lt.newList('ARRAY_LIST')
        lt.addLast(lstbandwidth, float(connection['capacityTBPS']))
        mp.put(map, connection['cable_id'], lstbandwidth)
    else:
        lstbandwidth = entry['value']
        if not lt.isPresent(lstbandwidth, float(connection['capacityTBPS'])):
            lt.addLast(lstbandwidth, float(connection['capacityTBPS']))
    return analyzer

def addLandingPointsCoords(analyzer, landingpoint):
    """
    Adiciona las coordenadas geográficas y el nombre de un punto
    de conexión específico
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
            fstcable = nxtcable

def addCountries(analyzer, country):
    """
    Adiciona la capital, la poblacion y el número de
    usuarios de internet de cada país
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
    Adiciona el punto de conexión de la capital de un país como vértice del
    grafo, adicionalmente crea un arco entre el vértice capital y los
    puntos de conexión de dicho país
    """
    countries = analyzer['landingpointsbycountry']
    coords = analyzer['landingpointscoords']
    name = country['CountryName']
    lstlandingpoints = me.getValue(mp.get(countries, str(name)))
    origin = str(country['CapitalName']) + '-' + name
    originlat = float(country['CapitalLatitude'])
    originlon = float(country['CapitalLongitude'])
    origincoords = originlat, originlon
    if lt.isEmpty(lstlandingpoints) == False:
        for landingpoint in lt.iterator(lstlandingpoints):
            cables = analyzer['cablesbylandingpoint']
            lstcables = me.getValue(mp.get(cables, landingpoint))
            for cable in lt.iterator(lstcables):
                destination = landingpoint + '-' + cable
                destlat = me.getValue(mp.get(coords, landingpoint))[0]
                destlon = me.getValue(mp.get(coords, landingpoint))[1]
                distance = hs.haversine((originlat, originlon), (destlat, destlon))
                addLandingPoint(analyzer, origin)
                addCapitalVertexsCoords(analyzer, origin, origincoords)
                addConnection(analyzer, origin, destination, distance)
    else:
        closestlandingpoint = getClosestLandingPoint(analyzer, origincoords)[0]
        destination = getVertexByLandingPoint(analyzer, closestlandingpoint)
        distance = getClosestLandingPoint(analyzer, origincoords)[1]
        addLandingPoint(analyzer, origin)
        addCapitalVertexsCoords(analyzer, origin, origincoords)
        addConnection(analyzer, origin, destination, distance)

def addVertexsCoords(analyzer, vertex):
    """
    Adiciona las coordenadas geográficas de un
    vértice específico
    """
    map = analyzer['vertexscoords']
    coords = analyzer['landingpointscoords']
    landingpoint = vertex.split('-')[0]
    latitude = me.getValue(mp.get(coords, landingpoint))[0]
    longitude = me.getValue(mp.get(coords, landingpoint))[1]
    mp.put(map, vertex, (latitude, longitude))

def addCapitalVertexsCoords(analyzer, vertex, coordinates):
    """
    Adiciona las coordenadas geográficas de un
    vértice capital específico
    """
    map = analyzer['vertexscoords']
    mp.put(map, vertex, coordinates)

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
    Calcula la distancia en km entre dos puntos
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

def getLandingPointName(analyzer, landingpoint):
    """
    Retorna el nombre de un punto de conexión
    específico
    """
    map = analyzer['landingpointscoords']
    landingpointname = me.getValue(mp.get(map, landingpoint))[2]
    return landingpointname

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
    Retorna el vértice del punto de conexión de la capital
    de un país específico
    """
    capital = getCapitalByCountry(analyzer, country)
    vertex = capital + '-' + country
    return vertex

def getHarvesineDistance(analyzer, origin, destination):
    """
    Retorna la distancia en km entre dos puntos
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

def getLandingPointCoordinates(analyzer, landingpoint):
    """
    Retorna las coordenadas geográficas de un punto
    de conexión específico
    """
    map = analyzer['landingpointscoords']
    latitude = me.getValue(mp.get(map, landingpoint))[0]
    longitude = me.getValue(mp.get(map, landingpoint))[1]
    coordinates = latitude, longitude
    return coordinates

def getLandingPointsCoordinates(analyzer, lstlandingpoints):
    """
    Retorna una lista con las coordenadas geográficas de cada
    punto de conexión de una lista
    """
    map = analyzer['landingpointscoords']
    lstcoordinates = lt.newList('ARRAY_LIST')
    for landingpoint in lt.iterator(lstlandingpoints):
        latitude = me.getValue(mp.get(map, landingpoint))[0]
        longitude = me.getValue(mp.get(map, landingpoint))[1]
        lt.addLast(lstcoordinates, (latitude, longitude))
    return lstcoordinates

def getVertexCoordinates(analyzer, vertex):
    """
    Retorna las coordenadas geográficas de
    un vértice específico
    """
    map = analyzer['vertexscoords']
    coordinates = me.getValue(mp.get(map, vertex))
    return coordinates

def getAdjacentVertexs(analyzer, vertex):
    """
    Retorna una lista con los vértices adyacentes a
    un vértice específico
    """
    graph = analyzer['connections']
    lstadjacents = gr.adjacents(graph, vertex)
    return lstadjacents

def getVertexsCoordinates(analyzer, lstadjacents):
    """
    Retorna una lista con las coordenadas geográficas de
    cada vértice de una lista
    """
    map = analyzer['vertexscoords']
    lstcoordinates = lt.newList('ARRAY_LIST')
    for vertex in lt.iterator(lstadjacents):
        coordinates = me.getValue(mp.get(map, vertex))
        lt.addLast(lstcoordinates, coordinates)
    return lstcoordinates

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

def getStronglyConnectedComponent(analyzer, component):
    """
    Retorna la lista de vértices de un componente
    fuertemente conectado
    """
    sscomponents = analyzer['sccomponents']['idscc']
    lstvertexs = mp.keySet(sscomponents)
    lstvertexsbycomponent = lt.newList('ARRAY_LIST')
    for vertex in lt.iterator(lstvertexs):
        value = me.getValue(mp.get(sscomponents, vertex))
        if value == component:
            lt.addLast(lstvertexsbycomponent, vertex)
    return lstvertexsbycomponent

def mostConnectedLandingPoint(analyzer):
    """
    Retorna un árbol tipo 'RBT' con los puntos de conexión
    con mayor número de conexiones
    """
    graph = analyzer['connections']
    map = analyzer['vertexscoords']
    ordmap = om.newMap('RBT', compareValuesDescOrder)
    lstvertexs = mp.keySet(map)
    for vertex in lt.iterator(lstvertexs):
        lstconnections = gr.adjacents(graph, vertex)
        connections = lt.size(lstconnections)
        om.put(ordmap, connections, vertex)
    return ordmap

def minimumCostPaths(analyzer, vertexa):
    """
    Retorna las rutas de costo mínimo desde un punto de conexión
    inicial a todos los demás puntos de conexión
    """
    graph = analyzer['connections']
    analyzer['minimumcostpaths'] = djk.Dijkstra(graph, vertexa)
    return analyzer

def hasPathTo(analyzer, vertexb):
    """
    Retorna si existe una ruta entre el punto de conexión
    inicial y un punto de conexión destino
    """
    paths = analyzer['minimumcostpaths']
    return djk.hasPathTo(paths, vertexb)

def minimumCostPath(analyzer, vertexb):
    """
    Retorna la ruta de costo mínimo entre el punto de conexión
    inicial y un punto de conexión destino
    """
    paths = analyzer['minimumcostpaths']
    return djk.pathTo(paths, vertexb)

def getMinimumCostPathVertexs(analyzer, vertexb):
    """
    Retorna una lista con los vértices de la ruta de costo
    mínimo entre dos puntos de conexión
    """
    map = analyzer['vertexscoords']
    lstvertexs = lt.newList('ARRAY_LIST')
    haspath = hasPathTo(analyzer, vertexb)
    if haspath == True:
        minimuncostpath = minimumCostPath(analyzer, vertexb)
        size = lt.size(minimuncostpath)
        index = 1
        while index <= size:
            connection = lt.getElement(minimuncostpath, index)
            vertex = connection['vertexA']
            if not lt.isPresent(lstvertexs, vertex):
                lt.addLast(lstvertexs, vertex)
            index += 1
        lt.addLast(lstvertexs, vertexb)
    return lstvertexs

def minimumSpanningTrees(analyzer):
    """
    Retorna el árbol de expansión mínima
    del grafo
    """
    graph = analyzer['connections']
    analyzer['minimumspanningtrees'] = pm.PrimMST(graph)
    return analyzer

def minimumSpanningTree(analyzer):
    """
    Retorna el número de vértices y el costo del árbol
    de expansión mínima
    """
    map = analyzer['minimumspanningtrees']['distTo']
    lstvertexs = mp.keySet(map)
    distance = 0
    vertexsize = 0
    for vertex in lt.iterator(lstvertexs):
        weight = me.getValue(mp.get(map, vertex))
        if vertex is not None:
            distance += weight
            vertexsize += 1
    return vertexsize, distance

def getLongestConnection(analyzer):
    """
    Retorna la conexión con mayor distancia en km del
    árbol de expansión mínima
    """
    lstconnections = analyzer['minimumspanningtrees']['edgeTo']['table']
    longestconnection = None
    maxdistance = 0
    for connection in lt.iterator(lstconnections):
        if connection['key'] is not None:
            distance = connection['value']['weight']
            if distance > maxdistance:
                longestconnection = connection['value']
                maxdistance = distance
    return longestconnection

def getShortestConnection(analyzer):
    """
    Retorna la conexión con menor distancia en km del
    árbol de expansión mínima
    """
    lstconnections = analyzer['minimumspanningtrees']['edgeTo']['table']
    shortestconnection = None
    mindistance = 1000000
    for connection in lt.iterator(lstconnections):
        if connection['key'] is not None:
            distance = connection['value']['weight']
            if mindistance > distance:
                shortestconnection = connection['value']
                mindistance = distance
    return shortestconnection

def getConnectedCountries(analyzer, landingpoint):
    """
    Retorna un árbol tipo 'RBT' con los países conectados a un
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

def getConnectedLandingPoints(analyzer, landingpoint):
    """
    Retorna una lista de los puntos de conexión conectados a
    un punto de conexión específico
    """
    map = analyzer['connectedlandingpoints']
    lstlandingpoints = me.getValue(mp.get(map, landingpoint))
    return lstlandingpoints

def getCountriesByCable(analyzer, cable):
    """
    Retorna la lista de países conectados a un cable
    específico
    """
    countriesbycable = mp.newMap(maptype='PROBING')
    map = analyzer['landingpointsbycable']
    lstlandingpoints = me.getValue(mp.get(map, cable))
    lstcountries = lt.newList('ARRAY_LIST')
    for landingpoint in lt.iterator(lstlandingpoints):
        country = getCountryByLandingPoint(analyzer, landingpoint)
        if not lt.isPresent(lstcountries, country):
            lt.addLast(lstcountries, country)
    mp.put(countriesbycable, cable, lstcountries)
    return me.getValue(mp.get(countriesbycable, cable))

def maximumBandwidthByCountry(analyzer, cable):
    """
    Retorna el máximo ancho de banda en mbps de los países
    conectados por un cable específico
    """
    bandwidthbycountry = mp.newMap(maptype='PROBING')
    map = analyzer['bandwidthbycable']
    lstcountries = getCountriesByCable(analyzer, cable)
    for country in lt.iterator(lstcountries):
        capacity = lt.firstElement(me.getValue(mp.get(map, cable)))
        users = me.getValue(mp.get(analyzer['countries'], country))[2]
        maxbandwidth = capacity/users
        mp.put(bandwidthbycountry, country, maxbandwidth*1000000)
    return bandwidthbycountry

def getCoordinatesByIPAddress(ipaddress):
    """
    Retorna las coordenadas geográficas de una
    dirección IP
    """
    geolocation = geo.lookup(ipaddress)
    coordinates = geolocation.location
    return coordinates

def getClosestLandingPoint(analyzer, coordinates):
    """
    Retorna el punto de conexión más cercano a un punto
    geográfico específico
    """
    map = analyzer['landingpointscoords']
    lstlandingpoints = mp.keySet(map)
    closestlandingpoint = None
    mindistance = 1000000
    for landingpoint in lt.iterator(lstlandingpoints):
        originlat = coordinates[0]
        originlon = coordinates[1]
        destlat = me.getValue(mp.get(map, landingpoint))[0]
        destlon = me.getValue(mp.get(map, landingpoint))[1]
        distance = hs.haversine((originlat, originlon), (destlat, destlon))
        if mindistance > distance:
            closestlandingpoint = me.getKey(mp.get(map, landingpoint))
            mindistance = distance
    return closestlandingpoint, mindistance

def minimumJumpsPaths(analyzer, vertexa):
    """
    Retorna un recorrido bfs sobre
    el grafo
    """
    graph = analyzer['connections']
    analyzer['minimumjumpspaths'] = bfs.BreadhtFisrtSearch(graph, vertexa)
    return analyzer

def hasJumpsPathTo(analyzer, vertexb):
    """
    Retorna si existe una ruta de saltos mínima entre el punto de
    conexión inicial y un punto de conexión destino
    """
    paths = analyzer['minimumjumpspaths']
    return bfs.hasPathTo(paths, vertexb)

def minimumJumpsPath(analyzer, vertexb):
    """
    Retorna la ruta de saltos mínima entre el punto de conexión
    inicial y un punto de conexión destino
    """
    paths = analyzer['minimumjumpspaths']
    return bfs.pathTo(paths, vertexb)

def getPathCoordinates(analyzer, lstvertexs):
    """
    Retorna una lista con las coordenadas geográficas de cada
    vértice de una ruta de vértices
    """
    map = analyzer['vertexscoords']
    lstcoordinates = lt.newList('ARRAY_LIST')
    for vertex in lt.iterator(lstvertexs):
        coordinates = me.getValue(mp.get(map, vertex))
        lt.addLast(lstcoordinates, coordinates)
    return lstcoordinates

# Funciones de comparación

def compareValues(value1, value2):
    """
    Compara dos valores en orden
    ascendente
    """
    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return 1
    else:
        return -1

def compareValuesDescOrder(value1, value2):
    """
    Compara dos valores en orden
    descendente
    """
    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return -1
    else:
        return 1