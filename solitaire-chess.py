import pygame, sys, re
from pygame.locals import *
ventana = pygame.display.set_mode(600,600)
pygame.display.set_caption("Solitaire Chess")


#funcion que cierra pygame y cierra el programa
def cerrar():
    #precondicion true

    #postcondicion true
    pygame.quit()
    sys.exit()

#funcion que detecta eventos y evalua si son teclas
def Leer():
    #precondicion true
    string = ""
    patron = re.compile("^[a-zA-Z0-9_ ]*$")
    while True:#(funcion de cota???, invariante???)
        for event in pygame.event.get():
            if event.type == QUIT:
                    cerrar()
            if event.type == KEYDOWN:
                if patron.match(pygame.key.name(event.key)):
                    string += pygame.key.name(event.key)
                elif
                    event.key == K_KP_ENTER:
                        #postcondicion string solo contiene elementos validos
                        try:
                            assert(patron.match(string))
                        except:
                            cerrar()
                        return string

#funcion que maneja el menu principal
def MenuPrincipal():
    #precondicion true