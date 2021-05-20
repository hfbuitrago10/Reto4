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
    Llama la función de inicialización del analizador
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
    Carga los puntos de conexión del archivo csv. Por cada punto de conexión
    se indica al modelo que debe adicionarlo al analizador
    """
    landingpointsfile = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(landingpointsfile, encoding='utf-8'))
    for landingpoint in input_file:
        model.addLandingPointsInfo(analyzer, landingpoint)

def loadConnections(analyzer):
    """
    Carga las conexiones del archivo csv. Por cada conexión se indica al
    modelo que debe adicionarlo al analizador
    """
    connectionsfile = cf.data_dir + 'connections.csv'
    input_file = csv.DictReader(open(connectionsfile, encoding='utf-8'))
    for connection in input_file:
        model.addLandingPointConnection(analyzer, connection)
    model.addLocalConnections(analyzer)
    return analyzer

def loadCountries(analyzer):
    """
    Carga los paises del archivo csv. Por cada país se indica al
    modelo que debe adicionarlo al analizador
    """
    countriesfile = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(countriesfile, encoding='utf-8'))
    for country in input_file:
        model.addCountry(analyzer, country)

# Funciones de consulta

def landingPointsSize(analyzer):
    """
    Retorna el número de puntos de conexión del
    grafo
    """
    return model.landingPointsSize(analyzer)

def connectionsSize(analyzer):
    """
    Retorna el número de conexiones entre los puntos
    de vértices del grafo
    """
    return model.connectionsSize(analyzer)

def countriesSize(analyzer):
    """
    Retorna el número de países cargados en el
    analizador
    """
    return model.countriesSize(analyzer)