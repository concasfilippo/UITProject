import multiprocessing
#import game
import game_esp_menu4 as game
import tensorflow as tf


def start_hand_tracking(pipe_conn): # Importing hand-tracking script
    import hand_tracking as handtracking
    handtracking.main_hand_tracking(pipe_conn)


if __name__ == '__main__':
    #print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    parent_conn, child_conn = multiprocessing.Pipe()

    # Start hand-tracking process
    hand_tracking_process = multiprocessing.Process(target=start_hand_tracking, args=(child_conn,))
    hand_tracking_process.start()

    # Start the game process (e.g., pyglet game)
    game.main(parent_conn)  # the game reads from the pipe and updates label


    hand_tracking_process.kill()
    # Wait for both processes to finish
    # hand_tracking_process.join()
