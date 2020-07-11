from controller import GameController
from play_tracker import PlayTracker
from bot_trainer import train_model
import interface as ui

PLAYS_FILE = "resources/plays.csv"
MODEL_FILE = "resources/model.pckl"
CATEGORIES_FILE = "resources/categories.csv"

def play_game():
    game = GameController()
    tracker = PlayTracker()

    while game.is_playing():
        ui.draw_board(game)
        x, y = ui.read_play(game)
        tracker.track(game, x, y)
        game.play(x, y)
        
    ui.draw_winner(game)
    tracker.store(game, PLAYS_FILE)
    train_model(PLAYS_FILE, MODEL_FILE, CATEGORIES_FILE)

if __name__ == "__main__":
    play_game()
