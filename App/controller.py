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
    model.addLocalConnections(analyzer)
    return analyzer

def loadCountries(analyzer):
    """
    Carga los puntos de conexión de las capitales de cada país. Por cada
    país se indica al modelo que debe adicione los respectivos vértices
    y conexiones al analizador
    """
    countriesfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(countriesfile, encoding='utf-8'))
    for country in input_file:
        model.addLandingPointsByCountry(analyzer, country)
        model.addCapitalLandingPoints(analyzer, country)

# Funciones de consulta