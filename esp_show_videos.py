# import pyglet
# from pyglet.shapes import Rectangle
# from pyglet.text import Label
# from pyglet.media import Player, Source, load
#
# class TutorialLevel(pyglet.window.Window):
#     def __init__(self):
#         super().__init__(800, 600, "Tutorial")
#
#         # Rettangoli
#         self.rectangles = [
#             Rectangle(50, 320, 300, 200, color=(200, 200, 200)),  # Primo rettangolo
#             Rectangle(450, 320, 300, 200, color=(200, 200, 200)),  # Secondo rettangolo
#             Rectangle(50, 50, 300, 200, color=(200, 200, 200)),    # Terzo rettangolo
#             Rectangle(450, 50, 300, 200, color=(200, 200, 200))    # Quarto rettangolo
#         ]
#
#         # Testi associati ai rettangoli
#         self.labels = [
#             Label("Fase 1 del tutorial:\nPosizionare una delle mani,\ntenendo un metro di distanza,\ndavanti alla fotocamera",
#                   x=200, y=420, anchor_x='center', anchor_y='center', color=(0, 0, 0, 255), width=280, multiline=True),
#             Label("Fase 2 del tutorial:\nApri il palmo per\nfar riconoscere la mano",
#                   x=600, y=420, anchor_x='center', anchor_y='center', color=(0, 0, 0, 255), width=280, multiline=True),
#             Label("Fase 3 del tutorial:\nRaggiungere la pallina rossa\ncon la mano aperta",
#                   x=200, y=150, anchor_x='center', anchor_y='center', color=(0, 0, 0, 255), width=280, multiline=True),
#             Label("Fase 4 del tutorial:\nMuovere la pallina rossa\nverso i pallini blu",
#                   x=600, y=150, anchor_x='center', anchor_y='center', color=(0, 0, 0, 255), width=280, multiline=True)
#         ]
#
#         # Caricamento dei video
#         self.players = []
#         video_files = ["videos/1a.mp4", "videos/2.mp4", "videos/3.mp4", "videos/4.mp4"]
#         self.video_positions = [(60, 330), (460, 330), (60, 60), (460, 60)]
#
#         for i, video_file in enumerate(video_files):
#             try:
#                 source = load(video_file)
#                 player = Player()
#                 player.queue(source)
#                 player.play()
#                 player.volume = 0  # Muta il video per non disturbare
#                 self.players.append((player, self.video_positions[i]))
#             except Exception as e:
#                 print(f"Errore nel caricamento del video {video_file}: {e}")
#
#     def on_draw(self):
#         self.clear()
#
#         # Disegna i rettangoli
#         for rect in self.rectangles:
#             rect.draw()
#
#         # Disegna i testi
#         for label in self.labels:
#             label.draw()
#
#         # Disegna i video
#         for player, position in self.players:
#             player.texture.blit(position[0], position[1])
#
# if __name__ == "__main__":
#     window = TutorialLevel()
#     pyglet.app.run()


# importing pyglet module
import pyglet

# width of window
width = 500

# height of window
height = 500

# caption i.e title of the window
title = "Geeksforgeeks"

# creating a window
window = pyglet.window.Window(width, height, title)

# video path
vidPath = "videos/1.gif"

# creating a media player object
player = pyglet.media.Player()

# creating a source object
source = pyglet.media.StreamingSource()

# load the media from the source
MediaLoad = pyglet.media.load(vidPath)

# add this media in the queue
player.queue(MediaLoad)

# play the video
player.play()


# on draw event
@window.event
def on_draw():
    # clear the window
    window.clear()

    # if player source exist
    # and video format exist
    if player.source and player.source.video_format:
        # get the texture of video and
        # make surface to display on the screen
        player.get_texture().blit(0, 0)


# key press event
@window.event
def on_key_press(symbol, modifier):
    # key "p" get press
    if symbol == pyglet.window.key.P:
        # pause the video
        player.pause()

        # printing message
        print("Video is paused")

    # key "r" get press
    if symbol == pyglet.window.key.R:
        # resume the video
        player.play()

        # printing message
        print("Video is resumed")


# run the pyglet application
pyglet.app.run()
