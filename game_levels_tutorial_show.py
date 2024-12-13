import settings
from game_levels import *
import pyglet
import cv2
import numpy as np

class Tutorial4(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='')
        # self.pipe_conn = pipe_conn
        # self.circle = pyglet.shapes.Circle(512, 384, 20, color=(255, 0, 0), batch=self.batch)
        # self.label.text += "\nControl the red circle with external inputs!"

        # Percorsi dei video
        self.new_sprite = [None] * 4
        self.video_paths = [
            "videos/1b.mp4",  # Percorso del primo video
            "videos/1c.mp4",  # Percorso del secondo video
            "videos/1d.mp4",  # Percorso del terzo video
            "videos/1e.mp4"  # Percorso del quarto video
        ]

        # Crea gli oggetti VideoCapture per ogni video
        self.caps = [cv2.VideoCapture(path) for path in self.video_paths]

        # Crea una lista per le texture di ogni video
        self.textures = [None] * len(self.caps)

        self.bg_group = Group(order=0)
        self.fg_group = Group(order=1)


        #placeholder




    #@window.event
    def update(self, dt):
        # Aggiorna le texture dei video
        # Funzione per aggiornare le texture da OpenCV
        for i, cap in enumerate(self.caps):
            ret, frame = cap.read()
            if not ret:
                # Se il video è finito, riavvialo dal primo frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()

            if ret:
                frame = cv2.resize(frame, (512, 384))

                # Ribalta verticalmente l'immagine
                frame = cv2.flip(frame, 0)

                # Converti l'immagine in RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Crea l'immagine di Pyglet
                image_data = pyglet.image.ImageData(
                    frame.shape[1], frame.shape[0], 'RGB', frame_rgb.tobytes()
                )



                # Ridimensiona usando pyglet
                resized_image = image_data.get_region(0, 0, frame.shape[1], frame.shape[0])
                resized_image = resized_image.get_texture()

                # Assegna la texture ridimensionata
                self.textures[i] = resized_image

                width = settings.width
                height = settings.height

                offset_ = width // 4 - resized_image.width // 2
                #print(offset_)

                # Posizioni aggiornate
                positions = [
                    # Video in basso a sinistra
                    (width // 4 - resized_image.width // 2 + offset_, height // 4 - resized_image.height // 3),

                    # Video in basso a destra??...
                    (3 * width // 4 - resized_image.width // 2 + offset_, height // 4 - resized_image.height // 3),

                    # Video in alto a sinistra
                    (width // 4 - resized_image.width // 2 + offset_, height // 2 + height // 24 ),

                    # Video in alto a destra
                    (3 * width // 4 - resized_image.width // 2 + offset_, height // 2 + height // 24)
                ]

                # Posiziona lo sprite
                self.new_sprite[i] = pyglet.sprite.Sprite(self.textures[i], x=positions[i][0], y=positions[i][1],
                                                          batch=self.batch, group=self.bg_group)



                # Posizione dell'etichetta a sinistra di ciascun video
                # label_x = positions[i][0] - 50  # Sposta l'etichetta a sinistra rispetto alla posizione del video
                # label_y = positions[i][1] + resized_image.height // 2  # Centra verticalmente l'etichetta rispetto al video

                self.label_1 = pyglet.text.Label('Passo 1:',
                                                 font_name='Arial', font_size=16,  x=positions[0][0] - 50, y=positions[0][1] + resized_image.height // 2,
                                                 anchor_x='center', anchor_y='center', batch=self.batch)
                self.label_2 = pyglet.text.Label('Passo 2:',
                                                 font_name='Arial', font_size=16,  x=positions[1][0] - 50, y=positions[1][1] + resized_image.height // 2,
                                                 anchor_x='center', anchor_y='center', batch=self.batch)
                self.label_3 = pyglet.text.Label('Passo 3:',
                                                 font_name='Arial', font_size=16,  x=positions[2][0] - 50, y=positions[2][1] + resized_image.height // 2,
                                                 anchor_x='center', anchor_y='center', batch=self.batch)
                self.label_4 = pyglet.text.Label('Passo 4:',
                                                 font_name='Arial', font_size=16,  x=positions[3][0] - 50, y=positions[3][1] + resized_image.height // 2,
                                                 anchor_x='center', anchor_y='center', batch=self.batch)

                # Crea l'etichetta
                # self.label = pyglet.text.Label("testo1", #labels[i],
                #                           font_name='Arial', font_size=14,
                #                           x=20, y=40, #x=label_x, y=label_y,
                #                           anchor_x='center', anchor_y='center', batch=self.batch)
                # print(label_x, label_y)


            else:
                print(f"Errore nel caricamento del video {i + 1}")

        # Verifica se ci sono texture da disegnare
        if not any(self.textures):
            print("Nessuna texture disponibile per il rendering.")
            return



        # Disegna il testo sopra i video
        self.label3 = pyglet.text.Label('Questo è un esempio di come deve essere usato l\'applicativo:',
                                  font_name='Arial', font_size=16, x=settings.width // 2, y=settings.height - 20,
                                  anchor_x='center', anchor_y='center', batch=self.batch)
        #label.draw()

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
        for i, texture in enumerate(self.textures):
            #print(i)
            if texture:
                #print(i)
                # Disegna il rettangolo colorato sotto il video
                x, y = positions[i]
                width, height = sizes[i]

                # Crea il rettangolo colorato
                self.rectangle = pyglet.shapes.Rectangle(x, y, width, height, color=colors[i])
                #rectangle.draw()

                # Disegna la texture del video sopra il rettangolo colorato
                #texture.blit(x, y, width=width, height=height)
                #texture[i].blit(x, y, width=100, height=100)

                # Disegna l'etichetta "Passo X" sotto il video
                # self.label = pyglet.text.Label(labels[i],
                #                           font_name='Arial', font_size=14, x=x + width // 2, y=y - 20,
                #                           anchor_x='center', anchor_y='center', batch=self.batch)
                # #self.label.draw()

        # Disegna il testo sotto i video
        self.label2 = pyglet.text.Label('Premi [spazio] per continuare, [T] per avviare il tutorial (e poi nuovamente [T] per uscirne)',
                                   font_name='Arial', font_size=14, x=settings.width // 2, y=40,
                                   anchor_x='center', anchor_y='center', batch=self.batch)
        #label2.draw()

        self.batch.draw()

    # Gestisci gli eventi da tastiera
    # @window.event
    # def on_key_press(symbol, modifiers):
    #     if symbol == pyglet.window.key.SPACE:
    #         print("Continuando...")
    #         # Aggiungi qui la logica per continuare
    #     elif symbol == pyglet.window.key.T:
    #         print("Avviando il tutorial...")
    #         # Aggiungi qui la logica per avviare il tutorial