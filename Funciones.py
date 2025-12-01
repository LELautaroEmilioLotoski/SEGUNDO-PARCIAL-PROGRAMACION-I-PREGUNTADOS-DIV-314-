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
        "cantidad_vidas":3,
        "i_pregunta":0,
        "volumen_musica":100,
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

def actualizar_tiempo(tiempo_inicio:float,datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        retorno = True
        tiempo_fin = time.time()
        lapso_tiempo = int(round((tiempo_fin - tiempo_inicio),0))
        datos_juego["tiempo_restante"] = TIEMPO_TOTAL - lapso_tiempo
    else:
        retorno = False
        
    return retorno
    

def modificar_vida(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        retorno = True
        datos_juego["cantidad_vidas"] += incremento
    else:
        retorno = False
        
    return retorno
    
def modificar_puntuacion(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("puntuacion") != None:
        retorno = True
        datos_juego["puntuacion"] += incremento
    else:
        retorno = False
        
    return retorno

def verificar_respuesta(pregunta_actual:dict,datos_juego:dict,respuesta:int,sonido_acierto:pygame.mixer.Sound,sonido_error:pygame.mixer.Sound) -> bool:
    if type(pregunta_actual) == dict and pregunta_actual.get("respuesta_correcta") != None:
        retorno = True
        
        if pregunta_actual.get("respuesta_correcta") == respuesta:
            modificar_puntuacion(datos_juego,100)
            datos_juego["contador_correctas"] += 1
            
            # AVERIGUAMOS SI LA CANTIDAD DE RESPUESTAS CORRECTAS ES 5 Y DE SER ASÍ, AGREGAMOS UNA VIDA MAS
            if datos_juego["contador_correctas"] == 5:
                modificar_vida(datos_juego, 1)
                datos_juego["contador_correctas"] = 0   # reiniciar
                
            sonido_acierto.play()
        else:
            modificar_puntuacion(datos_juego,-25)
            modificar_vida(datos_juego,-1)
            sonido_error.play()
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
            "cantidad_vidas":3
        })
    else:
        retorno = False
        
    return retorno

def verificar_indice(datos_juego:dict,lista_preguntas:list) -> bool:
    if type(datos_juego) == dict and datos_juego.get("i_pregunta") != None:
        retorno = True
        if datos_juego["i_pregunta"] == len(lista_preguntas):
            datos_juego["i_pregunta"] = 0
            mezclar_lista(lista_preguntas)    
    else:
        retorno = False
        
    return retorno

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

#FUNCIONES PYGAME

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

def mostrar_datos_juego_pygame(pantalla:pygame.Surface,datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        mostrar_texto(pantalla,f"Tiempo: {datos_juego.get("tiempo_restante")} segundos",(10,10),FUENTE_ARIAL_20)
        mostrar_texto(pantalla,f"Puntuacion: {datos_juego.get("puntuacion")}",(10,40),FUENTE_ARIAL_20)
        mostrar_texto(pantalla,f"Vidas: {datos_juego.get("cantidad_vidas")}",(10,70),FUENTE_ARIAL_20)
        retorno = True
    else:
        retorno = False
        
    return retorno

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

def responder_pregunta_pygame(lista_respuestas:list,sonido_acierto:pygame.mixer.Sound,sonido_error: pygame.mixer.Sound,pos_mouse:tuple,lista_preguntas:list,pregunta_actual:dict,datos_juego:dict):
    #Validar todo que sea correcto
    
    #DEVUELVE VERDADERO SI LE DI CLICK A UNA RESPUESTA
    #DEVUELVE FALSE SI LE DI CLICK FUERA DE UNA RESPUESTA
    retorno = False
    for i in range(len(lista_respuestas)):
        if lista_respuestas[i]["rectangulo"].collidepoint(pos_mouse):
            respuesta = i + 1
            verificar_respuesta(pregunta_actual,datos_juego,respuesta,sonido_acierto,sonido_error)
            pasar_pregunta(datos_juego,lista_preguntas)
            retorno = True
            
    return retorno

def dibujar_pantalla_juego(pantalla:pygame.Surface,datos_juego:dict,cuadro_pregunta:dict,lista_respuestas:dict,pregunta_actual:dict) -> None:
    pantalla.fill(COLOR_BLANCO)
    mostrar_datos_juego_pygame(pantalla,datos_juego)
    
    mostrar_texto(cuadro_pregunta["superficie"],f"{pregunta_actual["descripcion"]}",(20,20),FUENTE_ARIAL_30)
    pantalla.blit(cuadro_pregunta["superficie"],cuadro_pregunta["rectangulo"])

    
    for i in range(len(lista_respuestas)):
        mostrar_texto(lista_respuestas[i]["superficie"],f"{pregunta_actual.get(f"respuesta_{i+1}")}",(10,10),FUENTE_ARIAL_20,COLOR_BLANCO)
        pantalla.blit(lista_respuestas[i]["superficie"],lista_respuestas[i]["rectangulo"])


def obtener_ranking() -> list:

    # RECORREMOS EL ARCHIVO PARTIDAS JSON
    with open("partidas.json", "r") as archivo:
        partidas = json.load(archivo)

    # ORDENA LA LISTA COMPLETA POR PUNTUACIÓN
    partidas_ordenadas = sorted(partidas, key=lambda p: p["puntuacion"], reverse=True)

    # RETORNAMOS 10 DE LAS PARTIDAS FILTRADAS POR PUNTUACIÓN
    return partidas_ordenadas[:10]
