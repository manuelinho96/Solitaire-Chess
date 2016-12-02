import pygame, sys, re, time, copy
from pygame.locals import *

shift = False #variable booleana que indica el estado de la tecla shift
bloq_mayus = False #variable booleana que indica el estado de la tecla bloq mayus del teclado

#funcion que cierra pygame y cierra el programa
def cerrar():
    #precondicion true
    pygame.quit()
    sys.exit()
    # postcondicion true


#funcion que detecta eventos y evalua si son teclas
#y retorna la entrada del usuario
def Leer(x,y, color, longitud_maxima, xfinal, yfinal):
    #precondicion x,y,xfinal,yfinal deben estar entra 0 y 600, longitud maxima debe ser mayor o igual que 1
    try:
        assert(x >= 0 and x <= 600 and y >= 0 and y <= 600 and xfinal >= 0 and xfinal <= 600 and yfinal >= 0 \
               and yfinal <= 600 and longitud_maxima >0 )
    except:
        print("error en los parametros")
    string = ""
    patron = re.compile("^\w{1}$")
    patron2 = re.compile("\w")
    rectangulo = pygame.Rect(x, y, xfinal - x, yfinal - y)
    texto = ""
    global shift
    global bloq_mayus
    while True:#
        pygame.display.update()
        pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
        texto = fuente.render(string, 1, (255, 120, 255))
        ventana.blit(texto, (x + 7, y + 1))
        for event in pygame.event.get():
            if event.type == QUIT:
                    cerrar()
            if event.type == KEYDOWN:
                if event.key == 304: #presionar shift
                    shift = True
                elif event.key == 301: #presionar bloq mayus
                    bloq_mayus = True
                if ((patron.match(pygame.key.name(event.key)) != None or pygame.key.name(event.key) == "[-]" or
                    pygame.key.name(event.key) == "-") and len(string) < longitud_maxima):
                    # dibujar la letra, sumarle pixeles dependiendo de la longitud para que quede mas lejos la letra nueva
                    # recordar que se debe usar el color pasado por parametro
                    letra = pygame.key.name(event.key)
                    if pygame.key.name(event.key) == "[-]" or pygame.key.name(event.key) == "-":
                        letra = "-"
                    if shift != bloq_mayus:
                        letra = letra.upper()
                    string += letra
                elif event.key == 13:# presionar enter
                    #postcondicion string solo contiene elementos validos
                    try:
                        assert(patron2.match(string) != None or len(string) == 0)
                        return string
                    except:
                        print("Error en la lectura")
                elif event.key == 8 and len(string) > 0: #presionar backspace
                    string = string[:len(string)-1]
            elif event.type == KEYUP:
                if event.key == 304:
                    shift = False
                elif event.key == 301:
                    bloq_mayus = False
    #postcondicion true


#funcion que recibe un string del mensaje de la opcion
#y carga el sprite correspondiente y lo lleva a resolucion
#150x50
def formatearOpcion(opcion, x):
    #precondicion existe la imagen
    #postcondicion true
    try:
        return pygame.transform.scale(pygame.image.load("sources/sprites/" + opcion + ".png"), (x,50))
    except:
        print(opcion)
        return "no se encontro la imagen"


