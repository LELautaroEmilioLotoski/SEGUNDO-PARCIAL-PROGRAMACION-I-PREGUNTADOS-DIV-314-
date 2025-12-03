import random
import os
import time
from Constantes import *
from datetime import datetime
import json
import pygame

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
    """
    Renderiza texto con salto de línea automático según el ancho disponible
    en la superficie, dibujándolo palabra por palabra.

    Args:
        surface (pygame.Surface): Superficie donde se dibuja el texto.
        text (str): Texto a mostrar (puede incluir saltos de línea).
        pos (tuple): Posición inicial (x, y) del texto.
        font (pygame.font.Font): Fuente utilizada para renderizar.
        color (pygame.Color, optional): Color del texto. Default: negro.
    """
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def mostrar_texto_en_rect(surface, text, rect, font, color=pygame.Color('black')):
    """    La función divide el texto por palabras y genera tantas líneas como sean
    necesarias para que ninguna exceda el ancho disponible. Luego calcula la
    altura total generada para centrar el bloque completo dentro del rectángulo.

    Args:
        surface (pygame.Surface): Superficie donde se dibuja el texto.
        text (str): Texto a mostrar. Puede incluir saltos de línea.
        rect (pygame.Rect): Área donde debe ubicarse el texto.
        font (pygame.font.Font): Fuente usada para renderizar el texto.
        color (pygame.Color, optional): Color del texto. Por defecto negro.

    """
    words = [word.split(' ') for word in text.splitlines()]  # palabras por línea
    space = font.size(' ')[0]

    # Primero armamos todas las líneas renderizadas
    lines = []
    for line_words in words:
        line_surf = []
        line_width = 0
        for word in line_words:
            w_surf = font.render(word, True, color)
            w_width, w_height = w_surf.get_size()

            if line_width + w_width > rect.width - 10:  
                # Línea nueva si ya no entra en el ancho
                lines.append((line_surf, line_width))
                line_surf = []
                line_width = 0

            line_surf.append((w_surf, w_width))
            line_width += w_width + space

        lines.append((line_surf, line_width))

    # Altura total del texto
    total_height = len(lines) * font.get_height()

    # Coordenada Y inicial para centrar verticalmente
    y = rect.y + (rect.height - total_height) // 2

    # Dibujamos todas las líneas centradas
    for line_surf, line_width in lines:
        x = rect.x + (rect.width - line_width) // 2  # centrar horizontal
        for surf_word, w_width in line_surf:
            surface.blit(surf_word, (x, y))
            x += w_width + space
        y += font.get_height()

def borrar():
    os.system('clear') #MAC/LINUX
    os.system('clear')
    #os.system('cls') #WINDOWS
    #os.system('cls') #WINDOWS


def crear_datos_juego() -> dict:
    """la funcion crea el diccionario que se va a usar en el juego

    Returns:
        dict: el diccionario del juego
    """
    datos_juego = {
        "nombre":"",
        "tiempo_restante":TIEMPO_TOTAL,
        "puntuacion":0,
        "cantidad_vidas":CANTIDAD_VIDAS,
        "i_pregunta":0,
        "volumen_musica":100,
        "musica_activa":True,
        "comodin_bomba":False,
        "comodin_x2":False,
        "bandera_x2":False,
        "comodin_pass":False,
        "comodin_shield":False,
        "doble_chance_activo":False,
        "indice_shield":None,
        "indice_bomba_1":None,
        "indice_bomba_2":None,
        "contador_correctas": 0
    }
    

    return datos_juego

#obtenemos las preguntas desde un archivo csv
def cargar_preguntas_desde_csv(ruta:str) -> list:
    """ nos permite cargar las preguntas desde un archivo csv

    Args:
        ruta (str): ruta del archivo csv

    Returns:
        list: devuelve la lista con el json 
    """
    if type(ruta) == str:
        lista = []
        #abrimos el archivo en modo lectura
        with open(ruta, "r", encoding="utf-8") as archivo:
            encabezado = True
            #iteramos sobre el archivo csv
            for linea in archivo:
                if encabezado:
                    encabezado = False
                    continue
                
                #eliminamos los espacios que haya y dividimos los strings por comas
                partes = linea.strip().split(",")
                #creamos el diccionario
                pregunta = {
                    "descripcion": partes[0],
                    "respuesta_1": partes[1],
                    "respuesta_2": partes[2],
                    "respuesta_3": partes[3],
                    "respuesta_4": partes[4],
                    "respuesta_correcta": int(partes[5])
                }
                #guardamos el diccionario creado dentro de la lista
                lista.append(pregunta)
        
        #retornamos la lista
        return lista

