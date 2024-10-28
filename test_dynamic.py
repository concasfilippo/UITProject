import cv2
import mediapipe as mp

from google.protobuf.json_format import MessageToJson
import json

import pandas as pd
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For training:






# For feature extractor:
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

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks( image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            jsonObj = MessageToJson(results.multi_hand_landmarks[0])
            lmk = json.loads(jsonObj)['landmark']
            print(lmk)  # lmk = hand's landmark

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()