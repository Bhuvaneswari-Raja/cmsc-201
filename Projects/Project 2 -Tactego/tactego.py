"""
File:    tactego.py
Author:  Pooja Rajamanikandan
Date:    11/13/2023
Section: 54
E-mail:  le64534@umbc.edu
Description: This program will implement a game of simplified version of the game Stratego
"""
import random

def create_board(length, width):
    """
    Creates an empty game board with the specified dimensions.

    Parameters:
    - length (int): The number of rows.
    - width (int): The number of columns.

    Returns:
    - list: The empty game board.
    """
    return [[' ' for _ in range(width)] for _ in range(length)]

def load_pieces(file_name):
    """
    Loads pieces from a file and shuffles them.

    Parameters:
    - file_name (str): The name of the file containing piece information.

    Returns:
    - list: The list of shuffled pieces.
    """
    pieces = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip().split()
            if line[0] == 'F':
                pieces.extend(['F'] * int(line[1]))
            elif line[0] == 'M':
                pieces.extend(['M'] * int(line[1]))
            elif line[0] == 'S':
                pieces.extend(['S'] * int(line[1]))
            elif line[0] == 'A':
                pieces.extend(['A'] * int(line[1]))
            else:
                pieces.extend([int(line[0])] * int(line[1]))
    random.shuffle(pieces)
    return pieces

def place_pieces(board, pieces, player, length, width):
    """
    Places pieces on the board for a specific player.

    Parameters:
    - board (list): The game board.
    - pieces (list): The list of pieces.
    - player (str): The player ('red' or 'blue').
    - length (int): The number of rows.
    - width (int): The number of columns.

    Returns:
    - None
    """
    piece_index = 0
    if player == 'red':
        for i in range(length):
            for j in range(width):
                if pieces[piece_index] == 'F':
                    board[i][j] = 'RF' if player == 'red' else 'BF'
                else:
                    board[i][j] = f'{player[0].upper()}{pieces[piece_index]}'
                piece_index += 1
    else:
        for i in range(length - 1, -1, -1):
            for j in range(width):
                if pieces[piece_index] == 'F':
                    board[i][j] = 'RF' if player == 'red' else 'BF'
                else:
                    board[i][j] = f'{player[0].upper()}{pieces[piece_index]}'
                piece_index += 1

def draw_board(board):
    """
    Displays the current state of the game board.

    Parameters:
    - board (list): The game board.

    Returns:
    - None
    """
    print('\t' + '\t'.join(map(str, range(len(board[0])))))
    for i, row in enumerate(board):
        print(f'{i}\t' + '\t'.join(map(str, row)))

def valid_position(board, player, row, col):
    """
    Checks if a position on the board is valid for the specified player.

    Parameters:
    - board (list): The game board.
    - player (str): The player ('red' or 'blue').
    - row (int): The row index.
    - col (int): The column index.

    Returns:
    - bool: True if the position is valid, False otherwise.
    """
    return 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col][0] == player[0].upper()

def valid_move(board, player, start_row, start_col, end_row, end_col):
    """
    Checks if a move is valid for the specified player.

    Parameters:
    - board (list): The game board.
    - player (str): The player ('red' or 'blue').
    - start_row (int): The starting row index.
    - start_col (int): The starting column index.
    - end_row (int): The ending row index.
    - end_col (int): The ending column index.

    Returns:
    - bool: True if the move is valid, False otherwise.
    """
    if not valid_position(board, player, start_row, start_col):
        return False
    piece = board[start_row][start_col]
    distance = abs(end_row - start_row) + abs(end_col - start_col)
    return distance == 1 and valid_position(board, player, end_row, end_col) and piece[1:] != 'F'

