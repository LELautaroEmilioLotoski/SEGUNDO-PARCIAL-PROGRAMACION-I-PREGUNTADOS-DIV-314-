import pygame
from Constantes import *
from Funciones import *

pygame.init()

# boton_on = crear_elemento_juego("MENU PYGAME 314/texturas/ON.png", 120, 90, 430, 80)
# boton_off = crear_elemento_juego("MENU PYGAME 314/texturas/OFF.png", 120, 90, 430, 80)
# boton_suma = crear_elemento_juego("MENU PYGAME 314/texturas/mas.webp",60,60,250,200)
# boton_resta = crear_elemento_juego("MENU PYGAME 314/texturas/menos.webp",60,60,50,200)
# boton_volver = crear_elemento_juego("MENU PYGAME 314/texturas/textura_respuesta.jpg",100,40,10,10)
# fondo_prueba = crear_elemento_juego("MENU PYGAME 314/texturas/Fondo_de_prueba.png",500,200,50,70)

boton_on = crear_elemento_juego("texturas/ON.png", 120, 90, 430, 80)
boton_off = crear_elemento_juego("texturas/OFF.png", 120, 90, 430, 80)
boton_suma = crear_elemento_juego("texturas/mas.webp",60,60,250,200)
boton_resta = crear_elemento_juego("texturas/menos.webp",60,60,50,200)
boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)
fondo_prueba = crear_elemento_juego("texturas/Fondo_de_prueba.png",500,200,50,70)



#Administra los botones de el menu de configuracion (Collide, sonido, etc)
def administrar_botones(boton_suma:dict,boton_resta:dict,boton_volver:dict,datos_juego:dict,pos_mouse:tuple,back_up:int) -> str:
    ventana = "ajustes"


    if boton_on["rectangulo"].collidepoint(pos_mouse):
        datos_juego["musica_activa"] = not datos_juego["musica_activa"] # Cambiar estado (True -> False o False -> True)
        CLICK_SONIDO.play()
    elif boton_suma["rectangulo"].collidepoint(pos_mouse):
        if datos_juego["volumen_musica"] <= 99:
                datos_juego["volumen_musica"] += 1
                CLICK_SONIDO.play()
        else:
                ERROR_SONIDO.play()
    elif boton_resta["rectangulo"].collidepoint(pos_mouse):
        if datos_juego["volumen_musica"] > 0:
            datos_juego["volumen_musica"] -= 1
            CLICK_SONIDO.play()
        else: 
            ERROR_SONIDO.play()   
    elif boton_volver["rectangulo"].collidepoint(pos_mouse):
        CLICK_SONIDO.play()
        ventana = "menu"
        
    return ventana


#Muestra el menu de ajustes
def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    ventana = "ajustes"
    back_up = datos_juego["volumen_musica"]
    
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            ventana = administrar_botones(boton_suma,boton_resta,boton_volver,datos_juego,evento.pos,back_up)
    
    pantalla.fill(COLOR_BLANCO)
    pantalla.blit(fondo_prueba["superficie"],fondo_prueba["rectangulo"])
    
    pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])

    if datos_juego["musica_activa"]:
        pantalla.blit(boton_on["superficie"], boton_on["rectangulo"]) 
    else:
        pantalla.blit(boton_off["superficie"], boton_off["rectangulo"])
    
    pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    
    mostrar_texto(pantalla,f"{datos_juego["volumen_musica"]} %",(130,200),FUENTE_ARIAL_50,COLOR_BLANCO)
    mostrar_texto(pantalla,"Musica",(70,100),FUENTE_ARIAL_50,COLOR_BLANCO)
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)

    return ventana

##################################################################################################################

# import pygame
# from Constantes import *
# from Funciones import *

# pygame.init()

# boton_suma = crear_elemento_juego("texturas/mas.webp",60,60,420,200)
# boton_resta = crear_elemento_juego("texturas/menos.webp",60,60,20,200)
# boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)

# def administrar_botones(boton_suma:dict,boton_resta:dict,boton_volver:dict,datos_juego:dict,pos_mouse:tuple) -> str:
#     ventana = "ajustes"
    
#     if boton_suma["rectangulo"].collidepoint(pos_mouse):
#         if datos_juego["volumen_musica"] <= 95:
#             datos_juego["volumen_musica"] += 5
#             CLICK_SONIDO.play()
#         else:
#             ERROR_SONIDO.play()
#     elif boton_resta["rectangulo"].collidepoint(pos_mouse):
#         if datos_juego["volumen_musica"] > 0:
#             datos_juego["volumen_musica"] -= 5
#             CLICK_SONIDO.play()
#         else: 
#             ERROR_SONIDO.play()
#     elif boton_volver["rectangulo"].collidepoint(pos_mouse):
#         CLICK_SONIDO.play()
#         ventana = "menu"
        
#     return ventana

# def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
#     ventana = "ajustes"
    
#     for evento in cola_eventos:
#         if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
#             ventana = administrar_botones(boton_suma,boton_resta,boton_volver,datos_juego,evento.pos)
    
#     pantalla.fill(COLOR_BLANCO)
    
#     pantalla.blit(boton_suma["superficie"],boton_suma["rectangulo"])
#     pantalla.blit(boton_resta["superficie"],boton_resta["rectangulo"])
#     pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    
#     mostrar_texto(pantalla,f"{datos_juego["volumen_musica"]} %",(200,200),FUENTE_ARIAL_50,COLOR_NEGRO)
#     mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)

#     return ventana
    