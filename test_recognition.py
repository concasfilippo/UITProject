import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import pad_sequences
import math
import mediapipe as mp
import json
import pandas as pd
from google.protobuf.json_format import MessageToJson
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#Salvare i gesti del classificatore; quesi sono queli che si trovano attualmente nella cartella
import os
lista_gesti = []
for path, subdirs, files in os.walk('trainingv3'):
    for name in subdirs:
        lista_gesti.append(name)



def distance_between(p1_loc, p2_loc, results):
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
        distance_between(4,8, results),
        distance_between(4,12, results),
        distance_between(4,16, results),
        distance_between(4,20, results),
        #wrist to finger tip
        distance_between(4,0, results),
        distance_between(8,0, results),
        distance_between(12,0, results),
        distance_between(16,0, results),
        distance_between(20,0, results),
        #tip to tip (specific to this application)
        distance_between(8,12, results),
        distance_between(12,16, results),
        #within finger joint (detect bending)
        distance_between(1,4, results),
        distance_between(8,5, results),
        distance_between(12,9, results),
        distance_between(16,13, results),
        distance_between(20,17, results),
        #distance from each tip to thumb joint
        distance_between(2,8, results),
        distance_between(2,12, results),
        distance_between(2,16, results),
        distance_between(2,20, results) ])
    #use np normalize, as min_max may create confusion that the closest fingers has 0 distance
    emb_norm = emb / np.linalg.norm(emb)
    return emb_norm

def skip_frame(landmark_npy_all, frame=20):
    new_lmk_array = []
    #print(f'Lunghezza: {len(landmark_npy_all[0])}')
    #print(f'Prima del taglio: {landmark_npy_all[0]}')
    if len(landmark_npy_all[0]) > frame:
        landmark_npy_all = [landmark_npy_all[0][-frame:] ]   #sicuro che sto prendendo gli ultimi frame
    #print(f'Dopo il taglio: {landmark_npy_all[0]}')
    for each in landmark_npy_all:
        if len(each) <= frame:

            # Se la lunghezza è minore o uguale al numero di frame, non serve saltare
            new_lmk_array.append(each)
        else:
            # Salta frame prendendo ogni N-esimo elemento (arrotondato per eccesso)
            to_round = math.ceil(len(each) / frame)
            new_lmk_array.append(each[::to_round])
    return new_lmk_array



#buffer_gestures = [[None] * 10]


def predict_from_video(video_path, model_path, max_len=10):
    # Carica il modello salvato
    model = load_model(model_path)



    # Inizializza il rilevatore di mani di MediaPipe
    handnn = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.6)

    # Apre il video in tempo reale
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    #max_len = fps*max_len #max len aggioranto come 2 * numero di fps


    landmark_npy_single = []  # Array per salvare i landmarks

    while cap.isOpened():
        success, image = cap.read()  # Legge un frame dal video
        if not success:
            break  # Esce dal ciclo se non ci sono più frame

        # Pre-elaborazione dell'immagine
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False  # Blocca la scrittura sull'immagine per efficienza

        # Esegue il rilevamento delle mani
        results = handnn.process(image)

        image.flags.writeable = True  # Rende di nuovo scrivibile l'immagine
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Riconversione da RGB a BGR

        # Se rileva una mano nei risultati, salva i landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmark_npy_single.append(landmark_to_dist_emb(results))  # Converte landmarks in array
                #print(landmark_npy_single)

                # Esegui la predizione solo se hai sufficienti landmark
                if len(landmark_npy_single) >= 1:
                    # Applica il padding alla sequenza per garantire una lunghezza uniforme
                    #print(landmark_npy_single)

                    new_lmk_array = skip_frame([landmark_npy_single], frame=int(max_len))  # Salta i frame se necessario
                    #print(new_lmk_array)
                    train_x_new = pad_sequences(new_lmk_array, padding='post', maxlen=int(max_len), dtype='float32')
                    #print(train_x_new)

                    # train_x_new = landmark_npy_single[-10:]
                    # train_x_new = np.array(train_x_new)
                    # print(train_x_new)


                    # print(new_lmk_array)
                    # print(train_x_new)
                    # print(len(train_x_new[0]))
                    # Esegui la predizione
                    y_pred = model.predict(train_x_new, verbose=0)

                    # Ottieni la classe con argmax (classe predetta)
                    print(y_pred)
                    predicted_class = np.argmax(y_pred, axis=1)

                    # Stampa o visualizza il risultato
                    print(f"Predicted class: {predicted_class} - {lista_gesti[predicted_class[0]]}")

        # Mostra l'immagine con i risultati se necessario (opzionale)
        cv2.imshow("Video", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Esci se premi 'q'
            break

    # Rilascia il video
    cap.release()
    cv2.destroyAllWindows()  # Chiude tutte le finestre OpenCV


# Esempio di utilizzo
video_path = 0 #'path/to/your/realtime_video.mp4'  # Sostituisci con il tuo percorso video
model_path = 'modelloV1.keras'  # Percorso del modello salvato
#secondi = 2 #numero di secondi che vogliamo esporre
predict_from_video(video_path, model_path)
