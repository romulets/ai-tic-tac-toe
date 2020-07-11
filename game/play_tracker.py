import csv
from bot_player import flat_board
from controller import PLAYER_A, PLAYER_B, DRAW

WINNER = "WINNER"
LOSER = "LOSER"

class PlayTracker():

    def __init__(self):
        self.playsA = []
        self.playsB = []

    def track(self, game, x,y):
        plays = self.playsA if game.current_player_A() else self.playsB

        plays.append(flat_board(game) + ["_" + str(x) + str(y)])

    def store(self, game, file_dir):
        plays = self.get_plays_summary(game)

        with open(file_dir, "a+") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(plays)
                

    def get_plays_summary(self, game):
        resultA, resultB = self.get_labels(game)
        playsA = map(lambda x: x + [ resultA  ], self.playsA)
        playsB = map(lambda x: x + [ resultB  ], self.playsA)
        return list(playsA) + list(playsB)

    def get_labels(self, game):
        result = game.get_result()
        if result == DRAW:
            return DRAW, DRAW
        elif result == PLAYER_A:
            return WINNER, LOSER
        else:
            return LOSER, WINNER