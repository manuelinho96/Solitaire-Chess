import pygame, sys, re
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
                if ((patron.match(pygame.key.name(event.key)) != None or event.key == 47) and
                                len(string) < longitud_maxima):
                    # dibujar la letra, sumarle pixeles dependiendo de la longitud para que quede mas lejos la letra nueva
                    # recordar que se debe usar el color pasado por parametro
                    letra = pygame.key.name(event.key)
                    if event.key == 47:
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
                        cerrar()
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
def formatearOpcion(opcion):
    #precondicion existe la imagen
    #postcondicion true
    try:
        return pygame.transform.scale(pygame.image.load("sources/sprites/" + opcion + ".png"), (200,50))
    except:
        return "no se encontro la imagen"



#funcion que dibuja un menu y sus opciones
def dibujarMenu(titulo, opciones, orientacion,xtitulo,ytitulo,xopcion,yopcion,xintro,yintro):
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
            imagenes.append(formatearOpcion(opcion))
    for i in range(len(imagenes)):
        if orientacion == "vertical":
            ventana.blit(imagenes[i], (xopcion, yopcion + (i * 60)))
        else:
            ventana.blit(imagenes[i], (xopcion + (i * 210), yopcion))
    introduzca_opcion = pygame.transform.scale(pygame.image.load("sources/sprites/introduceunaopcion.png"),(300, 50))
    ventana.blit(introduzca_opcion, (xintro,yintro))
    #postcondicion true


#Funcion que maneja el menu de partida nueva
def PartidaNueva():
    #Precondicion: True
    while True:
        ventana.blit(imagenFondo, (0, 0))
        dibujarMenu("seleccionarnivel", ["facil", "dificil", "muydificil", "entrenamiento", "volver"], "vertical",
                    100, 30, 200, 150, 150, 450)
        pygame.display.update()
        opcion = Leer(415, 465, color_lectura, 1, 440, 486)
        #opcion = "1"
        if opcion == "5":
            break
        elif opcion == "1" or opcion == "2" or opcion == "4":
            nivel = IntroducirNivel()
            if validarString(nivel):
                tablero = MatrizDeString(nivel)
                cerrar()
    #postcondicion true

#funcion que determina si un string es un nivel de valido o no
def validarString(string) -> bool:
    #precondicion la string debe tener al menos un caracter
    assert(len(string) >= 0)
    lista = string.split("-")
    #POSTCONDICION = la funcion debe retornar True si la string al separarla por -
    #se divide en substring de 2 o 3 caracteres, cuando tiene 2 caracteres el primero
    #debe ser una letra minuscula entra a..d y el segundo un numero del 1 al 4
    #y en caso de tener 3 caracteres el primero debe ser "R","T","C","A","D", el segundo
    #debe ser una letra minuscula de entra a..d y ultimo un numero del 1 al 4
    #en ambos casos se debe retornar True, sino se retorna falso
    try:
        assert(all(len(substring) >= 2  and len(substring) <=3 for substring in lista))
    except:
        print("Error de cantidad de caracteres en los substrings")
        return False
    try:
        for substring in lista:
            if len(substring) == 2:
                assert(substring[0] in ["a","b","c","d"] and substring[1] in ["1", "2", "3", "4"])
            else:
                assert (substring[1] in ["a", "b", "c", "d"] and substring[2] in ["1", "2", "3", "4"] \
                        and substring[0] in ["R", "T", "C", "A", "D"])
        return True
    except:
        print("Cantidad de carecteres no corresponde a los caracteres en el string")
        return False


#Funcion que maneja la confirmacion de salida
def ConfirmacionSalida():
    #Precondicion: True
    ventana.blit(imagenFondo, (0, 0))
    dibujarMenu("salida",["si","no"],"horizontal",100,30,112,279,138,464)
    while True:
        pygame.display.update()
        opcion = Leer(403, 479, color_lectura, 1, 428, 500)
        #postcondicion opcion es 1 o 2
        if opcion == "1":
            cerrar()
        elif opcion == "2":
            break
        else:
            print("opcion invalida")

#funcion que maneja la pantalla en la que el usuario introduce el nivel desde el teclado
def IntroducirNivel():
    #Precondicion: True
    imagenNivel = pygame.transform.scale(pygame.image.load("sources/sprites/configurartablero.png"), (400,200))
    while True:
        ventana.blit(imagenFondo, (0, 0))
        ventana.blit(imagenTitulo, (150, 20))
        ventana.blit(imagenTexto, (10,346))
        ventana.blit(imagenNivel, (100,100))
        pygame.display.update()
        nivel = Leer(20, 356, color_lectura, 44, 580,378)
        #nivel = "Cc4-a2-Rd3"
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
                    100, 180, 200, 300, 150, 540)
        pygame.display.update()
        opcion = Leer(415,555, color_lectura,1,440,575)
        if opcion == "1":
            PartidaNueva()
        elif opcion == "2":
            print("Cargar!")
        elif opcion == "3":
            print("Records!")
        elif opcion == "4":
            ConfirmacionSalida()
        else:
            print("Error opcion invalida")
        # post condicion true

pygame.init()
color_cielo = pygame.Color(25,158,218)
color_lectura = pygame.Color(147, 55, 120)
ventana = pygame.display.set_mode((600,600))
pygame.display.set_caption("Solitaire Chess")
imagenTablero = pygame.image.load("sources/sprites/tablero.jpg")
imagenTitulo = pygame.transform.scale(pygame.image.load("sources/sprites/title.png"), (300,150))
imagenFondo = pygame.image.load("sources/sprites/fondo.jpg")
imagenTexto = pygame.image.load("sources/sprites/cuadrodetexto.png")
fuente = pygame.font.Font(None, 28)
MenuPrincipal()