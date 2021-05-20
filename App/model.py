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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
assert cf

"""
Se define la estructura del analizador de conexiones
"""

# Construcción de modelo

def newAnalyzer():
    """
    Inicializa el analizador de conexiones
    """
    analyzer = {'landingpoints': None,
                'connections': None,
                'cables': None,
                'countries': None}
    
    """
    Se crea un map para guardar los puntos de conexión
    """
    analyzer['landingpoints'] = mp.newMap(maptype='PROBING')

    """
    Se crea un grafo para modelar las conexiones entre puntos
    """
    analyzer['connections'] = gr.newGraph('ADJ_LIST')

    """
    Se crea un map para guardar la información de los cables
    """
    analyzer['cables'] = mp.newMap(maptype='PROBING')

    """
    Se crea un map para guardar la información de los países
    """
    analyzer['countries'] = mp.newMap(maptype='PROBING')

    return analyzer

# Funciones para agregar información al analizador

def addLandingPointConnection(analyzer, connection):
    """
    Adiciona los puntos de conexión como vértices del grafo y las
    conexiones entre véritices adyacentes como arcos
    """
    origin = vertexStructureOrigin(connection)
    destination = vertexStructureDestination(connection)
    distance = getDistance(connection)
    capacity = getCapacity(connection)
    weight = distance, capacity
    addLandingPoint(analyzer, origin)
    addLandingPoint(analyzer, destination)
    addConnection(analyzer, origin, destination, weight)
    addLandingPoints(analyzer, connection, '\ufefforigin')
    addLandingPoints(analyzer, connection, 'destination')
    addCableInfo(analyzer, connection)

def addLandingPoint(analyzer, landingpoint):
    """
    Adiciona un punto de conexión como vértice del grafo
    """
    if not gr.containsVertex(analyzer['connections'], landingpoint):
        gr.insertVertex(analyzer['connections'], landingpoint)
    return analyzer

def addConnection(analyzer, origin, destination, weight):
    """
    Adiciona un arco entre dos puntos de conexión
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, weight)
    return analyzer

def addLandingPoints(analyzer, connection, landingpoint):
    """
    Adiciona a un punto de conexión sus respectivos cables
    """
    entry = mp.get(analyzer['landingpoints'], connection[landingpoint])
    if entry is None:
        lstlandingpoints = lt.newList('ARRAY_LIST')
        lt.addLast(lstlandingpoints, connection['cable_id'])
        mp.put(analyzer['landingpoints'], connection[landingpoint], lstlandingpoints)
    else:
        lstlandingpoints = entry['value']
        cable = connection['cable_id']
        if not lt.isPresent(lstlandingpoints, cable):
            lt.addLast(lstlandingpoints, cable)
    return analyzer

def addLocalConnections(analyzer):
    """
    Adiciona un arco entre los vértices de cada punto de conexión
    """
    lstlandingpoints = mp.keySet(analyzer['landingpoints'])
    for landingpoint in lt.iterator(lstlandingpoints):
        lstconnections = mp.get(analyzer['landingpoints'], landingpoint)['value']
        precable = None
        for cable in lt.iterator(lstconnections):
            connection = landingpoint + '-' + cable
            if precable is not None:
                addConnection(analyzer, precable, connection, addWeight(analyzer, landingpoint))
                addConnection(analyzer, connection, precable, addWeight(analyzer, landingpoint))
            precable = connection

def addCableInfo(analyzer, connection):
    """
    Adiciona el ancho de banda en tbps de un cable específico
    al map de cables
    """
    cables = analyzer['cables']
    cable = connection['cable_id']
    existcable = mp.contains(cables, cable)
    if existcable:
        entry = mp.get(cables, cable)
        value = me.getValue(entry)
    else:
        value = connection['capacityTBPS']
        mp.put(cables, cable, value)

def addCountry(analyzer, country):
    """
    Adiciona la información de un país específico al map de
    paises
    """
    key = country['CountryName']
    key = key.replace(' ', '')
    mp.put(analyzer['countries'], key, country)

# Funciones para creación de datos

def vertexStructureOrigin(connection):
    """
    Crea la estructura del vértice con el id del punto de
    conexión y el id del cable de conexión
    """
    vertex = connection['\ufefforigin'] + '-'
    vertex = vertex  + connection['cable_id']
    return vertex

def vertexStructureDestination(connection):
    """
    Crea la estructura del vértice con el id del punto de
    conexión y el id del cable de conexión
    """
    vertex = connection['destination'] + '-'
    vertex = vertex  + connection['cable_id']
    return vertex

def getDistance(connection):
    """
    Retorna la distancia en km de un cable específico
    """
    distance = connection['cable_length']
    if distance == 'n.a.':
        distance = 0
    else:
        distance = distance.replace(' km', '')
        distance = distance.replace(',', '')
    return float(distance)

def getCapacity(connection):
    """
    Retorna el ancho de banda en tbps de un cable
    específico
    """
    capacity = connection['capacityTBPS']
    return float(capacity)

def addWeight(analyzer, landingpoint):
    """
    Retorna una tupla con la distancia en km y el ancho de banda
    mínimo en tbps como peso del arco entre dos vértices
    de un punto de conexión
    """
    distance = 0.10
    lstcapacity = []
    lstcables = mp.get(analyzer['landingpoints'], landingpoint)['value']
    for cable in lt.iterator(lstcables):
        capacity = mp.get(analyzer['cables'], cable)['value']
        lstcapacity.append(float(capacity))
    mincapacity = min(lstcapacity)
    return distance, mincapacity

# Funciones de consulta

# Funciones de comparación