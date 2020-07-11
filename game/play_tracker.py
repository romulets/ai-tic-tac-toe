import csv
from controller import PLAYER_A, PLAYER_B, DRAW

CSV_FILE = "resources/plays.csv"
WINNER = "WINNER"
LOSER = "LOSER"

def flat_board(game):
    isFull = lambda x, y: 0 if game.board[x][y] is None else 1
    return [
            isFull(0,0),
            isFull(0,1),
            isFull(0,2),
            isFull(1,0),
            isFull(1,1),
            isFull(1,2),
            isFull(2,0),
            isFull(2,1),
            isFull(2,2),
    ]

class PlayTracker():

    def __init__(self):
        self.playsA = []
        self.playsB = []

    def track(self, game, x,y):
        plays = self.playsA if game.current_player_A() else self.playsB

        plays.append(flat_board(game) + ["_" + str(x) + str(y)])

    def store(self, game):
        plays = self.get_plays_summary(game)

        with open(CSV_FILE, "a+") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            for play in plays:
                writer.writerow(play)

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