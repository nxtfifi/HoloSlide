import cv2
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import time

# Obtener la resolución de la pantalla
pantalla_ancho, pantalla_alto = pyautogui.size()

# Ajustar resolución de la presentación al 80% del tamaño de la pantalla
ancho, alto = int(pantalla_ancho * 0.8), int(pantalla_alto * 0.9)

# Parámetros iniciales
umbral_gesto = 360  # Línea para detectar los gestos
zoom_factor = 1.0  # Factor de zoom inicial
retraso = 30  # Retraso para evitar cambios rápidos de diapositiva
ultimo_zoom = time.time()  # Para controlar el tiempo de zoom
zoom_activado = False

# Inicializar la cámara
camara = cv2.VideoCapture(0)
camara.set(3, ancho)  # Ancho del cuadro
camara.set(4, alto)  # Alto del cuadro
detector_manos = HandDetector(detectionCon=0.8, maxHands=2) # Detectar hasta 2 manos

# Variables para controlar la transición de diapositivas
boton_presionado = False
contador = 0
ultimo_cambio = time.time()  # Para evitar cambios rápidos de diapositivas
alto_pequena, ancho_pequena = int(120 * 1), int(213 * 1)  # Dimensiones de la vista previa

# Bucle principal
while True:
    # Captura de la cámara
    exito, imagen = camara.read()
    imagen = cv2.flip(imagen, 1)  # Voltear la imagen horizontalmente para reflejo natural

    # Detectar manos
    manos, imagen = detector_manos.findHands(imagen)  # Detecta y dibuja las manos
    cv2.line(imagen, (0, umbral_gesto), (ancho, umbral_gesto), (0, 255, 0), 10)  # Línea de umbral

    if manos:
        mano_izquierda = None
        mano_derecha = None

        # Dividir las manos si hay más de una
        if len(manos) == 2:
            mano_izquierda, mano_derecha = manos

        # Si solo hay una mano, usar esa mano
        if len(manos) == 1:
            mano_derecha = manos[0]

        # Obtener las coordenadas del índice de la mano derecha (o la única)
        if mano_derecha:
            lista_puntos = mano_derecha["lmList"]  # Lista de puntos clave
            dedos_arriba = detector_manos.fingersUp(mano_derecha)  # Dedos levantados
            x_valor = int(np.interp(lista_puntos[8][0], [0, ancho], [0, pantalla_ancho]))
            y_valor = int(np.interp(lista_puntos[8][1], [150, alto - 150], [0, pantalla_alto]))
            dedo_indice = x_valor, y_valor

            # Mover el cursor con el índice de la mano detectada
            pyautogui.moveTo(x_valor, y_valor)

            # Gesto 1: Ir a la diapositiva anterior (pulgar arriba)
            if dedos_arriba == [1, 0, 0, 0, 0]:
                if time.time() - ultimo_cambio > retraso / 10:  # Control de tiempo para evitar cambios rápidos
                    print("Ir a la diapositiva anterior")
                    pyautogui.press('left')  # Comando para retroceder la diapositiva
                    boton_presionado = True
                    ultimo_cambio = time.time()

            # Gesto 2: Ir a la siguiente diapositiva (meñique arriba)
            if dedos_arriba == [0, 0, 0, 0, 1]:
                if time.time() - ultimo_cambio > retraso / 10:  # Control de tiempo para evitar cambios rápidos
                    print("Ir a la siguiente diapositiva")
                    pyautogui.press('right')  # Comando para avanzar la diapositiva
                    boton_presionado = True
                    ultimo_cambio = time.time()

            # Gesto 3: Mostrar puntero (solo índice arriba)
            if dedos_arriba == [0, 1, 0, 0, 0]:
                cv2.circle(imagen, dedo_indice, 12, (0, 0, 255), cv2.FILLED)

            # Gesto 4: Dibujar en la diapositiva (índice y medio arriba)
            #if dedos_arriba == [0, 1, 1, 0, 0]:
                # Dibujar en PowerPoint (simulación)
             #   pyautogui.click(button='left')  # Simula un clic para dibujar
              #  cv2.circle(imagen, dedo_indice, 12, (0, 255, 0), cv2.FILLED)

            # Gesto 5: Deshacer anotaciones (todos los dedos arriba menos el pulgar)
            if dedos_arriba == [0, 1, 1, 1, 1]:
                # Eliminar anotaciones o deshacer acciones
                pass

            # Gesto 6: Zoom (Pulgar e índice juntos para acercar)
        if mano_derecha:
            if dedos_arriba == [1, 0, 0, 0, 1]:
                distancia = np.linalg.norm(np.array(lista_puntos[8]) - np.array(lista_puntos[4]))  # Distancia entre pulgar e índice
                zoom_factor = np.clip(1.0 + (distancia / 100), 0.5, 2.0)

                if time.time() - ultimo_zoom > 0.5:  # Control para aplicar el zoom con un pequeño retraso
                    if zoom_factor > 1.2 and not zoom_activado:
                        pyautogui.hotkey('ctrl', '+')  # Comando de zoom in
                        zoom_activado = True
                    elif zoom_factor < 0.8 and zoom_activado:
                        pyautogui.hotkey('ctrl', '-')  # Comando de zoom out
                        zoom_activado = False
                    ultimo_zoom = time.time()

        # Gesto 7: Zoom Out con el índice de ambas manos levantados al mismo tiempo
        if mano_izquierda and mano_derecha:
            lista_puntos_izq = mano_izquierda["lmList"]
            dedos_arriba_izq = detector_manos.fingersUp(mano_izquierda)
            if dedos_arriba_izq == [0, 1, 0, 0, 0] and dedos_arriba == [0, 1, 0, 0, 0]:
                # Si ambos índices están levantados, hacer zoom out
                if time.time() - ultimo_zoom > 0.5:  # Para evitar aplicar el zoom repetidamente
                    pyautogui.hotkey('ctrl', '-')  # Comando de zoom out
                    zoom_activado = False
                    ultimo_zoom = time.time()
                    
    # Mostrar vista previa de la cámara
    imagen_pequena = cv2.resize(imagen, (ancho_pequena, alto_pequena))
    h, w, _ = imagen.shape
    imagen[0:alto_pequena, w - ancho_pequena: w] = imagen_pequena

    # Mostrar la cámara en la ventana
    cv2.imshow("Cámara", imagen)

    # Salir si se presiona 'q'
    tecla = cv2.waitKey(1)
    if tecla == ord('q'):
        break

# Liberar recursos
camara.release()
cv2.destroyAllWindows()