#Actualiza el tiempo
def actualizar_tiempo(tiempo_inicio:float,datos_juego:dict) -> bool:
    """Actualiza el tiempo restante del juego según el tiempo transcurrido
    desde que inició la partida.

    Args:
        tiempo_inicio (float): Momento en que comenzó el juego (timestamp).
        datos_juego (dict): Diccionario con los datos actuales del juego.

    Returns:
        bool: True si se actualizó correctamente, False en caso contrario.
    """
    if type(datos_juego) == dict:
        retorno = True
        tiempo_fin = time.time()
        lapso_tiempo = int(round((tiempo_fin - tiempo_inicio),0))
        datos_juego["tiempo_restante"] = TIEMPO_TOTAL - lapso_tiempo
    else:
        retorno = False

    return retorno

#Modifica la vida
def modificar_vida(datos_juego:dict,incremento:int) -> bool:
    """la funcion modifica la cantidad de vidas de acuerdo a la cantidad de incremento recibida por parámetro
    Args:
        datos_juego (dict): datos actuales del juego
        incremento (int): la cantidad por la cual se va aumentar las vidas

    Returns:
        bool: _description_
    """
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        retorno = True
        datos_juego["cantidad_vidas"] += incremento
    else:
        retorno = False

    return retorno

#Modifica la puntuacion
def modificar_puntuacion(datos_juego:dict,incremento:int) -> bool:
    """la funcion modifica la puntuación de acuerdo a la cantidad de incremento recibida por parámetro
    Args:
        datos_juego (dict): datos actuales del juego
        incremento (int): la cantidad por la cual se va aumentar la puntuación

    Returns:
        bool: _description_
    """
    if type(datos_juego) == dict and datos_juego.get("puntuacion") != None:
        retorno = True
        datos_juego["puntuacion"] += (incremento)
    else:
        retorno = False

    return retorno

# CREA UNA LISTA DE BOTONES
def crear_lista_botones(cantidad_botones:int,textura:str,ancho:int,alto:int,x:int,y:int) -> list | None:
    """Crea una lista de botones utilizando una textura y los posiciona
    verticalmente uno debajo del otro.

    Args:
        cantidad_botones (int): Cantidad de botones a generar.
        textura (str): Ruta de la imagen a usar como textura del botón.
        ancho (int): Ancho de cada botón.
        alto (int): Alto de cada botón.
        x (int): Posición X inicial de los botones.
        y (int): Posición Y inicial del primer botón.

    Returns:
        list | None: Lista de botones creados o None si la textura no existe.
    """
    if os.path.exists(textura):
        lista_botones = []

        for i in range(cantidad_botones):
            boton = crear_elemento_juego(textura,ancho,alto,x,y)
            lista_botones.append(boton)
            y += (alto + 15)
    else:
        lista_botones = None
        
    return lista_botones



# SUMA UNA VIDA SI RESPONDIÓ CORRECTAMENTE 5 VECES SEGUIDAS
def sumar_vida(pregunta_actual:dict,datos_juego:dict) -> bool:
    """Aumenta una vida si la respuesta actual es correcta; de lo contrario
    descuenta una.

    Args:
        pregunta_actual (dict): Datos de la pregunta actual.
        datos_juego (dict): Información del estado del juego.

    Returns:
        bool: True si la operación fue válida, False en caso contrario.
    """
    if type(pregunta_actual) == dict and pregunta_actual.get("respuesta_correcta") != None:
        # AGREGAMOS UNA VIDA MAS
        modificar_vida(datos_juego, 1)
        datos_juego["contador_correctas"] = 0   # reiniciar

    else:
        modificar_vida(datos_juego,-1)
                
