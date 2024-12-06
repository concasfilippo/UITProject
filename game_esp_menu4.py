import pyglet
from pyglet.window import key
from multiprocessing import Pipe, Process
import time
import math

import game_levels
from  settings import *
import csv


# width = 640
# height = 480

# class SceneTemplate:
#     """A template with common features for all scenes."""
#     def __init__(self, text):
#         self.batch = pyglet.graphics.Batch()
#         self.label = pyglet.text.Label(
#             text,
#             font_name='Arial', font_size=32,
#             color=(200, 255, 255, 255), x=32, y=300,
#             batch=self.batch)
#
#     def update(self, dt):
#         """Update the scene state over time."""
#         pass
#
#     def handle_key(self, symbol, modifiers):
#         """Handle key presses specific to the scene."""
#         pass




# class MainMenuScene(SceneTemplate):
#     def __init__(self):
#         super().__init__(text='Main Menu')
#         self.label.text += "\nLoading..."





class Window(pyglet.window.Window):
    def __init__(self, pipe_conn):
        super().__init__(width=width, height=height)
        self.pipe_conn = pipe_conn
        self.states = [game_levels.Tutorial1(pipe_conn),
                       game_levels.Tutorial2(pipe_conn),
                       game_levels.Tutorial3_1(pipe_conn),
                       #game_levels.Tutorial4(pipe_conn),
                       #Level2(pipe_conn),
                       # Level3(pipe_conn),
                       #game_levels.Level4(pipe_conn),
                       #game_levels.Level5(pipe_conn),
                       #game_levels.Level6_FollowPath(pipe_conn),
                       game_levels.LevelFollowPath1(pipe_conn),
                       game_levels.LevelFollowPath2(pipe_conn),
                       game_levels.LevelFollowPath3(pipe_conn),
                       game_levels.FinalScene(pipe_conn)
                       ]
        self.current_state = 0
        self.set_visible()


        # Schedule updates for active scene
        pyglet.clock.schedule_interval(self.update, 1 / 60)

    def on_draw(self):
        self.clear()
        self.states[self.current_state].batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q:
            #print("Chiusura applicativo")
            self.close()
        # Switch to the next scene on SPACE
        if symbol == key.SPACE:
            self.current_state = (self.current_state + 1) % len(self.states)
            print(f"Switched to scene {self.current_state}")
        else:
            # Forward other keys to the active scene
            self.states[self.current_state].handle_key(symbol, modifiers)

    def update(self, dt):
        """Update the current scene."""
        self.states[self.current_state].update(dt)


def main(pipe_conn):
    window = Window(pipe_conn)
    #window.set_fullscreen(True)
    pyglet.app.run()
    pass
