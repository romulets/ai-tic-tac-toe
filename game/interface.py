PLAYER_A = "X"
PLAYER_B = "O"

def draw_board(game):
    print()
    print(
        "\n-----------\n".join(
            map(
                lambda row:  " | ".join(map(get_piece, row)),
                game.board
            )
        )
    )

def draw_winner(game):
    draw_board(game)
    result = game.get_result()
    if result == "DRAW":
        print("DRAW")
    else:
        print("Winner is", result)

def get_piece(cell):
    if cell == "PLAYER_A": return PLAYER_A
    if cell == "PLAYER_B": return PLAYER_B
    return " "

def read_user_play(game):
    def read_play(game):
        x = int(input("X: "))
        y = int(input("Y: "))
        if not game.is_valid_play(x, y):
            print("Invalid.")
            x, y = read_play(game)
        return x, y

    print("Your turn")
    return read_play(game)

def print_bot_play(x, y):
    print("Bot plays", x, y)