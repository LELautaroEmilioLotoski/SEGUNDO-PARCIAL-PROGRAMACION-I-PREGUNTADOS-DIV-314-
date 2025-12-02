import pygame
from Funciones import *
from Constantes import *
import random

pygame.init()

evento_1_s = pygame.USEREVENT
pygame.time.set_timer(evento_1_s,1000)
lista_imagenes = ["texturas_comodines/Bomba.png","texturas_comodines/db.png","texturas_comodines/pass.png","texturas_comodines/x2.png"]


def crear_lista_botones_comodines(cantidad_botones:int,texturas:list,ancho:int,alto:int,x:int,y:int) -> list | None:
    lista_botones = []

    for i in range(cantidad_botones):
        if os.path.exists(texturas[i]):
            boton = crear_elemento_juego(texturas[i],ancho,alto,x,y)
            lista_botones.append(boton)
            y += (alto + 15)
        else:
            lista_botones = None
        
    return lista_botones



def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict, lista_preguntas:list) -> str:
    ventana = "jugar"
    
    pregunta_actual = obtener_pregunta_actual(datos_juego,lista_preguntas)
    cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,125,125)
    lista_respuestas = crear_lista_respuestas(CANTIDAD_DE_POSIBLES_RESPUESTAS,"texturas/textura_respuesta.jpg",ANCHO_RESPUESTA,ALTO_RESPUESTA,200,300)
    lista_comodines = crear_lista_botones_comodines(4,lista_imagenes,60,60,100,250)
    a_eliminar=[]


    #a.Manejar Eventos
    for evento in cola_eventos:
        #b.Actualizar Juego
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if responder_pregunta_pygame(lista_respuestas,CLICK_SONIDO,ERROR_SONIDO,evento.pos,lista_preguntas,pregunta_actual,datos_juego) == True:
                pregunta_actual = obtener_pregunta_actual(datos_juego,lista_preguntas)
                cuadro_pregunta = crear_elemento_juego("texturas/textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,125,125)
                lista_respuestas = crear_lista_respuestas(CANTIDAD_DE_POSIBLES_RESPUESTAS,"texturas/textura_respuesta.jpg",ANCHO_RESPUESTA,ALTO_RESPUESTA,200,300)
                reiniciar_indice_bomba(datos_juego)
           
            for i in range(len(lista_comodines)):
                if lista_comodines[i]["rectangulo"].collidepoint(evento.pos):
                    if i == 0:
                        if datos_juego["comodin_bomba"] == False:
                            activar_bomba(datos_juego,lista_respuestas,pregunta_actual)
                    elif i == 1:
                        activar_shield(datos_juego)
                    elif i == 2:
                        activar_pass(datos_juego,lista_preguntas)
                    elif i == 3:
                        activar_x2(datos_juego)
                            
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
    dibujar_pantalla_juego(pantalla,datos_juego,cuadro_pregunta,lista_respuestas,lista_comodines,pregunta_actual)    

    return ventana
