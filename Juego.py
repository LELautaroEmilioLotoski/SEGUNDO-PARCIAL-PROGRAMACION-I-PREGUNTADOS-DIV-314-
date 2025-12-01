import pygame
from Funciones import *
from Constantes import *
from Preguntas import *
import random

pygame.init()
lista_preguntas = cargar_preguntas_desde_csv("preguntas.csv")

evento_1_s = pygame.USEREVENT
pygame.time.set_timer(evento_1_s,1000)

def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    ventana = "jugar"
    
    pregunta_actual = obtener_pregunta_actual(datos_juego,lista_preguntas)
    cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,125,125)
    lista_respuestas = crear_lista_respuestas(4,"texturas/textura_respuesta.jpg",ANCHO_RESPUESTA,ALTO_RESPUESTA,200,300)

    #a.Manejar Eventos
    for evento in cola_eventos:
        #b.Actualizar Juego
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if responder_pregunta_pygame(lista_respuestas,CLICK_SONIDO,ERROR_SONIDO,evento.pos,lista_preguntas,pregunta_actual,datos_juego) == True:
                pregunta_actual = obtener_pregunta_actual(datos_juego,lista_preguntas)
                cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,125,125)
                lista_respuestas = crear_lista_respuestas(4,"texturas/textura_respuesta.jpg",ANCHO_RESPUESTA,ALTO_RESPUESTA,200,300)
        elif evento.type == evento_1_s:
            datos_juego["tiempo_restante"] -= 1
            
    #b.Actualizar Juego
    #Cuando sin vidas volver al menú
    if datos_juego["cantidad_vidas"] == 0:
        ventana = "terminado"
        
    
    #Cuando se termina el tiempo volver al menú
    if datos_juego["tiempo_restante"] == 0:
        ventana = "terminado"
    
    #c.Dibujar elementos en pantalla
    dibujar_pantalla_juego(pantalla,datos_juego,cuadro_pregunta,lista_respuestas,pregunta_actual)    

    return ventana