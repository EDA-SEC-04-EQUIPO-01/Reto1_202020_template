"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from Sorting import insertionsort as insort
from Sorting import selectionsort as selsort
from Sorting import shellsort as shsort

from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")




def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1



def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies ():
    lst = loadCSVFile("theMoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds) 
    print("Datos de películas cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def loadCasting():
    lst = loadCSVFile("theMoviesdb/MoviesCastingRaw-small.csv",compareRecordIds) 
    print("Datos del elenco cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst


def countElementsByCriteria(criteria, lst, lst2, type):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    t1_start = process_time()
    counter = 0
    iterator = it.newIterator(lst)
    pel_id = []
    while it.hasNext(iterator):
        element = it.next(iterator)
        if criteria.lower() == element["director_name"].lower():
            pel_id.append(element["id"])
            counter +=1
    
    iterator = it.newIterator(lst2)
    lst_pel=[]
    suma = 0
    div = 0
    promedio = 0
    while it.hasNext(iterator):
        element = it.next(iterator)
        if element[type] in pel_id:
            lst_pel.append(element["original_title"])
            suma+=float(element["vote_average"])
            div +=1
    
    try:
        promedio = round(suma/div,3)
    except:
        print("Este director no tiene películas en el registro")

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    
    return (lst_pel,counter,promedio)

def less_count(element1, element2):
    if float(element1['vote_count']) < float(element2['vote_count']):
        return True
    return False

def less_average(element1, element2):
    if float(element1['vote_average']) < float(element2['vote_average']):
        return True
    return False

def greater_count(element1, element2):
    if float(element1['vote_count']) > float(element2['vote_count']):
        return True
    return False

def greater_average(element1, element2):
    if float(element1['vote_average']) > float(element2['vote_average']):
        return True
    return False

def orderElementsByCriteria(lst,tipo,gb,cant):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    t1_start = process_time()
    if tipo == 1:
        print("Filtrando listas...")
        shsort.shellSort(lst,greater_count)
        if gb == 1:
            bestcount = []
            for a in list(range(1,cant+1)):
                element = lt.getElement(lst,a)
                bestcount.append({element["original_title"]:element["vote_count"]})
            print("Top",cant, "películas con mayor cantidad de votos: \n",bestcount)

        elif gb == 2:
            worstcount = []
            for a in list(range(lt.size(lst)-(cant),lt.size(lst))):
                element = lt.getElement(lst,a)
                worstcount.append({element["original_title"]:element["vote_count"]})
            print("Top",cant, "películas con menor cantidad de votos: \n",worstcount)

    if tipo == 2:
        print("Filtrando listas...")
        shsort.shellSort(lst,greater_average)
        if gb ==1:
            bestaverage = []
            for a in list(range(1,cant+1)):
                element = lt.getElement(lst,a)
                bestaverage.append({element["original_title"]:element["vote_average"]})
            print("Top",cant,"películas con mejor promedio de votos: \n",bestaverage)

        elif gb ==2:
            worstaverage = []
            for a in list(range(lt.size(lst)-(cant),lt.size(lst))):
                element = lt.getElement(lst,a)
                worstaverage.insert(0,{element["original_title"]:element["vote_average"]})
            print("Top",cant, "películas con peor promedio de votos: \n",worstaverage)

    t1_stop = process_time()
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

    return "Acción realizada con éxito"

def moviesByActor(criteria, lista, lista2):
    res=0 #cantidad de apariciones
    IdNombres=[]
    ListaNombres=[]
    Prom=0
    iterator = it.newIterator(lista)
    while it.hasNext(iterator):
        element = it.next(iterator)
        if (criteria == element['actor1_name']) or (criteria == element['actor2_name']) or (criteria == element['actor3_name']) or (criteria == element['actor4_name']) or (criteria == element['actor5_name']):
            IdNombres.append(element["id"])
            res +=1

    iterator2 = it.newIterator(lista2)
    while it.hasNext(iterator2):
        element = it.next(iterator2)
        if element["id"] in IdNombres: #buscar id de la lista 2
            ListaNombres.append(element['original_title'])
            Prom += float((element["vote_average"]))
    promedio= round(Prom/res,2)
    final= str("tu actor/actriz aparece en ") +str(res) +str(" peliculas con un promedio de ") +str(promedio) +str("\nEl nombre de estas peliculas son: ") +str(ListaNombres)
    return final

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """

    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies()
                lstcasting = loadCasting()

            elif int(inputs[0])==2: #opcion 2
                if lstmovies==None or lstmovies['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:
                    tipo = int(input("Ingrese si quiere ver la cantidad de votos o el promedio de votos (1 o 2): "))
                    guba = int(input("Ingrese si quiere ver las mejores o las peores (1 o 2): "))
                    cant = int(input("Ingrese la cantidad de películas que desea ver en el top: "))
                    orderElementsByCriteria(lstmovies, tipo, guba, cant)

            elif int(inputs[0])==3: #opcion 3
                if lstmovies==None or lstmovies['size']==0: #obtener la longitud de la lista
                    print("La lista de películas esta vacía")
                elif lstcasting == None or lstcasting['size']==0:
                    print("La lista del elenco esta vacía")
                else:
                    if lt.size(lstmovies)>2000:
                        type = "\ufeffid"
                    else:
                        type = "id"
                    criteria =input('Ingrese el nombre del director\n')
                    counter=countElementsByCriteria(criteria,lstcasting,lstmovies,type)
                    print("El director",criteria,"tiene un total de",counter[1],"películas con una calificación promedio de",counter[2],"\n",counter[0])

            elif int(inputs[0])==4: #opcion 4
                if lstmovies==None or lstmovies['size']==0: #obtener la longitud de la lista
                    print("La lista de películas esta vacía")
                elif lstcasting == None or lstcasting['size']==0:
                    print("La lista del elenco esta vacía")
                else:
                    if lt.size(lstmovies)>2000:
                        type = "\ufeffid"
                    else:
                        type = "id"
                    criteria =input('Escribe el nombre de un actor\n')
                    print("Cargando...")
                    counter=moviesByActor(criteria,lstcasting,lstmovies) 
                    print(counter)

            elif int(inputs[0])==3: #opcion 5
                pass

            elif int(inputs[0])==4: #opcion 6
                pass

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()