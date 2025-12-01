# import pygame
# from Constantes import *
# from Funciones import *

# #Crea la lista de botones del menu
# def crear_lista_botones(cantidad_botones:int,textura:str,ancho:int,alto:int,x:int,y:int) -> list | None:
#     if os.path.exists(textura):
#         lista_botones = []

#         for i in range(cantidad_botones):
#             boton = crear_elemento_juego(textura,ancho,alto,x,y)
#             lista_botones.append(boton)
#             y += (alto + 15)
#     else:
#         lista_botones = None
        
#     return lista_botones

# pygame.init()
# #FONDO
# fondo_menu = pygame.image.load("texturas/fondo.jpg")
# fondo_menu = pygame.transform.scale(fondo_menu,PANTALLA)

# #BOTONES
# lista_botones = crear_lista_botones(4,"texturas/textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,150,150)
# print(lista_botones)

# #LISTA AUX
# lista_textos_botones = ["JUGAR","AJUSTES","RANKINGS","SALIR"]

# def mostrar_menu(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:
#     ventana = "menu"
    
#     #Gestionar los eventos
#     for evento in cola_eventos:
#         if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
#             for i in range(len(lista_botones)):
#                 if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
#                     CLICK_SONIDO.play()
#                     ventana = lista_textos_botones[i].lower()            
    
#     #Actualizar Juego
    
#     #Dibujar en pantalla
#     pantalla.blit(fondo_menu,(0,0))
    
#     for i in range(len(lista_botones)):
#         pantalla.blit(lista_botones[i]["superficie"],lista_botones[i]["rectangulo"])
#         #AUTOMATICO
#         mostrar_texto(lista_botones[i]["superficie"],lista_textos_botones[i],(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
        
#     # #MANUAL
#     # mostrar_texto(lista_botones[0]["superficie"],"JUGAR",(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
#     # mostrar_texto(lista_botones[1]["superficie"],"AJUSTES",(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
#     # mostrar_texto(lista_botones[2]["superficie"],"RANKINGS",(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
#     # mostrar_texto(lista_botones[3]["superficie"],"SALIR",(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
    
        
#     return ventana

##########################################################################################################################


import pygame
from Constantes import *
from Funciones import *

def crear_lista_botones(cantidad_botones:int,textura:str,ancho:int,alto:int,x:int,y:int) -> list | None:
    if os.path.exists(textura):
        lista_botones = []

        for i in range(cantidad_botones):
            boton = crear_elemento_juego(textura,ancho,alto,x,y)
            lista_botones.append(boton)
            y += (alto + 15)
    else:
        lista_botones = None
        
    return lista_botones

pygame.init()
#FONDO
fondo_menu = pygame.image.load("texturas/fondo.jpg")
fondo_menu = pygame.transform.scale(fondo_menu,PANTALLA)

#BOTONES
lista_botones = crear_lista_botones(4,"texturas/textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,150,150)
print(lista_botones)

#LISTA AUX
lista_textos_botones = ["JUGAR","AJUSTES","RANKINGS","SALIR"]

def mostrar_menu(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event]) -> str:
    ventana = "menu"
    
    #Gestionar los eventos
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    ventana = lista_textos_botones[i].lower()            
    
    #Actualizar Juego
    
    #Dibujar en pantalla
    pantalla.blit(fondo_menu,(0,0))
    
    for i in range(len(lista_botones)):
        pantalla.blit(lista_botones[i]["superficie"],lista_botones[i]["rectangulo"])
        #AUTOMATICO
        mostrar_texto(lista_botones[i]["superficie"],lista_textos_botones[i],(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
        
    # #MANUAL
    # mostrar_texto(lista_botones[0]["superficie"],"JUGAR",(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
    # mostrar_texto(lista_botones[1]["superficie"],"AJUSTES",(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
    # mostrar_texto(lista_botones[2]["superficie"],"RANKINGS",(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
    # mostrar_texto(lista_botones[3]["superficie"],"SALIR",(100,10),FUENTE_ARIAL_30,COLOR_BLANCO)
    
        
    return ventana