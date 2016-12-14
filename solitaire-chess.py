import pygame, sys, re, time, copy
import datetime, random
from pygame.locals import *
random.seed

shift = False #variable booleana que indica el estado de la tecla shift
bloq_mayus = False #variable booleana que indica el estado de la tecla bloq mayus del teclado

#funcion que cierra pygame y cierra el programa
def cerrar():
    #precondicion true
    pygame.quit()
    sys.exit()
    # postcondicion true

#Funcion que muestra el cronometro de la partida.
def dibujarCronometro():
    ventana.blit(imagenFondoCronometro, (360,340))
    numeros = ["Cero","Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis", "Siete", "Ocho", "Nueve"]
    global tiempo_actual
    segundos = tiempo_actual%60
    string_segundos = str(segundos)
    if segundos < 10:
        string_segundos = "0" + str(segundos)
    string_del_tiempo = str(int(tiempo_actual/60)) + ":" + string_segundos
    for caracter in range(len(string_del_tiempo)):
        if string_del_tiempo[caracter] != ":":
            eval("ventana.blit(imagen" + numeros[int(string_del_tiempo[caracter])] + ", (370 + caracter*25,345))" )
        else:
            ventana.blit(imagenDospuntos, (366 + caracter*40,345))
    pygame.display.update()


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
    global shift
    global bloq_mayus
    global tiempo_maximo
    global tiempo_actual
    global contar_tiempo
    while True:#
        pygame.display.update()
        pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
        texto = fuente.render(string, 1, (255, 120, 255))
        ventana.blit(texto, (x + 7, y + 1))
        global tiempo_viejo
        global tiempo
        if contar_tiempo and int(tiempo_viejo) < pygame.time.get_ticks()/1000:
            dibujarCronometro()
            tiempo_viejo += 1
            tiempo += 1
            tiempo_actual = tiempo_maximo - tiempo
            if tiempo_actual <= -1:
                return "perdida_por_tiempo"
        elif not contar_tiempo and int(tiempo_viejo) < pygame.time.get_ticks()/1000:
            tiempo_viejo += 1
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


#Funcion que se encarga de pausar el juego cuando el usuario asi lo desee.
def pausar_juego():
    #Precondicion: True
    global tiempo_viejo
    global contar_tiempo
    contar_tiempo = False
    ventana.blit(imagenFondo,(0,0))
    dibujarMenu("juegopausado", ["continuar"], "vertical", 100, 20, 238, 270, 142, 480, 100)
    pygame.display.update()
    while True:
        opcion = Leer(408, 494, color_lectura, 1, 432, 515)
        if opcion == "1":
            contar_tiempo = True
            break
        else:
            print("opcion invalida")
    #Postcondicion: True


#Funcion que redibuja la interfaz
def DibujarInterfaz(tablero,titulomenu):
    #Precondicion: True
    DibujarTablero(tablero)
    ventana.blit(titulomenu, (100, 20))
    ventana.blit(imagenLeyenda, (360, 190))
    ventana.blit(pygame.image.load(direccion_imagenes + "cuadronombre.png"), (360, 124))
    rectangulo = pygame.Rect(381, 143, 186, 24)
    pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
    texto = fuente.render(nombre_jugador, 1, (255, 120, 255))
    ventana.blit(texto, (385, 145))
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

#Funcion que dada una lista de fichas en el tablero determina si el jugador gano la partida.
def VerificarGanador(fichasdeltablero) -> bool:
    victoria = False
    #Precondicion: True
    if len(fichasdeltablero) == 1:
        victoria = True
    #Postcondicion:
    assert((len(fichasdeltablero) == 1 and victoria) or (len(fichasdeltablero) !=1 and victoria == False))
    return victoria

#Funcion que dado un tablero verifica si el jugador ha perdido la partida.
def VerificarPerdedor(tablero) -> bool:
    posiciones_validas=[]
    perdedor = False
    #Precondicion: True
    for x in range(4):
        for y in range(4):
            if tablero[x][y] != "":
                if tablero[x][y] == "P":
                    posiciones_validas = posiciones_validas + PosicionesValidasAlfil(x, y, tablero, True)
                if tablero[x][y] == "A" or tablero[x][y] == "D":
                    posiciones_validas = posiciones_validas + PosicionesValidasAlfil(x, y, tablero, False)
                if tablero[x][y] == "T" or tablero[x][y] == "D":
                    posiciones_validas = posiciones_validas + PosicionesValidasTorre(x, y, tablero)
                if tablero[x][y] == "R":
                    posiciones_validas = posiciones_validas + PosicionesValidasRey(x, y, tablero)
                if tablero[x][y] == "C":
                    posiciones_validas = posiciones_validas + PosicionesValidasCaballo(x, y, tablero)
    if len(posiciones_validas) == 0:
        perdedor = True
        #Postcondicion:
        assert((perdedor and len(posiciones_validas) == 0) or (perdedor == False and any(x in posiciones_validas)))
    return perdedor


