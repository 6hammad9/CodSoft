import tkinter as tk
from tkinter import messagebox

# Function to check if the game is over
def game_over(board):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '':
            return True
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '':
            return True
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return True
    
    # Check if the board is full (draw)
    for row in board:
        if '' in row:
            return False
    return True
def reset_game():
    global board, player_turn
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text='', state=tk.NORMAL)
# Function to evaluate the game board
def evaluate(board):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] == 'O':
            return 1  # AI wins
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] == 'O':
            return 1  # AI wins
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] == 'O':
        return 1  # AI wins
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] == 'O':
        return 1  # AI wins
    
    # Check if the human player wins
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] == 'X':
            return -1  # Human wins
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] == 'X':
            return -1  # Human wins
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] == 'X':
        return -1  # Human wins
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] == 'X':
        return -1  # Human wins
    
    # If no one wins, it's a draw
    return 0

# Minimax algorithm
def minimax(board, depth, maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    eval = minimax(board, depth - 1, False)
                    board[i][j] = ''
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    eval = minimax(board, depth - 1, True)
                    board[i][j] = ''
                    min_eval = min(min_eval, eval)
        return min_eval

# Function to get the best move for the AI player
def best_move(board):
    best_score = float('-inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(board, 5, False)  # Adjust the depth as needed
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# Function called when a button is clicked
def on_click(row, col):
    global board, player_turn
    if board[row][col] == '' and not game_over(board):
        board[row][col] = 'X'
        buttons[row][col].config(text='X', state=tk.DISABLED)
        if game_over(board):
            messagebox.showinfo("Game Over", "You win!")
        else:
            ai_move()

# Function to make AI move
def ai_move():
    global board, player_turn
    if not game_over(board):
        row, col = best_move(board)
        board[row][col] = 'O'
        buttons[row][col].config(text='O', state=tk.DISABLED)
        if game_over(board):
            messagebox.showinfo("Game Over", "AI wins!")

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Initialize the game board
board = [['', '', ''], ['', '', ''], ['', '', '']]

# Create buttons for the game board
buttons = [[None, None, None], [None, None, None], [None, None, None]]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text='', font=('normal', 40), width=5, height=2, command=lambda i=i, j=j: on_click(i, j))
        buttons[i][j].grid(row=i, column=j)
reset_button = tk.Button(root, text='Reset', font=('normal', 14), command=reset_game)
reset_button.grid(row=3, column=1, columnspan=3)
root.mainloop()