#funcion que dibuja un menu y sus opciones
def dibujarMenu(titulo, opciones, orientacion,xtitulo,ytitulo,xopcion,yopcion,xintro,yintro, longitud_opciones):
    #precondicion al menos debe haber 1 opcion y el titulo debe no ser nulo
    #todas las opciones no deben ser nulas, la orientacion es vertical o horizontal
    #xtitulo, ytitulo, xopcion, yopcion, xintro, yintro deben estar en 0 y 600
    try:
        assert(len(opciones) > 0 and titulo != "" and all(opcion != "" for opcion in opciones) and
               (orientacion == "vertical" or orientacion == "horizontal"))
        assert(xtitulo >=0 and xtitulo <= 600 and ytitulo >=0 and ytitulo <= 600 and xopcion >=0 and xopcion <= 600 and
               yopcion >= 0 and yopcion <= 600 and xintro >= 0 and xintro <= 600 and yintro >=0 and yintro <= 600)
    except:
        print("Error con los datos del menu")
        cerrar()
    titulo_menu = pygame.transform.scale(pygame.image.load("sources/sprites/" + titulo + ".png"), (400, 100))
    ventana.blit(titulo_menu, (xtitulo,ytitulo))
    imagenes = []
    for opcion in opciones:
            imagenes.append(formatearOpcion(opcion, longitud_opciones))
    for i in range(len(imagenes)):
        if orientacion == "vertical":
            ventana.blit(imagenes[i], (xopcion, yopcion + (i * 60)))
        else:
            ventana.blit(imagenes[i], (xopcion + (i * (longitud_opciones + longitud_opciones*0.05)), yopcion))
    introduzca_opcion = pygame.transform.scale(pygame.image.load("sources/sprites/introduceunaopcion.png"),(300, 50))
    ventana.blit(introduzca_opcion, (xintro,yintro))
    #postcondicion true

"""
Funcion que busca fichas en la direccion diagonal principal.
"""
def BusquedaDiagonalSimetrica(x_inicial, x_final, y_inicial, direccion, tablero):
    #Precondicion:
    #Postcondicion:
    distancia = abs(x_final-x_inicial)
    resultado = True
    if direccion == "positiva" and distancia+y_inicial <= 3:
        if tablero[x_final][y_inicial + distancia] == "" and resultado:
            resultado = False
        else:
            for i in range(1,distancia):
                if tablero[x_inicial+i][y_inicial+i] != "":
                    resultado = False
    elif direccion == "negativa" and y_inicial-distancia >= 0:
        if tablero[x_final][y_inicial - distancia] == "" and resultado:
            resultado = False
        else:
            for i in range(1,distancia):
                if tablero[x_inicial-i][y_inicial-i] != "":
                    resultado = False
    else:
        resultado = False
    return resultado


"""
Funcion que busca fichas en la direccion diagonal secundaria.
"""
def BusquedaDiagonalAsimetrica(x_inicial, x_final, y_inicial, direccion, tablero):
    #Precondicion:
    #Postcondicion:
    distancia = abs(x_final-x_inicial)
    resultado = True
    if direccion == "positiva" and y_inicial - distancia >= 0:
        if tablero[x_final][y_inicial - distancia] == "" and resultado:
            resultado = False
        else:
            for i in range(1,distancia):
                if tablero[x_inicial+i][y_inicial-i] != "":
                    resultado = False
    elif direccion == "negativa" and y_inicial + distancia <= 3:
        if tablero[x_final][y_inicial + distancia] == "" and resultado:
            resultado = False
        else:
            for i in range(1,distancia):
                if tablero[x_inicial-i][y_inicial+i] != "":
                    resultado = False
    else:
        resultado = False
    return resultado


def TrasponerMatriz(matriz):
    #precondicion true
    matriz_traspuesta = []
    for x in range(len(matriz)):
        matriz_traspuesta.append(['' for y in matriz[0]])
    for x in range(len(matriz)):
        for y in range(len(matriz[x])):
            matriz_traspuesta[y][x] = matriz[x][y]
    #postcondicion la matriz esta traspuesta
    assert(all(all(matriz_traspuesta[y][x] == matriz[x][y] for y in range(len(matriz))) for x in range(len(matriz))))
    return matriz_traspuesta

"""
funcion que busca fichas en la direccion vertical, tanto en la casilla objetivo como en las anteriores
(las fichas que se mueven vertical no pueden saltar otras fichas
retorna true si la ficha se puede mover hasta su objetivo y matar
retorna falso si no hay una ficha en la casilla objetivo y si hay fichas atravesadas en su camino.
"""
def BusquedaVertical(x, y_inicial, y_final, direccion, tablero):
    assert (((y_inicial < y_final and direccion == "arriba") or (y_inicial > y_final and direccion == "abajo")) and
            y_inicial >= 0 and y_inicial <= 3 and y_final >= 0 and y_final <= 3 and x >= 0 and x <= 3)
    tablero = TrasponerMatriz(tablero)
    if direccion == "arriba":
        return BusquedaHorizontal(y_inicial, y_final, x, "derecha", tablero)
    else:
        return BusquedaHorizontal(y_inicial, y_final, x, "izquierda", tablero)