#funcion que genera un string de una matriz tablero
def StringDeTablero(tablero):
    string = ""
    cantidad_fichas = len([x for y in tablero for x in y if x != ""])
    contador_fichas_agregadas = 0
    for x in range(len(tablero)):
        for y in range(len(tablero)):
            if tablero[x][y] != "":
                if tablero[x][y] != "P":
                    string += tablero[x][y] + chr(x + 97) + str(y + 1)
                else:
                    string += chr(x + 97) + str(y + 1)
                contador_fichas_agregadas += 1
                if contador_fichas_agregadas < cantidad_fichas:
                    string += "-"
    return string

#Funcion que escribe informacion acerca de una partida guardada
def EscribirEnArchivoPartidaGuardada(string):
    with open("sources/files/partidasguardadas.txt", "a") as archivoSalida:
        archivoSalida.write(string)

#Funcion que lee informacion de un archivo
def LeerArchivo(nombre):
    with open("sources/files/" + nombre + ".txt", "r") as archivoEntrada:
        lineas = archivoEntrada.readlines()
    for x in range(len(lineas)):
        lineas[x] = lineas[x].split("\n")[0]
    return lineas


#Funcion que muestra menu de guardar partida y ejecuta esta accion en caso de que el usuario asi lo desee
def GuardarPartida(tablero, dificultad):
    #Precondicion: True
    dificultades = ["facil", "dificil", "muy_dificil", "entrenamiento"]
    global tiempo_actual
    fecha_actual = datetime.datetime.now()
    while True:
        ventana.blit(imagenFondo, (0, 0))
        dibujarMenu("GuardarPartida", ["si", "no"], "horizontal", 100, 50, 112, 279, 138, 464, 200)
        pygame.display.update()
        global partidas_ganadas
        opcion = Leer(403, 479, color_lectura, 1, 428, 500)
        if opcion == "1":
            partida_string =  StringDeTablero(tablero)
            partidas_guardadas = LeerArchivo("partidasguardadas")
            string = "Partida:" + str(len(partidas_guardadas) + 1) + " FECHA:" + str(fecha_actual.day) + "/" +\
                str(fecha_actual.month) + "/" + str(fecha_actual.year) + " " + "TIEMPO:" + str(tiempo_actual) +\
                " " + dificultades[dificultad - 1] + " " + partida_string + " " + nombre_jugador
            if dificultad == 3:
                string += "victorias:" + str(partidas_ganadas)
            string += "\n"
            EscribirEnArchivoPartidaGuardada(string)
            break
        elif opcion == "2":
            break
        else:
            MostrarMensaje(imagenOpcioninvalida, 100, 250, 1.5)
    #Postcondicion: True


#Funcion que dado un string carga una partida.
def parsearPartidaGuardada(partida):
    #Precondicion: True
    partida_lista = partida.split(" ")
    resultado = []
    tiempo = int(partida_lista[2].split(":")[1])
    resultado.append(tiempo)
    if partida_lista[3] == "dificil":
        resultado.append(2)
    if partida_lista[3] == "facil":
        resultado.append(1)
    if partida_lista[3] == "muy_dificil":
        resultado.append(3)
    if partida_lista[3] == "entrenamiento":
        resultado.append(4)
    resultado.append(MatrizDeString(partida_lista[4]))
    resultado.append(partida_lista[1].split(":")[1])
    resultado.append(partida_lista[0].split(":")[1])
    resultado.append(partida_lista[5])
    if partida_lista[3] == "muy_dificil":
        resultado.append(partida_lista[6].split(":")[1])
    return resultado
    #Postcondicion: True

#Funcion que dibuja el menu de cargar partida
def MenuCargar():
    #Precondicion: True
    partidas_cargadas = LeerArchivo("partidasguardadas")
    contador = 0
    while contador <= len(partidas_cargadas):
        #Cota: len(partidas_cargadas) - contador
        opciones = []
        if contador > 0:
            opciones.append("anteriores")
        opciones.append("seleccionar")
        if contador < len(partidas_cargadas) - 1:
            opciones.append("siguientes")
        opciones.append("volver")
        partida_seleccionada = parsearPartidaGuardada(partidas_cargadas[contador])
        numero_partida = fuente_prueba.render("Partida: " + partida_seleccionada[4], 1, (255, 120, 255))
        tiempo_partida = fuente_prueba.render("Tiempo restante: " + str(partida_seleccionada[0]), 1, (255, 120, 255))
        fecha_partida = fuente_prueba.render("Fecha: " + str(partida_seleccionada[3]), 1, (255, 120, 255))
        jugador_partida = fuente_prueba.render("Jugador: " + partida_seleccionada[5], 1, (255, 120, 255))
        if partida_seleccionada[1] == 2:
            string_dificultad = "dificil"
        if partida_seleccionada[1] == 1:
            string_dificultad = "facil"
        if partida_seleccionada[1] == 3:
            string_dificultad = "muy dificil"
            global partidas_ganadas
            partidas_ganadas = int(partida_seleccionada[6])
            ganadas_partida = fuente_prueba.render("Victorias: " + str(partidas_ganadas) + "/3", 1, (255,120,255))
        if partida_seleccionada[1] == 4:
            string_dificultad = "entrenamiento"
        dificultad_partida = fuente_prueba.render("Dificultad: " + string_dificultad, 1, (255, 120, 255))
        rectangulo = pygame.Rect(149, 176, 309, 205)
        ventana.blit(imagenFondo, (0, 0))
        dibujarMenu("cargarpartidatitulo", opciones, "horizontal", 100, 20, 30, 440, 150, 500, 130)
        ventana.blit(imagenPizarra, (100,140))
        pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
        ventana.blit(numero_partida, (152, 179))
        ventana.blit(tiempo_partida, (320,179))
        ventana.blit(dificultad_partida, (152, 195))
        ventana.blit(fecha_partida, (320, 195))
        ventana.blit(jugador_partida, (320, 210))
        if partida_seleccionada[1] == 3:
            ventana.blit(ganadas_partida, (152, 210))
        DibujarTablero_miniatura(partida_seleccionada[2])
        pygame.display.update()
        opcion = Leer(416,514,color_lectura,1, 440, 534)
        if opcion == "5":
            break
        elif opcion == "2" and contador < len(partidas_cargadas) - 1 :
            contador += 1
        elif opcion == "0" and (contador - 1) >= 0:
            contador -= 1
        elif opcion == "1":
            if partida_seleccionada[1] == 1:
                tiempo_final = 180
            elif partida_seleccionada[1] == 2:
                tiempo_final = 90
            elif partida_seleccionada[1] == 3:
                tiempo_final = 120
            elif partida_seleccionada[1] == 4:
                tiempo_final = 2
            controlador_juego(partida_seleccionada[2],partida_seleccionada[1],partida_seleccionada[0], tiempo_final)
        else:
            MostrarMensaje(imagenOpcioninvalida, 100, 250, 1.5)
    #Postcondicion: True


