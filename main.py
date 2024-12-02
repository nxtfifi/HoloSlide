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