""" funcion que busca fichas en la direccion horizontal, tanto en la casilla objetivo como en las anteriores
(las fichas que se mueven horizontalmente no pueden saltar otras fichas
retorna true si la ficha se puede mover hasta su objetivo y matar
retorna falso si no hay una ficha en la casilla objetivo y si hay fichas atravesadas en su camino """
def BusquedaHorizontal(x_inicial, x_final, y, direccion, tablero):
    """ precondicion: x_inicial menor x_final(si la direccion es a la derecha).
     x_inicial mayor x_final(si la direccion es a la izquierda). x_inicial, x_final, y deben estar entre 0 y 3,
    """
    assert(((x_inicial < x_final and direccion == "derecha") or (x_inicial > x_final and direccion == "izquierda")) and
           x_inicial >= 0 and x_inicial <= 3 and x_final >= 0 and x_final <= 3 and y >= 0 and y <= 3)
    resultado = True #inicializando valores
    if tablero[x_final][y] == "" and resultado:
        resultado = False
    if resultado and direccion == "derecha":
        for x in range(x_inicial + 1, x_final):
            if tablero[x][y] != "":
                resultado = False
    if resultado and direccion == "izquierda":
        for x in range(x_final + 1, x_inicial):
            if tablero[x][y] != "" and x > x_final:
                resultado = False
    # postcondicion
                #resultado debe ser true sino hay fichas de por medio y la casilla objetivo si tiene una ficha
                #resultado debe ser false si existe una ficha de por medio o si la casilla objetivo no tiene ficha
    assert((resultado and tablero[x_final][y] != "" and ((direccion == "izquierda" and
        all(tablero[x][y] == "" for x in range(x_final + 1, x_inicial))) or
            (direccion == "derecha" and all(tablero[x][y] == "" for x in range(x_inicial + 1, x_final))))) or
           (not resultado and (tablero[x_final][y] == "" or (direccion == "izquierda" and
        any(tablero[x][y] != "" for x in range(x_final + 1, x_inicial))) or (direccion == "derecha" and
        any(tablero[x][y] != "" for x in range(x_inicial + 1, x_final))))))
    return resultado


#Funcion que redibuja la interfaz
def DibujarInterfaz(tablero,titulomenu):
    #Precondicion: True
    DibujarTablero(tablero)
    ventana.blit(titulomenu, (100, 40))
    ventana.blit(imagenLeyenda, (360, 180))
    #Postcondicion: True

# funcion que controla cuando una ficha come a otra
def ComerFicha(tablero, ficha_asesina, x_origen, y_origen, x_objetivo, y_objetivo):
    #precondicion: el tablero en la casilla objetivo no puede estar vacio
    try:
        assert(tablero[x_objetivo][y_objetivo] != "")
    except:
        print("la casilla objetivo esta vacia")
        return tablero
    #postcondicion: la casilla objetivo es reescrita con la ficha asesina
    #assert(tablero[x_objetivo][y_objetivo] == ficha_asesina)
    MoverFicha(x_origen, y_origen, x_objetivo, y_objetivo, tablero, ficha_asesina)
    tablero[x_objetivo][y_objetivo] = ficha_asesina
    return tablero


