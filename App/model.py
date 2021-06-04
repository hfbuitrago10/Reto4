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
    
    analyzer['cablesbylandingpoint'] = mp.newMap()
    analyzer['connectedlandingpoints'] = mp.newMap()
    analyzer['landingpointsbycable'] = mp.newMap()
    analyzer['bandwidthbycable'] = mp.newMap()
    analyzer['landingpointscoords'] = mp.newMap()
    analyzer['landingpointsnames'] = mp.newMap()
    analyzer['countries'] = mp.newMap()
    analyzer['landingpointsbycountry'] = mp.newMap()
    analyzer['vertexscoords'] = mp.newMap()

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

def addLandingPointsByCable(analyzer, connection):
    """
    Adiciona la lista de puntos de conexión conectados por
    un cable específico
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
    Adiciona la capacidad de transferencia en terabits
    de cada cable
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
            origincoords = originlat, originlon
            destlat = me.getValue(mp.get(coords, landingpoint))[0]
            destlon = me.getValue(mp.get(coords, landingpoint))[1]
            distance = hs.haversine((originlat, originlon), (destlat, destlon))
            if lt.isEmpty(lstcables) == False:
                addLandingPoint(analyzer, origin)
                addCapitalVertexsCoords(analyzer, origin, origincoords)
                addConnection(analyzer, origin, destination, distance)

def addVertexsCoords(analyzer, vertex):
    """
    Adiciona las coordenadas geográficas de un
    vértice del gráfo
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
    vértice capital del grafo
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

def mostConnectedCapitalLandingPoint(analyzer):
    """
    Retorna un árbol tipo 'RBT' con los puntos de conexión de
    capitales por número de conexiones
    """
    graph = analyzer['connections']
    ordmap = om.newMap('RBT', compareValues)
    lstvertexs = gr.vertices(graph)
    lstcountries = mp.keySet(analyzer['countries'])
    for country in lt.iterator(lstcountries):
        capital = getCapitalByCountry(analyzer, country)
        connections = 0
        value = capital, country
        for vertex in lt.iterator(lstvertexs):
            if capital in vertex:
                connections += 1
        if capital != '':
            om.put(ordmap, connections, value)
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
    Retorna los árboles de expansión mínimos
    del grafo
    """
    graph = analyzer['connections']
    analyzer['minimumspanningtrees'] = pm.PrimMST(graph)
    return analyzer

def minimumSpanningTree(analyzer):
    """
    Retorna el número de vértices y el costo del árbol
    de expansión mínimo
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

def depthFirstSearch(analyzer):
    """
    Retorna un recorrido dfs sobre
    el grafo
    """
    pass

def getConnectedCountries(analyzer, landingpoint):
    """
    Retorna un árbol tipo 'RBT' de países conectados a un
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

def getCountriesByCable(analyzer, cable):
    """
    Retorna la lista de países conectados a un cable
    específico
    """
    countriesbycable = mp.newMap()
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
    Retorna el máximo ancho de banda de los países conectados
    por un cable específico
    """
    bandwidthbycountry = mp.newMap()
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
    return closestlandingpoint

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
    Retorna si existe un camino de saltos entre el punto de conexión
    inicial y un punto de conexión destino
    """
    paths = analyzer['minimumjumpspaths']
    return bfs.hasPathTo(paths, vertexb)

def minimumJumpsPath(analyzer, vertexb):
    """
    Retorna el camino con saltos mínimos entre el punto de conexión
    inicial y un punto de conexión destino
    """
    paths = analyzer['minimumjumpspaths']
    return bfs.pathTo(paths, vertexb)

def getPathCoordinates(analyzer, lstvertexs):
    """
    Retorna una lista con las coordenadas geográficas de cada
    vértice de una ruta
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