#ADMINISTRADOR DE VENTANAS

import pygame
from Constantes import *
from Funciones import *
#TODAS LAS VENTANAS QUE VAYAMOS A USAR
from Menu import *
from Juego import *
from Rankings import *
from Configuracion import *
from Terminado import *

pygame.init()
pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("texturas/icono.png")
pygame.display.set_icon(icono)
lista_preguntas = cargar_preguntas_desde_csv("preguntas.csv")

pantalla = pygame.display.set_mode(PANTALLA)
#Lo único global en todas las ventanas va a ser siempre los datos del juego
datos_juego = crear_datos_juego()
reloj = pygame.time.Clock()
ventana_actual = "menu"
bandera_juego = False
lista_rankings = []

#UNICO WHILE INFINITO DEL JUEGO 
while True:
    #Administrar los fps
    reloj.tick(FPS)
    #Crear la cola de eventos
    cola_eventos = pygame.event.get()
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            ventana_actual = "salir"
    
    #Administramos que ventana mostrar
    if ventana_actual == "menu":
        reiniciar_estadisticas(datos_juego)
        ventana_actual = mostrar_menu(pantalla,cola_eventos)
    elif ventana_actual == "jugar":
        if bandera_juego == False:
            musica_activa(datos_juego)
            random.shuffle(lista_preguntas)
            bandera_juego = True
        ventana_actual = mostrar_juego(pantalla,cola_eventos,datos_juego,lista_preguntas)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla,cola_eventos,lista_rankings)        
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla,cola_eventos,datos_juego)    
    elif ventana_actual == "terminado":
        if bandera_juego == True:
            pygame.mixer.music.stop()
            bandera_juego = False
        
        ventana_actual = mostrar_game_over(pantalla,cola_eventos,datos_juego)
    elif ventana_actual == "salir":
        break
    
    #Actualizar Fotograma
    pygame.display.flip()
        
pygame.quit()
