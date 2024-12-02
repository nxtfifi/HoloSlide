#librerias
from cvzone .HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

#Parmetros iniciales
ancho, alto=1280,720 #Resolución de la pantalla
umbral_gesto=360 #Linea para detectar los gestos
carpeta_presentacion="presentation" #Es la carpeta donde estaran los png

