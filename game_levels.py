import random

import pyglet
from pyglet.shapes import Circle
from pyglet.shapes import Circle, Rectangle
from pyglet.text import Label
from pyglet.window import key
import numpy as np
from settings import *
import time
import math
import numpy as np
from pyglet.graphics import Group
from game_utils import *

import csv
from shapely.geometry import Polygon

from game_utils_polygon_triangulation import  *
from esp_show_lines import *
from esp_show_lines import *

from decimal import Decimal
from playsound import playsound

class SceneTemplate:
    """A template with common features for all scenes."""
    def __init__(self, text):
        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label(
            text,
            font_name='Arial', font_size=32,
            color=(200, 255, 255, 255), x=32, y=300, #TODO: da aggiustare
            batch=self.batch)
        # self.disp_hand_gesture = pyglet.text.Label(
        #     text,
        #     font_name='Arial', font_size=32,
        #     color=(200, 255, 255, 255), x=32, y=100,  # TODO: da aggiustare
        #     batch=self.batch)
        self.x_ratio = 1
        self.y_ratio = 1

        # load gesture's names
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                  encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ]
        self.keypoint_classifier_labels = keypoint_classifier_labels

    def update(self, dt):
        """Update the scene state over time."""
        pass

    def handle_key(self, symbol, modifiers):
        """Handle key presses specific to the scene."""
        # if symbol == key.Q:
        #     exit(10)
        pass

# class MainMenuScene(SceneTemplate):
#     def __init__(self, pipe_conn):
#         super().__init__(text='Loading...')
#         self.pipe_conn = pipe_conn
#
#
#     def update(self, dt):
#         """Update the scene state."""
#         # Update the circle position from pipe data
#         if self.pipe_conn.poll():
#             #informazioni = self.pipe_conn.recv()
#             self.label.text = "Loaded!"
#
#     def handle_key(self, symbol, modifiers):
#         """Handle key presses."""




class Tutorial1(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='')
        # self.pipe_conn = pipe_conn
        # self.circle = pyglet.shapes.Circle(512, 384, 20, color=(255, 0, 0), batch=self.batch)
        # self.label.text += "\nControl the red circle with external inputs!"

        # Documento del testo di benvenuto
        welcome_document = pyglet.text.document.FormattedDocument()
        welcome_document.text = (
            "Benvenuto nel Sistema di Riabilitazione\n"
            "Preparati a migliorare i movimenti delle mani e delle braccia "
            "attraverso un percorso interattivo a livelli.\n\n"
            "Premi [SPAZIO] per iniziare, [I] per tornare indietro!"
        )
        welcome_document.set_style(0, 9, {'font_size': 36, 'bold': True,
                                          'color': (255, 255, 0, 255)})  # Stile per "Benvenuto"
        welcome_document.set_style(10, len(welcome_document.text), {'font_size': 20, 'color': (255, 255, 255, 255)})

        # Layout del testo
        text_layout = pyglet.text.layout.TextLayout(
            welcome_document,
            width= width - 150,
            multiline=True,
            x=50,
            y= height - 200,
            batch=self.batch
        )


