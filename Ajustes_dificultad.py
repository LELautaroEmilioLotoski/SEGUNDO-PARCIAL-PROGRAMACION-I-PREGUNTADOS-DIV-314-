import pygame
from Funciones import *
from Constantes import *

# CREA UNA LISTA DE BOTONES
def crear_lista_botones(cantidad_botones:int,textura:str,ancho:int,alto:int,x:int,y:int) -> list | None:
    """crea la lista de los botones para usar

    Args:
        cantidad_botones (int): cantidad
        textura (str): textura del boton
        ancho (int): ancho del boton
        alto (int): alto del boton
        x (int): posicion x del boton
        y (int): posicion y del boton

    Returns:
        list | None: retorna la lista creada o None si algo salió mal
    """
    if os.path.exists(textura):
        lista_botones = []

        for i in range(cantidad_botones):
            boton = crear_elemento_juego(textura,ancho,alto,x,y)
            lista_botones.append(boton)
            y += (alto + 45)
    else:
        lista_botones = None
        
    return lista_botones


# FONDO
fondo_menu = pygame.image.load("texturas/fondo.jpg")
fondo_menu = pygame.transform.scale(fondo_menu, PANTALLA)

# BOTONES
lista_botones = crear_lista_botones(4, "texturas/textura_respuesta.jpg", ANCHO_BOTON, ALTO_BOTON, 150, 90)

lista_textos_botones = ["VIDAS", "SUMAR PUNTOS", "RESTAR PUNTOS", "TIEMPO"]

pygame.init()

# Variable global para saber qué botón está seleccionado
boton_seleccionado = None

boton_volver = crear_elemento_juego("texturas/textura_respuesta.jpg",100,40,10,10)
boton_guardar_cambios = crear_elemento_juego("texturas/textura_respuesta.jpg",150,40,150,500)


inputs_usuario = {
    "VIDAS": "",
    "SUMAR PUNTOS": "",
    "RESTAR PUNTOS": "",
    "TIEMPO": ""
}


def ajustar_dificultad(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], datos_juego:dict) -> str | dict:
    """ajusta la dificultad de acuerdo a lo que eliga el jugador

    Args:
        pantalla (pygame.Surface): pantalla actual
        cola_eventos (list[pygame.event.Event]): eventos recibidos
        datos_juego (dict): datos actuales del juego

    Returns:
        str | dict: retorna la ventana actual y el diccionario de los inputs de usuario
    """
    global boton_seleccionado    
    ventana = "configuracion"

    # ----- DETECTAR CLICK -----
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for i, boton in enumerate(lista_botones):
                if boton["rectangulo"].collidepoint(pos):
                    CLICK_SONIDO.play()
                    boton_seleccionado = i   # GUARDAMOS QUÉ BOTÓN SE EDITA
                    break
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                ventana = "menu"
            if boton_guardar_cambios["rectangulo"].collidepoint(evento.pos):
                CLICK_SONIDO.play()
                ventana = "jugar"
                
                
        # ----- DETECTAR TEXTO INGRESADO -----
        if evento.type == pygame.TEXTINPUT and boton_seleccionado is not None:
            if evento.text.isdigit():  # Solo números

                opcion = lista_textos_botones[boton_seleccionado]

                # Acumula los dígitos
                inputs_usuario[opcion] += evento.text

                # Convierte el texto acumulado a número
                valor = int(inputs_usuario[opcion])

                if opcion == "VIDAS":
                    datos_juego["cantidad_vidas"] = valor

                elif opcion == "SUMAR PUNTOS":
                    datos_juego["puntos_acierto"] = valor

                elif opcion == "RESTAR PUNTOS":
                    datos_juego["puntos_error"] = valor

                elif opcion == "TIEMPO":
                    datos_juego["tiempo_restante"] = valor
        
        elif evento.type == pygame.KEYDOWN and boton_seleccionado is not None:
            if evento.key == pygame.K_BACKSPACE:

                opcion = lista_textos_botones[boton_seleccionado]

                # Borrar último carácter
                inputs_usuario[opcion] = inputs_usuario[opcion][:-1]

                # Si está vacío, ponelo en 0
                if inputs_usuario[opcion] == "":
                    valor = 0
                else:
                    valor = int(inputs_usuario[opcion])

                # Actualizar datos_juego
                if opcion == "VIDAS":
                    datos_juego["cantidad_vidas"] = valor

                elif opcion == "SUMAR PUNTOS":
                    datos_juego["puntos_acierto"] = valor

                elif opcion == "RESTAR PUNTOS":
                    datos_juego["puntos_error"] = valor

                elif opcion == "TIEMPO":
                    datos_juego["tiempo_restante"] = valor


    # ----- DIBUJAR -----
    pantalla.blit(fondo_menu, (0, 0))
    
    for i in range(len(lista_botones)):

        x = lista_botones[i]["rectangulo"].x
        y = lista_botones[i]["rectangulo"].y

        # ---- DIBUJAR LABEL ARRIBA DEL BOTÓN ----
        mostrar_texto(
            pantalla,
            lista_textos_botones[i],
            (x, y - 35),     # <-- 35 píxeles más arriba
            FUENTE_ARIAL_30,
            COLOR_BLANCO    
        )

        # ---- DIBUJAR EL BOTÓN VACÍO ----
        pantalla.blit(lista_botones[i]["superficie"], lista_botones[i]["rectangulo"])

        # ---- MOSTRAR EL VALOR INGRESADO ----
        texto_valor = inputs_usuario[lista_textos_botones[i]] or "0"

        mostrar_texto(
            pantalla,
            texto_valor,
            (x + 20, y + 10),
            FUENTE_ARIAL_25,
            COLOR_BLANCO
        )

    # -------- BOTON DE VOLVER  --------
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla,"VOLVER",(boton_volver["rectangulo"].x + 5, boton_volver["rectangulo"].y + 5),FUENTE_ARIAL_20,COLOR_BLANCO)


    # -------- BOTON DE GUARDAR CAMBIOS --------
    mostrar_texto(
    boton_guardar_cambios["superficie"], "Guardar cambios", (15, 6), FUENTE_ARIAL_20, COLOR_BLANCO)
    pantalla.blit(boton_guardar_cambios["superficie"], boton_guardar_cambios["rectangulo"]
    )

    return ventana, inputs_usuario
