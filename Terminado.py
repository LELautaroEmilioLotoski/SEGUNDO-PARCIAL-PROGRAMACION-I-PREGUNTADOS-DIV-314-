import pygame
from Constantes import *
from Funciones import *

pygame.init()

def mostrar_game_over(pantalla, cola_eventos, datos_juego):
    ventana = "terminado"

    # PERSISTEN ENTRE FRAMES
    if "error_nombre" not in datos_juego:
        datos_juego["error_nombre"] = False   # EL MENSAJE DE ERROR SE MOSTRARÁ SOLO CUANDO HAGA FALTA

    cuadro_texto = crear_elemento_juego("texturas/textura_respuesta.jpg",300,50,150,275)
    boton_guardar_partida = crear_elemento_juego("texturas/textura_respuesta.jpg",150,40,150,400)

    # -------- EVENTOS --------
    for evento in cola_eventos:
        if evento.type == pygame.TEXTINPUT:
            datos_juego["nombre"] += evento.text

            # SI ESCRIBE ALGO, EL MENSAJE DE ERROR DESAPARECE
            if datos_juego["nombre"]:
                datos_juego["error_nombre"] = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                datos_juego["nombre"] = datos_juego["nombre"][:-1]

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_guardar_partida["rectangulo"].collidepoint(evento.pos):
                
                estado_guardar_partida = guardar_partida(datos_juego)

                if estado_guardar_partida:
                    datos_juego["nombre"] = "" # LIMPIAMOS EL VALOR DEL NOMBRE INGRESADO
                    ventana = "menu"
                else:
                    # MOSTRAR EL ERROR PERSISTENTE
                    datos_juego["error_nombre"] = True

    # -------- INTERFAZ GRÁFICA--------
    pantalla.fill(COLOR_BLANCO)
    mostrar_texto(pantalla, f"PERDISTE EL JUEGO: {datos_juego['puntuacion']}", (100,50), FUENTE_ARIAL_50, COLOR_NEGRO)
    mostrar_texto(pantalla, "INGRESE SU NOMBRE:", (180,200), FUENTE_ARIAL_20, COLOR_NEGRO)
    mostrar_texto(cuadro_texto["superficie"], datos_juego["nombre"], (10,10), FUENTE_ARIAL_30, COLOR_BLANCO)
    pantalla.blit(cuadro_texto["superficie"], cuadro_texto["rectangulo"])
    
    # -------- BOTON DE GUARDAR PARTIDA --------
    mostrar_texto(
    boton_guardar_partida["superficie"], "Guardar partida", (15, 6), FUENTE_ARIAL_20, COLOR_BLANCO)
    pantalla.blit(boton_guardar_partida["superficie"], boton_guardar_partida["rectangulo"]
    )

    # -------- MENSAJE DE ERROR PERMANENTE --------
    if datos_juego["error_nombre"]:
        mostrar_texto(pantalla,"INGRESE UN NOMBRE PARA CONTINUAR", (50, 350), FUENTE_ARIAL_30, COLOR_ROJO)

    return ventana