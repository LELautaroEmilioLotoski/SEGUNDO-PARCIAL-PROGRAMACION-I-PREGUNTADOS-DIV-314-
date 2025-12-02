import random
import os
import time
from Constantes import *
from datetime import datetime
import json
import pygame

def mostrar_texto(surface, text, pos, font, color=pygame.Color('black')):
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

def borrar():
    os.system('clear') #MAC/LINUX
    os.system('clear')
    #os.system('cls') #WINDOWS
    #os.system('cls') #WINDOWS


def crear_datos_juego() -> dict:
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
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        retorno = True
        datos_juego["cantidad_vidas"] += incremento
    else:
        retorno = False

    return retorno

#Modifica la puntuacion
def modificar_puntuacion(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("puntuacion") != None:
        retorno = True
        datos_juego["puntuacion"] += (incremento)
    else:
        retorno = False

    return retorno

# SUMA UNA VIDA SI RESPONDIÓ CORRECTAMENTE 5 VECES SEGUIDAS
def sumar_vida(pregunta_actual:dict,datos_juego:dict) -> bool:
    if type(pregunta_actual) == dict and pregunta_actual.get("respuesta_correcta") != None:
        # AGREGAMOS UNA VIDA MAS
        modificar_vida(datos_juego, 1)
        datos_juego["contador_correctas"] = 0   # reiniciar

    else:
        modificar_vida(datos_juego,-1)
                
#Verifico que la respuesta sea correcta
def verificar_respuesta(pregunta_actual:dict,datos_juego:dict,respuesta:int,sonido_acierto:pygame.mixer.Sound,sonido_error:pygame.mixer.Sound) -> bool:

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
    if type(lista_preguntas) == list and len(lista_preguntas) > 0 and type(datos_juego) == dict and datos_juego.get("i_pregunta") != None:
        indice = datos_juego.get("i_pregunta")
        pregunta = lista_preguntas[indice]
    else:
        pregunta = None

    return pregunta

#Pasa de pregunta
def pasar_pregunta(datos_juego:dict,lista_preguntas:list) -> bool:
    if type(datos_juego) == dict and datos_juego.get("i_pregunta") != None:
        retorno = True
        datos_juego["i_pregunta"] += 1
        verificar_indice(datos_juego,lista_preguntas)
    else:
        retorno = False

    return retorno

def reiniciar_estadisticas(datos_juego:dict) -> bool:
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
    if type(lista_preguntas) == list and len(lista_preguntas) > 0:
        retorno = True
        random.shuffle(lista_preguntas)
    else:
        retorno = False

    return retorno

def guardar_partida(datos_juego:dict) -> bool:
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

    # RECORREMOS EL ARCHIVO PARTIDAS JSON
    with open("partidas.json", "r") as archivo:
        partidas = json.load(archivo)

    # ORDENA LA LISTA COMPLETA POR PUNTUACIÓN
    partidas_ordenadas = sorted(partidas, key=lambda p: p["puntuacion"], reverse=True)

    # RETORNAMOS 10 DE LAS PARTIDAS FILTRADAS POR PUNTUACIÓN
    return partidas_ordenadas[:10]


#Revisa que bloque de respuesta se clickeo
def responder_pregunta_pygame(lista_respuestas:list,sonido_acierto:pygame.mixer.Sound,sonido_error: pygame.mixer.Sound,pos_mouse:tuple,lista_preguntas:list,pregunta_actual:dict,datos_juego:dict):
    #Validar todo que sea correcto

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
    pantalla.fill(COLOR_BLANCO)
    mostrar_datos_juego_pygame(pantalla,datos_juego)


    mostrar_texto(cuadro_pregunta["superficie"],f"{pregunta_actual["descripcion"]}",(20,20),FUENTE_ARIAL_30)
    pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])

    for i in range(len(lista_respuestas)):
        if (i != datos_juego["indice_bomba_1"] and i != datos_juego["indice_bomba_2"] and i != datos_juego["indice_shield"]):
            mostrar_texto(lista_respuestas[i]["superficie"],f"{pregunta_actual.get(f"respuesta_{i+1}")}",(10,10),FUENTE_ARIAL_20,COLOR_BLANCO)
            pantalla.blit(lista_respuestas[i]["superficie"],lista_respuestas[i]["rectangulo"])
    
    mostrar_comodines(lista_comodines,pantalla,datos_juego)




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