#Funcion que dado un tablero solicita al usuario una posicion y devuelve una solucion.
def EncontrarPosicionValida(tablero, titulo_menu):
    #Precondicion: True
    while True:
        DibujarInterfaz(tablero, titulo_menu)
        ventana.blit(imagenCasillaInicial, (200, 410))
        pygame.display.update()
        casilla_inicial = Leer(354, 467, (color_lectura), 2, 388, 498)
        valida = True
        if validarString(casilla_inicial, "Introducir Casilla"):
            casilla_inicialx = ord(casilla_inicial[0]) - 97
            casilla_inicialy = int(casilla_inicial[1]) - 1
            if tablero[casilla_inicialx][casilla_inicialy] == "":
                valida = False
                MostrarMensaje(imagenJugadaInvalida, 80, 200, 1.5)
        else:
            valida = False
            MostrarMensaje(imagenJugadaInvalida, 80, 200, 1.5)
        ficha = tablero[casilla_inicialx][casilla_inicialy]
        if valida and ficha == "R":
            posiciones_validas = PosicionesValidasRey(casilla_inicialx, casilla_inicialy, tablero)
            if len(posiciones_validas) > 0:
                return posiciones_validas[random.randint(0,len(posiciones_validas)-1)]
        if valida and (ficha == "A" or ficha == "D"):
            posiciones_validas = PosicionesValidasAlfil(casilla_inicialx, casilla_inicialy, tablero, False)
            if len(posiciones_validas) > 0:
                return posiciones_validas[random.randint(0, len(posiciones_validas)-1)]
        if valida and (ficha == "T" or ficha == "D"):
            posiciones_validas = PosicionesValidasTorre(casilla_inicialx, casilla_inicialy, tablero)
            if len(posiciones_validas) > 0:
                return posiciones_validas[random.randint(0, len(posiciones_validas)-1)]
        if valida and ficha == "C":
            posiciones_validas = PosicionesValidasCaballo(casilla_inicialx, casilla_inicialy, tablero)
            if len(posiciones_validas) > 0:
                return posiciones_validas[random.randint(0, len(posiciones_validas)-1)]
        if valida and ficha == "P":
            posiciones_validas = PosicionesValidasAlfil(casilla_inicialx, casilla_inicialy, tablero, True)
            if len(posiciones_validas) > 0:
                return posiciones_validas[random.randint(0, len(posiciones_validas)-1)]
        return None



#Funcion que muestra el menu de terminar una partida
def TerminarPartida(tablero, dificultad):
    #Precondicion: True
    while True:
        ventana.blit(imagenFondo, (0, 0))
        dibujarMenu("TerminarPartida", ["si", "no"], "horizontal", 100, 50, 112, 279, 138, 464, 200)
        pygame.display.update()
        global contar_tiempo
        contar_tiempo = False
        opcion = Leer(403, 479, color_lectura, 1, 428, 500)
        if opcion == "1":
            GuardarPartida(tablero, dificultad)
            return True
        elif opcion == "2":
            contar_tiempo = True
            break
        else:
            MostrarMensaje(imagenOpcioninvalida, 100, 250, 1.5)
    #Postcondicion: True


