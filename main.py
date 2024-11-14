import cv2
import mediapipe as mp
import pyautogui
import time

# Inicializa MediaPipe para detección de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Funciones de control de diapositivas
def advance_slide():
    pyautogui.press('right')

def previous_slide():
    pyautogui.press('left')

# Configuración para captura de video
cap = cv2.VideoCapture(0)
time.sleep(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear la imagen para hacerla más intuitiva (si es necesario)
    frame = cv2.flip(frame, 1)

    # Procesamiento con MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Dibujar las manos y realizar acciones
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Dibujar las marcas de la mano
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtener las coordenadas de los puntos de la mano
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Usar el índice de los dedos para detectar gestos
            if index_finger.y < wrist.y and thumb.y < wrist.y:
                # Avanzar diapositiva si el dedo índice y pulgar están arriba de la muñeca
                print("Avanzando diapositiva...")
                advance_slide()
                time.sleep(1)  # Evitar múltiples acciones por gesto

            elif index_finger.y > wrist.y and thumb.y > wrist.y:
                # Retroceder diapositiva si el dedo índice y pulgar están debajo de la muñeca
                print("Retrocediendo diapositiva...")
                previous_slide()
                time.sleep(1)  # Evitar múltiples acciones por gesto

    # Mostrar el frame
    cv2.imshow("Gestos para controlar diapositivas", frame)

    # Salir del bucle con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