def controlador_juego(tablero, dificultad):
    titulo_menu = pygame.transform.scale(pygame.image.load("sources/sprites/menujuego.png"), (400, 100))
    opciones_validas = ["1", "3", "4"]
    opciones = ["jugar"]
    if dificultad == 1 or dificultad == 4:
        opciones.append("deshacer")
        opciones_validas.append("2")
    opciones.append("pausar")
    opciones.append("terminar")
    if dificultad == 4:
        opciones.append("solucionar")
        opciones_validas.append("5")
    tableroviejo = tablero
    while True:
        print(tableroviejo)
        DibujarTablero(tablero)
        dibujarMenu("menujuego",  opciones, "horizontal", 100, 40, 20, 420, 20, 480, 100)
        ventana.blit(imagenLeyenda, (360, 180))
        pygame.display.update()
        opcion = Leer(285, 495, color_lectura, 1, 311, 514)
        #opcion = "1"
        if opcion not in opciones_validas:
            EntradaInvalida(imagenOpcioninvalida, 100,200, 1.5)
        if opcion == "5":
            EntradaInvalida(imagenEnConstruccion, 80,200,1.5)
        if opcion == "2":
            print("viejo",tableroviejo)
            tablero = tableroviejo
            print("nuevo",tablero)
            EntradaInvalida(imagenDeshacerJugada, 80, 200, 1.5)
        if opcion == "1":
            DibujarInterfaz(tablero,titulo_menu)
            ventana.blit(imagenIntroducirCasillas,(200,400))
            pygame.display.update()
            casilla_inicial = Leer(359, 461, (color_lectura), 2, 359+26, 461+21)
            valida = True
            if validarString(casilla_inicial, "Introducir Casilla"):
                casilla_inicialx=ord(casilla_inicial[0])-97
                casilla_inicialy=int(casilla_inicial[1])-1
                if tablero[casilla_inicialx][casilla_inicialy] == "":
                    valida = False
                    EntradaInvalida(imagenJugadaInvalida, 80, 200, 1.5)
            else:
                valida = False
                EntradaInvalida(imagenJugadaInvalida, 80, 200, 1.5)
            if valida:
                casilla_final = Leer(359, 470, (color_lectura), 2, 359+26, 470+21)
                if validarString(casilla_inicial, "Introducir Casilla"):
                    casilla_finalx=ord(casilla_final[0])-97
                    casilla_finaly=int(casilla_final[1])-1
                else:
                    valida = False
                    EntradaInvalida(imagenJugadaInvalida, 80, 200, 1.5)
                ficha = tablero[casilla_inicialx][casilla_inicialy]
                if (valida and
                ((ficha == "R" and (casilla_finalx,casilla_finaly) in PosicionesValidasRey(casilla_inicialx,casilla_inicialy,tablero))
                or ((ficha == "A" or ficha == "D") and
                (casilla_finalx,casilla_finaly) in (PosicionesValidasAlfil(casilla_inicialx,casilla_inicialy,tablero,False)))
                or ((ficha == "T" or ficha == "D")
                and (casilla_finalx,casilla_finaly) in (PosicionesValidasTorre(casilla_inicialx,casilla_inicialy,tablero)))
                or (ficha == "C"
                and (casilla_finalx,casilla_finaly) in (PosicionesValidasCaballo(casilla_inicialx,casilla_inicialy,tablero)))
                or (ficha == "P"
                and (casilla_finalx,casilla_finaly) in (PosicionesValidasAlfil(casilla_inicialx,casilla_inicialy,tablero,True))))):
                    tableroviejo = copy.deepcopy(tablero)
                    print("viejo dentro del if",tableroviejo)
                    tablero = ComerFicha(tablero,ficha,casilla_inicialx,casilla_inicialy,casilla_finalx,casilla_finaly)
                else:
                    EntradaInvalida(imagenJugadaInvalida, 80, 200, 1.5)
    cerrar()


#Funcion que maneja el menu de seleccionar nivel
def SeleccionarNivel():
    #Precondicion: True
    while True:
        ventana.blit(imagenFondo, (0, 0))
        dibujarMenu("seleccionarnivel", ["facil", "dificil", "muydificil", "entrenamiento", "volver"], "vertical",
                    100, 30, 200, 150, 150, 450, 200)
        pygame.display.update()
        opcion = Leer(415, 465, color_lectura, 1, 440, 486)
        #opcion = "1"
        if opcion == "5":
            break
        elif opcion == "1" or opcion == "2":
            nivel_valido = False
            while nivel_valido == False:
                nivel = IntroducirNivel()
                nivel_valido = validarString(nivel,"Introducir Nivel")
                if nivel_valido == False:
                    EntradaInvalida(imagenTableroInvalido, 100, 200, 1.5)
            tablero = MatrizDeString(nivel)
            controlador_juego(tablero, int(opcion))
        elif opcion == "3" or opcion == "4":
            EntradaInvalida(imagenEnConstruccion, 100,200, 1.5)
        else:
            EntradaInvalida(imagenOpcioninvalida, 100, 200, 1.5)

    #postcondicion true


