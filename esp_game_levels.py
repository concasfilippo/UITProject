










class Level2(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='Level 2')
        self.pipe_conn = pipe_conn
        self.circle = pyglet.shapes.Circle(320, 240, 20, color=(255, 0, 0), batch=self.batch)
        self.label.text += "\nControl the red circle with external inputs!"

        # Timer setup
        self.time_elapsed = 0.0  # Timer starts at 0 seconds
        self.timer_label = pyglet.text.Label(
            "Time: 0.0", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 20, batch=self.batch)
        self.timer_running = True  # Timer starts running

    def update(self, dt):
        """Update the scene state."""
        # Update the timer if it's running
        if self.timer_running:
            self.time_elapsed += dt
            self.timer_label.text = f"Time: {self.time_elapsed:.1f}"  # Update label

        # Update the circle position from pipe data
        if self.pipe_conn.poll():
            informazioni = self.pipe_conn.recv()
            if informazioni['gesture'] != -1:
                self.circle.x = informazioni['landmarks'][8][0]
                self.circle.y = height - informazioni['landmarks'][8][1]

    def handle_key(self, symbol, modifiers):
        """Handle key presses."""
        if symbol == key.T:  # Press 'T' to toggle the timer
            self.timer_running = not self.timer_running



class Level3(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='Level 3')
        self.pipe_conn = pipe_conn


        # Rettangolo
        self.rect_width = int(width * 0.8)
        self.rect_height = 50
        self.rect_x = (width - self.rect_width) // 2
        self.rect_y = (height - self.rect_height) // 2
        self.rectangle = pyglet.shapes.Rectangle(
            self.rect_x, self.rect_y, self.rect_width, self.rect_height,
            color=(200, 200, 200), batch=self.batch)

        # Pallino rosso
        self.circle = pyglet.shapes.Circle(
            self.rect_x, self.rect_y + self.rect_height // 2, 10,
            color=(255, 0, 0), batch=self.batch)

        # Timer e stato
        self.timer_running = False
        self.time_elapsed = 0.0
        self.timer_label = pyglet.text.Label(
            "Time: 0.0", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 20, batch=self.batch)

        # Accumulate area
        self.path = []  # Lista di coordinate tracciate dal pallino
        self.accuracy_label = pyglet.text.Label(
            "", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 40, batch=self.batch)

    def start_game(self):
        """Avvia il timer e consente il movimento del pallino."""
        self.timer_running = True
        self.time_elapsed = 0.0
        self.path = []  # Resetta il percorso del pallino

    def stop_game(self):
        """Ferma il gioco e calcola l'accuratezza."""
        self.timer_running = False

        # Calcola l'accuratezza
        if len(self.path) > 1:
            x_coords, y_coords = zip(*self.path)
            # Retta iniziale-finale
            x_start, y_start = self.path[0]
            x_end, y_end = self.path[-1]
            line_y = np.interp(x_coords, [x_start, x_end], [y_start, y_end])
            area_path = np.trapz(y_coords, x_coords)
            area_line = np.trapz(line_y, x_coords)
            area_diff = abs(area_path - area_line)
            rect_area = self.rect_width * self.rect_height
            accuracy = 1 - min(area_diff / rect_area, 1)
            self.accuracy_label.text = f"Accuracy: {accuracy:.2%}"

    def reset_game(self):
        """Ripristina lo stato iniziale del livello."""
        self.timer_running = False
        self.time_elapsed = 0.0
        self.timer_label.text = "Time: 0.0"
        self.circle.x = self.rect_x
        self.circle.y = self.rect_y + self.rect_height // 2
        self.path = []
        self.accuracy_label.text = ""

    def update(self, dt):
        """Aggiorna la posizione del pallino e il timer."""
        if self.timer_running:
            self.time_elapsed += dt
            self.timer_label.text = f"Time: {self.time_elapsed:.1f}"

            # Riceve dati dal pipe e aggiorna la posizione
            if self.pipe_conn.poll():
                informazioni = self.pipe_conn.recv()
                if informazioni['gesture'] != -1:
                    x = informazioni['landmarks'][8][0]
                    y = height - informazioni['landmarks'][8][1]
                    new_x = max(self.rect_x, min(self.rect_x + self.rect_width, x))
                    new_y = max(self.rect_y, min(self.rect_y + self.rect_height, y))
                    self.circle.x = new_x
                    self.circle.y = new_y
                    self.path.append((new_x, new_y))


                    # Ferma il gioco se il pallino raggiunge il lato destro
                    if new_x >= self.rect_x + self.rect_width:
                        self.stop_game()

    def reset(self):
        """Reset the level to its initial state."""
        self.circle.x, self.circle.y = self.initial_circle_position
        self.checkpoints_reached = [False] * len(self.checkpoints)
        self.start_time = None
        self.timer_running = False
        print("Level reset!")

    def handle_key(self, symbol, modifiers):
        """Gestisce l'input da tastiera."""
        if symbol == key.P and not self.timer_running:
            self.start_game()
        elif symbol == key.R:  # Ripristina il livello con il tasto R
            self.reset_game()





