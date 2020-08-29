"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 * :D
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


def greater_count(element1, element2):
    if float(element1['vote_count']) > float(element2['vote_count']):
        return True
    return False

def greater_average(element1, element2):
    if float(element1['vote_average']) > float(element2['vote_average']):
        return True
    return False

def orderElementsByCriteria(lst, count_average, best_worst, number):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    if lst["size"]<10 or number <10:
        return 0
    else:
        if count_average.lower()=="count":
            objeto = "vote_count"
            shsort.shellSort(lst, greater_count)
        elif count_average.lower()=="average":
            objeto = "vote_average"
            shsort.shellSort(lst, greater_average)
        else:
            return 0
        lista = [{}]
        if best_worst.lower() == "best":
            for i in range(1,number+1):
                fila =lt.getElement(lst,i)
                lista[0][fila["original_title"]]=fila[objeto]
        elif best_worst.lower() == "worst":
            atras = lst["size"]+1
            while atras!=lst["size"]-number:
                atras-=1
                fila = lt.getElement(lst,atras)
                lista[0][fila["original_title"]]=fila[objeto]
        else:
            return 0
    return lista

def orderElementsByRankingGenre(lstmovies,genre,top,best_worst,average_count):
    t1_start = process_time()
    if lstmovies["size"]<top or top<10:
        t1_stop = process_time()
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
        return 0
    else:
        genreList = lt.newList("ARRAY_LIST")
        finalList = [{}]
        for i in range(1, lstmovies["size"]+1):
            fila = lt.getElement(lstmovies,i)
            if genre.lower() in fila["genres"].lower():
                lt.addLast(genreList,fila)
        if genreList["size"]>0:
            if genreList["size"] < top:
                top = genreList["size"]
            prom=0
            if average_count.lower()=="count":
                busqueda = "vote_count"
                shsort.shellSort(genreList,greater_count)
            else:
                busqueda = "vote_average"
                shsort.shellSort(genreList,greater_average)
            if best_worst.lower() == "best":
                for j in range(1, top+1):
                    fila = lt.getElement(genreList,j)
                    prom +=float(fila[busqueda])
                    finalList[0][fila["original_title"]]=fila[busqueda]
            else:
                atras = genreList["size"]+1
                while atras != atras-top and atras != 0:
                    atras-=1
                    fila = lt.getElement(genreList,atras)
                    prom +=float(fila[busqueda])
                    finalList[0][fila["original_title"]]=fila[busqueda]
        else:
            t1_stop = process_time()
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
            return 0
    t1_stop = process_time()
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")        
    return (finalList, prom/top)


def moviesByActor(criteria, lista, lista2):
    res=0 #cantidad de apariciones
    IdNombres=[]
    ListaNombres=[]
    Prom=0
    iterator = it.newIterator(lista)
    while it.hasNext(iterator):
        element = it.next(iterator)
        if (criteria.lower() == element['actor1_name'].lower()) or (criteria.lower() == element['actor2_name'].lower()) or (criteria.lower() == element['actor3_name'].lower()) or (criteria.lower() == element['actor4_name'].lower()) or (criteria.lower() == element['actor5_name'].lower()):
            IdNombres.append(element["id"])
            res +=1

    iterator2 = it.newIterator(lista2)
    while it.hasNext(iterator2):
        element = it.next(iterator2)
        if element["id"] in IdNombres: #buscar id de la lista 2
            ListaNombres.append(element['original_title'])
            Prom += float((element["vote_average"]))
    try:
        promedio= round(Prom/res,2)
        final= str("Tu actor/actriz aparece en ") +str(res) +str(" peliculas con un promedio de ") +str(promedio) +str("\nEl nombre de estas peliculas son: ") +str(ListaNombres)
    except:
        final= "Tu actor no existe en esta lista"
    return final

def conocerUnGenero(lst,genero):
    t1_start = process_time()
    iterator = it.newIterator(lst)
    pelis = []
    sumpr = 0
    counter = 0
    if lst['size']==0:
        print("La lista esta vacía")  
        return 0
    else:
        while it.hasNext(iterator):
            element = it.next(iterator)
            if genero.lower() in element["genres"].lower():
                pelis.append(element["original_title"])
                sumpr += float(element["vote_average"])
                counter+=1
    try:
        promedio = sumpr/counter
    except:
        promedio = 0
    t1_stop = process_time() #tiempo final
    
    print(pelis)
    print("\nLa lista que se imprimió contiene los nombres de todas pas películas del género",genero)
    print("\nEl género",genero,"tiene un total de",counter,"películas con un promedio acumulado de",round(promedio,3))
    print("\nTiempo de ejecución ",t1_stop-t1_start," segundos")
    return "Acción realizada con éxito"


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
                    tipo = input("Ingrese COUNT si quiere ver la cantidad de votos o AVERAGE si quiere ver el promedio de votos:\n")
                    guba = input("Ingrese BEST si quiere ver las mejores o  WORST si quiere ver las peores:\n")
                    cant = int(input("Ingrese la cantidad de películas que desea ver en el top: "))
                    if orderElementsByCriteria(lstmovies, tipo, guba, cant) != 0:
                        print(orderElementsByCriteria(lstmovies, tipo, guba, cant))
                    else:
                        print("Ingrese valores válidos para poder hacer el ranking")

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

            elif int(inputs[0])==5: #opcion 5
                genero = input("Ingrese el género que desea conocer: ")
                conocerUnGenero(lstmovies,genero)
    

            elif int(inputs[0])==6: #opcion 6
                genre = input("Escriba el genero que quiere rankear:\n")
                top = int(input("Escriba el numero de películas que quiere que aparezcan en el ranking:\n"))
                best_worst = input("Escriba BEST si quiere hacer el ranking ascendente o WORST si lo quiere descendente\n")
                count_average = input("Escriba COUNT si quiere hacer el ranking de acuerdo a la cantidad de votos por película o AVERAGE si quiere que sea por el promedio de ellos\n")
                ranking = orderElementsByRankingGenre(lstmovies,genre,top,best_worst,count_average)
                if ranking == 0:
                    print("La lista es demasiada corta para el numero de películas que quiere filtar o quiere hacer un ranking menor a 10 películas o introdujo un género inexistente en la base de datos, intentelo de nuevo\n")
                else:
                    print("El ranking del genero", genre, "por", best_worst, count_average, "es:", ranking[0], "y el promedio del ranking es", ranking[1], "votos")

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()