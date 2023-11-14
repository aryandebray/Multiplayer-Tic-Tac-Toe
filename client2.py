import socket

# Initialize the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
def print_board(board):
    for i in range(0,9,3):
        print(board[i],"\t",board[i+1],"\t",board[i+2],"\n")
    print("------------------------------------")
# Main game loop
while True:
    # Receive and display the current game state
    state = client_socket.recv(1024).decode()
    if(state=='Winner is Player 2') or (state=="It is a Draw") or (state=="Player 2 lost"):
        print(state)
        break
    print_board(state)

    # Allow the player to make a move and send it to the server
    move = (input("Enter your move (1-9): "))
    #state=state[:int(move)-1]+"O"+state[:int(move)]
    client_socket.send(move.encode())

# Close the client socket
client_socket.close()
