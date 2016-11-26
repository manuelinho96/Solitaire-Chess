import pygame, sys, re
from pygame.locals import *

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
    while True:#(funcion de cota???, invariante???)
        pygame.display.update()
        pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
        texto = fuente.render(string, 1, (255, 120, 255))
        ventana.blit(texto, (x+5, y-4))
        for event in pygame.event.get():
            if event.type == QUIT:
                    cerrar()
            if event.type == KEYDOWN:
                if ((patron.match(pygame.key.name(event.key)) != None or pygame.key.name(event.key) == "-") and
                                len(string) < longitud_maxima):
                    # dibujar la letra, sumarle pixeles dependiendo de la longitud para que quede mas lejos la letra nueva
                    # recordar que se debe usar el color pasado por parametro
                    string += pygame.key.name(event.key)
                elif event.key == 13:
                    #postcondicion string solo contiene elementos validos
                    try:
                        assert(patron2.match(string) != None or len(string) == 0)
                        return string
                    except:
                        print("Error en la lectura")
                        cerrar()
                elif event.key ==8 and len(string)>0:
                    string = string[:len(string)-1]

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
    ventana.fill(color_cielo)
    dibujarMenu("seleccionarnivel", ["facil", "dificil", "muydificil", "entrenamiento","volver"], "vertical",
                100,30,200,150,150,400)
    while True:
        pygame.display.update()
        opcion = Leer(420, 416, color_lectura, 1, 444, 430)
        if opcion == "5":
            break

#Funcion que maneja la confirmacion de salida
def ConfirmacionSalida():
    #Precondicion: True
    #Postcondicion: True
    ventana.fill(color_cielo)
    dibujarMenu("salida",["si","no"],"horizontal",100,30,112,279,138,464)
    while True:
        pygame.display.update()
        opcion = Leer(408, 480, color_lectura, 1, 432, 494)
        if opcion == "1":
            cerrar()
        elif opcion == "2":
            break
        else:
            print("opcion invalida")

#funcion que maneja el menu principal
def MenuPrincipal():
    #precondicion true
    #mostrar opciones al usuario
    while True:
        ventana.fill(color_cielo)
        ventana.blit(imagenTitulo, (150, 20))
        pygame.display.update()
        dibujarMenu("menuprincipal", ["partidanueva", "cargarpartida", "mostrarrecords", "salirjuego"], "vertical",
                    100, 180, 200, 300, 150, 540)
        pygame.display.update()
        x = 10
        y = 10
        opcion = Leer(420,556, color_lectura,1,444,570)
        if opcion == "1":
            PartidaNueva()
        elif opcion == "2":
            print("Cargar")
        elif opcion == "3":
            print("Records")
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
fuente = pygame.font.Font(None, 28)
MenuPrincipal()