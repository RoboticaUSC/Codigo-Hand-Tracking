import cv2
import numpy as np
import mediapipe as mp
from math import acos, degrees

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#Pulgar
points_pulgar = [1, 2, 4]
pulgar_Retraido = False
#Indice, medio, anular y meñique
points_palma = [0, 1, 2, 5, 9, 13, 17]
points_punta_dedos = [8, 12, 16, 20]
points_base_dedos = [6, 10, 14, 18]

def Centro_Palma(List_coordenadas):
    coordenadas = np.array(List_coordenadas)
    centro = np.mean(coordenadas, axis = 0)
    centro = int(centro[0]), int(centro[1])
    return centro

with mp_hands.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.5) as hands:
    while True:
        ret, frame = cap.read()
        frameFlip = cv2.flip(frame,1)
        frameRGB = cv2.cvtColor(frameFlip, cv2.COLOR_BGR2RGB)

        results = hands.process(frameRGB)

        al, an, _ = frame.shape

        if results.multi_hand_landmarks is not None:
            #print(results.multi_handedness[0].classification[0].label)
            coordenadas_pulgar = []
            coordenadas_palma = []
            coordenadas_DP = []     #Punta de los Dedos
            coordenadas_DB = []     #Base de los Dedos
            for hand_landmarks in results.multi_hand_landmarks:
                if results.multi_handedness[0].classification[0].label == "Right":
                    #Coodernadas del pulgar
                    for index in points_pulgar:
                        x = int(hand_landmarks.landmark[index].x * an)
                        y = int(hand_landmarks.landmark[index].y * al)
                        coordenadas_pulgar.append([x, y])
                    
                    #Coordenadas de la palma
                    for index in points_palma:
                        x = int(hand_landmarks.landmark[index].x * an)
                        y = int(hand_landmarks.landmark[index].y * al)
                        coordenadas_palma.append([x, y])

                    #Coordenadas de la punta de los dedos
                    for index in points_punta_dedos:
                        x = int(hand_landmarks.landmark[index].x * an)
                        y = int(hand_landmarks.landmark[index].y * al)
                        coordenadas_DP.append([x, y])
                    
                    #Coordenadas de la base de los dedos
                    for index in points_base_dedos:
                        x = int(hand_landmarks.landmark[index].x * an)
                        y = int(hand_landmarks.landmark[index].y * al)
                        coordenadas_DB.append([x, y])
                    
                    #************************Calculos del pulgar************************
                    p1 = np.array(coordenadas_pulgar[0])
                    p2 = np.array(coordenadas_pulgar[1])
                    p3 = np.array(coordenadas_pulgar[2])

                    l1 = np.linalg.norm(p2 - p3)
                    l2 = np.linalg.norm(p1 - p3)
                    l3 = np.linalg.norm(p1 - p2)

                    #Calculo del angulo de apertura del pulgar
                    try:
                        angulo_P = degrees(acos((l1**2 + l3**2 - l2**2)/(2*l1*l3)))
                    except:
                        angulo_P = 150
                    print(angulo_P)
                    if angulo_P <= 140:
                        pulgar_Retraido = True
                    else:
                        pulgar_Retraido = False
                    #print("Pulgar retraido: ", pulgar_Retraido, "Angulo: ", angulo_P)

                    #************************Calculos del Indice, medio, anular y meñique************************
                    #Calculo del centro de la palma
                    px, py = Centro_Palma(coordenadas_palma)
                    cv2.circle(frameFlip, (px, py), 3, (0, 255, 0), -1)
                    coordenadas_centro = np.array([px, py])
                    coordenadas_DP = np.array(coordenadas_DP)
                    coordenadas_DB = np.array(coordenadas_DB)

                    #calculo de las distancias
                    Dist_cent_DP = np.linalg.norm(coordenadas_centro - coordenadas_DP, axis = 1)
                    #print("Distancia del cento con la punta de los dedos: ", Dist_cent_DP)
                    Dist_cent_DB = np.linalg.norm(coordenadas_centro - coordenadas_DB, axis = 1)
                    diff_Dist = Dist_cent_DP - Dist_cent_DB


                    mp_drawing.draw_landmarks(frameFlip, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Frame", frameFlip)
        
        if cv2.waitKey(1) == 27:
            break

cap.release()
cv2.destroyAllWindows()
