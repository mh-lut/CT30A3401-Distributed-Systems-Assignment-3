#0608560
#CT30A3401 Distributed Systems
#Assignment 3
#Client part
#Help received: https://www.youtube.com/watch?v=3UOyky9sEQY

import socket
import threading

#ask nickname
nickname = input("Choose a nickname: ")

# server address
IP = "127.0.0.1"
PORT = 9995
BUFFER_SIZE = 1024

# TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

# a loop that listens to the server
def receive():
    while True:
        try:
            msg = client.recv(BUFFER_SIZE).decode("utf-8")
            if msg == '!NICKNAME!':
                client.send(nickname.encode("utf-8"))
            else:
                print(msg)
        except:
            client.close()
            break
                

# a loop that waits for user input and sends it to the server or terminates the program
def write():
    while True:
        msg = f'{nickname}: {input("")}' # message
        if msg[len(nickname)+2:] == "/quit":
            client.close() # termite connection
            break
        else:
            client.send(msg.encode("utf-8")) #send message


# this makes two threads, one listens to the server and the other sends messages to the server if user wants
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
