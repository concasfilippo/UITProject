import multiprocessing
import game

def start_hand_tracking(pipe_conn): # Importing hand-tracking script
    import hand_tracking
    hand_tracking.main_hand_tracking(pipe_conn)


if __name__ == '__main__':
    parent_conn, child_conn = multiprocessing.Pipe()

    # Start hand-tracking process
    hand_tracking_process = multiprocessing.Process(target=start_hand_tracking, args=(child_conn,))
    hand_tracking_process.start()

    # Start the game process (e.g., pyglet game)
    game.main(parent_conn)  # the game reads from the pipe and updates label

    # Wait for both processes to finish
    hand_tracking_process.join()
