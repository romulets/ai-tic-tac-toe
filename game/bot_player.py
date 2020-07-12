from operator import itemgetter
import pickle
import csv
import itertools
from random import shuffle

class BotPlayer():

    def __init__(self, model_dir, play_categories_dir, result_categories_dir):
        self.model = self.load_model(model_dir)
        self.play_categories = self.load_play_categories(play_categories_dir)
        self.result_categories = self.load_result_categories(result_categories_dir)

    def load_model(self, dir):
        with open(dir, "rb") as file:
            return pickle.load(file)

    def load_play_categories(self, dir):
        with open(dir, "r") as file:
            reader = csv.reader(file)
            return { int(cat[0]): cat[1] for cat in reader }
    
    def load_result_categories(self, dir):
        with open(dir, "r") as file:
            reader = csv.reader(file)
            return { cat[1]: int(cat[0]) for cat in reader }

    def play(self, game):
        return self.get_best_play(game)
        
    def get_best_play(self, game):
        possible_plays = self.get_possible_plays(game)
        probabilities = self.model.predict_proba(possible_plays)

        structured_plays = []
        for proba, play in zip(probabilities, possible_plays):
            structured_plays.append({
                "play": play[-1],
                "win": proba[self.result_categories["WINNER"]],
                "draw": proba[self.result_categories["DRAW"]],
                "loose": proba[self.result_categories["LOSER"]]
            })
        
        structured_plays = sorted(structured_plays, key=itemgetter('loose'), reverse=True)
        structured_plays = sorted(structured_plays, key=itemgetter('draw'))
        structured_plays = sorted(structured_plays, key=itemgetter('win'))

        best_play = list(structured_plays)[0]
        print(best_play)
        return self.convert_play(self.play_categories[best_play.get("play")])

    def get_possible_plays(self, game):
        plays = list(
            map(
                lambda play: play[0],
                filter(
                    lambda play_cat: game.is_valid_play(self.convert_play(play_cat[1])[0], self.convert_play(play_cat[1])[1]), 
                    map(
                        lambda play: (play, self.play_categories[play]),
                        range(9)
                    )
                )
            )
        )

        plays = [ flat_board(game) + [ play ] for play in plays]
        shuffle(plays)
        return plays

    def convert_play(self, play_str):
        return int(play_str[1]), int(play_str[2])


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