#Verifico que la respuesta sea correcta
def verificar_respuesta(pregunta_actual:dict,datos_juego:dict,respuesta:int,sonido_acierto:pygame.mixer.Sound,sonido_error:pygame.mixer.Sound) -> bool:
    """
    Verifica si la respuesta elegida es correcta y actualiza el estado del juego.

    Args:
        pregunta_actual (dict): Pregunta actual con su respuesta correcta.
        datos_juego (dict): Datos del juego (vidas, puntuación, comodines, etc.).
        respuesta (int): Respuesta seleccionada por el jugador.
        sonido_acierto (pygame.mixer.Sound): Sonido a reproducir si acierta.
        sonido_error (pygame.mixer.Sound): Sonido a reproducir si falla.

    Returns:
        bool: True si la respuesta es correcta, False en caso contrario.
    """
    if type(pregunta_actual) == dict and pregunta_actual.get("respuesta_correcta") != None:
        if pregunta_actual.get("respuesta_correcta") == respuesta:
            datos_juego["contador_correctas"] += 1
            datos_juego["doble_chance_activo"] = False
            if datos_juego["comodin_x2"] == True and datos_juego["bandera_x2"] == False:
                datos_juego["bandera_x2"] = True
                modificar_puntuacion(datos_juego,(100*2))
                sonido_acierto.play()
            else:
                modificar_puntuacion(datos_juego,100)
                sonido_acierto.play()
            retorno = True
            if datos_juego["contador_correctas"] == 5:
                # AVERIGUAMOS SI LA CANTIDAD DE RESPUESTAS CORRECTAS ES 5 Y DE SER ASÍ, AGREGAMOS UNA VIDA MAS
                sumar_vida(pregunta_actual, datos_juego)
        else:
            if (datos_juego["comodin_shield"] == True or datos_juego["comodin_shield"] == False) and datos_juego["doble_chance_activo"] == False:
                sonido_error.play()
                modificar_puntuacion(datos_juego,-25)
                modificar_vida(datos_juego,-1)
            retorno = False
    else:
        retorno = False

    return retorno

def obtener_pregunta_actual(datos_juego:dict,lista_preguntas:list) -> dict | None:
    """nos permite obtener la pregunta actual

    Args:
        datos_juego (dict): los datos actuales del juego
        lista_preguntas (list): la lista total de preguntas

    Returns:
        dict | None: 'dict' si encontró la pregunta | 'None' si no la encontró
    """
    if type(lista_preguntas) == list and len(lista_preguntas) > 0 and type(datos_juego) == dict and datos_juego.get("i_pregunta") != None:
        indice = datos_juego.get("i_pregunta")
        pregunta = lista_preguntas[indice]
    else:
        pregunta = None

    return pregunta

#Pasa de pregunta
def pasar_pregunta(datos_juego:dict,lista_preguntas:list) -> bool:
    """
    Avanza a la siguiente pregunta y valida que el índice no supere el límite.

    Args:
        datos_juego (dict): Estado del juego, incluyendo el índice de pregunta.
        lista_preguntas (list): Lista completa de preguntas del juego.

    Returns:
        bool: True si se pudo avanzar, False si hubo algún error.
    """
    if type(datos_juego) == dict and datos_juego.get("i_pregunta") != None:
        retorno = True
        datos_juego["i_pregunta"] += 1
        verificar_indice(datos_juego,lista_preguntas)
    else:
        retorno = False

    return retorno

def reiniciar_estadisticas(datos_juego:dict) -> bool:
    """Reiniciamos las estadísticas actuales

    Args:
        datos_juego (dict): datos actuales del juego

    Returns:
        bool: 'True' si todo salió bien | 'False' si algo salió mal
    """
    if type(datos_juego) == dict:
        retorno = True
        datos_juego.update({
            "tiempo_restante":TIEMPO_TOTAL,
            "puntuacion":0,
            "cantidad_vidas":CANTIDAD_VIDAS
        })
    else:
        retorno = False

    return retorno