def controlador_juego(tablero, dificultad, tiempoinicial, tiempofinal):
    titulo_menu = pygame.transform.scale(pygame.image.load("sources/sprites/menujuego.png"), (400, 100))
    opciones_validas = ["1", "4"]
    opciones = ["jugar"]
    ganador = False
    perdedor = False
    ayuda = False
    posicion_valida = []
    global partidas_ganadas
    # configuraciones de dificultad
    if dificultad == 1 or dificultad == 4:
        opciones.append("deshacer")
        opciones_validas.append("2")
    if dificultad != 4:
        opciones.append("pausar")
        opciones_validas. append ("3")
    opciones.append("terminar")
    if dificultad == 4:
        opciones.append("solucionar")
        opciones_validas.append("5")
    tableroviejo = tablero
    salir = False
    #configuraciones del tiempo
    global tiempo_maximo
    global contar_tiempo
    contar_tiempo = True
    if dificultad == 4:
        contar_tiempo = False
    tiempo_maximo = tiempofinal
    global tiempo
    tiempo = tiempo_maximo - tiempoinicial
    global tiempo_viejo
    tiempo_viejo = pygame.time.get_ticks() / 1000
    global tiempo_actual
    while True:
        tiempo_actual = tiempo_maximo - tiempo
        perdedor = VerificarPerdedor(tablero)
        DibujarTablero(tablero)
        dibujarMenu("menujuego",  opciones, "horizontal", 100, 20, 20, 420, 20, 480, 100)
        ventana.blit(pygame.image.load(direccion_imagenes + "cuadronombre.png"), (360, 124))
        ventana.blit(imagenLeyenda, (360, 190))
        rectangulo = pygame.Rect(381, 143, 186, 24)
        pygame.display.update()
        pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
        texto = fuente.render(nombre_jugador, 1, (255, 120, 255))
        ventana.blit(texto, (385,145))
        if ayuda:
            if posicion_valida != None:
                ventana.blit(pygame.image.load(direccion_imagenes + "cuadronombre.png"), (360, 345))
                rectangulo = pygame.Rect(382, 364, 186, 24)
                pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
                texto = fuente.render("Solucion: " + chr(posicion_valida[0] + 97) + str(posicion_valida[1] + 1), 1, (255, 120, 255))
                ventana.blit(texto, (385, 368))
            else:
                ventana.blit(pygame.image.load(direccion_imagenes + "cuadronombre.png"), (360, 345))
                rectangulo = pygame.Rect(382, 364, 186, 24)
                pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
                texto = fuente.render("Solucion: -", 1, (255, 120, 255))
                ventana.blit(texto, (385, 368))
            ayuda = False
        pygame.display.update()
        if perdedor:
            bgm.stop()
            lose.play()
            MostrarMensaje(imagenDerrota, 130, 100, 6)
            bgm.play(-1)
            contar_tiempo = False
            break
        opcion = Leer(285, 495, color_lectura, 1, 311, 514)
        if opcion == "perdida_por_tiempo":
            MostrarMensaje(imagenDerrota, 130, 100, 5)
            contar_tiempo = False
            break
        if opcion not in opciones_validas:
            MostrarMensaje(imagenOpcioninvalida, 100,200, 1.5)
        if opcion == "4":
            salir = TerminarPartida(tablero, dificultad)
        if opcion == "5" and "5" in opciones_validas:
            ayuda = True
            posicion_valida = EncontrarPosicionValida(tablero, titulo_menu)
        if opcion == "3" and "3" in opciones_validas:
            pausar_juego()
        if opcion == "2" and "2" in opciones_validas:
            tablero = tableroviejo
            MostrarMensaje(imagenDeshacerJugada, 80, 200, 1.5)
        if opcion == "1":
            DibujarInterfaz(tablero,titulo_menu)
            ventana.blit(imagenIntroducirCasillas,(200,410))
            pygame.display.update()
            casilla_inicial = Leer(354, 446, (color_lectura), 2, 354+33, 446+20)
            valida = True
            if validarString(casilla_inicial, "Introducir Casilla"):
                casilla_inicialx=ord(casilla_inicial[0])-97
                casilla_inicialy=int(casilla_inicial[1])-1
                if tablero[casilla_inicialx][casilla_inicialy] == "":
                    valida = False
                    MostrarMensaje(imagenJugadaInvalida, 80, 200, 1.5)
            else:
                valida = False
                MostrarMensaje(imagenJugadaInvalida, 80, 200, 1.5)
            if valida:
                casilla_final = Leer(354, 480, (color_lectura), 2, 354+34, 480+21)
                if validarString(casilla_final, "Introducir Casilla"):
                    casilla_finalx=ord(casilla_final[0])-97
                    casilla_finaly=int(casilla_final[1])-1
                else:
                    valida = False
                    MostrarMensaje(imagenJugadaInvalida, 80, 200, 1.5)
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
                    tablero = ComerFicha(tablero,ficha,casilla_inicialx,casilla_inicialy,casilla_finalx,casilla_finaly)
                else:
                    MostrarMensaje(imagenJugadaInvalida, 80, 200, 1.5)
            fichas_del_tablero = [x for y in tablero for x in y if x != ""]
            ganador = VerificarGanador(fichas_del_tablero)
            if ganador and dificultad != 3:
                time.sleep(1)
                bgm.stop()
                win.play()
                MostrarMensaje(imagenVictoria, 40, 100, 6)
                bgm.play(-1)
                contar_tiempo = False
                if dificultad != 4:
                    Controlador_Records(dificultad)
                break
            if ganador and dificultad == 3 and partidas_ganadas < 2:
                partidas_ganadas += 1
                partidas_desafio = LeerArchivo("cartasdesafio")
                tablero = MatrizDeString(partidas_desafio[random.randint(0,len(partidas_desafio)-1)])
                controlador_juego(tablero, 3, tiempo_actual, 120)
                break
            if ganador and dificultad == 3 and partidas_ganadas == 2:
                MostrarMensaje(imagenVictoria, 40, 100, 5)
                Controlador_Records(dificultad)
                contar_tiempo = False
                break
        if salir:
            break


