import cv2
import mediapipe as mp
import pyautogui
import time
import threading
def pausa():
    print("Se iniicio el time")
    time.sleep(10)
    print("se finalizo el time")
# Inicializar MediaPipe para la detección de manos
mp_manos = mp.solutions.hands
mp_dibujo = mp.solutions.drawing_utils

# Variables de control
avanzar_gesto = False
retroceder_gesto = False
diapositiva_avanzada=False # Nueva Variable de control

# Configurar captura de video (0 es generalmen  te la cámara web predeterminada)
captura_video = cv2.VideoCapture(0)
with mp_manos.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as manos:
    while captura_video.isOpened():
        # Leer cada cuadro del video
        revisado, cuadro = captura_video.read()
        if not revisado:
            break
        
        # Convertir la imagen a RGB para MediaPipe
        cuadro_rgb = cv2.cvtColor(cuadro, cv2.COLOR_BGR2RGB)
        resultados = manos.process(cuadro_rgb)
        
        # Revisar si hay manos detectadas en el cuadro
        if resultados.multi_hand_landmarks:
            for mano_landmarks in resultados.multi_hand_landmarks:
                # Dibujar las conexiones de la mano en la imagen
                mp_dibujo.draw_landmarks(cuadro, mano_landmarks, mp_manos.HAND_CONNECTIONS)
                
                # Obtener las coordenadas del pulgar y el índice
                pulgar = mano_landmarks.landmark[mp_manos.HandLandmark.THUMB_TIP]
                indice = mano_landmarks.landmark[mp_manos.HandLandmark.INDEX_FINGER_TIP]
                muñeca = mano_landmarks.landmark[mp_manos.HandLandmark.WRIST]
                
                # Calcular si la mano está abierta (distancia entre muñeca y índice es mayor que una distancia umbral)
                distancia_mano_abierta = abs(indice.y - muñeca.y) > 0.1
                pulgar_arriba = pulgar.y < indice.y  # Pulgar levantado por encima del índice
                
                # Control de gestos para avanzar o retroceder
                if distancia_mano_abierta and not avanzar_gesto and not diapositiva_avanzada:
                    hilo= threading.Thread(target=pausa)
                    print("Avanzar diapositiva")
                    pyautogui.press("right")
                    avanzar_gesto = True
                    hilo.start()
                    retroceder_gesto = False
                    diapositiva_avanzada=True
                elif pulgar_arriba and not retroceder_gesto:
                    hilo2=threading.Thread(target=pausa)
                    print("Retroceder diapositiva")
                    pyautogui.press("left")
                    retroceder_gesto = True
                    hilo2.start()
                    avanzar_gesto = False
                    diapositiva_avanzada=False
                elif not distancia_mano_abierta and not pulgar_arriba:
                    avanzar_gesto = False
                    diapositiva_avanzada=False
                    retroceder_gesto = False
        
        # Mostrar el cuadro con los dibujos de los gestos
        cv2.imshow("Control de Diapositivas con Gestos de Mano", cuadro)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Liberar recursosx
captura_video.release()
cv2.destroyAllWindows()