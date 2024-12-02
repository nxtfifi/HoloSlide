#librerias
from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import pyautogui
def aplicar_zoom(imagen, nivel_zoom):
    # Redimensionar la imagen según el nivel de zoom
    altura, ancho = imagen.shape[:2]
    nueva_altura = int(altura * nivel_zoom)
    nuevo_ancho = int(ancho * nivel_zoom)
    
    # Centrar el zoom (opcional, para evitar desplazamientos)
    imagen_zoom = cv2.resize(imagen, (nuevo_ancho, nueva_altura), interpolation=cv2.INTER_LINEAR)
    
    # Muestra la imagen en la ventana o actualiza su contenido
    cv2.imshow("Imagen con Zoom", imagen_zoom)

# Obtener la resolución de la pantalla
pantalla_ancho, pantalla_alto = pyautogui.size()

# Ajustar resolución de la presentación al 80% del tamaño de la pantalla
ancho, alto = int(pantalla_ancho * 0.), int(pantalla_alto * 0.9)

#Parmetros iniciales
ancho, alto=1280,720 #Resolución de la pantalla
umbral_gesto=360 #Linea para detectar los gestos
carpeta_presentacion="presentation" #Es la carpeta donde estaran los png


camara=cv2.VideoCapture(0)
camara.set(3,ancho) #Ancho del cuadro
camara.set(4,alto) #Alto del cuadro
detector_manos=HandDetector(detectionCon=0.8,maxHands=1)

#-----
nivel_zoom = 1  # Nivel de zoom inicial
max_zoom = 3  # Zoom máximo (3x)
min_zoom = 0.5  # Zoom mínimo (0.5x)
#-----

lista_imagenes=[]
retraso=30
boton_presionado=False
contador=0
modo_dibujo=False
numero_imagen=0
contador_retraso=0
anotaciones=[[]] #Lista para guardas anotaciones
numero_anotacion=-1 #Indice de anotacion actual
inicio_anotacion=False
alto_pequena, ancho_pequena=int(120*1),int(213*1) #Dimensiones de la vista previa

#lista imagenes
rutas_imagenes=sorted(os.listdir(carpeta_presentacion),key=len)
print(rutas_imagenes)

while True:
    # Capturar cuadro de la cámara
    exito, imagen = camara.read()
    imagen = cv2.flip(imagen, 1)  # Voltear la imagen horizontalmente para reflejo natural
    ruta_imagen_actual = os.path.join(carpeta_presentacion, rutas_imagenes[numero_imagen])
    imagen_actual = cv2.imread(ruta_imagen_actual)
    
    # Detectar manos
    manos, imagen = detector_manos.findHands(imagen)  # Detecta y dibuja las manos
    cv2.line(imagen, (0, umbral_gesto), (ancho, umbral_gesto), (0, 255, 0), 10)  # Línea de umbral

    if manos and not boton_presionado:  # Si se detecta una mano y no hay botón activo
        mano = manos[0]  # Usar la primera mano detectada
        cx, cy = mano["center"]  # Centro de la mano
        lista_puntos = mano["lmList"]  # Lista de puntos clave
        dedos_arriba = detector_manos.fingersUp(mano)  # Dedos levantados

        # Coordenadas del índice para anotaciones
        x_valor = int(np.interp(lista_puntos[8][0], [ancho // 2, ancho], [0, ancho]))
        y_valor = int(np.interp(lista_puntos[8][1], [150, alto - 150], [0, alto]))
        dedo_indice = x_valor, y_valor
        
        if cy <= umbral_gesto:  # Si la mano está a la altura de la cara
            # Gesto 1 - Ir a la diapositiva anterior (pulgar arriba)
            if dedos_arriba == [1, 0, 0, 0, 0]:
                print("Ir a la diapositiva anterior")
                boton_presionado = True
                if numero_imagen > 0:
                    numero_imagen -= 1
                    anotaciones = [[]]
                    numero_anotacion = -1
                    inicio_anotacion = False

            # Gesto 2 - Ir a la siguiente diapositiva (meñique arriba)
            if dedos_arriba == [0, 0, 0, 0, 1]:
                print("Ir a la siguiente diapositiva")
                boton_presionado = True
                if numero_imagen < len(rutas_imagenes) - 1:
                    numero_imagen += 1
                    anotaciones = [[]]
                    numero_anotacion = -1
                    inicio_anotacion = False

        # Gesto 3 - Mostrar puntero (índice y medio arriba)
        if dedos_arriba == [0, 1, 1, 0, 0]:
            cv2.circle(imagen_actual, dedo_indice, 12, (0, 0, 255), cv2.FILLED)

        # Gesto 4 - Dibujar en la diapositiva (solo índice arriba)
        if dedos_arriba == [0, 1, 0, 0, 0]:
            if not inicio_anotacion:
                inicio_anotacion = True
                numero_anotacion += 1
                anotaciones.append([])
            anotaciones[numero_anotacion].append(dedo_indice)
            cv2.circle(imagen_actual, dedo_indice, 12, (0, 0, 255), cv2.FILLED)

        # Gesto 5 - Borrar anotaciones (todos los dedos arriba menos el pulgar)
        if dedos_arriba == [0, 1, 1, 1, 1]:
            if anotaciones:
                anotaciones.pop(-1)
                numero_anotacion -= 1
                boton_presionado = True

    if boton_presionado:  # Control del retraso
        contador += 1
        if contador > retraso:
            contador = 0
            boton_presionado = False

    # Dibujar anotaciones en la diapositiva actual
    for i, anotacion in enumerate(anotaciones):
        for j in range(len(anotacion)):
            if j != 0:
                cv2.line(imagen_actual, anotacion[j - 1], anotacion[j], (0, 0, 200), 12)
    # Mostrar vista previa de la cámara
    imagen_pequena = cv2.resize(imagen, (ancho_pequena, alto_pequena))
    h, w, _ = imagen_actual.shape
    imagen_actual[0:alto_pequena, w - ancho_pequena: w] = imagen_pequena
    
    # Configurar la ventana en modo pantalla completa
    cv2.namedWindow("Presentación", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Presentación", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)



    # Mostrar ventanas
    cv2.imshow("Presentación", imagen_actual)
    cv2.imshow("Cámara", imagen)

    # Salir si se presiona 'q'
    tecla = cv2.waitKey(1)
    if tecla == ord('q'):
        break

# Liberar recursos
camara.release()
cv2.destroyAllWindows()


