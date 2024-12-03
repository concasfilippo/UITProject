import pyglet

from pyglet import shapes
from pyglet.graphics import allocation
from pyglet.window import mouse
from pyglet.window import key
from pyglet import image

import numpy as np
from pyglet.graphics import Group

width = 640
height = 480


#funzione per i controllo dell'area della palla
# Checking if a point is inside a polygon
def raycasting(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    # Loop through each edge of the polygon
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # next vertex

        # Check if the edge intersects the ray from the point
        if min(y1, y2) < y <= max(y1, y2) and x <= max(x1, x2):
            if y1 != y2:  # Avoid division by zero
                x_intersection = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x1 == x2 or x <= x_intersection:
                inside = not inside

    return inside


def calculate_centroid(polygon):
    n = len(polygon)
    A = 0  # Area
    C_x = 0  # Coordinata x del baricentro
    C_y = 0  # Coordinata y del baricentro

    for i in range(n):
        x_i, y_i = polygon[i]
        x_next, y_next = polygon[(i + 1) % n]  # Il prossimo punto (ciclico)

        # Calcolo dell'area
        area_component = (x_i * y_next - x_next * y_i)
        A += area_component

        # Calcolo delle coordinate del baricentro
        C_x += (x_i + x_next) * area_component
        C_y += (y_i + y_next) * area_component

    A *= 0.5  # Area finale
    C_x /= (6 * A)  # Coordinata x del baricentro
    C_y /= (6 * A)  # Coordinata y del baricentro

    return (C_x, C_y), A




def main(pipe_conn):
    window= pyglet.window.Window(width=width, height=height)
    #window.set_location(80, 60)
    batch = pyglet.graphics.Batch() #list in which put every object to be draw

    # Creazione di gruppi per impostare i layer di priorità
    bg_group = Group(order=0)
    fg_group = Group(order=1)

    #Oggetto da far muovere
    circle = shapes.Circle(x=400, y=150, radius=30, color=(255, 10, 10), batch=batch, group=fg_group)

    def update(dt):
        window.clear()
        if pipe_conn.poll():
            informazioni = pipe_conn.recv()  # Receiving the hand-tracking data
            global sprites
            window.clear()  # Pulisce la finestra
            #print(informazioni)


            #Per il background, prendo l'informazione, la conservo in uno sprite e va nel batch per essere disgenato
            new_image = pyglet.image.ImageData(width, height, 'RGB', informazioni["image"].tobytes(), pitch=-width * 3)
            new_sprite = pyglet.sprite.Sprite(new_image, x=0, y=0, batch=batch, group=bg_group)
            sprites = [new_sprite]  # Aggiungi il nuovo sprite al batch

            #Per il disegno del pallino rosso, se viene grabbato
            if informazioni["gesture"] == 3 or informazioni["gesture"] == 1:
            #if informazioni[2] == 3 or informazioni[2] == 1: #Now grabbing
                #we have to track the following landmarks: 0,4,8,12,16,20
                landmark0 = tuple(informazioni["landmarks"][0])
                landmark4 = tuple(informazioni["landmarks"][4])
                landmark8 = tuple(informazioni["landmarks"][8])
                landmark12 = tuple(informazioni["landmarks"][12])
                landmark16 = tuple(informazioni["landmarks"][16])
                landmark20 = tuple(informazioni["landmarks"][20])
                polygon = [landmark0, landmark4, landmark8, landmark12, landmark16, landmark20]
                polygon = list(map(lambda x: (x[0], -x[1] + height), polygon))
                #print(polygon)
                point = circle.position
                #print(point)
                inside = raycasting(point, polygon)
                #print("Inside" if inside else "Outside")  # This will print 'Inside'
                centroid, area = calculate_centroid(polygon)
                if inside:
                    circle.position = centroid


                #hand_data = informazioni[0][8]
                #x, y = hand_data
                #circle.position = (x,-y+height)


            batch.draw()


    pyglet.clock.schedule_interval(update, 1/60.0)

    @window.event
    def on_draw():
        window.clear()
        batch.draw()


    pyglet.app.run()
