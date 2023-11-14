import socket
import numpy as np
# Initialize the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(2)
print("Waiting for players to connect...")

# Accept two player connections
player1_socket, player1_address = server_socket.accept()
print("Player 1 connected from", player1_address)
player2_socket, player2_address = server_socket.accept()
print("Player 2 connected from", player2_address)

# Initialize the game state
board = ['.' for _ in range(9)]
current_player = 'X'
def print_board():
    for i in range(0,9,3):
        print(board[i],"\t",board[i+1],"\t",board[i+2],"\n")
    print("------------------------------------")
# Function to send the current game state to both players
def send_state1():
    state = "".join(board)
    player1_socket.send(state.encode())
    #player2_socket.send(state.encode())
def send_state2():
    state = "".join(board)
    #player1_socket.send(state.encode())
    player2_socket.send(state.encode())
def row_win(board, player):
    #win=False
    for i in range(0,9,3):
        if(board[i]==board[i+1] and board[i+1]==board[i+2] and board[i]==player):
            return True
    return False
        
def col_win(board, player):
    for i in range(0,3):
        if(board[i]==board[i+3] and board[i+3]==board[i+6] and board[i]==player):
            return True
    return False
def diag_win(board, player):
    if(board[0]==board[4] and board[4]==board[8] and board[0]==player) or (board[2]==board[4] and board[4]==board[6] and board[2]==player):
        return True
    return False
def draw(board):
    for i in board:
        if i=='.':
            return False
    return True
def evaluate(board):
    winner = 'N'
 
    for player in ['X','O']:
        if (row_win(board, player) or
                col_win(board, player) or
                diag_win(board, player)):
 
            winner = player
 
    if np.all(board != 0) and winner == 0:
        winner = 'N'
    return winner
# Main game loop
while True:
    send_state1()
    move1 = player1_socket.recv(1024).decode()
    # Handle player 1's move
    # Check for a win or draw
    # Send updates to both players
    m=int(move1)
    board[m-1]='X'
    print_board()
    res=evaluate(board)
    if(res=='X'):
        print("Winner is player 1")
        state1 = "Winner is Player 1"
        state2 = "Player 2 lost"
        player1_socket.send(state1.encode())
        player2_socket.send(state2.encode())
        break
    if(draw(board)==True):
        print("Draw")
        state="It is a Draw"
        player1_socket.send(state.encode())
        player2_socket.send(state.encode())
        break
    send_state2()
    move2 = player2_socket.recv(1024).decode()
    # Handle player 2's move
    # Check for a win or draw
    # Send updates to both players
    m=int(move2)
    board[m-1]='O'
    print_board()
    res=evaluate(board)
    if(res=='O'):
        print("Winner is player 2")
        state2 = "Winner is Player 2"
        state1 = "Player 1 lost"
        player1_socket.send(state1.encode())
        player2_socket.send(state2.encode())
        break
# Close sockets and clean up
player1_socket.close()
player2_socket.close()
server_socket.close()
