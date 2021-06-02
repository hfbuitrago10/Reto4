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
                'landingpointscoords': None,
                'landingpointsbycountry': None,
                'sccomponents': None,
                'minimumcostpaths': None}
    
    analyzer['connections'] = gr.newGraph('ADJ_LIST',
                                           True,
                                           100000)
    
    analyzer['cablesbylandingpoint'] = mp.newMap()
    analyzer['landingpointscoords'] = mp.newMap()
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

def getLandingPoint(analyzer, landingpoint):
    """
    Retorna el id del punto de conexión
    """
    pass

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