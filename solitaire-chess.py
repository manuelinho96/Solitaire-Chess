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
    #precondicion true
    string = ""
    patron = re.compile("^\w{1}$")
    patron2 = re.compile("\w")
    rectangulo = pygame.Rect(x, y, xfinal - x, yfinal - y)
    texto = ""
    global shift
    global bloq_mayus
    while True:#(funcion de cota???, invariante???)
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

#funcion que recibe un string del mensaje de la opcion
#y carga el sprite correspondiente y lo lleva a resolucion
#150x50
def formatearOpcion(opcion):
    #precondicion existe la imagen
    return pygame.transform.scale(pygame.image.load("sources/sprites/" + opcion + ".png"), (200,50))
    #postcondicion true


#funcion que dibuja un menu y sus opciones
def dibujarMenu(titulo, opciones, orientacion,xtitulo,ytitulo,xopcion,yopcion,xintro,yintro):
    #precondicion al menos debe haber 1 opcion y el titulo debe no ser nulo
    #todas las opciones no deben ser nulas, la orientacion es vertical o horizontal
    try:
        assert(len(opciones) > 0 and titulo != "" and all(opcion != "" for opcion in opciones) and
               (orientacion == "vertical" or orientacion == "horizontal"))
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
    #Postcondicion:
    ventana.blit(imagenFondo, (0, 0))
    dibujarMenu("seleccionarnivel", ["facil", "dificil", "muydificil", "entrenamiento","volver"], "vertical",
                100,30,200,150,150,450)
    while True:
        pygame.display.update()
        opcion = Leer(415, 465, color_lectura, 1, 440, 486)
        if opcion == "5":
            break
        elif opcion == "1" or opcion == "2" or opcion == "4":
            IntroducirNivel()

#Funcion que maneja la confirmacion de salida
def ConfirmacionSalida():
    #Precondicion: True
    #Postcondicion: True
    ventana.blit(imagenFondo, (0, 0))
    dibujarMenu("salida",["si","no"],"horizontal",100,30,112,279,138,464)
    while True:
        pygame.display.update()
        opcion = Leer(403, 479, color_lectura, 1, 428, 500)
        if opcion == "1":
            cerrar()
        elif opcion == "2":
            break
        else:
            print("opcion invalida")

def IntroducirNivel():
    #Precondicion: True
    #Postcondicion:
    imagenNivel = pygame.transform.scale(pygame.image.load("sources/sprites/configurartablero.png"), (400,200))
    while True:
        ventana.blit(imagenFondo, (0, 0))
        ventana.blit(imagenTitulo, (150, 20))
        ventana.blit(imagenTexto, (10,346))
        ventana.blit(imagenNivel, (100,100))
        pygame.display.update()
        nivel = Leer(20, 356, color_lectura, 44, 580,378)


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
        x = 10
        y = 10
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