#Verifica el indice
def verificar_indice(datos_juego:dict,lista_preguntas:list) -> bool:
    """
    Verifica que el índice de pregunta sea válido y reinicia la lista si llega al final.

    Args:
        datos_juego (dict): Datos del juego, incluyendo el índice actual.
        lista_preguntas (list): Lista de preguntas disponibles.

    Returns:
        bool: 'True' si todo salió bien | 'False' si algo salió mal
    """
    if type(datos_juego) == dict and datos_juego.get("i_pregunta") != None:
        retorno = True
        if datos_juego["i_pregunta"] == len(lista_preguntas):
            datos_juego["i_pregunta"] = 0
            mezclar_lista(lista_preguntas)
    else:
        retorno = False

    return retorno

#Mezcla la lista de preguntas
def mezclar_lista(lista_preguntas:list) -> bool:
    """
    Mezcla aleatoriamente la lista de preguntas.

    Args:
        lista_preguntas (list): Lista de preguntas a mezclar.

    Returns:
        bool: True si la lista se mezcló correctamente, False si ocurrió un error.
    """
    if type(lista_preguntas) == list and len(lista_preguntas) > 0:
        retorno = True
        random.shuffle(lista_preguntas)
    else:
        retorno = False

    return retorno

def guardar_partida(datos_juego:dict) -> bool:
    """
    Guarda la partida actual validando el nombre del jugador y confirmando que los datos se hayan almacenado correctamente.

    Args:
        datos_juego (dict): Datos actuales del juego (nombre, puntuación, etc.).

    Returns:
        bool: True si la partida se guardó con éxito, False si falló la validación o el guardado.
    """
    if type(datos_juego) == dict:

        # SETEAMOS UN ESTADO PARA GUARDAR EL RESULTADO DE LA VALIDACION DE LA PARTIDA GUARDADA
        estado = None

        # CREAMOS EL NUEVO DICCIONARIO
        nueva_partida = {
            "nombre": datos_juego["nombre"],
            "puntuacion": datos_juego["puntuacion"],
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # VALIDAMOS QUE HAYA PUESTO UN NOMBRE:
        if len(nueva_partida["nombre"]) == 0:
            estado = False
            return estado
        else:
            # CARGAMOS LOS DATOS:
            cargar_datos(nueva_partida)

        # VALIDAMOS QUE SE HAYA GUARDADO LA PARTIDA CORRECTAMENTE:
        validacion_de_partida = validacion_partida_guardada(nueva_partida)

        # DEPENDIENDO DEL VALOR DE ESTADO OBTENIDO, LO SETEAMOS
        if validacion_de_partida == True: estado = True
        else: estado = False

        # DEVOLVEMOS EL ESTADO OBTENIDO
        return estado

    print(nueva_partida)

def cargar_datos(nueva_partida_a_cargar:dict) -> None:
        """
    Agrega una nueva partida al archivo partidas.json.

    Args:
        nueva_partida_a_cargar (dict): Partida a guardar, incluyendo nombre, puntuación y fecha.

    Returns:
        None
    """
        # VALIDAMOS QUE LOS DATOS DE LA NUEVA PARTIDA SEA UN DICCIONARIO
        if type(nueva_partida_a_cargar) == dict:

            # LEEMOS EL ARCHIVO PARTIDAS.JSON Y GUARDAMOS EL CONTENIDO EN UNA VARIABLE
            with open("partidas.json", "r") as archivo:
                partidas = json.load(archivo)

            # CARGAMOS EL JSON CON LA NUEVA PARTIDA
            partidas.append(nueva_partida_a_cargar)

            # ESCRIBIMOS EL ARCHIVO JSON CON EL CONTENIDO YA CARGADO
            with open("partidas.json", "w") as archivo:
                json.dump(partidas, archivo, indent=4)
                
def validacion_partida_guardada(nueva_partida:dict) -> bool:
        """
    Verifica si la partida recién guardada existe dentro del archivo partidas.json.

    Args:
        nueva_partida (dict): Datos de la partida que se desea validar.

    Returns:
        bool: True si la partida fue encontrada en el archivo, False en caso contrario.
    """
    
        # VALIDAMOS QUE LOS DATOS DE LA NUEVA PARTIDA SEA UN DICCIONARIO
        if type(nueva_partida) == dict:
            estado = None
            # LEEMOS EL ARCHIVO PARTIDAS.JSON Y GUARDAMOS EL CONTENIDO EN UNA VARIABLE
            with open("partidas.json", "r") as archivo:
                partidas = json.load(archivo)

            # RECORREMOS EL JSON OBTENIDO DEL ARCHIVO
            for indice, dato in enumerate(partidas):

                # VALIDAMOS QUE LOS DATOS INGRESADOS DE LA NUEVA PARTIDA EXISTAN DENTRO DEL ARCHIVO
                if (dato["nombre"] == nueva_partida["nombre"] and dato["puntuacion"] == nueva_partida["puntuacion"] and dato["fecha"] == nueva_partida["fecha"]):
                    estado = True # ACTUALIZAMOS ESTADO Y LO RETORNAMOS
                else:
                    estado = False # ACTUALIZAMOS ESTADO Y LO RETORNAMOS
            return estado
        
    
#GENERAL --> Un elemento de nuestro juego va a tener una superficie (textura) y un rectangulo (coordenadas y su compotamiento)
def crear_elemento_juego(textura:str,ancho_elemento:int,alto_elemento:int,pos_x:int,pos_y:int) -> dict | None:
        """
    Crea un elemento del juego cargando su textura, escalándola y generando su rectángulo asociado.

    Args:
        textura (str): Ruta de la imagen a cargar.
        ancho_elemento (int): Ancho deseado del elemento.
        alto_elemento (int): Alto deseado del elemento.
        pos_x (int): Posición X en pantalla.
        pos_y (int): Posición Y en pantalla.

    Returns:
        dict | None: Diccionario con superficie y rectángulo, o None si la textura no existe.
    """
        if os.path.exists(textura):
            elemento_juego = {}
            elemento_juego["superficie"] = pygame.image.load(textura)
            elemento_juego["superficie"] = pygame.transform.scale(elemento_juego["superficie"],(ancho_elemento,alto_elemento))
            elemento_juego["rectangulo"] = pygame.rect.Rect(pos_x,pos_y,ancho_elemento,alto_elemento)
        else:
            elemento_juego = None

        return elemento_juego

#muestro los datos
def mostrar_datos_juego_pygame(pantalla:pygame.Surface,datos_juego:dict) -> bool:
    """
    Muestra en pantalla la información principal del juego (tiempo, puntuación y vidas).

    Args:
        pantalla (pygame.Surface): Superficie donde se renderiza el texto.
        datos_juego (dict): Datos actuales del juego.

    Returns:
        bool: True si los datos fueron mostrados correctamente, False si ocurrió un error.
    """
    if type(datos_juego) == dict:
        mostrar_texto(pantalla,f"Tiempo: {datos_juego.get("tiempo_restante")} segundos",(10,10),FUENTE_ARIAL_20)
        mostrar_texto(pantalla,f"Puntuacion: {datos_juego.get("puntuacion")}",(10,40),FUENTE_ARIAL_20)
        mostrar_texto(pantalla,f"Vidas: {datos_juego.get("cantidad_vidas")}",(10,70),FUENTE_ARIAL_20)
        retorno = True
    else:
        retorno = False

    return retorno

#Crea la lista de respuesta dependiendo la pregunta
def crear_lista_respuestas(cantidad_respuestas:int,textura:str,ancho:int,alto:int,x:int,y:int) -> list | None:
    """
    Crea una lista de cuadros de respuesta posicionados verticalmente a partir de una textura.

    Args:
        cantidad_respuestas (int): Número de respuestas a generar.
        textura (str): Ruta de la imagen a usar en cada cuadro.
        ancho (int): Ancho de cada cuadro de respuesta.
        alto (int): Alto de cada cuadro de respuesta.
        x (int): Posición X inicial.
        y (int): Posición Y inicial.

    Returns:
        list | None: Lista de cuadros de respuesta creados, o None si la textura no existe.
    """
    if os.path.exists(textura):
        lista_respuestas = []

        for i in range(cantidad_respuestas):
            cuadro_respuesta = crear_elemento_juego(textura,ancho,alto,x,y)
            lista_respuestas.append(cuadro_respuesta)
            y += (alto + 15)
    else:
        lista_respuestas = None

    return lista_respuestas

def obtener_ranking() -> list:
    """
    Obtiene las 10 mejores partidas desde el archivo partidas.json,
    ordenadas por puntuación de mayor a menor.

    Returns:
        list: Lista con las 10 partidas con mayor puntuación.
    """
    # RECORREMOS EL ARCHIVO PARTIDAS JSON
    with open("partidas.json", "r") as archivo:
        partidas = json.load(archivo)

    # ORDENA LA LISTA COMPLETA POR PUNTUACIÓN
    partidas_ordenadas = sorted(partidas, key=lambda p: p["puntuacion"], reverse=True)

    # RETORNAMOS 10 DE LAS PARTIDAS FILTRADAS POR PUNTUACIÓN
    return partidas_ordenadas[:10]


#Revisa que bloque de respuesta se clickeo
def responder_pregunta_pygame(lista_respuestas:list,sonido_acierto:pygame.mixer.Sound,sonido_error: pygame.mixer.Sound,pos_mouse:tuple,lista_preguntas:list,pregunta_actual:dict,datos_juego:dict):
    """
    Procesa el clic del jugador sobre una respuesta, valida si es correcta y
    avanza a la siguiente pregunta según corresponda.

    Args:
        lista_respuestas (list): Elementos gráficos de las respuestas.
        sonido_acierto (pygame.mixer.Sound): Sonido al acertar.
        sonido_error (pygame.mixer.Sound): Sonido al fallar.
        pos_mouse (tuple): Posición del clic del mouse.
        lista_preguntas (list): Lista completa de preguntas.
        pregunta_actual (dict): Pregunta actualmente mostrada.
        datos_juego (dict): Estado y datos del juego.

    Returns:
        bool: True si se hizo clic sobre una respuesta, False si se clickeó fuera.
    """
    #DEVUELVE VERDADERO SI LE DI CLICK A UNA RESPUESTA
    #DEVUELVE FALSE SI LE DI CLICK FUERA DE UNA RESPUESTA
    retorno = False
    check = None
    for i in range(len(lista_respuestas)):
        if lista_respuestas[i]["rectangulo"].collidepoint(pos_mouse):
            respuesta = i + 1
            datos_juego["indice_shield"] = None
            check =  verificar_respuesta(pregunta_actual,datos_juego,respuesta,sonido_acierto,sonido_error)
            if check == True and (datos_juego["comodin_shield"] == True or datos_juego["comodin_shield"] == False) and datos_juego["doble_chance_activo"] == False:
                pasar_pregunta(datos_juego,lista_preguntas)
            elif check == False and datos_juego["comodin_shield"] == True and datos_juego["doble_chance_activo"] == True:
                datos_juego["doble_chance_activo"] = False
                datos_juego["indice_shield"] = i
            else:
                pasar_pregunta(datos_juego,lista_preguntas)
            retorno = True

    return retorno

def mostrar_comodines(lista_comodines:list,pantalla:pygame.Surface,datos_juego:dict) -> None:
    """Muestreo de los comodines

    Args:
        lista_comodines (list): Lista de comodines del juego
        pantalla (pygame.Surface): Pantalla donde se muestran los comodines
        datos_juego (dict): Datos del juego
    """
    for i in range(len(lista_comodines)):
        if i == 0 and datos_juego["comodin_bomba"] == True:
            continue  # NO lo muestro y sigo
        if i == 1 and datos_juego["comodin_shield"] == True:
            continue
        if i == 2 and datos_juego["comodin_pass"] == True:
            continue
        if i == 3 and datos_juego["comodin_x2"] == True:
            continue

        pantalla.blit(lista_comodines[i]["superficie"],lista_comodines[i]["rectangulo"])


#Muestra la pantalla de juego
def dibujar_pantalla_juego(pantalla:pygame.Surface,datos_juego:dict,cuadro_pregunta:dict,lista_respuestas:dict,lista_comodines:list,pregunta_actual:dict) -> None:
    """
    Dibuja todos los elementos principales de la pantalla de juego para la dificultad "facil":
    fondo, datos del jugador, pregunta actual, respuestas y comodines.

    Args:
        pantalla (pygame.Surface): Superficie donde se renderiza la escena.
        datos_juego (dict): Datos actuales del estado del juego.
        cuadro_pregunta (dict): Elemento gráfico que contiene la pregunta.
        lista_respuestas (list): Lista de elementos gráficos de respuestas.
        lista_comodines (list): Elementos de comodines disponibles.
        pregunta_actual (dict): Pregunta que se muestra actualmente.
    """
    # FONDO
    fondo_menu = pygame.image.load("texturas/juego.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, PANTALLA)
    
    # ---- DIBUJAR FONDO ----
    pantalla.blit(fondo_menu, (0, 0))
    mostrar_datos_juego_pygame(pantalla,datos_juego)


    mostrar_texto(cuadro_pregunta["superficie"], f"{pregunta_actual["descripcion"]}",(20,20),FUENTE_ARIAL_30)
    pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])

    for i in range(len(lista_respuestas)):
        if (i != datos_juego["indice_bomba_1"] and i != datos_juego["indice_bomba_2"] and i != datos_juego["indice_shield"]):
            mostrar_texto(lista_respuestas[i]["superficie"],f"{pregunta_actual.get(f"respuesta_{i+1}")}",(10,10),FUENTE_ARIAL_20,COLOR_BLANCO)
            pantalla.blit(lista_respuestas[i]["superficie"],lista_respuestas[i]["rectangulo"])
    
    mostrar_comodines(lista_comodines,pantalla,datos_juego)