#Funcion que maneja el menu de seleccionar nivel
def SeleccionarNivel():
    #Precondicion: True
    while True:
        opcion_entrada = ""
        ventana.blit(imagenFondo, (0, 0))
        dibujarMenu("seleccionarnivel", ["facil", "dificil", "muydificil", "entrenamiento", "volver"], "vertical",
                    100, 30, 200, 150, 150, 450, 200)
        pygame.display.update()
        opcion = Leer(415, 465, color_lectura, 1, 440, 486)
        if opcion == "5":
            break
        elif opcion == "1" or opcion == "2" or opcion == "4" or opcion == "3":
            if opcion != "3":
                while True:
                    ventana.blit(imagenFondo, (0, 0))
                    dibujarMenu("metododeentrada", ["teclado", "cartadesafio","volver"], "vertical", 100, 30, 200, 200, 150, 450, 200)
                    opcion_entrada = Leer(415, 465, color_lectura, 1, 440, 486)
                    pygame.display.update()
                    if opcion_entrada != "1" and opcion_entrada != "2" and opcion_entrada != "5":
                        MostrarMensaje(imagenOpcioninvalida, 100, 200, 1.5)
                    else:
                        break
            if opcion_entrada == "1":
                nivel_valido = False
                while nivel_valido == False:
                    nivel = IntroducirNivel()
                    nivel_valido = validarString(nivel,"Introducir Nivel")
                    if nivel_valido == False:
                        MostrarMensaje(imagenTableroInvalido, 50, 200, 1.5)
                tablero = MatrizDeString(nivel)
            if opcion_entrada == "2":
                tablero = MenuCartaDesafio()
            if opcion == "1" and opcion_entrada != "5": #Facil
                controlador_juego(tablero, int(opcion), 180, 180)
            elif opcion == "2" and opcion_entrada != "5": #Dificil
                controlador_juego(tablero, int(opcion), 90, 90)
            elif opcion == "4" and opcion_entrada != "5": #Entrenamiento
                controlador_juego(tablero, int(opcion), 2, 2)
            elif opcion == "3": #Muy dificil
                global partidas_ganadas
                partidas_ganadas = 0
                tablero = MatrizDeString(LeerArchivo("cartasdesafio")[random.randint(0,len(LeerArchivo("cartasdesafio")) - 1)])
                controlador_juego(tablero, int(opcion), 120, 120)
        else:
            MostrarMensaje(imagenOpcioninvalida, 100, 200, 1.5)
    #postcondicion true


#Funcion que dibuja el menu de seleccionar carta de desafio
def MenuCartaDesafio():
    # Precondicion: True
    partidas_desafio = LeerArchivo("cartasdesafio")
    contador = 0
    while contador <= len(partidas_desafio):
        # Cota: len(partidas_desafio) - contador
        opciones = []
        if contador > 0:
            opciones.append("anteriores")
        opciones.append("seleccionar")
        if contador < len(partidas_desafio) - 1:
            opciones.append("siguientes")
        partida_seleccionada = partidas_desafio[contador]
        rectangulo = pygame.Rect(149, 176, 309, 205)
        ventana.blit(imagenFondo, (0, 0))
        dibujarMenu("seleccionardesafio", opciones, "horizontal", 100, 20, 100, 440, 150, 500, 130)
        ventana.blit(imagenPizarra, (100, 140))
        pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
        DibujarTablero_miniatura(MatrizDeString(partida_seleccionada))
        pygame.display.update()
        opcion = Leer(416, 514, color_lectura, 1, 440, 534)
        if opcion == "2" and (contador + 1) < len(partidas_desafio):
            contador += 1
        elif opcion == "0" and (contador - 1) >= 0:
            contador -= 1
        elif opcion == "1":
            return MatrizDeString(partida_seleccionada)
        else:
            MostrarMensaje(imagenOpcioninvalida, 100, 250, 1.5)
        # Postcondicion: True


#funcion que determina si un string es un nivel de valido o no
def validarString(string,menu) -> bool:
    #precondicion la string debe tener al menos un caracter
    assert(len(string) >= 0)
    lista = string.split("-")
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
            assert(contador_rey <= 1 and  contador_reina <= 1 and contador_alfiles <= 2 and  contador_caballos <= 2 and
               contador_torres <= 2 and contador_peones <= 2 and len(lista)>=2)
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
            MostrarMensaje(imagenOpcioninvalida, 100, 250, 1.5)


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

