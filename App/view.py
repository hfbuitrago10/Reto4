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
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
assert cf

sys.setrecursionlimit(1000000*10)

"""
La vista se encarga de la interacción con el usuario
"""

# Funciones para la impresión de resultados

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
    
    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass

    elif int(inputs[0]) == 7:
        pass

    elif int(inputs[0]) == 8:
        pass

    elif int(inputs[0]) == 9:
        pass

    else:
        sys.exit(0)
sys.exit(0)