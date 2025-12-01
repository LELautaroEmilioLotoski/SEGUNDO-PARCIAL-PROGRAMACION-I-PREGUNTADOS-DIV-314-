
# NO FUE NECESARIO COMENTAR NADA

import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)

def mostrar_rankings(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],lista_rankings:list) -> str:
    ventana = "rankings"
    
    y_base = 150  # posición inicial en Y
    
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    ventana = "menu"
                    
    
    pantalla.fill(COLOR_BLANCO)
    
    # OBTENEMOS EL RANKING DE LAS 10 MEJORES PUNTUACIONES
    top_de_ranking_obtenido = obtener_ranking()
    
    # OBTENEMOS LA ALTURA DE LA FUENTE EN PIXELES
    altura_fuente = FUENTE_ARIAL_30.get_height()

    mostrar_texto(pantalla, "TOP 10 DE LAS PUNTUACIONES MAS ALTAS", (200, 10), FUENTE_ARIAL_30, COLOR_NEGRO)
    mostrar_texto(pantalla, "NOMBRE", (20, 100), FUENTE_ARIAL_30, COLOR_NEGRO)
    mostrar_texto(pantalla, "PUNTUACION", (180, 100), FUENTE_ARIAL_30, COLOR_NEGRO)
    mostrar_texto(pantalla, "FECHA", (400, 100), FUENTE_ARIAL_30, COLOR_NEGRO)

    # MOSTRAMOS LOS DATOS DEL RANKING
    for i in range(len(top_de_ranking_obtenido)):
        y = y_base + i * (altura_fuente + 10)

        mostrar_texto(pantalla, top_de_ranking_obtenido[i]["nombre"], (20, y), FUENTE_ARIAL_30, COLOR_NEGRO)
        mostrar_texto(pantalla, str(top_de_ranking_obtenido[i]["puntuacion"]), (200, y), FUENTE_ARIAL_30, COLOR_NEGRO)
        mostrar_texto(pantalla, top_de_ranking_obtenido[i]["fecha"], (350, y), FUENTE_ARIAL_30, COLOR_NEGRO)
    
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)

    return ventana
    