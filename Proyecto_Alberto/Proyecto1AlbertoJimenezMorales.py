#para que el programa guarde los cambios tiene que salirse con la opcion de terminar el programa del menu principal
import shelve

#Esto genera el album y toas lassecciones a partir de un diccionario
def hacerAlbum(selecciones):
    album = {}

    album[""] = []
    album['FWC'] = []

    for spaces in range(29):
        album['FWC'].append("")

    for section in range(len(selecciones)):
        album[selecciones[section]] = []
        for numFicha in range(20):
            album[selecciones[section]].append("")

    return album

#Esto se encarga de asignarle el espacio correspondiente a cada carta y va a darle un 2 si es un duplicado, un 1 si la logro pegar y un -1 si no logro pegarla
def hacerIndiceDeCartas(selecciones):
    indiceDeCartas = {}

    indiceDeCartas[""] = [0]
    indiceDeCartas['FWC'] = []

    for spaces in range(29):
        indiceDeCartas['FWC'].append(0)

    for section in range(len(selecciones)):
        indiceDeCartas[selecciones[section]] = []
        for numFicha in range(20):
            indiceDeCartas[selecciones[section]].append(0)

    return indiceDeCartas

#esto es un booleano que le indica si la postal esta pegada
def pegarFicha(ficha, album):
    if len(ficha) == 2:
        if ficha == "00":
            if album[""][0] == ficha:
                return 2
            elif album[""][0] == "":
                album[""][0] = ficha
                return 1
        else:
            return -1
    else:
        seccion = ficha[:3]
        numero = int(ficha[-2:])
        if seccion not in album:
            return -1
        elif seccion == "FWC" and numero > 29:
            return -1
        elif numero > 20:
            return -1

        if album[seccion][numero - 1] == ficha:
            return 2
        elif album[seccion][numero - 1] == "":
            album[seccion][numero - 1] = ficha
            return 1

        return -1
    
#esto es un booleano que le indica si la postal esta pegada
def buscarPostal(ficha, album):
    if len(ficha) == 2:
        if ficha == "00":
            if album[""][0] == ficha:
                return True
            return False
        else:
            return False
    else:
        seccion = ficha[:3]
        numero = int(ficha[-2:])
        if seccion not in album:
            return False
        elif seccion == "FWC" and numero > 29:
            return False
        elif numero > 20:
            return False

        if album[seccion][numero - 1] == ficha:
            return True
        elif album[seccion][numero - 1] == "":
            return False

        return False
    
#esto hace verificaciones
def introducirBarajaAux(fichas, album, indiceDeCartas):

    results = []

    for ficha in fichas:
        tempResult = pegarFicha(ficha, album)
        if tempResult == 2:
            if len(ficha) == "00":
                indiceDeCartas[""][0] += 1
            indiceDeCartas[ficha[:3]][int(ficha[-2:]) - 1] += 1
        elif tempResult == 1:
            indiceDeCartas[ficha[:3]][int(ficha[-2:]) - 1] = 1
        elif tempResult == -1:
            print("Se encontró un error en la baraja")

        results.append(tempResult)

    return results

#esto agarra una lista de fichas y las introduce al album(no pude como tal usarlo para introducir varias pero si para ingresar 1 a la vez)
def introducirBaraja(entradaDeFichas, album, indiceDeCartas):

    if not isinstance(entradaDeFichas, list):
        if isinstance(entradaDeFichas, str):
            return introducirBarajaAux([entradaDeFichas], album, indiceDeCartas)
        else:
            print("Se encontró un error con la(s) ficha(s)")
    else:
        return introducirBarajaAux(entradaDeFichas, album, indiceDeCartas)

#esto le va indicar el porcentaje del album que ha completado
def obtenerPorcentajeTotalDelAlbum(indiceDeCartas):

    total = 0
    completado = 0

    for key in indiceDeCartas:
        seccion = indiceDeCartas[key]

        for i in range(len(seccion)):
            if seccion[i] != 0:
                completado += 1
            total += 1

    return completado/total * 100

#esto se encarga de asegurarse de que la seccion que ingreso si existe
def verificarExistenciaDeSeccion(seccion, indiceDeCartas):

    if seccion in indiceDeCartas:
        return True
    return False