def dibujar_pantalla_juego_general(pantalla:pygame.Surface,datos_juego:dict,cuadro_pregunta:dict,lista_respuestas:dict,pregunta_actual:dict) -> None:
    """
    Dibuja todos los elementos principales de la pantalla de juego para el resto de dificultades:
    fondo, datos del jugador, pregunta actual y respuestas

    Args:
        pantalla (pygame.Surface): Superficie donde se renderiza la escena.
        datos_juego (dict): Datos actuales del estado del juego.
        cuadro_pregunta (dict): Elemento gráfico que contiene la pregunta.
        lista_respuestas (list): Lista de elementos gráficos de respuestas.
        pregunta_actual (dict): Pregunta que se muestra actualmente.
    """
    # FONDO
    fondo_menu = pygame.image.load("texturas/juego.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, PANTALLA)
    
    # ---- DIBUJAR FONDO ----
    pantalla.blit(fondo_menu, (0, 0))
    mostrar_datos_juego_pygame(pantalla,datos_juego)

    mostrar_datos_juego_pygame(pantalla,datos_juego)

    mostrar_texto(cuadro_pregunta["superficie"],f"{pregunta_actual["descripcion"]}",(20,20),FUENTE_ARIAL_30)
    pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])

    for i in range(len(lista_respuestas)):
        mostrar_texto(lista_respuestas[i]["superficie"],f"{pregunta_actual.get(f"respuesta_{i+1}")}",(10,10),FUENTE_ARIAL_20,COLOR_BLANCO)
        pantalla.blit(lista_respuestas[i]["superficie"],lista_respuestas[i]["rectangulo"])
    



