#librerias
from cvzone .HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

#Parmetros iniciales
ancho, alto=1280,720 #Resolución de la pantalla
umbral_gesto=360 #Linea para detectar los gestos
carpeta_presentacion="presentation" #Es la carpeta donde estaran los png
zoom_factor = 1.0  # Factor de zoom inicial

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

         # Calcular distancia entre el pulgar (punto 4) y el índice (punto 8)
        if len(lista_puntos) > 8:  # Si se han detectado al menos 9 puntos (pulgar e índice)
            dist = np.linalg.norm(np.array(lista_puntos[4]) - np.array(lista_puntos[8]))  # Distancia Euclidiana entre el pulgar y el índice

            # Control de zoom (aumentar o reducir según la distancia)
            if dist < 50:  # Si la distancia es pequeña, estamos acercando los dedos (zoom out)
                zoom_factor -= 0.01  # Reducir el zoom
            elif dist > 100:  # Si la distancia es grande, estamos separando los dedos (zoom in)
                zoom_factor += 0.01  # Aumentar el zoom

            # Limitar el zoom dentro de un rango razonable
            zoom_factor = np.clip(zoom_factor, 0.5, 2.0)
            
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

    #Aplicar el zoom a la imagen
    imagen_actual_zoom = cv2.resize(imagen_actual, None, fx=zoom_factor, fy=zoom_factor)

    # Dibujar anotaciones en la diapositiva actual
    for i, anotacion in enumerate(anotaciones):
        for j in range(len(anotacion)):
            if j != 0:
                cv2.line(imagen_actual, anotacion[j - 1], anotacion[j], (0, 0, 200), 12)
    # Mostrar vista previa de la cámara
    imagen_pequena = cv2.resize(imagen, (ancho_pequena, alto_pequena))
    h, w, _ = imagen_actual.shape
    imagen_actual[0:alto_pequena, w - ancho_pequena: w] = imagen_pequena

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


