PLAYER_A = "PLAYER_A"
PLAYER_B = "PLAYER_B"
DRAW = "DRAW"

class GameController():

    def __init__(self):
        self.current_player = PLAYER_A
        self.board = [[None for x in range(3)] for x in range(3)]

    def current_player_A(self):
        return self.current_player == PLAYER_A

    def is_playing(self):
        return self.get_result() == None

    def is_valid_play(self, x, y):
        if not 0 <= x <= 2: return False
        if not 0 <= y <= 2: return False
        if not self.is_playing(): return False
        if not self.board[x][y] is None: return False
        return True

    def play(self, x, y):
        if not self.is_valid_play(x, y): return
        self.board[x][y] = self.current_player
        self.swap_players()

    def swap_players(self):
        self.current_player = PLAYER_B if self.current_player_A() else PLAYER_A

    def get_result(self):
        pos = lambda x,y: self.board[x][y]
        horizontal_winner = lambda x: not pos(x, 0) is None and pos(x, 0) == pos(x, 1) == pos(x, 2)
        vertical_winner = lambda y: not pos(0, y) is None and pos(0, y) == pos(1, y) == pos(2, y)

        if horizontal_winner(0):
            return pos(0, 0)
        elif horizontal_winner(1):
            return pos(1, 0)
        elif horizontal_winner(2):
            return pos(2, 0)
        elif vertical_winner(0):
            return pos(0, 0)
        elif vertical_winner(1):
            return pos(0, 1)
        elif vertical_winner(2):
            return pos(0, 2)
        elif not pos(0, 0) is None and pos(0, 0) == pos(1, 1) == pos(2, 2):
            return pos(0, 0)
        elif not pos(0, 2) is None and pos(0, 2) == pos(1, 1) == pos(2, 0):
            return pos(0, 2)

        if all(map(lambda x: all((map(lambda y: not y is None, x))), self.board)):
            return DRAW
        
        return None

if __name__ == "__main__":
    game = GameController()
    game.board[0] = [PLAYER_A for x in range(3)] 
    assert game.get_result() == PLAYER_A, "Should be Player A"
    assert not game.is_playing()

    game = GameController()
    game.board[1] = [PLAYER_B for x in range(3)] 
    assert game.get_result() == PLAYER_B, "Should be Player B"
    assert not game.is_playing()

    game = GameController()
    game.board[2] = [PLAYER_B for x in range(3)] 
    assert game.get_result() == PLAYER_B, "Should be Player B"
    assert not game.is_playing()

    game = GameController()
    for x in range(3): game.board[x][0] = PLAYER_A
    assert game.get_result() == PLAYER_A, "Should be Player A"
    assert not game.is_playing()

    game = GameController()
    for x in range(3): game.board[x][1] = PLAYER_A
    assert game.get_result() == PLAYER_A, "Should be Player A"
    assert not game.is_playing()

    game = GameController()
    for x in range(3): game.board[x][2] = PLAYER_B
    assert game.get_result() == PLAYER_B, "Should be Player B"
    assert not game.is_playing()

    game = GameController()
    game.board[0][0] = PLAYER_A
    game.board[1][1] = PLAYER_A
    game.board[2][2] = PLAYER_A
    assert game.get_result() == PLAYER_A, "Should be Player A"
    assert not game.is_playing()

    game = GameController()
    game.board[0][2] = PLAYER_B
    game.board[1][1] = PLAYER_B
    game.board[2][0] = PLAYER_B
    assert game.get_result() == PLAYER_B, "Should be Player B"
    assert not game.is_playing()

    game = GameController()
    game.board[0][2] = PLAYER_A
    game.board[1][1] = PLAYER_B
    game.board[2][0] = PLAYER_B
    assert game.get_result() is None, "Should be None"
    assert game.is_playing()

    game = GameController()
    for x in range(3):
        game.play(x, 1)
        for y in range(3):
            game.play(x, y)
    assert game.get_result() is DRAW, "Should be Draw"
    assert not game.is_playing()

    assert not game.is_valid_play(0, 3)
    assert not game.is_valid_play(3, 0)
    assert not game.is_valid_play(-1, 0)