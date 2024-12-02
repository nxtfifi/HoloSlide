#librerias
from cvzone .HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

#Parmetros iniciales
ancho, alto=1280,720 #Resolución de la pantalla
umbral_gesto=360 #Linea para detectar los gestos
carpeta_presentacion="presentation" #Es la carpeta donde estaran los png

camara=cv2.VideoCapture(0)
camara.set(3,ancho) #Ancho del cuadro
camara.set(4,alto) #Alto del cuadro
detector_manos=HandDetector(detectionCon=0.8,maxHands=1)

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