def activar_bomba(datos_juego:dict,lista_respuestas:list,pregunta_actual:dict) -> bool:
    """Activa el comodin de la bomba

    Args:
        datos_juego (dict): Datos del juego
        lista_respuestas (list): Lista de repuestas de la pregunta actual
        pregunta_actual (dict): Pregunta actual

    Returns:
        bool: Retorna True o False si todo se pudo hacer correctamente
    """
    a_eliminar = []
    lista_incorrectas = []

    if type(lista_respuestas) == list and len(lista_respuestas) > 0 and type(datos_juego) == dict and type(pregunta_actual) == dict:


        if "respuesta_correcta" not in pregunta_actual:
            return False
        if type(pregunta_actual["respuesta_correcta"]) != int:
            return False

        respuesta_correcta = pregunta_actual["respuesta_correcta"]

        if respuesta_correcta < 1 or respuesta_correcta > len(lista_respuestas):
            return False


        for x in range(len(lista_respuestas)):
            if (x+1) != respuesta_correcta:
                lista_incorrectas.append(x)

        if len(lista_incorrectas) < 2:
            return False

        try:
            a_eliminar = random.sample(lista_incorrectas, 2)
        except:
            return False

        datos_juego["comodin_bomba"] = True
        datos_juego["indice_bomba_1"] = a_eliminar[0]
        datos_juego["indice_bomba_2"] = a_eliminar[1]

        return True

    else:
        return False




