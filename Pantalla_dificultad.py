import pygame
from Constantes import *
from Funciones import *

pygame.init()
boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)

# FONDO
fondo_menu = pygame.image.load("texturas/fondo.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, PANTALLA)


# ---- LISTA DE BOTONES (texto, posición Y) ----
botones_info = [
    (DIFICULTAD_FACIL, 150),
    (DIFICULTAD_MEDIA, 250),
    (DIFICULTAD_DIFICIL, 350),
    (DIFICULTAD_PERSONALIZADA, 450)
]


lista_botones = []

# ---- CREAR BOTONES ----
for texto, y in botones_info:
    boton = crear_elemento_juego("texturas/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, 150, y)
    lista_botones.append((boton, texto))


def seleccionar_dificultad(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event]) -> str:
    ventana = "dificultad"
    dificultad = None
    
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                ventana = "menu"
            
            # RECORREMOS LOS BOTONES CREADOS
            for boton, nombre_boton in lista_botones:
                if boton["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    
                    # SETEAMOS EL VALOR DE LA DIFICULTAD CON EL BOTON CORRESPONDIENTE
                    dificultad = nombre_boton
                    
                    # SI EL JUGADOR ELIJE "DIFICULTAD PERSONALIZADA", LO ENVÍA A LA PARTE DE CONFIGURACIÓN PARA SETEAR LOS VALORES
                    if nombre_boton == DIFICULTAD_PERSONALIZADA:
                        ventana = "configuracion"
                        break
                    else:
                        ventana = "jugar"
                    

    # ---- DIBUJAR FONDO ----
    pantalla.blit(fondo_menu, (0, 0))

    # ---- DIBUJAR BOTONES + TEXTO ----
    for boton, texto in lista_botones:
        superficie = boton["superficie"]
        rect = boton["rectangulo"]

        pantalla.blit(superficie, rect)

        mostrar_texto(
            pantalla,
            texto,
            (rect.x + 60, rect.y + 10),
            FUENTE_ARIAL_30,
            COLOR_BLANCO
        )
    
    mostrar_texto(pantalla, "ELIGE LA DIFICULTAD CON LA CUAL QUERÉS JUGAR:", (150,50), FUENTE_ARIAL_30, COLOR_NEGRO)

    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla,"VOLVER",(boton_volver["rectangulo"].x + 5, boton_volver["rectangulo"].y + 5),FUENTE_ARIAL_20,COLOR_BLANCO)
    

    return ventana, dificultad        
