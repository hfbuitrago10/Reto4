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
                'connections': None}
    
    """
    Se crea un map para guardar los puntos de conexión
    """
    analyzer['landingpoints'] = mp.newMap(maptype='PROBING')

    """
    Se crea un grafo para modelar las conexiones entre puntos
    """
    analyzer['connections'] = gr.newGraph('ADJ_LIST')

    return analyzer

# Funciones para agregar información al analizador

def addLandingPointConnection(analyzer, landingpoint, connection):
    """
    Adiciona los puntos de conexión como vértices del grafo y las
    conexiones entre véritices adyacentes como arcos
    """
    pass

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

# Funciones para creación de datos

def vertexStructure(landingpoint, connection):
    """
    Crea la estructura del vértice con el id del punto de
    conexión y el id del cable de conexión
    """
    vertex = landingpoint['landing_point_id'] + '-'
    vertex = vertex  + connection['cable_id']
    return vertex

# Funciones de consulta

# Funciones de comparación