def DibujarFichamMiniatura(ficha, x, y):
    if ficha == "R":
        ventana.blit(imagenReymini, (x,y))
    elif ficha == "D":
        ventana.blit(imagenReinamini, (x,y))
    elif ficha == "A":
        ventana.blit(imagenAlfilmini, (x,y))
    elif ficha == "C":
        ventana.blit(imagenCaballomini, (x,y))
    elif ficha == "T":
        ventana.blit(imagenTorremini, (x,y))
    elif ficha == "P":
        ventana.blit(imagenPeonmini, (x,y))


#Funcion que dado un tablero lo dibuja en la interfaz grafica.
def DibujarTablero(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    ventana.blit(imagenFondo, (0,0))
    ventana.blit(imagenTablero, (x_fichas - 34, y_fichas - 70))
    for fila in range(filas):
        for columna in range(columnas):
            # se trabaja con la posicion columnas - columna para que se dubijen de arriba a abajo
            pos_columna = columnas - 1 - columna
            DibujarFicha(tablero[fila][pos_columna], x_fichas + (fila * cambio_x), y_fichas - (pos_columna * cambio_y))


#Funcion que dado un tablero dibuja su version en miniatura.
def DibujarTablero_miniatura(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    imagentablero =  pygame.transform.scale(pygame.image.load(direccion_imagenes + "tablero.png"), (310,150))
    ventana.blit(imagentablero, (x_miniatura - 40, y_miniatura - 84))
    for fila in range(filas):
        for columna in range(columnas):
            # se trabaja con la posicion columnas - columna para que se dibujen de arriba a abajo
            pos_columna = columnas - 1 - columna
            DibujarFichamMiniatura(tablero[fila][pos_columna], x_miniatura + (fila * cambiomin_x),
                                   y_miniatura - (pos_columna * cambiomin_y))


# funcion que controla la animacion de mover una ficha de una casilla a otra, controlado en pixeles
def MoverFicha(fila, columna, filafinal, columnafinal, tablero, ficha):
    titulo_menu = pygame.transform.scale(pygame.image.load("sources/sprites/menujuego.png"), (400, 100))
    tiempo_inicio = pygame.time.get_ticks()
    tablero[fila][columna] = ""
    # precondicion x,y,xf,yf deben estar entre 0 y 600
    global tiempo_viejo
    x = x_fichas + (fila * cambio_x)
    y = y_fichas - (columna * cambio_y)
    xf = x_fichas + (filafinal * cambio_x)
    yf = y_fichas - (columnafinal * cambio_y)
    tiempo_viejo = pygame.time.get_ticks()/1000
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
        if contar_tiempo:
            dibujarCronometro()
        else:
            pygame.display.update()
        if int(tiempo_viejo) < pygame.time.get_ticks()/1000:
            tiempo_viejo += 1
    coin.play()
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


def EscribirEnArchivoRecords(records, dificultad):
    with open("sources/files/records" + str(dificultad) + ".txt", "w") as archivoRecords:
        for record in records:
            archivoRecords.write(record + "\n")


def Controlador_Records(dificultad):
    #precondicion true
    lista_records = LeerArchivo("records" + str(dificultad))
    indice_jugador = -1
    for i in range(len(lista_records)):
        if lista_records[i].split(":")[0] == nombre_jugador:
            indice_jugador = i
    if indice_jugador == -1:
        lista_records.append(nombre_jugador + ":1")
    else:
        lista_records[indice_jugador] = nombre_jugador + ":" + str(int(lista_records[i].split(":")[1]) + 1)
    EscribirEnArchivoRecords(lista_records, dificultad)
    #postcondicion true


def PosicionesValidasAlfil(xorigen, yorigen, tablero, espeon):
    #Precondicion: True
    posiciones_validas = []
    if espeon:
        distanciamaxima = xorigen+2
        if distanciamaxima >= 4:
            distanciamaxima = 4
        distanciamaxima2 = xorigen-1
        if distanciamaxima2 <= 0:
            distanciamaxima2 = 0
    else:
        distanciamaxima = 4
        distanciamaxima2 = 0
    if not espeon:
        for x in range(xorigen):
            if BusquedaDiagonalSimetrica(xorigen, x, yorigen, "negativa", tablero):
                posiciones_validas.append((x, yorigen - (xorigen - x)))
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
        if y != yorigen and tablero[xorigen][y] != "":
            posiciones_validas.append((xorigen,y))
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
        ventana.blit(imagenNivel, (100, 40))
        ventana.blit(pygame.image.load(direccion_imagenes + "maximo10fichas.png"), (120, 260))
        pygame.display.update()
        nivel = Leer(23, 407, color_lectura, 40, 580,431)
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

def PantallaRecords():
    opcion_vieja = ""
    opcion = "1"
    while True:
        ventana.blit(imagenFondo, (0, 0))
        dificultades = ["Facil", "Dificil", "Muy Dificil", "volver"]
        dibujarMenu("tableroderecords", ["facil", "dificil", "muydificil", "volver"], "horizontal", 100, 20, 90, 430,
                    150,
                    500, 100)
        ventana.blit(imagenPizarra, (100, 130))
        pygame.draw.rect(ventana, (0,0,0), (149, 167, 309, 205))
        if opcion == "1" or opcion == "2" or opcion == "3":
            pygame.draw.rect(ventana, (255, 255, 0), (90 + ((int(opcion) - 1) * 105), 430, 100, 50), 5)
            lista_records = LeerArchivo("records" + opcion)
            lista_ordenada = []
            #ordernando la lista de records por cantidad de victorias y luego por orden alfanumerico del nombre
            for i in range(len(lista_records)):
                while len(lista_ordenada) < int(lista_records[i].split(":")[1]):
                    lista_ordenada.append([])
            #ordenados por cantidad de victorias
            for i in range(len(lista_records)):
                lista_ordenada[int(lista_records[i].split(":")[1]) - 1].append(lista_records[i].split(":")[0])
            #ordenados por nombre en caso de empates
            for i in range(len(lista_ordenada)):
                lista_ordenada[i].sort()
            imagenDificultad = fuente.render(dificultades[int(opcion) - 1] + ":", 1, (255,255,0))
            #renderizado del texto de todos los records
            lista_imagenes_texto = []
            for x in range(len(lista_ordenada)):
                victorias = len(lista_ordenada) - x -1
                for jugador in range(len(lista_ordenada[victorias])):
                    if x == 0 and jugador == 0:
                        lista_imagenes_texto.append(fuente.render(lista_ordenada[victorias][jugador] + ": " +
                                                                  str(victorias + 1) + " Victorias", 1, (200, 200, 120)))
                    else:
                        lista_imagenes_texto.append(
                            fuente.render(lista_ordenada[victorias][jugador] + ": " + str(victorias + 1) + " Victorias", 1,
                                          (255, 255, 255)))
            #escritura del record
            for y in range(len(lista_imagenes_texto[:9])):
                ventana.blit(lista_imagenes_texto[y], (156, 190 + (20 * y)))
            ventana.blit(imagenDificultad, (156, 174))
        pygame.display.update()
        opcion_vieja = opcion
        opcion = Leer(415, 515, (0, 0, 0), 1, 440, 534)
        if opcion == "5":
            break
        elif opcion != "1" and opcion != "2" and opcion != "3":
            MostrarMensaje(imagenOpcioninvalida, 100, 100, 1.5)
            opcion = opcion_vieja


#funcion que maneja el menu principal
def MenuPrincipal():
    #precondicion true
    #mostrar opciones al usuario
    while True:
        ventana.blit(imagenFondo, (0, 0))
        ventana.blit(imagenTitulo, (150, 20))
        dibujarMenu("menuprincipal", ["partidanueva", "cargarpartida", "mostrarrecords", "salirjuego"], "vertical",
                    100, 180, 200, 300, 150, 540, 200)
        pygame.display.update()
        opcion = Leer(415,555, color_lectura,1,440,575)
        if opcion == "1":
            SeleccionarNivel()
        elif opcion == "2":
            MenuCargar()
        elif opcion == "3":
            PantallaRecords()
        elif opcion == "4":
            ConfirmacionSalida()
        else:
            MostrarMensaje(imagenOpcioninvalida, 100,300, 1.5)
        #postcondicion: true

def FormatearFicha(imagen):
    return pygame.transform.scale(imagen, (50,90))


#funcion que un mensaje especial
def MostrarMensaje(imagen, x,y, tiempo):
    ventana.blit(imagen, (x,y))
    pygame.display.update()
    time.sleep(tiempo)


def IntroducirNombre():
    ventana.blit(imagenFondo, (0, 0))
    ventana.blit(pygame.image.load(direccion_imagenes + "cuadronombre.png"), (180, 396))
    ventana.blit(imagenNombre, (100, 40))
    ventana.blit(pygame.image.load(direccion_imagenes + "maximo10caracteres.png"), (88,240))
    nombre = Leer(200, 415, color_lectura, 10, 386,440)
    return nombre

#Funcion que indica al usuario como realizar sus acciones.
def MostrarTutorial():
    #Precondicion: True
    ventana.blit(imagenFondo, (0,0))
    ventana.blit(imagenTitulo, (150, 20))
    ventana.blit(imagenTutorial, (100, 200))
    pygame.display.update()
    time.sleep(8)
    #Postcondicion: True

pygame.init()
color_cielo = pygame.Color(25,158,218)
color_lectura = pygame.Color(147, 55, 120)
ventana = pygame.display.set_mode((600,600))
pygame.display.set_caption("Solitaire Chess")
direccion_imagenes = "sources/sprites/"
direccion_imagenes_numeros = "sources/sprites/numeros/"
imagenTitulo = pygame.transform.scale(pygame.image.load(direccion_imagenes + "title.png"), (300,150))
imagenFondo = pygame.image.load(direccion_imagenes + "fondo.jpg")
imagenTexto = pygame.image.load(direccion_imagenes + "cuadrodetexto.png")
imagenTablero = pygame.transform.scale(pygame.image.load(direccion_imagenes + "tablero.png"), (310,204))
imagenRey = FormatearFicha(pygame.image.load(direccion_imagenes + "rey.png"))
imagenAlfil = FormatearFicha(pygame.image.load(direccion_imagenes + "alfil.png"))
imagenReina = FormatearFicha(pygame.image.load(direccion_imagenes + "reina.png"))
imagenCaballo = FormatearFicha(pygame.image.load(direccion_imagenes + "caballo.png"))
imagenTorre = FormatearFicha(pygame.image.load(direccion_imagenes + "torre.png"))
imagenPeon = FormatearFicha(pygame.image.load(direccion_imagenes + "peon.png"))
imagenReymini = pygame.transform.scale(pygame.image.load(direccion_imagenes + "rey.png"), (40,40))
imagenAlfilmini = pygame.transform.scale(pygame.image.load(direccion_imagenes + "alfil.png"), (40,40))
imagenReinamini = pygame.transform.scale(pygame.image.load(direccion_imagenes + "reina.png"), (40,40))
imagenCaballomini = pygame.transform.scale(pygame.image.load(direccion_imagenes + "caballo.png"), (40,40))
imagenTorremini = pygame.transform.scale(pygame.image.load(direccion_imagenes + "torre.png"), (40,40))
imagenPeonmini = pygame.transform.scale(pygame.image.load(direccion_imagenes + "peon.png"), (40,40))
imagenOpcioninvalida = pygame.image.load(direccion_imagenes + "opcioninvalida.png")
imagenEnConstruccion = pygame.image.load(direccion_imagenes + "enconstruccion.png")
imagenTableroInvalido = pygame.image.load(direccion_imagenes + "tableroinvalido.png")
imagenTutorial = pygame.image.load(direccion_imagenes + "tutorial.png")
imagenLeyenda =  pygame.transform.scale(pygame.image.load(direccion_imagenes + "leyenda.png"), (220,150))
imagenIntroducirCasillas = pygame.transform.scale(pygame.image.load(direccion_imagenes + "introducircasillas.png"), (200,100))
imagenJugadaInvalida = pygame.transform.scale(pygame.image.load(direccion_imagenes + "jugadainvalida.png"), (300,200))
imagenDeshacerJugada = pygame.transform.scale(pygame.image.load(direccion_imagenes + "deshacerjugada.png"), (300,200))
imagenVictoria = pygame.image.load(direccion_imagenes + "ganador.png")
imagenDerrota = pygame.image.load(direccion_imagenes + "derrota.png")
imagenGuardarPartida = pygame.image.load(direccion_imagenes + "guardarpartida.png")
imagenTerminarPartida = pygame.image.load(direccion_imagenes + "terminarpartida.png")
imagenUno = pygame.image.load(direccion_imagenes_numeros + "uno.png")
imagenDos = pygame.image.load(direccion_imagenes_numeros + "dos.png")
imagenTres = pygame.image.load(direccion_imagenes_numeros + "tres.png")
imagenCuatro = pygame.image.load(direccion_imagenes_numeros + "cuatro.png")
imagenCinco = pygame.image.load(direccion_imagenes_numeros + "cinco.png")
imagenSeis = pygame.image.load(direccion_imagenes_numeros + "seis.png")
imagenSiete = pygame.image.load(direccion_imagenes_numeros + "siete.png")
imagenOcho = pygame.image.load(direccion_imagenes_numeros + "ocho.png")
imagenNueve = pygame.image.load(direccion_imagenes_numeros + "nueve.png")
imagenCero = pygame.image.load(direccion_imagenes_numeros + "cero.png")
imagenDospuntos = pygame.image.load(direccion_imagenes_numeros + "dospuntos.png")
imagenNombre = pygame.image.load(direccion_imagenes + "introducirnombre.png")
imagenFondoCronometro = pygame.image.load(direccion_imagenes + "fondocronometro.png")
imagenPausa =  pygame.image.load(direccion_imagenes + "juegopausado.png")
imagenContinuar = pygame.image.load(direccion_imagenes + "continuar.png")
imagenPizarra = pygame.transform.scale(pygame.image.load(direccion_imagenes + "pizarra.png"), (400,280))
imagenCasillaInicial = pygame.transform.scale(pygame.image.load(direccion_imagenes + "casillainicial.png"), (200,100))
fuente = pygame.font.Font(None, 28)
fuente_prueba = pygame.font.Font(None, 18)

#variables para controlar el tiempo
contar_tiempo = False
tiempo_viejo = pygame.time.get_ticks()/1000
tiempo_actual = 0
tiempo = 0
tiempo_maximo = 0

######cambiar los valores de estas variables
#####para mover el tablero en la pantalla
x_fichas = 54
cambio_x = 70 #valor original 76
y_fichas = 250
cambio_y = 41 #valor original 50

##Valores para el tablero miniatura
x_miniatura = 187
y_miniatura = 316
cambiomin_x = 69
cambiomin_y = 32


pygame.mixer.init()
bgm = pygame.mixer.Sound("sources/sounds/overworld.wav")
coin = pygame.mixer.Sound("sources/sounds/coin.wav")
win = pygame.mixer.Sound("sources/sounds/win.wav")
lose = pygame.mixer.Sound("sources/sounds/lose.wav")
bgm.play(-1)

MostrarTutorial()
nombre_jugador = IntroducirNombre()
MenuPrincipal()