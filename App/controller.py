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
import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo
"""

# Inicialización del analizador

def initAnalyzer():
    """
    Llama la función de inicialización del analizador de
    conexiones
    """
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    """
    Carga los datos de los archivos csv en las estructuras
    de datos
    """
    loadLandingPoints(analyzer)
    loadConnections(analyzer)
    loadCountries(analyzer)

def loadLandingPoints(analyzer):
    """
    Carga las coordenadas geográficas de los puntos de conexión. Por cada
    punto de conexión se indica al modelo que debe adicionar sus
    coordenadas al analizador
    """
    landingpointsfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(landingpointsfile, encoding='utf-8-sig'))
    for landingpoint in input_file:
        model.addLandingPointsCoords(analyzer, landingpoint)
        model.addLandingPointsNames(analyzer, landingpoint)

def loadConnections(analyzer):
    """
    Carga las conexiones entre los vértices de los puntos de conexión. Por
    cada punto de conexión se indica al modelo que adicione sus vértices
    y conexiones al analizador
    """
    connectionsfile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(connectionsfile, encoding='utf-8-sig'))
    for connection in input_file:
        model.addLandingPointConnection(analyzer, connection)
        model.addConnectedLandingPoints(analyzer, connection)
        model.addLandingPointsByCable(analyzer, connection)
        model.addBandwidthByCable(analyzer, connection)
    model.addLocalConnections(analyzer)
    return analyzer

def loadCountries(analyzer):
    """
    Carga los puntos de conexión de las capitales de cada país. Por cada
    país se indica al modelo que adicione sus respectivos vértices
    y conexiones al analizador
    """
    countriesfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(countriesfile, encoding='utf-8'))
    for country in input_file:
        model.addCountries(analyzer, country)
        model.addLandingPointsByCountry(analyzer, country)
        model.addCapitalLandingPoints(analyzer, country)

# Funciones de consulta

def getLandingPoint(analyzer, landingpointname):
    """
    Retorna el identificador de un punto de conexión
    específico
    """
    return model.getLandingPoint(analyzer, landingpointname)

def getLandingPointName(analyzer, landingpoint):
    """
    Retorna el nombre de un punto de conexión
    específico
    """
    return model.getLandingPointName(analyzer, landingpoint)

def getVertexByLandingPoint(analyzer, landingpoint):
    """
    Retorna un vértice de un punto de conexión
    específico
    """
    return model.getVertexByLandingPoint(analyzer, landingpoint)

def getCapitalVertexByCountry(analyzer, country):
    """
    Retorna el vértice del punto de conexión de la
    capital de un país específico
    """
    return model.getCapitalVertexByCountry(analyzer, country)

def getLandingPointsByCountry(analyzer, country):
    """
    Retorna una lista con los puntos de conexión de un país
    específico
    """
    return model.getLandingPointsByCountry(analyzer, country)

def getLandingPointCoordinates(analyzer, landingpoint):
    """
    Retorna las coordenadas geográficas de un punto
    de conexión específico
    """
    return model.getLandingPointCoordinates(analyzer, landingpoint)

def getLandingPointsCoordinates(analyzer, lstlandingpoints):
    """
    Retorna una lista con las coordenadas geográficas de cada
    punto de conexión de una lista
    """
    return model.getLandingPointsCoordinates(analyzer, lstlandingpoints)

def getVertexCoordinates(analyzer, vertex):
    """
    Retorna las coordenadas geográficas de
    un vértice específico
    """
    return model.getVertexCoordinates(analyzer, vertex)

def getAdjacentVertexs(analyzer, vertex):
    """
    Retorna una lista con los vértices adyacentes a
    un vértice específico
    """
    return model.getAdjacentVertexs(analyzer, vertex)

def getVertexsCoordinates(analyzer, lstadjacents):
    """
    Retorna una lista con las coordenadas geográficas de
    cada vértice de una lista
    """
    return model.getVertexsCoordinates(analyzer, lstadjacents)

def stronglyConnectedComponents(analyzer):
    """
    Retorna el número de componentes fuertemente conectados
    del grafo
    """
    return model.stronglyConnectedComponents(analyzer)

def stronglyConnectedVertexs(analyzer, vertexa, vertexb):
    """
    Retorna si dos vértices están fuertemente
    conectados o no
    """
    return model.stronglyConnectedVertexs(analyzer, vertexa, vertexb)

def getStronglyConnectedComponent(analyzer, component):
    """
    Retorna la lista de vértices de un componente
    fuertemente conectado
    """
    return model.getStronglyConnectedComponent(analyzer, component)

def mostConnectedLandingPoint(analyzer):
    """
    Retorna un árbol tipo 'RBT' con los puntos de conexión
    con mayor número de conexiones
    """
    return model.mostConnectedLandingPoint(analyzer)

def minimumCostPaths(analyzer, vertexa):
    """
    Retorna las rutas de costo mínimo desde un punto de conexión
    inicial a todos los demás puntos de conexión
    """
    return model.minimumCostPaths(analyzer, vertexa)

def hasPathTo(analyzer, vertexb):
    """
    Retorna si existe una ruta entre el punto de conexión
    inicial y un punto de conexión destino
    """
    return model.hasPathTo(analyzer, vertexb)

def minimumCostPath(analyzer, vertexb):
    """
    Retorna la ruta de costo mínimo entre el punto de conexión
    inicial y un punto de conexión destino
    """
    return model.minimumCostPath(analyzer, vertexb)

def getMinimumCostPathVertexs(analyzer, vertexb):
    """
    Retorna una lista con los vértices de la ruta de costo
    mínimo entre dos puntos de conexión
    """
    return model.getMinimumCostPathVertexs(analyzer, vertexb)

def minimumSpanningTrees(analyzer):
    """
    Retorna el árbol de expansión mínima
    del grafo
    """
    return model.minimumSpanningTrees(analyzer)

def minimumSpanningTree(analyzer):
    """
    Retorna el número de vértices y el costo del árbol
    de expansión mínima
    """
    return model.minimumSpanningTree(analyzer)

def getLongestConnection(analyzer):
    """
    Retorna la conexión con mayor distancia en km del
    árbol de expansión mínima
    """
    return model.getLongestConnection(analyzer)

def getShortestConnection(analyzer):
    """
    Retorna la conexión con menor distancia en km del
    árbol de expansión mínima
    """
    return model.getShortestConnection(analyzer)

def getConnectedCountries(analyzer, landingpoint):
    """
    Retorna un árbol tipo 'RBT' de países conectados a un
    punto de conexión específico
    """
    return model.getConnectedCountries(analyzer, landingpoint)

def getConnectedLandingPoints(analyzer, landingpoint):
    """
    Retorna una lista de los puntos de conexión conectados a
    un punto de conexión específico
    """
    return model.getConnectedLandingPoints(analyzer, landingpoint)

def getCountriesByCable(analyzer, cable):
    """
    Retorna la lista de paises conectados a un cable
    específico
    """
    return model.getCountriesByCable(analyzer, cable)

def maximumBandwidthByCountry(analyzer, cable):
    """
    Retorna el máximo ancho de banda de los países conectados
    por un cable específico
    """
    return model.maximumBandwidthByCountry(analyzer, cable)

def getCoordinatesByIPAddress(ipaddress):
    """
    Retorna las coordenadas geográficas de una
    dirección IP
    """
    return model.getCoordinatesByIPAddress(ipaddress)

def getClosestLandingPoint(analyzer, coordinates):
    """
    Retorna el punto de conexión más cercano a un punto
    geográfico específico
    """
    return model.getClosestLandingPoint(analyzer, coordinates)

def minimumJumpsPaths(analyzer, vertexa):
    """
    Retorna un recorrido bfs sobre
    el grafo
    """
    return model.minimumJumpsPaths(analyzer, vertexa)

def hasJumpsPathTo(analyzer, vertexb):
    """
    Retorna si existe una ruta de saltos mínima entre el punto de
    conexión inicial y un punto de conexión destino
    """
    return model.hasJumpsPathTo(analyzer, vertexb)

def minimumJumpsPath(analyzer, vertexb):
    """
    Retorna la ruta de saltos mínima entre el punto de conexión
    inicial y un punto de conexión destino
    """
    return model.minimumJumpsPath(analyzer, vertexb)

def getPathCoordinates(analyzer, lstvertexs):
    """
    Retorna una lista con las coordenadas geográficas de cada
    vértice de una ruta de vértices
    """
    return model.getPathCoordinates(analyzer, lstvertexs)