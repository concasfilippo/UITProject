This repository is based on https://github.com/kinivi/hand-gesture-recognition-mediapipe

To get started, install all the requirements with
pip install -r requirements.txt

The project is structured as follows:
- main.py: the file to run to play with the camera
- game.py : file containing the logical implementation of the game rules, objects to interact with etc.
- hand_tracking.py : file contaning everything needeed to run the camera and track hand gestures
- settings.py : file with some parameters for the camera

For training use:
- keypoint_classification_EN.ipynb : for static gesture recognition
- training.ipynb : for video recognition (experimental)
- training.py : same (experimental)

Other files:
- cvfpscalc.py : to count fps during recognition
- hand-landmarks.png : reference to use landmarks
- modelloV1.keras : name of the model for gesture recognition form video
