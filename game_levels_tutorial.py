from game_levels import *

class Tutorial_FollowPath(SceneTemplate):
    def __init__(self, pipe_conn,
                 polygon_points = [(0, 0), (0, height), (width, height), (width, 0)],
                 circle_position_x = 320,
                 circle_position_y  = 20, #posizione di default
                 checkpoint_list = [{'x': (210-105), 'y':(200), 'radius': 15},
                                    {'x': (420-105), 'y':(200), 'radius': 15},
                                    {'x': (630-105), 'y':(200), 'radius': 15}],
                 level_title = ""
                 #difficulty_times = {'facile': 30.0, 'medio':20.0, 'difficile': 8.0}
    ):
        super().__init__(text='')

        #self.difficulty_times = difficulty_times
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
            color=(0, 0, 0, 0),  # Colore di riempimento (trasparente)
            batch=self.batch,
            group=self.fg_group
        )
        self.poligono.opacity = 0

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

        # self.timer_remaining_label = pyglet.text.Label(
        #     "Tempo rimanente: 0.0", font_name="Arial", font_size=16,
        #     color=(255, 255, 255, 255), x=10, y=height - 40, batch=self.batch, group=self.fg_group)


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

        for i in range(len(self.checkpoint_shapes)):
            self.checkpoint_shapes[i].visible = False

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

        ########## DEFINIZIONE SCHERMATA DI TUTORIAL 1 (MUOVERE LA MANO NELLO SCHERMO CORRETTAMENTE)
        self.tutorial1_rect_width = int(width * 0.75)
        self.tutorial1_rect_height = int(height * 0.35)
        self.tutorial1_rect_x = (width - self.tutorial1_rect_width) // 2
        self.tutorial1_rect_y = ((height - self.tutorial1_rect_height) // 2) * 1.8
        self.tutorial1_rectangle = pyglet.shapes.Rectangle(
            self.tutorial1_rect_x, self.tutorial1_rect_y, self.tutorial1_rect_width, self.tutorial1_rect_height,
            color=(200, 200, 200), batch=self.batch, group=self.fg_group)
        self.tutorial1_rectangle.opacity = 180
        self.tutorial1_rectangle.visible = True

        self.level_difficulty_chosen = 'facile'

        self.tutorial1_hand_was_seen = False
        self.tutorial1_hand_over_redpoint = False

        self.tutorial1_document = pyglet.text.document.FormattedDocument()
        #time_level = self.difficulty_times[self.level_difficulty_chosen]
        label_tutorial1 = (
            f"PRIMO PASSO:\n"  # Titolo grande
            f"Posiziona la mano in modo che sia completamente visibile sullo schermo, occupando circa metà dell'area visibile, senza coprirla interamente."
            f"Apri quindi il palmo della mano. Premi [ENTER] per iniziare a giocare."
        )
        self.tutorial1_document.text = label_tutorial1
        # Stile per "SUCCESSO"
        self.tutorial1_document.set_style(0, 12,
                                          {'font_size': 80, 'color': (0, 255, 255, 255), 'bold': True, 'align': 'center',
                                       'font_name': 'Arial'})
        # Stile per il resto del testo
        self.tutorial1_document.set_style(12, len(self.tutorial1_document.text),
                                          {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})
        # Usa un layout per il testo
        self.text_layout_tutorial1 = pyglet.text.layout.TextLayout(
            document=self.tutorial1_document,
            width=self.tutorial1_rect_width - 10,  # Larghezza del testo con margini laterali
            #height= self.success_rect_height,
            multiline=True,
            batch=self.batch, group=self.fg_group,
            x=0,  # Margine sinistro
            y=0  # Centra verticalmente il titolo
        )
        self.text_layout_tutorial1.x = ((width - self.text_layout_tutorial1.content_width) // 2)   # Centra orizzontalmente
        self.text_layout_tutorial1.y = ((height - self.text_layout_tutorial1.content_height) // 2) * 1.75 # Centra verticalmente
        print(self.text_layout_tutorial1.x)
        print(self.text_layout_tutorial1.y)
        self.text_layout_tutorial1.visible = True

        #self.first_checkpoint_not_reached = True
        #self.first_checkpoint_reached_time_elapsed = 0.0

    def start_game(self):
        """Avvia il timer e consente il movimento del pallino."""
        self.timer_running = True
        self.time_elapsed = 0.0
        #self.first_checkpoint_reached_time_elapsed = 0.0
        self.path = []  # Resetta il percorso del pallino


    def stop_game(self):
        """Ferma il gioco e calcola l'accuratezza."""
        self.timer_running = False

        #time_level = self.difficulty_times[self.level_difficulty_chosen]
        #is_win = float(self.timer_label.text[12:]) < time_level
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

            # if is_debugging_mode:
            #     main(player_intersection, checkpoint_intersection, [], [])

            rect_area = polygon_area_decimal(self.polygon) #area totale oltre cui non uscire

            area_diff = calcola_area_totale_decimal(checkpoint_intersection, player_intersection_sicuro)

            accuracy = 1 - min(area_diff / rect_area, 1)

            # Schermata di vittoria (o sconfitta?? :O )


            if True:
                # label_winning = (
                #     "SUCCESSO\n"  # Titolo grande
                #     f"Hai completato il percorso in {self.timer_label.text[12:]} secondi e con una accuratezza del {float(accuracy):.2%}!. "
                #     "\nPremi [spazio] per andare al prossimo livello; [Q] Esci; [R] Rigioca il livello attuale."
                # )
                self.text_layout_tutorial1.visible = False
                self.tutorial1_rectangle.visible = False

                label_winning = (
                    "SUCCESSO\n"  # Titolo grande
                    f"Hai completato il percorso centrando tutti i checkpoint!. "
                    "\nPremi [spazio] per andare al prossimo livello; [Q] Esci; [R] Rigioca il livello attuale."
                )
                self.text_layout_success.document.text = label_winning
                self.document_success.set_style(0, 8, {'font_size': 80, 'color': (0, 255, 0, 255), 'bold': True, 'align': 'center',
                                               'font_name': 'Arial'})
                self.document_success.set_style(8, len(self.document_success.text),
                                                {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})

                if is_end_level_audio_enabled:
                    sound = pyglet.media.load('sounds/win.wav', streaming=False)
                    sound.play()
            # else:
            #     if all(self.checkpoints_reached):
            #         label_winning = (
            #             "RIPROVA!\n"  # Titolo grande
            #             f"Hai completato il percorso in {self.timer_label.text[12:]} secondi, ma avevi solo {time_level} secondi!. "
            #             "\nPremi [spazio] per andare al prossimo livello; [Q] Esci; [R] Rigioca il livello attuale."
            #         )
            #     else:
            #         label_winning = (
            #             "RIPROVA!\n"  # Titolo grande
            #             f"Non sei riuscito a completare il percorso nei {time_level} secondi previsti!. "
            #             "\nPremi [spazio] per andare al prossimo livello; [Q] Esci; [R] Rigioca il livello attuale."
            #         )
            #
            #     self.text_layout_success.document.text = label_winning
            #     self.document_success.set_style(0, 8, {'font_size': 80, 'color': (255, 0, 0, 255), 'bold': True,
            #                                            'align': 'center',
            #                                            'font_name': 'Arial'})
            #     self.document_success.set_style(8, len(self.document_success.text),
            #                                     {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})
            #
            #     if is_end_level_audio_enabled:
            #         sound = pyglet.media.load('sounds/lose.wav', streaming=False)
            #         sound.play()
        # else:
        #     # Tempo scaduto, mostro il messaggio di sconfitta
        #     # label_winning = (
        #     #     "RIPROVA!\n"  # Titolo grande
        #     #     f"Non sei riuscito a completare il percorso nei {time_level} secondi previsti!. "
        #     #     "\nPremi [spazio] per andare al prossimo livello; [Q] Esci; [R] Rigioca il livello attuale."
        #     # )
        #     # self.text_layout_success.document.text = label_winning
        #     # self.document_success.set_style(0, 8, {'font_size': 80, 'color': (255, 0, 0, 255), 'bold': True,
        #     #                                        'align': 'center',
        #     #                                        'font_name': 'Arial'})
        #     # self.document_success.set_style(8, len(self.document_success.text),
        #     #                                 {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})
        #     #
        #     # if is_end_level_audio_enabled:
        #     #     sound = pyglet.media.load('sounds/lose.wav', streaming=False)
        #     #     sound.play()




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

        self.tutorial1_hand_was_seen = False
        self.tutorial1_hand_over_redpoint = False
        #forse è meglio richicamare init... o fare una funzione di initialize...

        label_tutorial1 = (
            f"PRIMO PASSO:\n"  # Titolo grande
            f"Posiziona la mano in modo che sia completamente visibile sullo schermo, occupando circa metà dell'area visibile, senza coprirla interamente."
            f"Apri quindi il palmo della mano. Premi [ENTER] per iniziare a giocare."
        )
        self.tutorial1_document.text = label_tutorial1
        # Stile per "SUCCESSO"
        self.tutorial1_document.set_style(0, 12,
                                          {'font_size': 80, 'color': (0, 255, 255, 255), 'bold': True,
                                           'align': 'center',
                                           'font_name': 'Arial'})

        self.tutorial1_document.set_style(12, len(self.tutorial1_document.text),
                                          {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})

        for cp in range(0, len(self.checkpoint_shapes)):
            self.checkpoint_shapes[cp].color = (200, 0, 0)
            self.checkpoint_shapes[cp].visible = False

        self.checkpoints_reached = self.checkpoints_reached = [False] * len(self.checkpoints)
        #[False, False, False]
        self.checkpoint_shapes[0].color = (0, 0, 200)  # evidenziamo il primo checkpoint da prendere

        self.circle.visible = False



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

                # time_remaining = self.time_elapsed #valore base che aggiorneremo
                # time_level = self.difficulty_times[self.level_difficulty_chosen]
                # if not self.first_checkpoint_not_reached:
                #     time_remaining = time_level-self.time_elapsed
                #
                #     if time_remaining > 0:
                #         self.timer_remaining_label.text = f"Tempo rimanente: {(time_level-self.time_elapsed):.1f}"
                #     else:
                #         self.timer_remaining_label.text = f"Tempo rimanente: 0.0"

                #print(self.keypoint_classifier_labels[0])
                gesto_nome = self.keypoint_classifier_labels[informazioni['gesture']]
                gesto_id = informazioni['gesture']



                self.label_gesture.text = "Gesto rilevato: " + str(gesto_nome) + " (" + str(gesto_id) + ")"
                if is_debugging_mode:
                    self.label_gesture.visible = True
                else:
                    self.label_gesture.visible = False

                rilevamento_grabbing = False
                if self.tutorial1_hand_was_seen == False:
                    rilevamento_grabbing = informazioni['gesture'] == 1
                else:
                    rilevamento_grabbing = informazioni['gesture'] != -1

                if rilevamento_grabbing: #grabbing and ale grabbing
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

                    #Aggiornamento condizioni del tutorial
                    self.tutorial1_hand_was_seen = True

                    if self.tutorial1_hand_was_seen and self.tutorial1_hand_over_redpoint == False:
                        self.circle.visible = True
                        #Abilita la nuova schermata
                        label_tutorial = (
                            f"SECONDO PASSO:\n"  # Titolo grande
                            f"Ora che sei riuscito a far riconoscere la mano, tienila sempre aperta. Prova a prendere il pallino rosso con la mano, muovendola e tenendola sempre aperta."
                            #f"Premi [ENTER] per iniziare a giocare."
                        )
                        self.tutorial1_document.text = label_tutorial
                        self.tutorial1_document.set_style(0, 14, {'font_size': 80, 'color': (0, 225, 255, 255), 'bold': True,
                                                               'align': 'center',
                                                               'font_name': 'Arial'})
                        self.tutorial1_document.set_style(14, len(self.document_success.text),
                                                        {'font_size': 32, 'color': (255, 255, 255, 255), 'font_name': 'Arial'})



                    point = self.circle.position
                    inside = raycasting(point, polygon)
                    centroid, area = calculate_centroid(polygon)

                    if inside:
                        self.tutorial1_hand_over_redpoint = True
                        x = centroid[0]
                        y = centroid[1]

                        # if self.first_checkpoint_not_reached: #finché non tocca il pallino aggiorniamo il tempo
                        #     self.first_checkpoint_reached_time_elapsed += self.time_elapsed

                        # self.first_checkpoint_not_reached = False #basta una sola volta

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

                        if self.tutorial1_hand_over_redpoint:
                            # Abilita la nuova schermata
                            for i in range(len(self.checkpoint_shapes)):
                                self.checkpoint_shapes[i].visible = True

                            label_tutorial = (
                                f"TERZO PASSO:\n"  # Titolo grande
                                f"Ora che sei riuscito a catturare il pallino rosso, spostalo sul prossimo pallino blu che vedi."

                            )
                            self.tutorial1_document.text = label_tutorial
                            self.tutorial1_document.set_style(0, 12,
                                                              {'font_size': 80, 'color': (0, 195, 255, 235), 'bold': True,
                                                               'align': 'center',
                                                               'font_name': 'Arial'})
                            self.tutorial1_document.set_style(12, len(self.document_success.text),
                                                              {'font_size': 32, 'color': (255, 255, 255, 255),
                                                               'font_name': 'Arial'})


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
                if all(self.checkpoints_reached):
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

                        if i == 0: #al primo checkpoint cambio messaggio mostrato
                            label_tutorial = (
                                f"ULTIMO PASSO:\n"  # Titolo grande
                                f"Continua così, spostandoti verso i pallini in blu che vedi!"
                            )
                            self.tutorial1_document.text = label_tutorial
                            self.tutorial1_document.set_style(0, 13,
                                                              {'font_size': 80, 'color': (0, 255, 255, 255), 'bold': True,
                                                               'align': 'center',
                                                               'font_name': 'Arial'})
                            self.tutorial1_document.set_style(13, len(self.document_success.text),
                                                              {'font_size': 32, 'color': (255, 255, 255, 255),
                                                               'font_name': 'Arial'})

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

            # time_level = self.difficulty_times[self.level_difficulty_chosen]
            # self.timer_remaining_label.text = f"Tempo rimanente: {time_level}"
        if symbol == key._2:
            self.level_difficulty_chosen = 'medio'
            self.label_warning.text = "Scelto il livello 2"

            # time_level = self.difficulty_times[self.level_difficulty_chosen]
            # self.timer_remaining_label.text = f"Tempo rimanente: {time_level}"
        if symbol == key._3:
            self.level_difficulty_chosen = 'difficile'
            self.label_warning.text = "Scelto il livello 3"

            # time_level = self.difficulty_times[self.level_difficulty_chosen]
            # print(time_level)
            # self.timer_remaining_label.text = f"Tempo rimanente: {time_level}"


        """Gestisce l'input da tastiera."""
        if symbol == key.R:  # Ripristina il livello con il tasto R
            #al reset facciamo riscegliere la difficoltà?
            self.text_layout_tutorial1.visible = True
            self.tutorial1_rectangle.visible = True

            self.pause_rectangle.visible = False
            self.text_layout_pause.visible = False

            self.reset_game()
            #self.start_game()

        if symbol == key.ENTER and not self.timer_running:
            #self.text_layout_tutorial1.visible = False
            #self.tutorial1_rectangle.visible = False


            self.label_instructions.visible = False
            self.label_level.visible = True
            #self.reset_game()
            self.reset_game()
            self.start_game()

            self.label_warning.text = "Avvio del tutorial"

        if symbol == key.P:
            if self.timer_running:
                #print("Hai tentato di mettere in pausa il gioco")
                self.timer_running = False
                self.pause_rectangle.visible = True
                self.text_layout_pause.visible = True

                self.success_rectangle.visible = False
                self.text_layout_success.visible = False

                self.tutorial1_rectangle.visible = False
                self.text_layout_tutorial1.visible = False


            else:
                #print("Hai tentato di continuare il gioco")

                #mettiamo un countdown di qualche secondo prima di far continuare
                self.timer_running = True
                self.pause_rectangle.visible = False
                self.text_layout_pause.visible = False

                self.success_rectangle.visible = False
                self.text_layout_success.visible = False

                self.tutorial1_rectangle.visible = True
                self.text_layout_tutorial1.visible = True



class LevelTutorialPath(Tutorial_FollowPath):
    def __init__(self, pipe_conn):
        x_ratio = screen_width / 640
        y_ratio = screen_height / 480

        # self.polygon_vertices = [
        #     (85, 100),  # Punto in basso a sinistra con padding
        #     (500, 100),  # Punto in basso alla fine della parte lunga della L
        #     (500, 200),  # Punto in alto della gambetta corta
        #     (150, 200),  # Angolo superiore destro della gambetta corta
        #     (150, 400),  # Angolo superiore destro dello schermo
        #     (85, 400),  # Angolo in alto a sinistra con padding
        # ]

        # #posizione iniziale del cerchio per questo livello
        # self.position_x = 120
        # self.position_y = 400

        checkpoints = [
            {'x': (210 - 105) * x_ratio, 'y': (200) * y_ratio, 'radius': 15},
            {'x': (420 - 105) * x_ratio, 'y': (200) * y_ratio, 'radius': 15},
            {'x': (630 - 105) * x_ratio, 'y': (200) * y_ratio, 'radius': 15}
        ]

        #
        # self.polygon_vertices = list(map(lambda v: (v[0] * x_ratio, v[1]* y_ratio),
        #                                  self.polygon_vertices))

        super().__init__(
            pipe_conn,
            polygon_points=[(0, 0), (0, height), (width, height), (width, 0)],
            circle_position_x=320,
            circle_position_y=90,  # posizione di default
            checkpoint_list=checkpoints,
            level_title=""
        )