class Level4(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='Level 4')
        self.pipe_conn = pipe_conn
        self.initial_circle_position = (100, 384)
        self.circle = pyglet.shapes.Circle(
            *self.initial_circle_position, 20, color=(255, 0, 0), batch=self.batch)
        self.checkpoints = [
            {'x': 200, 'y': 200, 'radius': 15},
            {'x': 400, 'y': 300, 'radius': 15},
            {'x': 600, 'y': 400, 'radius': 15}
        ]
        self.checkpoints_reached = [False, False, False]
        self.checkpoint_shapes = []
        for checkpoint in self.checkpoints:
            checkpoint_shape = pyglet.shapes.Circle(
                checkpoint['x'], checkpoint['y'], checkpoint['radius'], color=(0, 255, 0), batch=self.batch)
            self.checkpoint_shapes.append(checkpoint_shape)
        self.start_time = None
        self.reset()


    def update(self, dt):
        if self.pipe_conn and self.pipe_conn.poll():
            informazioni = self.pipe_conn.recv()
            if informazioni['gesture'] != -1:
                self.circle.x = informazioni['landmarks'][8][0]
                self.circle.y = height - informazioni['landmarks'][8][1]

        self.check_for_checkpoints()

        if self.circle.x >= width - self.circle.radius:
            self.stop_timer()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True

    def stop_timer(self):
        if self.timer_running:
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            self.timer_running = False
            self.calculate_accuracy()

    def calculate_accuracy(self):
        total_checkpoints = len(self.checkpoints)
        reached_checkpoints = sum(self.checkpoints_reached)
        accuracy = (reached_checkpoints / total_checkpoints) * 100
        print(f"Accuracy: {accuracy}%")

    def check_for_checkpoints(self):
        for i, checkpoint in enumerate(self.checkpoints):
            if not self.checkpoints_reached[i]:
                distance = math.sqrt((self.circle.x - checkpoint['x']) ** 2 + (self.circle.y - checkpoint['y']) ** 2)
                if distance < checkpoint['radius']:
                    self.checkpoints_reached[i] = True
                    print(f"Checkpoint {i+1} reached!")

    def reset(self):
        """Reset the level to its initial state."""
        self.circle.x, self.circle.y = self.initial_circle_position
        self.checkpoints_reached = [False] * len(self.checkpoints)
        self.start_time = None
        self.timer_running = False
        print("Level reset!")

    def handle_key(self, symbol, modifiers):
        """Gestisce l'input da tastiera."""
        if symbol == key.P and not self.timer_running:
            self.start_timer()
        elif symbol == key.R:  # Ripristina il livello con il tasto R
            self.reset()