#esto le indica el porcentaje de completidud de la seccion solicitada
def obtenerPorcentajeDeCompletitudPorSeccion(seccion, indiceDeCartas):

    completado = 0
    total = 0

    seccionDeAlbum = indiceDeCartas[seccion]

    for i in range(len(seccionDeAlbum)):
        if seccionDeAlbum[i] != 0:
            completado += 1
        total += 1

    return completado/total * 100

#esto le dice que postales tiene pegadas en el album
def obtenerPostalesActuales(album):

    postales = []

    for key in album:
        seccion = album[key]
        for i in range(len(seccion)):
            if seccion[i] != "":
                postales.append(seccion[i])

    return postales

#este le indica las postales que le hacen falta
def obtenerPostalesFaltantes(album):

    postales = []

    for key in album:
        seccion = album[key]
        for i in range(len(seccion)):
            if seccion[i] == "":
                postales.append(key + "-" + str(i + 1))

    return postales

#este le indica las postales que tiene repedias
def obtenerPostalesRepetidas(indiceDeCartas):
    postales = []

    for key in indiceDeCartas:
        seccion = indiceDeCartas[key]
        for i in range(len(seccion)):
            if seccion[i] > 1:
                postales.append(key + "-" + str(i + 1))

    return postales

#esto le verifica que la postal que ingreso es valida
def verificarExistenciaDeUnaPostal(ficha, album):
    if len(ficha) == 2:
        if ficha == "00":
            return True
        else:
            return False
    else:
        seccion = ficha[:3]
        numero = int(ficha[-2:])
        if seccion not in album:
            return False
        elif seccion == "FWC" and numero > 29:
            return False
        elif numero > 20:
            return False

        return True

#esto le permite ya sea agregar una postal, borrala o agregarla como repetida
def actualizarCantidadDeUnaPostal(postal, cantidad, album, indiceDeCartas):

    if cantidad == 0:
        if len(postal) == 2:
            if postal == "00":
                album[""][0] = ""
                indiceDeCartas[""][0] = 0
                return True
            else:
                return False
        else:
            seccion = postal[:3]
            numero = int(postal[-2:])

            album[seccion][numero-1]  = ""
            indiceDeCartas[seccion][numero-1] = 0
            return True
    elif cantidad > 0:
        pegarFicha(postal, album)

        seccion = postal[:3]
        numero = int(postal[-2:])

        indiceDeCartas[seccion][numero-1] = cantidad
        return True
    return False


#a partir de aca son los menus
def registroDeCartas(album, indiceDeCartas):

    while True:
        print("\nCuántas desea registrar?\n")
        print("1. Una sola postal\n"
              "2. Múltiples postales\n"
              "3. Salir\n")

        opcion = eval(input())

        match opcion:
            case 1:
                postal = input("Ingrese la postal que desea agregar al álbum: ")
                while True:
                    if not isinstance(postal, str):
                        postal = input(eval("Favor introducir un número de ficha válido: "))

                    result = introducirBaraja([postal], album, indiceDeCartas)[0]
                    if result == 2:
                        print("Esta postal se encuentra repetida por lo que se no se agregará al álbum pero aumentara"
                              " su contador")
                        break
                    elif result == 1:
                        print("La postal se ha agregado al álbum correctamente")
                        break
                    elif result == -1:
                        print("Existe un error con el código de la postal, el mismo no es válido")
                        break
            case 2:
                pass
            case 3:
                break
            case _:
                print("Favor elegir una de las siguientes opciones")


def informacion(album, indiceDeCartas):
    while True:
        print("\nCuál información desea consultar?\n")
        print("1. Estado de una postal\n"
              "2. Porcentajes de completitud\n"
              "3. Listado de fichas\n"
              "4. Salir")

        opcion = eval(input())

        match opcion:
            case 1:
                postal = input("Ingrese la postal que desea consultar: ")
                result = buscarPostal(postal, album)
                if result:
                    print("\nEsta postal ya se encuentra en el album\n")
                else:
                    print("\nEsta postal se no se encuentra en el album\n")
                break
            case 2:
                print("\nCuál porcentaje desea conocer?\n")
                print("1. Completitud total del album\n"
                      "2. Por sección\n"
                      "3. Salir")
                while True:
                    option1 = eval(input())

                    match option1:
                        case 1:
                            result = obtenerPorcentajeTotalDelAlbum(indiceDeCartas)
                            print("\nEl album se encuentra completo en un " + str(result) + " porciento\n")
                            break
                        case 2:
                            while True:
                                seccion = input("Indique la seccion que desea consultar: ")

                                if verificarExistenciaDeSeccion(seccion, indiceDeCartas):
                                    result = obtenerPorcentajeDeCompletitudPorSeccion(seccion, indiceDeCartas)
                                    print("\nLa seccion del album se encuentra completa en un " + str(result) + " porciento\n")
                                    break
                                else:
                                    print("\nFavor introducir una seccion válida\n")
                                break

                        case 3:
                            break
            case 3:
                print("\nQue listado desea conocer?\n")
                print("1. Total de postales pegadas\n"
                      "2. Total de postales faltantes\n"
                      "3. Total de postales repetidas\n"
                      "4. Salir")
                while True:
                    option2 = eval(input())

                    match option2:
                        case 1:
                            result = obtenerPostalesActuales(album)
                            print(result)
                            print("\n")
                            break
                        case 2:
                            result = obtenerPostalesFaltantes(album)
                            print(result)
                            print("\n")
                            break
                        case 3:
                            result = obtenerPostalesRepetidas(indiceDeCartas)
                            print(result)
                            print("\n")
                            break
                        case 4:
                            break
            case 4:
                break
            case _:
                print("Favor elegir una de las siguientes opciones")