class Tutorial2(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='')
        # Creazione di un cerchio rosso che rappresenta il pallino
        self.ball_radius = 20
        self.ball = Circle(x= width // 2, y= height // 2, radius=self.ball_radius, color=(255, 0, 0), batch=self.batch)

        self.ball_direction = 1  # Movimento oscillante
        self.ball_speed = 100  # Velocità del pallino

        # Documento del testo che spiega le meccaniche
        gameplay_document = pyglet.text.document.FormattedDocument()
        gameplay_document.text = (
            "In questo gioco, controllerai un'entità tramite i "
            "gesti della mano.\nUna pallina rossa apparirà sullo schermo e dovrai farla muovere con i tuoi movimenti.\n\n"
            "Premi [SPAZIO] per continuare, [I] per tornare indietro."
        )
        # Evidenzia "gesti della mano"
        gameplay_document.set_style(48, 66, {'font_size': 24, 'bold': True,
                                             'color': (0, 255, 0, 255)})  # Verde evidenziato per 'gesti della mano'
        # gameplay_document.set_style(0, 9,
        #                             {'font_size': 36, 'bold': True, 'color': (255, 255, 0, 255)})  # Stile per il titolo
        gameplay_document.set_style(0, len(gameplay_document.text), {'font_size': 20, 'color': (255, 255, 255, 255)})

        # Layout del testo
        text_layout = pyglet.text.layout.TextLayout(
            gameplay_document,
            width= width - 150,
            multiline=True,
            x=50,
            y= height - 200,
            batch=self.batch
        )

    def update(self, dt):
        """Aggiorna lo stato dell'animazione del pallino."""
        #global ball_direction
        self.ball.x += self.ball_direction * self.ball_speed * dt
        if self.ball.x > width - self.ball_radius or self.ball.x < self.ball_radius:
            self.ball_direction *= -1  # Inverte direzione
        self.ball.y = height // 2  # Mantieni il pallino a metà altezza
        self.batch.draw()


class Tutorial3(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='')
        # Creazione della pallina controllata dal giocatore (rossa)
        self.ball_radius = 20
        self.player_ball = Circle(x= width // 3,
                             y= height // 2,
                             radius=self.ball_radius, color=(255, 0, 0),
                             batch=self.batch)

        # Creazione del checkpoint (pallina blu)
        self.checkpoint_ball = Circle(x=2 * width // 3, y=height // 2, radius=self.ball_radius, color=(0, 0, 255),
                                 batch=self.batch)



        # Documento del testo che descrive l'esercizio
        exercise_description = pyglet.text.document.FormattedDocument()

        # Aggiornamento del testo con stili diversi
        exercise_description.text = (
            "Esempio di esercizio:\n1)Posiziona una delle tue mani davanti alla fotocamera.\n"
            "2) Apri il palmo per far muovere la pallina rossa,\n3)chiudi il palmo per fermarla o cambiare direzione.\n\n"
            "L'obiettivo è spostare la pallina rossa attraverso i checkpoint (pallini blu), rimanendo nel box.\n"
            "Premi SPAZIO per continuare tra i livelli, [P] per avviare il livello, [I] per tornare indietro."
        )

        # Impostazioni degli stili per la formattazione del testo
        exercise_description.set_style(0, len(exercise_description.text), {
            'font_name': 'Arial',  # Font del testo
            'font_size': 18,  # Dimensione del font
            'color': (255, 255, 255, 255),  # Colore del testo (bianco)
            'bold': False  # Testo in grassetto
        })

        # Layout del testo
        text_layout = pyglet.text.layout.TextLayout(
            exercise_description,
            width=width - 100,
            multiline=True,
            x=50,
            y=height - 250,
            batch=self.batch
        )

        # Aggiunta delle etichette descrittive per le palline
        self.player_ball_label = pyglet.text.Label('Pallina controllata dal giocatore (Rossa)', font_name='Arial',
                                              font_size=12,
                                              x=self.player_ball.x, y=self.player_ball.y - 30, color=(255, 255, 255, 255),
                                              batch=self.batch,
                                              anchor_x='center', anchor_y='center')

        self.checkpoint_ball_label = pyglet.text.Label('Checkpoint (Blu)', font_name='Arial', font_size=12,
                                                  x=self.checkpoint_ball.x, y=self.checkpoint_ball.y - 30,
                                                  color=(255, 255, 255, 255),
                                                  batch=self.batch, anchor_x='center', anchor_y='center')

        # Creazione di un box semitrasparente che contiene i pallini
        self.box_width = int(width * 0.8)
        self.box_height = int(height * 0.382)
        self.box_x = (width - self.box_width) // 2
        self.box_y = (height - self.box_height) // 2
        self.boxangle = pyglet.shapes.Rectangle(
            self.box_x, self.box_y, self.box_width, self.box_height,
            color=(50, 50, 50), batch=self.batch)
        self.boxangle.opacity = 100

class Tutorial3_1(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='')

        # Creazione della pallina controllata dal giocatore (rossa)
        self.ball_radius = 20
        self.player_ball = Circle(x=width // 3,
                                  y=height // 2 - 100,
                                  radius=self.ball_radius, color=(255, 0, 0),
                                  batch=self.batch)

        # Creazione del checkpoint (pallina blu)
        self.checkpoint_ball = Circle(x=2 * width // 3,
                                      y=height // 2 - 100,
                                      radius=self.ball_radius, color=(0, 0, 255),
                                      batch=self.batch)

        # Documento del testo che descrive l'esercizio
        exercise_description = pyglet.text.document.FormattedDocument()

        # Testo descrittivo
        exercise_description.text = (
            "Esempio di esercizio:\n1) Posiziona una delle tue mani davanti alla fotocamera.\n"
            "2) Apri il palmo per far muovere la pallina rossa,\n3) chiudi il palmo per fermarla o cambiare direzione.\n\n"
            "L'obiettivo è spostare la pallina rossa attraverso i checkpoint (pallini blu), rimanendo nel box.\n"
            "Premi [SPAZIO] per spostarti tra un livello e l'altro, [I] per tornare indietro."
        )

        # Impostazioni degli stili per la formattazione del testo
        exercise_description.set_style(0, len(exercise_description.text), {
            'font_name': 'Arial',
            'font_size': 18,
            'color': (255, 255, 255, 255),
            'bold': False
        })

        # Layout del testo: larghezza metà schermo
        text_layout = pyglet.text.layout.TextLayout(
            exercise_description,
            width=(width // 2) - 100,
            multiline=True,
            x=50,
            y=height - 250,
            batch=self.batch
        )

        # Aggiunta delle etichette descrittive per le palline
        self.player_ball_label = pyglet.text.Label('Pallina controllata dal giocatore (Rossa)', font_name='Arial',
                                                   font_size=12,
                                                   x=self.player_ball.x, y=self.player_ball.y - 30,
                                                   color=(255, 255, 255, 255),
                                                   batch=self.batch,
                                                   anchor_x='center', anchor_y='center')

        self.checkpoint_ball_label = pyglet.text.Label('Checkpoint (Blu)', font_name='Arial', font_size=12,
                                                       x=self.checkpoint_ball.x, y=self.checkpoint_ball.y - 30,
                                                       color=(255, 255, 255, 255),
                                                       batch=self.batch, anchor_x='center', anchor_y='center')

        # Creazione di un box semitrasparente che contiene i pallini
        self.box_width = int(width * 0.8)
        self.box_height = int(height * 0.382)
        self.box_x = (width - self.box_width) // 2
        self.box_y = (height - self.box_height) // 2 - 100
        self.boxangle = pyglet.shapes.Rectangle(
            self.box_x, self.box_y, self.box_width, self.box_height,
            color=(50, 50, 50), batch=self.batch)
        self.boxangle.opacity = 100

        # Caricamento e disegno dell'immagine
        image_path = "img_tut1.png"  # Sostituisci con il percorso corretto dell'immagine
        self.image = pyglet.image.load(image_path)
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x=width // 2 + 50,  # L'immagine occupa la metà destra dello schermo
            y=height // 2 + 100,
            batch=self.batch
        )

class Tutorial4(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='')
        # Testo da visualizzare
        text_content = """
        Poni una delle due mani davanti allo schermo,
        come vedi nei video a lato. Cerca di non
        avvicinarti troppo alla fotocamera, poni la 
        mano davanti ai tuoi occhi. Se non venisse
        rilevata, muovi la mano avanti e indietro.

        Perfetto, la mano è rilevabile correttamente.

        Adesso prova ad aprire il palmo. Perfetto!
        Adesso prova a chiuderla. Bene.

        Quelli che seguiranno saranno degli esercizi
        in cui dovrai muovere una pallina rossa; per
        farlo dovrai centrare la tua mano sulla pallina,
        aprire la mano, e muovere la mano dove
        vuoi che vada la pallina.
        Cerca di muoverla affinché raggiunga i checkpoint
        (pallini blu), eseguendo una traiettoria il più
        precisa possibile. Non te ne pentirai.

        Fai pratica con questa pallina. Quando ti sentirai
        pronto, premi spazio per attraversare i livelli.
        """

        # Crea un batch per raggruppare il testo
        self.batch = pyglet.graphics.Batch()

        # Creazione del layout di testo
        self.instructions_label = Label(text=text_content,
                                   font_name='Arial',
                                   font_size=12,
                                   x=10,  # Margine sinistro
                                   y=height - 20,  # Margine superiore
                                   anchor_x='left',
                                   anchor_y='top',
                                   width=width // 2,  # Limita la larghezza al 50% dello schermo
                                   multiline=True,
                                   color=(255, 255, 255, 255),  # Colore bianco
                                   batch=self.batch)

class Exercise_FollowPath(SceneTemplate):
    def __init__(self, pipe_conn,
                 polygon_points = [(171, 505), (171, 455), (1536, 455), (1536, 505)],
                 circle_position_x = 100,
                 circle_position_y  = 240, #posizione di default
                 checkpoint_list = [{'x': 123, 'y':367, 'radius': 15}],
                 level_title = "",
                 difficulty_times = {'facile': 30.0, 'medio':20.0, 'difficile': 8.0}
    ):
        super().__init__(text='')

        self.difficulty_times = difficulty_times
        self.pipe_conn = pipe_conn

        self.bg_group = Group(order=0)
        self.fg_group = Group(order=1)

        flag = True
        while flag:
            informazioni = self.pipe_conn.recv()
            # updating ratios of re-drawing
            self.x_ratio = width / informazioni['cam_width']
            self.y_ratio = height / informazioni['cam_height']
            #self.initialize()
            flag = self.pipe_conn.poll()


        self.polygon_vertices = polygon_points
        self.polygon = list(map(lambda v: (v[0], -v[1] + height), self.polygon_vertices))

        self.poligono = pyglet.shapes.Polygon(
            *self.polygon_vertices,
            color=(50, 100, 255),  # Colore di riempimento (azzurro)
            batch=self.batch,
            group=self.fg_group
        )
        self.poligono.opacity = 90

        # Pallino rosso
        self.circle_x = circle_position_x * self.x_ratio
        self.circle_y = circle_position_y * self.y_ratio
        self.circle = pyglet.shapes.Circle(
            self.circle_x, self.circle_y, 25,
            color=(255, 0, 0), batch=self.batch, group=self.fg_group)

        #rettangolo per evidenziare meglio la warning label
        self.warning_box = pyglet.shapes.Rectangle(
            0, 0, width, 50,
            color=(50, 50, 50, 180), batch=self.batch, group=self.fg_group)

        # Livello, Cronometro, Gesto corrente, warning, <Accuracy>
        self.timer_running = False
        self.time_elapsed = 0.0
        #self.timer_label_warning = 0.0
        self.timer_label = pyglet.text.Label(
            "Cronometro: 0.0", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 40, batch=self.batch, group=self.fg_group)
        self.timer_label.visible = False

        self.timer_remaining_label = pyglet.text.Label(
            "Tempo rimanente: 0.0", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 40, batch=self.batch, group=self.fg_group)

        self.label_instructions = pyglet.text.Label(  # label livello
            "Premi [Enter] per iniziare, [R] per ricominciare il livello, [P] per mettere in pausa.", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 20, batch=self.batch, group=self.fg_group)

        self.label_level = pyglet.text.Label( #label livello
            level_title, font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 20, batch=self.batch, group=self.fg_group)
        self.label_level.visible = False

        self.label_gesture = pyglet.text.Label( #gesto rilevato
            "Gesto rilevato: ", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 60, batch=self.batch, group=self.fg_group)
        self.label_gesture.visible = False

        self.label_warning = pyglet.text.Label(  # warning outside box
            "", font_name="Arial", font_size=32,
            color=(255, 100, 100, 255), x=10, y=10, batch=self.batch, group=self.fg_group)

        # Accumulate area #TODO refactoring nel menu secondario
        self.path = []  # Lista di coordinate tracciate dal pallino
        self.accuracy_label = pyglet.text.Label(
            "", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 80, batch=self.batch, group=self.fg_group)
        self.accuracy_label.visible = False

        #checkpoint logic (defined as centroid of each triangle)
        self.checkpoints = checkpoint_list
        self.checkpoints_reached = [False] * len(self.checkpoints) #[False, False, False]
        #self.checkpoints_reached[0] = True
        self.checkpoint_shapes = []

        for checkpoint in self.checkpoints:
            checkpoint_shape = pyglet.shapes.Circle(
                checkpoint['x'], checkpoint['y'], checkpoint['radius'],
                color=(200, 0, 0), batch=self.batch, group=self.fg_group)
            self.checkpoint_shapes.append(checkpoint_shape)

        self.checkpoint_shapes[0].color = (0, 0, 200) #evidenziamo il primo checkpoint da prendere

        self.x_ratio = 1.0 #width / informazioni["cam_width"]
        self.y_ratio = 1.0 #height / informazioni["cam_height"]

        ########## DEFINIZIONE SCHERMATA DI VITTORIA
        # Rettangolo
        self.success_rect_width = int(width * 0.5)
        self.success_rect_height = int(height * 0.382)
        self.success_rect_x = (width - self.success_rect_width) // 2
        self.success_rect_y = (height - self.success_rect_height) // 2
        self.success_rectangle = pyglet.shapes.Rectangle(
            self.success_rect_x, self.success_rect_y, self.success_rect_width, self.success_rect_height,
            color=(200, 200, 200), batch=self.batch, group=self.fg_group)
        self.success_rectangle.opacity = 180
        self.success_rectangle.visible = False

        self.document_success = pyglet.text.document.FormattedDocument()
        label_winning = (
            "SUCCESSO\n"  # Titolo grande
            f"Hai completato il percorso in {00.0} secondi e con una accuratezza del {float(0.0):.2%}%. "
            "Puoi passare al prossimo livello."
        )
        self.document_success.text = label_winning
        # Stile per "SUCCESSO"
        self.document_success.set_style(0, 8, {'font_size': 80, 'color': (0, 255, 0, 255), 'bold': True, 'align': 'center',
                                  'font_name': 'Arial'})
        # Stile per il resto del testo
        self.document_success.set_style(8, len(self.document_success.text),
                                        {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})
        # Usa un layout per il testo
        self.text_layout_success = pyglet.text.layout.TextLayout(
            document=self.document_success,
            width=self.success_rect_x * 2 - 10,  # Larghezza del testo con margini laterali
            # height= self.success_rect_height,
            multiline=True,
            batch=self.batch, group=self.fg_group,
            x=0,  # Margine sinistro
            y=0  # Centra verticalmente il titolo
        )
        self.text_layout_success.x = (width - self.text_layout_success.content_width) // 2  # Centra orizzontalmente
        self.text_layout_success.y = (height - self.text_layout_success.content_height) // 2  # Centra verticalmente
        self.text_layout_success.visible = False

        ########## DEFINIZIONE SCHERMATA DI PAUSA
        # Rettangolo
        self.pause_rect_width = int(width * 0.5)
        self.pause_rect_height = int(height * 0.382)
        self.pause_rect_x = (width - self.pause_rect_width) // 2
        self.pause_rect_y = (height - self.pause_rect_height) // 2
        self.pause_rectangle = pyglet.shapes.Rectangle(
            self.pause_rect_x, self.pause_rect_y, self.pause_rect_width, self.pause_rect_height,
            color=(200, 200, 200), batch=self.batch, group=self.fg_group)
        self.pause_rectangle.opacity = 180
        self.pause_rectangle.visible = False

        self.pause_document = pyglet.text.document.FormattedDocument()
        label_pause = (
            "PAUSA\n"  # Titolo grande
            f"Il gioco è attualmente in pausa. Per riprendere l'esecuzione premere [P]. Per resettare invece premere [R]"
        )
        self.pause_document.text = label_pause
        # Stile per "SUCCESSO"
        self.pause_document.set_style(0, 5,
                                        {'font_size': 80, 'color': (0, 255, 0, 255), 'bold': True, 'align': 'center',
                                         'font_name': 'Arial'})
        # Stile per il resto del testo
        self.pause_document.set_style(5, len(self.pause_document.text),
                                        {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})
        # Usa un layout per il testo
        self.text_layout_pause = pyglet.text.layout.TextLayout(
            document=self.pause_document,
            width=self.pause_rect_x * 2 - 10,  # Larghezza del testo con margini laterali
            # height= self.success_rect_height,
            multiline=True,
            batch=self.batch, group=self.fg_group,
            x=0,  # Margine sinistro
            y=0  # Centra verticalmente il titolo
        )
        self.text_layout_pause.x = (width - self.text_layout_pause.content_width) // 2  # Centra orizzontalmente
        self.text_layout_pause.y = (height - self.text_layout_pause.content_height) // 2  # Centra verticalmente
        self.text_layout_pause.visible = False


        self.enable_player_rendering = True #bolleano per indicare se streammare o meno il player

        ########## DEFINIZIONE SCHERMATA DI SELEZIONE DIFFICOLTA
        # Rettangolo
        self.chosediff_rect_width = int(width * 0.5)
        self.chosediff_rect_height = int(height * 0.42)
        self.chosediff_rect_x = (width - self.chosediff_rect_width) // 2
        self.chosediff_rect_y = (height - self.chosediff_rect_height) // 2
        self.chosediff_rectangle = pyglet.shapes.Rectangle(
            self.chosediff_rect_x, self.chosediff_rect_y, self.chosediff_rect_width, self.chosediff_rect_height,
            color=(200, 200, 200), batch=self.batch, group=self.fg_group)
        self.chosediff_rectangle.opacity = 180
        self.chosediff_rectangle.visible = True

        self.level_difficulty_chosen = 'facile'

        self.chosediff_document = pyglet.text.document.FormattedDocument()
        #time_level = self.difficulty_times[self.level_difficulty_chosen]
        label_chosediff = (
            f"DIFFICOLTA'\n"  # Titolo grande
            f"Scegli la difficoltà del gioco, espressa in termini di tempo richiesti per completate il livello. "
            f"Premi [1] per la difficoltà facile ({self.difficulty_times['facile']} s.), "
            f"[2] per la media ({self.difficulty_times['medio']} s.) e [3] per la difficile ({self.difficulty_times['difficile']} s.). "
            f"Premi [ENTER] per iniziare a giocare."
        )
        self.chosediff_document.text = label_chosediff
        # Stile per "SUCCESSO"
        self.chosediff_document.set_style(0, 11,
                                      {'font_size': 80, 'color': (0, 255, 255, 255), 'bold': True, 'align': 'center',
                                       'font_name': 'Arial'})
        # Stile per il resto del testo
        self.chosediff_document.set_style(11, len(self.chosediff_document.text),
                                      {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})
        # Usa un layout per il testo
        self.text_layout_chosediff = pyglet.text.layout.TextLayout(
            document=self.chosediff_document,
            width=self.chosediff_rect_x * 2 - 10,  # Larghezza del testo con margini laterali
            # height= self.success_rect_height,
            multiline=True,
            batch=self.batch, group=self.fg_group,
            x=0,  # Margine sinistro
            y=0  # Centra verticalmente il titolo
        )
        self.text_layout_chosediff.x = (width - self.text_layout_chosediff.content_width) // 2  # Centra orizzontalmente
        self.text_layout_chosediff.y = (height - self.text_layout_chosediff.content_height) // 2  # Centra verticalmente
        self.text_layout_chosediff.visible = True

        self.first_checkpoint_not_reached = True
        self.first_checkpoint_reached_time_elapsed = 0.0

    def start_game(self):
        """Avvia il timer e consente il movimento del pallino."""
        self.timer_running = True
        self.time_elapsed = 0.0
        self.first_checkpoint_reached_time_elapsed = 0.0
        self.path = []  # Resetta il percorso del pallino

    def stop_game(self):
        """Ferma il gioco e calcola l'accuratezza."""
        self.timer_running = False

        time_level = self.difficulty_times[self.level_difficulty_chosen]
        is_win = float(self.timer_label.text[12:]) < time_level
        #print(is_win)

        # Calcola l'accuratezza
        if len(self.path) > 1:
            # punti che delineano le posizioni dei checkpoint
            checkpoints = [(d['x'], d['y']) for d in self.checkpoints if 'x' in d and 'y' in d]

            #conversione di ogni elemento con Decimal per evitare problemi di conversione
            checkpoints = [(Decimal(x), Decimal(y)) for x, y in checkpoints]
            self.path = [(Decimal(x), Decimal(y)) for x, y in self.path]
            #print(checkpoints)



            # punti del giocatore + intersezione con la linea ideale
            _ , player_intersection = elimina_codini(checkpoints, self.path)
            #print(f'Player points (elimina code): {player_intersection}')
            player_intersection = insert_intersections_decimal(checkpoints, list(player_intersection))
            player_intersection = [(round(x, 1), round(y, 1)) for x, y in player_intersection]
            #print(f'Path del player + punti di intersezione con il path dei checkpoint (player_intersection): {player_intersection}')

            # punti dei checkpoint + intersezioni con l'utente sulla linea ideale
            checkpoint_intersection = insert_intersections_decimal(player_intersection, checkpoints)
            checkpoint_intersection = [(round(x, 1), round(y, 1)) for x, y in checkpoint_intersection]
            #print(f'Checkpoints e intersezione con il path del player (checkpoint_intersection): {checkpoint_intersection}')

            #c'è un bug per cui a volte un elemento di checkpoint interaction è
            #presente nella lista mentre non dovrebbe esserci
            intersezioni_pla_check = [elemento for elemento in checkpoints if elemento not in checkpoint_intersection]
            intersezioni_pla_check = [(round(x, 1), round(y, 1)) for x, y in intersezioni_pla_check]
            #secondo arrootondamento esterno per evitare problemi di python
            #intersezioni_pla_check = aggiorna_punti(checkpoint_intersection, intersezioni_pla_check)
            #print(f'Intersezioni tra player e checkpoint (aggiorna punti): {intersezioni_pla_check}')

            #forse bisogna fare un ciclo di queste operazioni....

            player_intersection = rimuovi_duplicati_consecutivi(player_intersection)
            checkpoint_intersection = rimuovi_duplicati_consecutivi(checkpoint_intersection)

            player_intersection_sicuro  = rimuovi_duplicati_consecutivi(aggiorna_punti(checkpoint_intersection, player_intersection))

            # Aggiorna la prima lista rimuovendo gli elementi non presenti nella seconda lista
            checkpoint_intersection = [coppia for coppia in checkpoint_intersection if coppia in player_intersection_sicuro]

            if is_debugging_mode:
                main(player_intersection, checkpoint_intersection, [], [])

            rect_area = polygon_area_decimal(self.polygon) #area totale oltre cui non uscire

            area_diff = calcola_area_totale_decimal(checkpoint_intersection, player_intersection_sicuro)

            accuracy = 1 - min(area_diff / rect_area, 1)

            # Schermata di vittoria (o sconfitta?? :O )


            if is_win:
                label_winning = (
                    "SUCCESSO\n"  # Titolo grande
                    f"Hai completato il percorso in {self.timer_label.text[12:]} secondi e con una accuratezza del {float(accuracy):.2%}!. "
                    "\nPremi [Spazio] per andare al prossimo livello; [I] per tornare indietro; [Q] Esci; [R] Rigioca il livello attuale."
                )
                self.text_layout_success.document.text = label_winning
                self.document_success.set_style(0, 8, {'font_size': 80, 'color': (0, 255, 0, 255), 'bold': True, 'align': 'center',
                                               'font_name': 'Arial'})
                self.document_success.set_style(8, len(self.document_success.text),
                                                {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})

                if is_end_level_audio_enabled:
                    sound = pyglet.media.load('sounds/win.wav', streaming=False)
                    sound.play()
            else:
                if all(self.checkpoints_reached):
                    label_winning = (
                        "RIPROVA!\n"  # Titolo grande
                        f"Hai completato il percorso in {self.timer_label.text[12:]} secondi, ma avevi solo {time_level} secondi!. "
                        "\nPremi [spazio] per andare al prossimo livello; [Q] Esci; [R] Rigioca il livello attuale."
                    )
                else:
                    label_winning = (
                        "RIPROVA!\n"  # Titolo grande
                        f"Non sei riuscito a completare il percorso nei {time_level} secondi previsti!. "
                        "\nPremi [spazio] per andare al prossimo livello; [Q] Esci; [R] Rigioca il livello attuale."
                    )

                self.text_layout_success.document.text = label_winning
                self.document_success.set_style(0, 8, {'font_size': 80, 'color': (255, 0, 0, 255), 'bold': True,
                                                       'align': 'center',
                                                       'font_name': 'Arial'})
                self.document_success.set_style(8, len(self.document_success.text),
                                                {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})

                if is_end_level_audio_enabled:
                    sound = pyglet.media.load('sounds/lose.wav', streaming=False)
                    sound.play()
        else:
            # Tempo scaduto, mostro il messaggio di sconfitta
            label_winning = (
                "RIPROVA!\n"  # Titolo grande
                f"Non sei riuscito a completare il percorso nei {time_level} secondi previsti!. "
                "\nPremi [spazio] per andare al prossimo livello; [Q] Esci; [R] Rigioca il livello attuale."
            )
            self.text_layout_success.document.text = label_winning
            self.document_success.set_style(0, 8, {'font_size': 80, 'color': (255, 0, 0, 255), 'bold': True,
                                                   'align': 'center',
                                                   'font_name': 'Arial'})
            self.document_success.set_style(8, len(self.document_success.text),
                                            {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})

            if is_end_level_audio_enabled:
                sound = pyglet.media.load('sounds/lose.wav', streaming=False)
                sound.play()




        self.text_layout_success.visible = True
        self.success_rectangle.visible = True



    def reset_game(self):
        """Ripristina lo stato iniziale del livello."""
        self.timer_running = False
        self.time_elapsed = 0.0
        #self.timer_label_warning = 0.0
        self.timer_label.text = "Cronometro: 0.0"
        #self.timer_remaining_label.text = "Tempo rimanente: 0.0"
        self.label_gesture.text = "Gesto rilevato: "
        self.label_warning.text = ""
        self.circle.x = self.circle_x #self.rect_x
        self.circle.y = self.circle_y #self.rect_y + self.rect_height // 2
        self.path = []
        self.accuracy_label.text = ""
        self.text_layout_success.visible = False
        self.success_rectangle.visible = False
        #forse è meglio richicamare init... o fare una funzione di initialize...

        for cp in range(0, len(self.checkpoint_shapes)):
            self.checkpoint_shapes[cp].color = (200, 0, 0)
        self.checkpoints_reached = self.checkpoints_reached = [False] * len(self.checkpoints)
        #[False, False, False]
        self.checkpoint_shapes[0].color = (0, 0, 200)  # evidenziamo il primo checkpoint da prendere

    def update(self, dt):
        """Aggiorna la posizione del pallino e il timer."""
        # Riceve dati dalla pipe e aggiorna la posizione
        if self.pipe_conn.poll():
            informazioni = self.pipe_conn.recv()

            # updating ratios of re-drawing
            self.x_ratio = width / informazioni["cam_width"]
            self.y_ratio = height / informazioni["cam_height"]

            # Display camera
            if self.enable_player_rendering:
                global sprites
                new_image = pyglet.image.ImageData(640, 480, 'RGB', informazioni["image"].tobytes(), pitch=-640 * 3)
                texture = new_image.get_texture()
                new_sprite = pyglet.sprite.Sprite(texture, x=0, y=0,
                                                  batch=self.batch,
                                                  group=self.bg_group)
                new_sprite.scale_x = self.x_ratio
                new_sprite.scale_y = self.y_ratio
                sprites = [new_sprite]  # Add the new sprite to the list

            if self.timer_running:
                self.time_elapsed += (dt * 3.8) #il programma è cosi lento che serve un moltiplicatore
                self.timer_label.text = f"Cronometro: {self.time_elapsed:.1f}"

                time_remaining = self.time_elapsed #valore base che aggiorneremo
                time_level = self.difficulty_times[self.level_difficulty_chosen]
                if not self.first_checkpoint_not_reached:
                    time_remaining = time_level-self.time_elapsed

                    if time_remaining > 0:
                        self.timer_remaining_label.text = f"Tempo rimanente: {(time_level-self.time_elapsed):.1f}"
                    else:
                        self.timer_remaining_label.text = f"Tempo rimanente: 0.0"

                #print(self.keypoint_classifier_labels[0])
                gesto_nome = self.keypoint_classifier_labels[informazioni['gesture']]
                gesto_id = informazioni['gesture']



                self.label_gesture.text = "Gesto rilevato: " + str(gesto_nome) + " (" + str(gesto_id) + ")"
                if is_debugging_mode:
                    self.label_gesture.visible = True
                else:
                    self.label_gesture.visible = False


                if informazioni['gesture'] != -1: #grabbing and ale grabbing
                    #we track the landmarks, create a polygon in which the ball lies and we
                    #move the ball according these positions
                    landmark0 = tuple(informazioni["landmarks"][0])
                    landmark4 = tuple(informazioni["landmarks"][4])
                    landmark8 = tuple(informazioni["landmarks"][8])
                    landmark12 = tuple(informazioni["landmarks"][12])
                    landmark16 = tuple(informazioni["landmarks"][16])
                    landmark20 = tuple(informazioni["landmarks"][20])
                    polygon = [landmark0, landmark4, landmark8, landmark12, landmark16, landmark20]
                    polygon = list(map(lambda x: (x[0] * self.x_ratio, -x[1]*self.y_ratio + height), polygon))

                    point = self.circle.position

                    inside = raycasting(point, polygon)

                    centroid, area = calculate_centroid(polygon)
                    if inside:
                        x = centroid[0]
                        y = centroid[1]

                        if self.first_checkpoint_not_reached: #finché non tocca il pallino aggiorniamo il tempo
                            self.first_checkpoint_reached_time_elapsed += self.time_elapsed

                        self.first_checkpoint_not_reached = False #basta una sola volta

                        #i valori sono boundati al rettangolo in questo caso per il calcolo della accuracy
                        new_x, new_y = clamp_point_in_polygon(
                            (x, y),
                            self.polygon_vertices
                        )

                        #in ogni caso sono vincolati alle dimensioni dello schermo per evitare che esca il pallino
                        x, y = clamp_point_in_polygon(
                            (x, y),
                            [(0+20, 0+20), (0+20, height-20), (width-20, height-20), (width-20, 0+20)],
                        )

                        #la mano è libera ma le coordinate per l'accuracy sono incolate al poligono
                        self.circle.x = x
                        self.circle.y = y
                        self.path.append((new_x, new_y))
                        #self.path.append((x, y))


                        #avvertimento se esce dal poligono
                        #logica per rendere indipendente questo controllo
                        warning_text = "Attento, stai uscendo dall'area indicata!"
                        if self.label_warning.text == warning_text:
                            self.label_warning.text = ""
                        #self.label_warning.text = str(self.circle.x) + " " + str(self.circle.y)
                        if not raycasting((self.circle.x, self.circle.y), self.polygon_vertices):
                            #print("DENTRO IL POLIGONO")
                            self.label_warning.color = (255, 100, 100, 255)
                            self.label_warning.text = warning_text

                        self.check_for_checkpoints() #check if a checkpoint is crossed

                # Ferma il gioco se il pallino raggiunge il lato destro (e non è rimasto li dalla iterazione precedente)
                # if new_x >= self.rect_x + self.rect_width and self.time_elapsed > 1.0:
                if all(self.checkpoints_reached) or time_remaining < 0:
                    self.stop_game()

                self.batch.draw()

    def check_for_checkpoints(self):
        for i, checkpoint in enumerate(self.checkpoints):
            if not self.checkpoints_reached[i]:
                distance = math.sqrt((self.circle.x - checkpoint['x']) ** 2 + (self.circle.y - checkpoint['y']) ** 2)
                if distance < (checkpoint['radius']) + 20:
                    #aggiungiamo un controllo per attraversare i checkpint in ordine
                    if self.checkpoints_reached[i-1] and i > 0 or i == 0: #tranne il primo
                        # if i == 0: #elimino tutto il percorso fatto fin'ora
                        #     self.path.clear()
                        #playsound
                        #playsound('/sounds/coin.wav')
                        sound = pyglet.media.load('sounds/coin.wav', streaming=False)
                        sound.play()

                        self.checkpoints_reached[i] = True
                        self.checkpoint_shapes[i].color = (0, 255, 0)
                        self.label_warning.text = f"Checkpoint {i+1} raggiunto, continua così!"
                        self.label_warning.color = (0, 200, 0, 255)

                        #aggiungo un punto esatto nel path per semplificare i calcoli
                        self.path.append((self.checkpoint_shapes[i].x, self.checkpoint_shapes[i].y))
                        #se non si rompe ok
                        if i != len(self.checkpoints) - 1: #coloriamo il successivo in blu per tracciare il peth
                            self.checkpoint_shapes[i+1].color = (0, 0, 255)




    def handle_key(self, symbol, modifiers):
        # Scelta difficoltà facile
        if symbol == key._1:
            self.level_difficulty_chosen = 'facile'             #{'facile': 30.0, 'medio':20.0, 'difficile': 8}
            self.label_warning.text = "Scelto il livello 1"

            time_level = self.difficulty_times[self.level_difficulty_chosen]
            self.timer_remaining_label.text = f"Tempo rimanente: {time_level}"
        if symbol == key._2:
            self.level_difficulty_chosen = 'medio'
            self.label_warning.text = "Scelto il livello 2"

            time_level = self.difficulty_times[self.level_difficulty_chosen]
            self.timer_remaining_label.text = f"Tempo rimanente: {time_level}"
        if symbol == key._3:
            self.level_difficulty_chosen = 'difficile'
            self.label_warning.text = "Scelto il livello 3"

            time_level = self.difficulty_times[self.level_difficulty_chosen]
            print(time_level)
            self.timer_remaining_label.text = f"Tempo rimanente: {time_level}"


        """Gestisce l'input da tastiera."""
        if symbol == key.R:  # Ripristina il livello con il tasto R
            #al reset facciamo riscegliere la difficoltà?
            self.text_layout_chosediff.visible = True
            self.chosediff_rectangle.visible = True

            self.pause_rectangle.visible = False
            self.text_layout_pause.visible = False

            self.reset_game()
            #self.start_game()

        if symbol == key.ENTER and not self.timer_running:
            self.text_layout_chosediff.visible = False
            self.chosediff_rectangle.visible = False

            self.label_instructions.visible = False
            self.label_level.visible = True
            #self.reset_game()
            self.reset_game()
            self.start_game()

        if symbol == key.P:
            if self.timer_running:
                #print("Hai tentato di mettere in pausa il gioco")
                self.timer_running = False
                self.pause_rectangle.visible = True
                self.text_layout_pause.visible = True

                self.success_rectangle.visible = False
                self.text_layout_success.visible = False

            else:
                #print("Hai tentato di continuare il gioco")

                #mettiamo un countdown di qualche secondo prima di far continuare
                self.timer_running = True
                self.pause_rectangle.visible = False
                self.text_layout_pause.visible = False

                self.success_rectangle.visible = False
                self.text_layout_success.visible = False







class LevelFollowPath1(Exercise_FollowPath):
    def __init__(self, pipe_conn):
        x_ratio = screen_width / 640
        y_ratio = screen_height / 480

        self.polygon_vertices = [
            (100, 350),  # Punto in basso a sinistra con padding
            (540, 350),  # Punto in basso alla fine della parte lunga della L
            (540, 150),  # Punto in alto della gambetta corta
            (100, 150),  # Angolo superiore destro della gambetta corta
        ]

        #posizione iniziale del cerchio per questo livello
        self.position_x = 150
        self.position_y = 250

        checkpoints = [
            {'x': 150 * x_ratio, 'y': 250 * y_ratio, 'radius': 15},
            {'x': 490 * x_ratio, 'y': 250 * y_ratio, 'radius': 15}
        ]


        self.polygon_vertices = list(map(lambda v: (v[0] * x_ratio, v[1]* y_ratio),
                                         self.polygon_vertices))

        super().__init__(pipe_conn,
                         polygon_points=self.polygon_vertices,
                         circle_position_x=self.position_x,
                         circle_position_y=self.position_y,
                         checkpoint_list=checkpoints,
                         level_title="Esercizio 1",
                         difficulty_times={'facile': 25.0, 'medio': 15.0, 'difficile': 10.0}
        )



class LevelFollowPath2(Exercise_FollowPath):
    def __init__(self, pipe_conn):
        x_ratio = screen_width / 640
        y_ratio = screen_height / 480

        self.polygon_vertices = [
            (85, 100),  # Punto in basso a sinistra con padding
            (500, 100),  # Punto in basso alla fine della parte lunga della L
            (500, 200),  # Punto in alto della gambetta corta
            (150, 200),  # Angolo superiore destro della gambetta corta
            (150, 400),  # Angolo superiore destro dello schermo
            (85, 400),  # Angolo in alto a sinistra con padding
        ]

        #posizione iniziale del cerchio per questo livello
        self.position_x = 120
        self.position_y = 400

        checkpoints = [
            {'x': 123 * x_ratio, 'y': 367 * y_ratio, 'radius': 15},
            {'x': 123 * x_ratio, 'y': 153 * y_ratio, 'radius': 15},
            {'x': 496 * x_ratio, 'y': 153 * y_ratio, 'radius': 15}
        ]


        self.polygon_vertices = list(map(lambda v: (v[0] * x_ratio, v[1]* y_ratio),
                                         self.polygon_vertices))

        super().__init__(pipe_conn,
                         polygon_points=self.polygon_vertices,
                         circle_position_x=self.position_x,
                         circle_position_y=self.position_y,
                         checkpoint_list=checkpoints,
                         level_title="Esercizio 2",
                         difficulty_times={'facile': 30.0, 'medio': 20.0, 'difficile': 15.0}
        )


class LevelFollowPath3(Exercise_FollowPath):
    def __init__(self, pipe_conn):
        x_ratio = screen_width / 640 * 0.9
        y_ratio = screen_height / 480 * 0.9

        self.polygon_vertices = [
            (100, 450),  # B1
            (100, 220),  # B12
            (480, 220),  # B11
            (480, 130),  # B10
            (100, 130),  # B9
            (100, 30),  # B8
            (540, 30),  # B7
            (540, 300),  # B6
            (170, 300),  # B5
            (170, 380),  # B4
            (540, 380),  # B3
            (540, 450),  # B2
            (100, 450)  # B1 (chiusura del poligono)
        ]

        #posizione iniziale del cerchio per questo livello
        self.position_x = 520
        self.position_y = 400

        checkpoints = [
            {'x': 500 * x_ratio, 'y': 420 * y_ratio, 'radius': 15},
            {'x': 140 * x_ratio, 'y': 420 * y_ratio, 'radius': 15},
            {'x': 140 * x_ratio, 'y': 270 * y_ratio, 'radius': 15},
            {'x': 500 * x_ratio, 'y': 270 * y_ratio, 'radius': 15},
            {'x': 500 * x_ratio, 'y': 80 * y_ratio, 'radius': 15},
            {'x': 140 * x_ratio, 'y': 80 * y_ratio, 'radius': 15}
        ]

        self.polygon_vertices = list(map(lambda v: (v[0] * x_ratio, v[1]* y_ratio),
                                         self.polygon_vertices))

        super().__init__(pipe_conn,
                         polygon_points=self.polygon_vertices,
                         circle_position_x=self.position_x,
                         circle_position_y=self.position_y,
                         checkpoint_list=checkpoints,
                         level_title="Esercizio 3",
                         difficulty_times={'facile': 60.0, 'medio': 45.0, 'difficile': 30.0}
        )


class FinalScene(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='')
        # Creazione della pallina controllata dal giocatore (rossa) e del checkpoint (blu)
        ball_radius = 20
        self.player_ball = Circle(x=width // 3, y=height // 2, radius=ball_radius, color=(255, 0, 0),
                             batch=self.batch)
        self.checkpoint_ball = Circle(x=2 * width // 3, y=height // 2, radius=ball_radius, color=(0, 0, 255),
                                 batch=self.batch)

        # Creazione della finestra finale
        self.congrats_text = pyglet.text.Label("Congratulazioni!\nHai completato tutte le sfide!",
                                          font_name='Arial', font_size=24,
                                          x=width // 2, y=height // 2 + 100,
                                          anchor_x='center', anchor_y='center', color=(255, 255, 255, 255), batch=self.batch)

        self.next_steps_text = pyglet.text.Label("Premi SPAZIO per ripetere le sfide\nPremi Q per uscire, I per tornare indietro.",
                                            font_name='Arial', font_size=18,
                                            x=width // 2, y=height // 2 - 50,
                                            anchor_x='center', anchor_y='center', color=(255, 255, 255, 255),
                                            batch=self.batch)

        # Funzione per gestire l'evento di pressione dei tasti