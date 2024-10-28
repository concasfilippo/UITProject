import os
import cv2
import mediapipe as mp
import cv2
import mediapipe as mp

from google.protobuf.json_format import MessageToJson
import json

import pandas as pd
import numpy as np
import re
#from test_dynamic import landmark_to_dist_emb

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def distance_between(p1_loc, p2_loc):
    jsonObj = MessageToJson(results.multi_hand_landmarks[0])
    lmk = json.loads(jsonObj)['landmark']
    p1 = pd.DataFrame(lmk).to_numpy()[p1_loc]
    p2 = pd.DataFrame(lmk).to_numpy()[p2_loc]
    squared_dist = np.sum((p1-p2)**2, axis=0)
    return np.sqrt(squared_dist)

def landmark_to_dist_emb(results):
    jsonObj = MessageToJson(results.multi_hand_landmarks[0])
    lmk = json.loads(jsonObj)['landmark']
    emb = np.array([
        #thumb to finger tip
        distance_between(4,8),
        distance_between(4,12),
        distance_between(4,16),
        distance_between(4,20),
        #wrist to finger tip
        distance_between(4,0),
        distance_between(8,0),
        distance_between(12,0),
        distance_between(16,0),
        distance_between(20,0),
        #tip to tip (specific to this application)
        distance_between(8,12),
        distance_between(12,16),
        #within finger joint (detect bending)
        distance_between(1,4),
        distance_between(8,5),
        distance_between(12,9),
        distance_between(16,13),
        distance_between(20,17),
        #distance from each tip to thumb joint
        distance_between(2,8),
        distance_between(2,12),
        distance_between(2,16),
        distance_between(2,20) ])
    #use np normalize, as min_max may create confusion that the closest fingers has 0 distance
    emb_norm = emb / np.linalg.norm(emb)
    return emb_norm


# Lista di file video nella cartella specificata
path_training_videos = 'training/'
arr = os.listdir(path_training_videos)
video_class_all = []
landmark_npy_all = []

# Inizializza il rilevatore di mani di MediaPipe
handnn = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.6)

# Itera su ogni video nella cartella
for idx, eachVideo in enumerate(arr):
    landmark_npy_single = []  # Array per salvare i landmarks del singolo video
    video = path_training_videos + eachVideo  # Percorso completo del video
    print(f"Analisi del video: {video}")
    # Apre il video usando OpenCV
    cap = cv2.VideoCapture(video)

    # Estrae la classe del video (assumendo che la classe sia nel nome del file, separata da '_')

    video_class_all.append(int(re.search(r'_(\d+)', video).group(1)))

    # Leggi i frame del video finché è aperto
    while cap.isOpened():
        success, image = cap.read()  # Legge un frame dal video
        if not success:
            break  # Esce dal ciclo se non ci sono più frame

        # Pre-elaborazione dell'immagine: flip e conversione da BGR a RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False  # Blocca la scrittura sull'immagine per efficienza

        # Esegue il rilevamento delle mani
        results = handnn.process(image)

        # Rende di nuovo l'immagine scrivibile
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Riconversione da RGB a BGR

        # Se rileva una mano nei risultati, salva i landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmark_npy_single.append(
                    landmark_to_dist_emb(results))  # Funzione ipotetica per convertire landmarks in array

    # Salva i landmarks di tutti i frame di questo video
    landmark_npy_all.append(landmark_npy_single)


    # Rilascia il video
    cap.release()

# Stampa il messaggio finale
print(f"Finished for total {len(arr)} videos. Completed.")
print(landmark_npy_all)
