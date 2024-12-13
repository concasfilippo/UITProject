import pyglet
import cv2
import numpy as np

# Crea una finestra
window = pyglet.window.Window()
window.set_fullscreen(True)

# Percorsi dei video
video_paths = [
    "videos/1b.mp4",  # Percorso del primo video
    "videos/1c.mp4",  # Percorso del secondo video
    "videos/1d.mp4",  # Percorso del terzo video
    "videos/1e.mp4"  # Percorso del quarto video
]

# Crea gli oggetti VideoCapture per ogni video
caps = [cv2.VideoCapture(path) for path in video_paths]

# Crea una lista per le texture di ogni video
textures = [None] * len(caps)


# Funzione per aggiornare le texture da OpenCV
def update_textures():
    global textures
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            # Se il video è finito, riavvialo dal primo frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        if ret:
            # Ribalta verticalmente l'immagine
            frame = cv2.flip(frame, 0)

            # Converti l'immagine in RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Crea la texture usando ImageData
            image_data = pyglet.image.ImageData(
                frame.shape[1], frame.shape[0], 'RGB', frame_rgb.tobytes()
            )

            # Assegna la texture
            textures[i] = image_data.get_texture()


@window.event
def on_draw():
    window.clear()

    # Disegna il testo sopra i video
    label = pyglet.text.Label('Questo è un esempio di come deve essere usato l\'applicativo:',
                              font_name='Arial', font_size=16, x=window.width // 2, y=window.height - 20,
                              anchor_x='center', anchor_y='center')
    label.draw()

    # Aggiorna le texture dei video
    update_textures()

    # Posizioni e dimensioni per ciascun video
    positions = [
        (0, 240),  # Video 1 (top-left)
        (320, 240),  # Video 2 (top-right)
        (0, 0),  # Video 3 (bottom-left)
        (320, 0)  # Video 4 (bottom-right)
    ]
    sizes = [
        (320, 240),  # Video 1 dimensione
        (320, 240),  # Video 2 dimensione
        (320, 240),  # Video 3 dimensione
        (320, 240)  # Video 4 dimensione
    ]
    labels = [
        "Passo 1",  # Etichetta per il primo video
        "Passo 2",  # Etichetta per il secondo video
        "Passo 3",  # Etichetta per il terzo video
        "Passo 4"  # Etichetta per il quarto video
    ]

    # Colori dei rettangoli
    colors = [
        (255, 0, 0),  # Rosso
        (0, 255, 0),  # Verde
        (0, 0, 255),  # Blu
        (255, 255, 0)  # Giallo
    ]

    # Disegna ogni video in un rettangolo colorato usando pyglet.shapes.Rectangle
    for i, texture in enumerate(textures):
        if texture:
            # Disegna il rettangolo colorato sotto il video
            x, y = positions[i]
            width, height = sizes[i]

            # Crea il rettangolo colorato
            rectangle = pyglet.shapes.Rectangle(x, y, width, height, color=colors[i])
            rectangle.draw()

            # Disegna la texture del video sopra il rettangolo colorato
            texture.blit(x, y, width=width, height=height)

            # Disegna l'etichetta "Passo X" sotto il video
            label = pyglet.text.Label(labels[i],
                                      font_name='Arial', font_size=14, x=x + width // 2, y=y - 20,
                                      anchor_x='center', anchor_y='center')
            label.draw()

    # Disegna il testo sotto i video
    label2 = pyglet.text.Label('Premi [spazio] per continuare, [T] per avviare il tutorial',
                               font_name='Arial', font_size=14, x=window.width // 2, y=40,
                               anchor_x='center', anchor_y='center')
    label2.draw()


# Gestisci gli eventi da tastiera
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        print("Continuando...")
        # Aggiungi qui la logica per continuare
    elif symbol == pyglet.window.key.T:
        print("Avviando il tutorial...")
        # Aggiungi qui la logica per avviare il tutorial


# Avvia il loop principale di Pyglet
pyglet.app.run()

# Rilascia le risorse quando il programma termina
for cap in caps:
    cap.release()