def actualizacion(album, indiceDeCartas):
    while True:
        print("\nQué información desea actualizar?\n")
        print("1. Cantidad de una postal específica\n"
              "2. Salir")

        opcion = eval(input())

        match opcion:
            case 1:
                postal = input("Ingrese la postal que desea actualizar: ")
                while True:
                    if not isinstance(postal, str):
                        postal = input(eval("Favor introducir un número de ficha válido: "))

                    cantidad = eval(input("Ingrese la cantidad a la que desea actualizar: "))

                    result = actualizarCantidadDeUnaPostal(postal, cantidad, album, indiceDeCartas)

                    if result:
                        print("\nSe realizó el cambio con éxito\n")
                    else:
                        print("\nNo se pudo realizar el cambio\n")
                    break
            case 2:
                break


def eliminacion(album, indiceDeCartas):
    postal = input("Ingrese la postal que desea eliminar: ")
    if not isinstance(postal, str):
        postal = input(eval("Favor introducir un número de ficha válido: "))

    result = actualizarCantidadDeUnaPostal(postal, 0, album, indiceDeCartas)

    if result:
        print("\nSe realizó el cambio con éxito\n")
    else:
        print("\nNo se pudo realizar el cambio\n")

def menu(album, indiceDeCartas):

    while True:
        print("\nBienvenido al sistema de album Mundial 2022\n")
        print("\nFavor seleccioné una de las siguientes opciones:\n")
        print("1.Registrar 1 o más postales\n"
              "2.Información sobre postales o albúm\n"
              "3.Actualizar información de postales\n"
              "4.Eliminar información de postal\n"
              "5.Terminar programa\n")

        opcion = eval(input())

        while True:
            if not isinstance(opcion, int):
                opcion = eval(input("Favor introducir una opcion válida"))
            else:
                break

        match opcion:
            case 1:
                registroDeCartas(album,indiceDeCartas)
            case 2:
                informacion(album, indiceDeCartas)
            case 3:
                actualizacion(album, indiceDeCartas)
            case 4:
                eliminacion(album, indiceDeCartas)
            case 5:
                infoDB = shelve.open("paniniAlbum.db")
                infoDB["album"] = album
                infoDB["indice"] = indiceDeCartas
                break
            case _:
                print("\nFavor introducir un valor válido\n")


def inicializadorDePrograma():
    naciones = ["QAT", "ECU", "SEN", "NED", "ENG", "IRN", "USA", "WAL", "ARG", "KSA", "MEX", "POL", "FRA", "AUS", "DEN",
                "TUN", "ESP", "CRC", "GER", "JPN", "BEL", "CAN", "MAR", "CRO", "BRA", "SRB", "SUI", "CMR", "POR", "GHA",
                "URU", "KOR"]

    album = dict()
    indiceDeCartas = dict()

    paniniAlbum = shelve.open("paniniAlbum.db")
    if len(paniniAlbum.keys()) == 0:
        album = hacerAlbum(naciones)
        indiceDeCartas = hacerIndiceDeCartas(naciones)
    else:
        album = paniniAlbum["album"]
        indiceDeCartas = paniniAlbum["indice"]
    paniniAlbum.close()

    menu(album, indiceDeCartas)

inicializadorDePrograma()

###############################################################################################################################################
#proyecto 2

from tkinter import *




















































