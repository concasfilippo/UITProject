default_camera = 0

visible_mediapipe_camera = False #booleano per far vedere la finestra di mediapipe
is_fullscreen = True #booleano per indicare se debba andare in fullscreen

import tkinter as tk
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

width = screen_width #640
height = screen_height #480


### IMPOSTAZIONI DI DEBUG DEGLI ESERCIZI
is_debugging_mode = False

is_end_level_audio_enabled = False