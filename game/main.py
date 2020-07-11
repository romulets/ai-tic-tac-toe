from controller import GameController
from play_tracker import PlayTracker
import interface as ui

def start_game():
    game = GameController()
    tracker = PlayTracker()

    while game.is_playing():
        ui.draw_board(game)
        x, y = ui.read_play(game)
        tracker.track(game, x, y)
        game.play(x, y)
        
    ui.draw_winner(game)
    tracker.store(game)

if __name__ == "__main__":
    start_game()
