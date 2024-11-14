#Mapeo de manos
import cv2
import mediapipe as mp

# Inicialización de MediaPipe para manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Configuración de captura de video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear la imagen para que sea más intuitiva (reflejo horizontal)
    frame = cv2.flip(frame, 1)

    # Convertir la imagen de BGR a RGB para procesarla con MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe Hands
    result = hands.process(rgb_frame)

    # Si se detectan manos
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Dibujar los landmarks de la mano
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Imprimir las coordenadas de los puntos clave
            for id, landmark in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)  # Convertir las coordenadas normalizadas a píxeles

                # Dibujar los puntos clave
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

                # Mostrar el ID del punto y las coordenadas
                #cv2.putText(frame, f'{id}: ({cx}, {cy})', (cx, cy + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Mostrar el resultado en pantalla
    cv2.imshow('Hand Detection and Mapping', frame)

    # Romper el bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