class Level5(SceneTemplate):
    def __init__(self, pipe_conn):
        super().__init__(text='Level 5')

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



        # Rettangolo
        self.rect_width = int(width * 0.8)
        self.rect_height = 50
        self.rect_x = (width - self.rect_width) // 2
        self.rect_y = (height - self.rect_height) // 2
        self.rectangle = pyglet.shapes.Rectangle(
            self.rect_x, self.rect_y, self.rect_width, self.rect_height,
            color=(200, 200, 200), batch=self.batch, group=self.fg_group)
        self.rectangle.opacity = 90

        # Pallino rosso
        self.circle = pyglet.shapes.Circle(
            self.rect_x, self.rect_y + self.rect_height // 2, 10,
            color=(255, 0, 0), batch=self.batch, group=self.fg_group)

        # Timer e stato
        self.timer_running = False
        self.time_elapsed = 0.0
        self.timer_label = pyglet.text.Label(
            "Time: 0.0", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 20, batch=self.batch, group=self.fg_group)

        # Accumulate area
        self.path = []  # Lista di coordinate tracciate dal pallino
        self.accuracy_label = pyglet.text.Label(
            "", font_name="Arial", font_size=16,
            color=(255, 255, 255, 255), x=10, y=height - 40, batch=self.batch, group=self.fg_group)

        #checkpoint logic
        self.checkpoints = [
            {'y': 240 * self.y_ratio, 'x': 200 * self.x_ratio, 'radius': 15},
            {'y': 240 * self.y_ratio, 'x': 300 * self.x_ratio, 'radius': 15},
            {'y': 240 * self.y_ratio, 'x': 400 * self.x_ratio, 'radius': 15}
        ]
        self.checkpoints_reached = [False, False, False]
        self.checkpoint_shapes = []
        for checkpoint in self.checkpoints:
            checkpoint_shape = pyglet.shapes.Circle(
                checkpoint['x'], checkpoint['y'], checkpoint['radius'],
                color=(0, 255, 0), batch=self.batch, group=self.fg_group)
            self.checkpoint_shapes.append(checkpoint_shape)



    def start_game(self):
        """Avvia il timer e consente il movimento del pallino."""
        self.timer_running = True
        self.time_elapsed = 0.0
        self.path = []  # Resetta il percorso del pallino

    def stop_game(self):
        """Ferma il gioco e calcola l'accuratezza."""
        self.timer_running = False

        # Calcola l'accuratezza
        if len(self.path) > 1:
            x_coords, y_coords = zip(*self.path)
            # Retta iniziale-finale
            x_start, y_start = self.path[0]
            x_end, y_end = self.path[-1]
            line_y = np.interp(x_coords, [x_start, x_end], [y_start, y_end])
            area_path = np.trapz(y_coords, x_coords)
            area_line = np.trapz(line_y, x_coords)
            area_diff = abs(area_path - area_line)
            rect_area = self.rect_width * self.rect_height
            accuracy = 1 - min(area_diff / rect_area, 1)

            if all(self.checkpoints_reached):
                self.accuracy_label.text = f"Accuracy: {accuracy:.2%}"
            else:
                self.accuracy_label.text = f"Accuracy: {0.0:.2%} - Hai dimenticato dei checkpoint"

    def reset_game(self):
        """Ripristina lo stato iniziale del livello."""
        self.timer_running = False
        self.time_elapsed = 0.0
        self.timer_label.text = "Cronometro: 0.0"
        self.circle.x = self.rect_x
        self.circle.y = self.rect_y + self.rect_height // 2
        self.path = []
        self.accuracy_label.text = ""
        #forse è meglio richicamare init... o fare una funzione di initialize...

        for cp in range(0, len(self.checkpoint_shapes)):
            self.checkpoint_shapes[cp].color = (0, 255, 0)
        self.checkpoints_reached = [False, False, False]

    def update(self, dt):
        """Aggiorna la posizione del pallino e il timer."""
        if self.timer_running:
            self.time_elapsed += dt
            self.timer_label.text = f"Cronometro: {self.time_elapsed:.1f}"


            # Riceve dati dal pipe e aggiorna la posizione
            if self.pipe_conn.poll():
                informazioni = self.pipe_conn.recv()

                #updating ratios of re-drawing
                self.x_ratio = width / informazioni["cam_width"]
                self.y_ratio = height / informazioni["cam_height"]

                #Display camera
                global sprites
                new_image = pyglet.image.ImageData(640, 480, 'RGB', informazioni["image"].tobytes(), pitch=-640 * 3)
                texture = new_image.get_texture()
                new_sprite = pyglet.sprite.Sprite(texture, x=0, y=0,
                                                  batch=self.batch,
                                                  group=self.bg_group)
                new_sprite.scale_x = self.x_ratio
                new_sprite.scale_y = self.y_ratio
                sprites = [new_sprite]  # Add the new sprite to the list

                self.disp_hand_gesture.text = (f"Gesto rilevato: " 
                                               f"{self.keypoint_classifier_labels[informazioni['gesture']]}"
                                               f" ({informazioni['gesture']})")

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

                        #self.circle.position = centroid
                        x = centroid[0]
                        y = centroid[1]

                        #x = informazioni['landmarks'][8][0] * self.x_ratio
                        #y = height - (informazioni['landmarks'][8][1] * self.y_ratio)

                        #i valori sono boundati al rettangolo in questo caso
                        new_x = max(self.rect_x, min(self.rect_x + self.rect_width, x))
                        new_y = max(self.rect_y, min(self.rect_y + self.rect_height, y))

                        self.circle.x = x #new_x
                        self.circle.y = y #new_y
                        self.path.append((new_x, new_y))

                        self.check_for_checkpoints() #check if a checkpoint is crossed

                        # Ferma il gioco se il pallino raggiunge il lato destro (e non è rimasto li dalla iterazione rpecedente)
                        if new_x >= self.rect_x + self.rect_width and self.time_elapsed > 1.0:
                            self.stop_game()

                self.batch.draw()

    def check_for_checkpoints(self):
        for i, checkpoint in enumerate(self.checkpoints):
            if not self.checkpoints_reached[i]:
                distance = math.sqrt((self.circle.x - checkpoint['x']) ** 2 + (self.circle.y - checkpoint['y']) ** 2)
                if distance < checkpoint['radius']:
                    self.checkpoints_reached[i] = True
                    self.checkpoint_shapes[i].color = (0, 0, 255)
                    print(f"Checkpoint {i+1} reached!")

    def handle_key(self, symbol, modifiers):
        """Gestisce l'input da tastiera."""
        if symbol == key.P and not self.timer_running:
            self.start_game()
        elif symbol == key.R:  # Ripristina il livello con il tasto R
            self.reset_game()