def activar_x2(datos_juego:dict) -> bool:
    """Activa el comodin de pasar pregunta

    Args:
        datos_juego (dict): Datos del juego

    Returns:
        bool: Retorna True o False si todo se pudo hacer correctamente
    """
    if type(datos_juego) == dict and ("comodin_x2" in datos_juego) and (type(datos_juego["comodin_x2"]) == bool):

        retorno = True
        if datos_juego["comodin_x2"] == False:
            datos_juego["comodin_x2"] = True

    else:
        retorno = False

    return retorno



def activar_pass(datos_juego:dict,lista_preguntas:dict) -> bool:
    """Activa el comodin de pasar pregunta

    Args:
        datos_juego (dict): Datos del juego
        lista_preguntas (list): Lista de preguntas

    Returns:
        bool: Retorna True o False si todo se pudo hacer correctamente
    """
    if (type(datos_juego) == dict) and (type(lista_preguntas) == list) and ("comodin_pass" in datos_juego) and ("indice_bomba_1" in datos_juego) and ("indice_bomba_2" in datos_juego) and (type(datos_juego["comodin_pass"]) == bool):

        retorno = True
        if datos_juego["comodin_pass"] == False:
            datos_juego["comodin_pass"] = True
            pasar_pregunta(datos_juego,lista_preguntas)
            datos_juego["indice_bomba_1"] = None
            datos_juego["indice_bomba_2"] = None
    else:
        retorno = False

    return retorno