#funcion que determina si un string es un nivel de valido o no
def validarString(string,menu) -> bool:
    #precondicion la string debe tener al menos un caracter
    assert(len(string) >= 0)
    lista = string.split("-")
    print(lista)
    #POSTCONDICION = la funcion debe retornar True si la string al separarla por -
    #se divide en substring de 2 o 3 caracteres, cuando tiene 2 caracteres el primero
    #debe ser una letra minuscula entra a..d y el segundo un numero del 1 al 4
    #y en caso de tener 3 caracteres el primero debe ser "R","T","C","A","D", el segundo
    #debe ser una letra minuscula de entra a..d y ultimo un numero del 1 al 4
    #en ambos casos se debe retornar True, sino se retorna falso
    #no deben haber mas de 2 peones,alfiles, caballos y torres, 1 sola reina y ajuro un rey
    try:
        assert(all(len(substring) >= 2  and len(substring) <=3 for substring in lista))
    except:
        print("Error de cantidad de caracteres en los substrings")
        return False
    contador_peones = 0
    contador_alfiles = 0
    contador_caballos = 0
    contador_rey = 0
    contador_reina = 0
    contador_torres = 0
    try:
        for substring in lista:
            if len(substring) == 2:
                assert(substring[0] in ["a","b","c","d"] and substring[1] in ["1", "2", "3", "4"])
                contador_peones += 1
            else:
                assert (substring[1] in ["a", "b", "c", "d"] and substring[2] in ["1", "2", "3", "4"] \
                        and substring[0] in ["R", "T", "C", "A", "D"])
                if substring[0] == "R":
                    contador_rey += 1
                elif substring[0] == "T":
                    contador_torres += 1
                elif substring[0] == "D":
                    contador_reina += 1
                elif substring[0] == "A":
                    contador_alfiles += 1
                elif substring[0] == "C":
                    contador_caballos += 1
        if menu == "Introducir Nivel":
            assert(contador_rey == 1 and  contador_reina <= 1 and contador_alfiles <= 2 and  contador_caballos <= 2 and
               contador_torres <= 2 and contador_peones <= 2)
            return True
        elif menu == "Introducir Casilla":
            return True
    except:
        print("Cantidad de carecteres no corresponde a los caracteres en el string")
        return False


#Funcion que maneja la confirmacion de salida
def ConfirmacionSalida():
    #Precondicion: True
    while True:
        ventana.blit(imagenFondo, (0, 0))
        dibujarMenu("salida", ["si", "no"], "horizontal", 100, 30, 112, 279, 138, 464, 200)
        pygame.display.update()
        opcion = Leer(403, 479, color_lectura, 1, 428, 500)
        #postcondicion opcion es 1 o 2
        if opcion == "1":
            cerrar()
        elif opcion == "2":
            break
        else:
            EntradaInvalida(imagenOpcioninvalida, 100, 250, 1.5)


def DibujarFicha(ficha, x, y):
    if ficha == "R":
        ventana.blit(imagenRey, (x,y))
    elif ficha == "D":
        ventana.blit(imagenReina, (x,y))
    elif ficha == "A":
        ventana.blit(imagenAlfil, (x,y))
    elif ficha == "C":
        ventana.blit(imagenCaballo, (x,y))
    elif ficha == "T":
        ventana.blit(imagenTorre, (x,y))
    elif ficha == "P":
        ventana.blit(imagenPeon, (x,y))


