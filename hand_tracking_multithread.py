import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque
import threading
import cv2 as cv
import numpy as np
import mediapipe as mp
from cvfpscalc import CvFpsCalc
from model import KeyPointClassifier
from model import PointHistoryClassifier
import settings

# Coordinate history
history_length = 16
point_history = deque(maxlen=history_length)

# Finger gesture history
finger_gesture_history = deque(maxlen=history_length)

keypoint_classifier_labels = None
point_history_classifier_labels = None


def main_hand_tracking(pipe_conn=None):
    # Argument parsing
    args = get_args()
    cap_device = args.device
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    # Camera setup
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

    # Model load
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                           min_detection_confidence=min_detection_confidence,
                           min_tracking_confidence=min_tracking_confidence)

    keypoint_classifier = KeyPointClassifier()
    point_history_classifier = PointHistoryClassifier()

    # Read labels
    with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

    with open('model/point_history_classifier/point_history_classifier_label.csv', encoding='utf-8-sig') as f:
        point_history_classifier_labels = csv.reader(f)
        point_history_classifier_labels = [row[0] for row in point_history_classifier_labels]

    # FPS Measurement
    cvFpsCalc = CvFpsCalc(buffer_len=10)





    mode = 0
    while True:
        fps = cvFpsCalc.get()

        # Process Key (ESC: end)
        key = cv.waitKey(10)
        if key == 27:  # ESC
            break
        number, mode = select_mode(key, mode)

        # Camera capture
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv.flip(frame, 1)  # Mirror display

        # Process hand tracking in a separate thread
        processing_thread = threading.Thread(target=process_hand_tracking, args=(
        frame, hands, keypoint_classifier, point_history_classifier, pipe_conn))
        processing_thread.start()
        processing_thread.join()

        # Display the results
        debug_image = process_hand_tracking(frame, hands, keypoint_classifier, point_history_classifier)
        debug_image = draw_point_history(debug_image, point_history)
        debug_image = draw_info(debug_image, fps, mode, number)

        cv.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()


from hand_tracking_utils import *


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=int, default=settings.default_camera)
    parser.add_argument("--width", help='cap width', type=int, default=100)
    parser.add_argument("--height", help='cap height', type=int, default=100)
    parser.add_argument("--min_detection_confidence", help='min_detection_confidence', type=float, default=0.7)
    parser.add_argument("--min_tracking_confidence", help='min_tracking_confidence', type=int, default=0.5)
    args = parser.parse_args()
    return args



def process_hand_tracking(frame, hands, keypoint_classifier, point_history_classifier, pipe_conn=None):
    # Process the frame for hand tracking and gesture recognition
    debug_image = copy.deepcopy(frame)
    debug_image = cv.cvtColor(debug_image, cv.COLOR_BGR2RGB)
    debug_image.flags.writeable = False
    results = hands.process(debug_image)
    debug_image.flags.writeable = True

    if results.multi_hand_landmarks is not None:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Calculate bounding rectangle and landmarks
            brect = calc_bounding_rect(debug_image, hand_landmarks)
            landmark_list = calc_landmark_list(debug_image, hand_landmarks)
            pre_processed_landmark_list = pre_process_landmark(landmark_list)
            pre_processed_point_history_list = pre_process_point_history(debug_image, point_history)

            # Hand sign classification
            hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

            if pipe_conn is not None:
                pipe_conn.send([landmark_list, debug_image, hand_sign_id])

            # Process gesture classification and update history
            point_history.append(landmark_list[8] if hand_sign_id == 2 else [0, 0])
            finger_gesture_id = 0
            if len(pre_processed_point_history_list) == (history_length * 2):
                finger_gesture_id = point_history_classifier(pre_processed_point_history_list)
            finger_gesture_history.append(finger_gesture_id)
            most_common_fg_id = Counter(finger_gesture_history).most_common()

            # Drawing landmarks and information
            debug_image = draw_bounding_rect(True, debug_image, brect)
            debug_image = draw_landmarks(debug_image, landmark_list)
            debug_image = draw_info_text(debug_image, brect, handedness,
                                         keypoint_classifier_labels[hand_sign_id],
                                         point_history_classifier_labels[most_common_fg_id[0][0]])
    return debug_image
# Other utility functions like calc_bounding_rect, calc_landmark_list, pre_process_landmark, etc. remain the same as in your original code.
