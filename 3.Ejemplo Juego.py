
# NO FUE NECESARIO COMENTAR NADA


import pygame
from Funciones import *
from Constantes import *
from Preguntas import *
import random

pygame.init()
pygame.display.set_caption("PREGUNTADOS 114")
icono = pygame.image.load("texturas/icono.png")
pygame.display.set_icon(icono)
pantalla = pygame.display.set_mode(PANTALLA)

ejecutando = True
reloj = pygame.time.Clock()
datos_juego = crear_datos_juego()

evento_1_s = pygame.USEREVENT
pygame.time.set_timer(evento_1_s,1000)

click_sonido = pygame.mixer.Sound("sonidos/click.mp3")
sonido_error = pygame.mixer.Sound("sonidos/error.mp3")
random.shuffle(lista_preguntas)

cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,125,125)
pregunta_actual = obtener_pregunta_actual(datos_juego,lista_preguntas)
lista_respuestas = crear_lista_respuestas(3,"texturas/textura_respuesta.jpg",ANCHO_RESPUESTA,ALTO_RESPUESTA,200,300)
        
while ejecutando:
    
    reloj.tick(FPS)
    
    #a.Manipular Eventos
    for evento in pygame.event.get():
        #b.Actualizar Juego
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if responder_pregunta_pygame(lista_respuestas,click_sonido,sonido_error,evento.pos,lista_preguntas,pregunta_actual,datos_juego) == True:
                pregunta_actual = obtener_pregunta_actual(datos_juego,lista_preguntas)
                cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,125,125)
                lista_respuestas = crear_lista_respuestas(3,"texturas/textura_respuesta.jpg",ANCHO_RESPUESTA,ALTO_RESPUESTA,200,300)
        elif evento.type == evento_1_s:
            datos_juego["tiempo_restante"] -= 1
            
    #b.Actualizar Juego

    #c.Dibujar elementos en pantalla
    dibujar_pantalla_juego(pantalla,datos_juego,cuadro_pregunta,lista_respuestas,pregunta_actual)
    
    #d.Actualizar el Fotograma
    pygame.display.flip()
    
pygame.quit()