def activar_shield(datos_juego:dict) -> bool:
    """Activa el comodin de doble chance

    Args:
        datos_juego (dict): Datos del juego

    Returns:
        bool: Retorna True o False si todo se pudo hacer correctamente
    """
    if (type(datos_juego) == dict) and ("comodin_shield" in datos_juego) and ("doble_chance_activo" in datos_juego) and (type(datos_juego["comodin_shield"]) == bool) and (type(datos_juego["doble_chance_activo"]) == bool):

        retorno = True
        if datos_juego["comodin_shield"] == False:
            datos_juego["comodin_shield"] = True
            datos_juego["doble_chance_activo"] = True

    else:
        retorno = False

    return retorno

def reiniciar_indice_bomba(datos_juego:dict) -> bool:
    """Reinicio los indices del comodin bomba

    Args:
        datos_juego (dict): Datos del juego

    Returns:
        bool: Retorna True o False si todo se pudo hacer correctamente
    """
    if (type(datos_juego) == dict) and ("comodin_bomba" in datos_juego) and ("indice_bomba_1" in datos_juego) and ("indice_bomba_2" in datos_juego) and (type(datos_juego["comodin_bomba"]) == bool):

        retorno = True
        if datos_juego["comodin_bomba"] == True:
            datos_juego["indice_bomba_1"] = None
            datos_juego["indice_bomba_2"] = None
    else:
        retorno = False

    return retorno

def musica_activa(datos_juego:dict) -> bool:
    """Verifica si la musica esta activa o no

    Args:
        datos_juego (dict): Datos del juego

    Returns:
        bool: Retorna True o False si la validacion fue correcta o no
    """
    if (type(datos_juego) == dict) and ("musica_activa" in datos_juego) and (type(datos_juego["musica_activa"]) == bool):
        if datos_juego["musica_activa"]:

            try:
                pygame.mixer.init()
                pygame.mixer.music.load("sonidos/musica.mp3")
                volumen = datos_juego.get("volumen_musica",0) / 100
                pygame.mixer.music.set_volume(volumen)
                pygame.mixer.music.play(-1)
                return True
            except pygame.error as e:
                print(f"Error en Pygame: No se pudo cargar o reproducir la música. {e}")
                return False

        return True