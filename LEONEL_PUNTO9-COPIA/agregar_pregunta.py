import pygame
from Constantes import *
from Funciones import *

def crear_lista_botones(cantidad_botones:int,textura:str,ancho:int,alto:int,x:int,y:int) -> list | None:
    if os.path.exists(textura):
        lista_botones = []

        for i in range(cantidad_botones):
            boton = crear_elemento_juego(textura,ancho,alto,x,y)
            lista_botones.append(boton)
            y += (alto + 30)
    else:
        lista_botones = None
        
    return lista_botones

pygame.init()

campos = ["Pregunta", "Respuesta 1", "Respuesta 2", "Respuesta 3", "Respuesta 4", "Respuesta Correcta (1 - 4)"]
lista_preguntas = cargar_preguntas_desde_csv("MENU PYGAME 314/preguntas.csv")
boton_volver = crear_elemento_juego("MENU PYGAME 314/texturas/textura_respuesta.jpg",100,40,10,10)
boton_guardar = crear_elemento_juego("MENU PYGAME 314/texturas/textura_respuesta.jpg",100,40,490,10)

def guardar_pregunta(ruta:str, textos:list) -> bool:
    """Guarda las preguntas en el csv

    Args:
        ruta (str): Ruta del csv
        textos (list): Lista de elementos a guardar

    Returns:
        bool: Retorna True o False si la validacion es correcta
    """
    if not isinstance(ruta, str) or not isinstance(textos, list) or not textos:
        print("Advertencia: Tipos de datos o lista de textos incorrectos/vacíos.")
        return False
    else:
        linea = ",".join(textos) 
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")
        return True
   
    

def validar_conjunto(textos:list) -> bool:
    """Valido los elementos a guardar en el csv

    Args:
        textos (list): Elementos a guardar

    Returns:
        bool: Envia True o False si se pudo hacer la verificacion correctamente
    """
    for i in range(5):
        if len(textos[i]) == 0:
            return False
    
    resp_corr = textos[5]

    if (len(resp_corr) != 1) or (ord(resp_corr) < 49 or ord(resp_corr) > 52):
        return False
    
    return True
    
def agregar_pregunta_a_mano(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    """Agrega la pregunta al csv de manera manual

    Args:
        pantalla (pygame.Surface): Pantalla del juego
        cola_eventos (list[pygame.event.Event]): Cola de eventos 
        datos_juego (dict): Datos del juego

    Returns:
        str: La ventana en la cual esta ubicado
    """
    lista_botones = crear_lista_botones(6,"MENU PYGAME 314/texturas/textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,150,50)

    if "textos" not in datos_juego:
        datos_juego["textos"] = [""] * 6

    if "indice" not in datos_juego:
        datos_juego["indice"] = None
    
    if "save" not in datos_juego:
        datos_juego["save"] = None

    textos = datos_juego["textos"]
    indice = datos_juego["indice"]
    
    ventana = "agregar pregunta"


    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            # --- BOTÓN VOLVER ---
            try:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    ventana = "menu"
            except Exception:
                pass


            # --- BOTÓN GUARDAR ---
            try:
                if boton_guardar["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    try:
                        if validar_conjunto(textos):
                            guardar_pregunta("MENU PYGAME 314/preguntas.csv",textos)
                            datos_juego["textos"] = [""] * 6
                            datos_juego["indice"] = None
                            datos_juego["save"] = True
                        else:
                            datos_juego["save"] = False
                    except Exception:
                        datos_juego["save"] = False
                        # Evita crash si guardar falla
            except Exception:
                pass
            

            # --- ELEMENTOS ---
            for i in range(len(lista_botones)):
                try:
                    if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                        datos_juego["indice"] = i
                except Exception:
                    pass
                         
        indice = datos_juego["indice"]

        # --- TEXTO ---
        if (evento.type == pygame.TEXTINPUT) and (indice != None):
            textos[indice] += evento.text
        
        # --- TECLAS ESPECIALES ---
        if (evento.type == pygame.KEYDOWN) and (indice != None):
            if evento.key == pygame.K_BACKSPACE:
               textos[indice] = textos[indice][0:-1]  
            elif evento.key == pygame.K_RETURN:
                pass

    pantalla.fill(COLOR_BLANCO)
    
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(boton_volver["superficie"],"VOLVER",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)
    pantalla.blit(boton_guardar["superficie"],boton_guardar["rectangulo"])
    mostrar_texto(boton_guardar["superficie"],"GUARDAR",(5,5),FUENTE_ARIAL_20,COLOR_BLANCO)

    for i in range(len(lista_botones)):
        x = lista_botones[i]["rectangulo"].x
        y = lista_botones[i]["rectangulo"].y - 25
        mostrar_texto(pantalla, campos[i], (x, y), FUENTE_ARIAL_20, COLOR_NEGRO)
        mostrar_texto(lista_botones[i]["superficie"], f"{textos[i]}", (10, 10), FUENTE_ARIAL_20, COLOR_BLANCO)
        pantalla.blit(lista_botones[i]["superficie"],lista_botones[i]["rectangulo"])


    if datos_juego["save"] == False:
        mostrar_texto(pantalla,f"Error, verificar alguno de los parametros",(150,565),FUENTE_ARIAL_20,COLOR_NEGRO)

        
    return ventana
    