def DibujarTablero(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    ventana.blit(imagenFondo, (0,0))
    ventana.blit(imagenTablero, (x_fichas - 14, y_fichas - 90))
    for fila in range(filas):
        for columna in range(columnas):
            # se trabaja con la posicion columnas - columna para que se dubijen de arriba a abajo
            pos_columna = columnas - 1 - columna
            DibujarFicha(tablero[fila][pos_columna], x_fichas + (fila * cambio_x), y_fichas - (pos_columna * cambio_y))


# funcion que controla la animacion de mover una ficha de una casilla a otra, controlado en pixeles
def MoverFicha(fila, columna, filafinal, columnafinal, tablero, ficha):
    titulo_menu = pygame.transform.scale(pygame.image.load("sources/sprites/menujuego.png"), (400, 100))
    tiempo_inicio = pygame.time.get_ticks()
    tablero[fila][columna] = ""
    # precondicion x,y,xf,yf deben estar entre 0 y 600
    x = x_fichas + (fila * cambio_x)
    y = y_fichas - (columna * cambio_y)
    xf = x_fichas + (filafinal * cambio_x)
    yf = y_fichas - (columnafinal * cambio_y)
    assert(x >= 0 and x <= 600 and xf >= 0 and xf <= 600 and y >= 0 and y <= 600 and yf >= 0 and yf <= 600)
    i = 0
    while i <= 1:
        # cota i - 1 <= 0
        try:
            assert(i - 1 <= 0)
        except:
            print("El ciclo de la animacion se excedio de iteraciones")
        i += 0.005
        # parametrizacion de la recta entre el pixel inicial y el pixel final
        x_actual = (xf-x) * i + x
        y_actual = (yf - y) * i + y
        DibujarInterfaz(tablero,titulo_menu)
        DibujarFicha(ficha, x_actual, y_actual)
        pygame.display.update()
    # postcondicion True


def PosicionesValidasCaballo(xorigen, yorigen, tablero):
    posiciones_validas = []
    if xorigen >= 2 :
        if yorigen > 0 and tablero[xorigen - 2][yorigen - 1] != "":
            posiciones_validas.append((xorigen - 2, yorigen - 1))
        if yorigen < 3 and tablero[xorigen - 2][yorigen + 1] != "":
                posiciones_validas.append((xorigen - 2, yorigen + 1))
    if xorigen <= 1 :
        if yorigen > 0 and tablero[xorigen + 2][yorigen - 1] != "":
            posiciones_validas.append((xorigen + 2, yorigen - 1))
        if yorigen < 3 and tablero[xorigen + 2][yorigen + 1] != "":
            posiciones_validas.append((xorigen + 2, yorigen + 1))
    if yorigen >= 2 :
        if xorigen > 0 and tablero[xorigen - 1][yorigen - 2] != "":
            posiciones_validas.append((xorigen - 1, yorigen - 2))
        if xorigen < 3 and tablero[xorigen + 1][yorigen - 2] != "":
                posiciones_validas.append((xorigen + 1, yorigen - 2))
    if yorigen <= 1 :
        if xorigen > 0 and tablero[xorigen - 1][yorigen + 2] != "":
            posiciones_validas.append((xorigen - 1, yorigen + 2))
        if xorigen < 3 and tablero[xorigen + 1][yorigen + 2] != "":
            posiciones_validas.append((xorigen + 1, yorigen + 2))
    return posiciones_validas


def PosicionesValidasTorre(xorigen, yorigen, tablero):
    #Precondicion: True
    posiciones_validas = []
    for x in range(xorigen+1,4):
        if BusquedaHorizontal(xorigen, x, yorigen, "derecha", tablero):
            posiciones_validas.append((x, yorigen))
            break
    for x in range(xorigen):
        if BusquedaHorizontal(xorigen, x, yorigen, "izquierda", tablero):
            posiciones_validas.append((x, yorigen))
            break
    for y in range(yorigen):
        if BusquedaVertical(xorigen, yorigen, y, "abajo", tablero):
            posiciones_validas.append((xorigen,y))
            break
    for y in range(yorigen+1,4):
        if BusquedaVertical(xorigen, yorigen, y, "arriba", tablero):
            posiciones_validas.append((xorigen,y))
            break
    return posiciones_validas
    #Postcondicion: True



def PosicionesValidasAlfil(xorigen, yorigen, tablero, espeon):
    #Precondicion: True
    posiciones_validas = []
    if espeon:
        distanciamaxima = xorigen+2
        distanciamaxima2 = xorigen-2
    else:
        distanciamaxima = 4
        distanciamaxima2 = 0
    if  not espeon:
        for x in range(xorigen):
            if BusquedaDiagonalSimetrica(xorigen, x, yorigen, "negativa", tablero):
                posiciones_validas.append((x, yorigen - x + xorigen))
                break
        for x in range(xorigen + 1, 4):
            if BusquedaDiagonalAsimetrica(xorigen, x, yorigen, "positiva", tablero):
                posiciones_validas.append((x, yorigen - (x - xorigen)))
                break
    for x in range(xorigen+1,distanciamaxima):
        if BusquedaDiagonalSimetrica(xorigen, x, yorigen, "positiva", tablero):
            posiciones_validas.append((x, yorigen+x-xorigen))
            break
    for x in range(distanciamaxima2,xorigen):
        if BusquedaDiagonalAsimetrica(xorigen, x, yorigen, "negativa", tablero):
            posiciones_validas.append((x, yorigen+xorigen-x))
            break
    return posiciones_validas
    #Postcondicion: True


def PosicionesValidasRey(xorigen,yorigen,tablero):
    #Precondicion:
    posiciones_validas = []
    if yorigen != 0:
        yinicio = yorigen-1
    else:
        yinicio = yorigen
    if yorigen != 3:
        yfin = yorigen+2
    else:
        yfin = yorigen+1
    for y in range(yinicio,yfin):
        if xorigen != 0 and tablero[xorigen - 1][y] != "":
            posiciones_validas.append((xorigen - 1, y))
        if xorigen != 3 and tablero[xorigen+1][y] != "":
            posiciones_validas.append((xorigen + 1, y))
        if y != yorigen and tablero[0][y] != "":
            posiciones_validas.append((0,y))
    return posiciones_validas
    #Postcondicion


# funcion que maneja la pantalla en la que el usuario introduce el nivel desde el teclado
def IntroducirNivel():
    # Precondicion: True
    imagenNivel = pygame.transform.scale(pygame.image.load("sources/sprites/configurartablero.png"), (400,200))
    while True:
        ventana.blit(imagenFondo, (0, 0))
        ventana.blit(imagenTitulo, (150, 20))
        ventana.blit(imagenTexto, (10, 396))
        ventana.blit(imagenNivel, (100, 180))
        pygame.display.update()
        nivel = Leer(23, 407, color_lectura, 40, 580,431)
        #nivel = "Cd1-b1-c2-Ra2"
        #postcondicion nivel no es vacio
        try:
            assert(len(nivel) > 0)
        except:
            print("Debe haber al menos un caracter en el nivel")
        return nivel

#funcion que dado un string de nivel, retorna una matriz con el tablero
#equivalente al string
def MatrizDeString(string):
    #precondicion True
    matriz = [["" for x in range(4)] for i in range(4)]
    lista = string.split("-")
    for substring in lista:
        if len(substring) == 3:
            if substring[1] == "a":
                matriz[0][int(substring[2]) - 1] = substring[0]
            elif substring[1] == "b":
                matriz[1][int(substring[2]) - 1] = substring[0]
            elif substring[1] == "c":
                matriz[2][int(substring[2]) - 1] = substring[0]
            else:
                matriz[3][int(substring[2]) - 1] = substring[0]
        else:
            if substring[0] == "a":
                matriz[0][int(substring[1]) - 1] = "P"
            elif substring[0] == "b":
                matriz[1][int(substring[1]) - 1] = "P"
            elif substring[0] == "c":
                matriz[2][int(substring[1]) - 1] = "P"
            else:
                matriz[3][int(substring[1]) - 1] = "P"
    #postcondicion true
    return matriz

#funcion que maneja el menu principal
def MenuPrincipal():
    #precondicion true
    #mostrar opciones al usuario
    while True:
        ventana.blit(imagenFondo, (0,0))
        ventana.blit(imagenTitulo, (150, 20))
        dibujarMenu("menuprincipal", ["partidanueva", "cargarpartida", "mostrarrecords", "salirjuego"], "vertical",
                    100, 180, 200, 300, 150, 540, 200)
        pygame.display.update()
        opcion = Leer(415,555, color_lectura,1,440,575)
        #opcion = "1"
        if opcion == "1":
            SeleccionarNivel()
        elif opcion == "2":
            EntradaInvalida(imagenEnConstruccion, 80, 200, 2)
        elif opcion == "3":
            EntradaInvalida(imagenEnConstruccion, 800, 200, 2)
        elif opcion == "4":
            ConfirmacionSalida()
        else:
            EntradaInvalida(imagenOpcioninvalida, 100,300, 1.5)
        # post condicion true

def FormatearFicha(imagen):
    return pygame.transform.scale(imagen, (50,90))


#funcion que nuestra el mensaje de entrada invalida correspondiente a la entrada en la que se equivoco el usuario
def EntradaInvalida(imagen, x,y, tiempo):
    ventana.blit(imagen, (x,y))
    pygame.display.update()
    time.sleep(tiempo)

#Funcion que indica al usuario como realizar sus acciones.
def MostrarTutorial():
    #Precondicion: True
    ventana.blit(imagenFondo, (0,0))
    ventana.blit(imagenTitulo, (150, 20))
    ventana.blit(imagenTutorial, (100, 200))
    pygame.display.update()
    time.sleep(0)
    #Postcondicion: True

pygame.init()
color_cielo = pygame.Color(25,158,218)
color_lectura = pygame.Color(147, 55, 120)
ventana = pygame.display.set_mode((600,600))
pygame.display.set_caption("Solitaire Chess")
direccion_imagenes = "sources/sprites/"
imagenTitulo = pygame.transform.scale(pygame.image.load(direccion_imagenes + "title.png"), (300,150))
imagenFondo = pygame.image.load(direccion_imagenes + "fondo.jpg")
imagenTexto = pygame.image.load(direccion_imagenes + "cuadrodetexto.png")
imagenTablero = pygame.image.load(direccion_imagenes + "tablero.jpg")
imagenRey = FormatearFicha(pygame.image.load(direccion_imagenes + "rey.png"))
imagenAlfil = FormatearFicha(pygame.image.load(direccion_imagenes + "alfil.png"))
imagenReina = FormatearFicha(pygame.image.load(direccion_imagenes + "reina.png"))
imagenCaballo = FormatearFicha(pygame.image.load(direccion_imagenes + "caballo.png"))
imagenTorre = FormatearFicha(pygame.image.load(direccion_imagenes + "torre.png"))
imagenPeon = FormatearFicha(pygame.image.load(direccion_imagenes + "peon.png"))
imagenOpcioninvalida = pygame.image.load(direccion_imagenes + "opcioninvalida.png")
imagenEnConstruccion = pygame.image.load(direccion_imagenes + "enconstruccion.png")
imagenTableroInvalido = pygame.image.load(direccion_imagenes + "tableroinvalido.png")
imagenTutorial = pygame.image.load(direccion_imagenes + "tutorial.png")
imagenLeyenda =  pygame.transform.scale(pygame.image.load(direccion_imagenes + "leyenda.png"), (220,150))
imagenIntroducirCasillas = pygame.transform.scale(pygame.image.load(direccion_imagenes + "introducircasillas.png"), (200,100))
imagenJugadaInvalida = pygame.transform.scale(pygame.image.load(direccion_imagenes + "jugadainvalida.png"), (300,200))
imagenDeshacerJugada = pygame.transform.scale(pygame.image.load(direccion_imagenes + "deshacerjugada.png"), (300,200))
fuente = pygame.font.Font(None, 28)


######cambiar los valores de estas variables
#####para mover el tablero en la pantalla
x_fichas = 44
cambio_x = 76 #valor original 76
y_fichas = 270
cambio_y = 50 #valor original 50


MostrarTutorial()
MenuPrincipal()