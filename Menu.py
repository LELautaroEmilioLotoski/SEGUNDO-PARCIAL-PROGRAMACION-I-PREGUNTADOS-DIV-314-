import pygame
from Constantes import *
from Funciones import *

pygame.init()

#FONDO
fondo_menu = pygame.image.load("texturas/fondo.jpg")
fondo_menu = pygame.transform.scale(fondo_menu,PANTALLA)

#BOTONES
lista_botones = crear_lista_botones(7,"texturas/textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,150,50)

#LISTA AUX
lista_textos_botones = ["JUGAR","AJUSTES","RANKINGS","SALIR", "DIFICULTAD", "CONFIGURACION", "AGREGAR PREGUNTA"]

def mostrar_menu(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:
    ventana = "menu"
    
    #Gestionar los eventos
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    ventana = lista_textos_botones[i].lower()          
    
    #Dibujar en pantalla
    pantalla.blit(fondo_menu,(0,0))
    
    for i in range(len(lista_botones)):
        pantalla.blit(lista_botones[i]["superficie"],lista_botones[i]["rectangulo"])
        #AUTOMATICO
        # mostrar_texto(lista_botones[i]["superficie"],lista_textos_botones[i],(80,10),FUENTE_ARIAL_30,COLOR_BLANCO)
        
        rect_original = lista_botones[i]["rectangulo"]
        rect_interno = pygame.Rect(0, 0, rect_original.width, rect_original.height)
        # mostrar_texto(lista_botones[i]["superficie"],lista_textos_botones[i],lista_botones[i]["rectangulo"],FUENTE_ARIAL_20,COLOR_BLANCO)
        mostrar_texto_en_rect(lista_botones[i]["superficie"],lista_textos_botones[i],rect_interno,FUENTE_ARIAL_30,COLOR_BLANCO)
        
    return ventana