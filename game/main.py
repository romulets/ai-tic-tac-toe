from controller import GameController
from play_tracker import PlayTracker
from bot_trainer import train_model
from bot_player import BotPlayer
import interface as ui

PLAYS_FILE = "resources/plays.csv"
MODEL_FILE = "resources/model.pckl"
PLAYS_CATEGORIES_FILE = "resources/plays_categories.csv"
RESULT_CATEGORIES_FILE = "resources/result_categories.csv"

def play_game():
    game = GameController()
    tracker = PlayTracker()
    bot = BotPlayer(MODEL_FILE, PLAYS_CATEGORIES_FILE, RESULT_CATEGORIES_FILE)

    while game.is_playing():
        ui.draw_board(game)
        
        x, y = -1, -1
        if game.current_player_A():
            x, y = ui.read_user_play(game)
        else:
            x, y = bot.play(game)
            ui.print_bot_play(x, y)

        tracker.track(game, x, y)
        game.play(x, y)
        
    ui.draw_winner(game)
    tracker.store(game, PLAYS_FILE)
    train_model(PLAYS_FILE, MODEL_FILE, PLAYS_CATEGORIES_FILE, RESULT_CATEGORIES_FILE)

if __name__ == "__main__":
    # train_model(PLAYS_FILE, MODEL_FILE, PLAYS_CATEGORIES_FILE, RESULT_CATEGORIES_FILE)
    play_game()
    