def combat(attacker, defender):
    """
    Determines the outcome of combat between an attacker and a defender.

    Parameters:
    - attacker (str): The piece of the attacking player.
    - defender (str): The piece of the defending player.

    Returns:
    - str: 'attacker' if the attacker wins, 'defender' if the defender wins.
    """
    if defender[1:] == 'A':
        return 'attacker'  # Attacker wins against Assassin
    elif attacker[1:] == 'A':
        return 'defender'  # Defender wins against Assassin
    elif defender[1:] == 'S':
        return 'defender'  # Defender wins against Sapper
    elif attacker[1:] == 'S':
        return 'attacker'  # Attacker wins against Sapper
    elif defender[1:] == 'M':
        return 'attacker'  # Attacker wins against Mine
    elif attacker[1:] == 'M':
        return 'defender'  # Defender wins against Mine
    else:
        return 'attacker' if int(attacker[1:]) > int(defender[1:]) else 'defender'

def remove_piece(board, row, col):
    """
    Removes a piece from the specified position on the board.

    Parameters:
    - board (list): The game board.
    - row (int): The row index.
    - col (int): The column index.

    Returns:
    - None
    """
    board[row][col] = ' '

def check_victory(board):
    """
    Checks for a victory condition in the game.

    Parameters:
    - board (list): The game board.

    Returns:
    - bool: True if a player has won, False otherwise.
    """
    red_flags = sum(row.count('RF') for row in board)
    blue_flags = sum(row.count('BF') for row in board)
    return red_flags == 0 or blue_flags == 0

def tactego(pieces_file, length, width):
    """
    Main function to run the tactego game.

    Parameters:
    - pieces_file (str): The name of the file containing piece information.
    - length (int): The number of rows.
    - width (int): The number of columns.

    Returns:
    - None
    """
    # Load pieces for both players
    red_pieces = load_pieces(pieces_file)
    blue_pieces = load_pieces(pieces_file)

    # Create and initialize game boards
    red_board = create_board(length, width)
    blue_board = create_board(length, width)

    # Place pieces on the boards for both players
    place_pieces(red_board, red_pieces, 'red', length, width)
    place_pieces(blue_board, blue_pieces, 'blue', length, width)

    # Initialize current player
    current_player = 'red'

    while True:
        # Display the current state of the board
        draw_board(red_board if current_player == 'red' else blue_board)

        # Get starting position from the current player
        while True:
            try:
                start_position = input(f"Select Piece to Move by Position for {current_player} >> ").split()
                start_row, start_col = map(int, start_position)

                if valid_position(red_board if current_player == 'red' else blue_board, current_player, start_row, start_col):
                    break
                else:
                    print("Invalid starting position. Try again.")
            except ValueError:
                print("Invalid input. Enter integers for row and column.")

        # Get ending position for the move
        while True:
            try:
                end_position = input(f"Select Position to move Piece >> ").split()
                end_row, end_col = map(int, end_position)

                if valid_move(red_board if current_player == 'red' else blue_board, current_player, start_row, start_col, end_row, end_col):
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter integers for row and column.")

        # Get the pieces at the starting and ending positions
        start_piece = red_board[start_row][start_col] if current_player == 'red' else blue_board[start_row][start_col]
        end_piece = red_board[end_row][end_col] if current_player == 'red' else blue_board[end_row][end_col]

        # Determine the outcome of combat
        outcome = combat(start_piece, end_piece)

        # Update the boards based on combat outcome
        if outcome == 'attacker':
            remove_piece(red_board, start_row, start_col) if current_player == 'red' else remove_piece(blue_board, start_row, start_col)
            blue_board[end_row][end_col] = start_piece if current_player == 'red' else blue_board[end_row][end_col]
        else:
            remove_piece(blue_board, end_row, end_col) if current_player == 'red' else remove_piece(red_board, end_row, end_col)
            red_board[start_row][start_col] = end_piece if current_player == 'red' else red_board[start_row][start_col]

        # Check for victory conditions
        if check_victory(red_board) or check_victory(blue_board):
            winner = 'Red' if check_victory(blue_board) else 'Blue'
            print(f"\nGame Over! {winner} player wins!")
            break

        # Switch to the other player's turn
        current_player = 'blue' if current_player == 'red' else 'red'

if __name__ == '__main__':
    random.seed(input('What is seed? '))
    file_name = input('What is the filename for the pieces? ')
    length = int(input('What is the length? '))
    width = int(input('What is the width? '))
    # Run the tactego game
    tactego(file_name, length, width)