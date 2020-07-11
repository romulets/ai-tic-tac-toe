import pickle
import csv
import itertools

class BotPlayer():

    def __init__(self, model_dir, categories_dir):
        self.model = self.load_model(model_dir)
        self.categories = self.load_categories(categories_dir)

    def load_model(self, dir):
        with open(dir, "rb") as file:
            return pickle.load(file)

    def load_categories(self, dir):
        with open(dir, "r") as file:
            reader = csv.reader(file)
            return { int(cat[0]): cat[1] for cat in reader }

    def play(self, game):
        x, y = self.predict_next_play(game)
        if game.is_valid_play(x, y):
            print("Predicted play")
            return x, y

        for x, y in itertools.product(range(3), range(3)):
            if game.is_valid_play(x, y):
                print("Sequence play")
                return x, y
                
        

    def predict_next_play(self, game):
        prediction = self.model.predict([flat_board(game)])[0]
        play = self.categories.get(prediction)
        assert not play is None, "Play should not be null"
        return int(play[1]), int(play[2])


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