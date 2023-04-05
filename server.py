#0608560
#CT30A3401 Distributed Systems
#Assignment 3
#Server part
#Help receiver: https://www.youtube.com/watch?v=3UOyky9sEQY, https://www.youtube.com/watch?v=F_JDA96AdEI



import socket
import threading

IP = "127.0.0.1" #localhost
PORT = 9995
BUFFER_SIZE = 1024

#make server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET = internet socket , socket.SOCK_STREAM = TCP / socket.SOCK_DGRAM = UPD
server.bind((IP, PORT)) #take port
server.listen() #set the server to listen

#lists
clients = [] # client address
nicknames = [] # client  nickname
channel = [] # the channel the user is on


def broadcast(msg, x): #send message to all clients
    index  = 0
    for client in clients:
        if channel[index] == x: #check that channel is right
            client.send(msg) #send message
        index += 1


def handle_client(client, nickname):
    while True:
        try: 
            index = clients.index(client) # find client index
            message = client.recv(BUFFER_SIZE).decode("utf-8") #wait and receive message
            
            #help command
            if message[len(nickname)+2:] == '/help': # if user needs help
                client.send(("/help --> get all commands...\n/channel [0-3] --> change channel to [0-3]\n/private [nickname] --> send private message to user [nickname]\n/quit --> disconnect and turn program off").encode("utf-8"))
            
            # different channels
            elif message[len(nickname)+2:] == '/channel 0': # change the channel
                channel[index] = 0 # set channel
                client.send(("------------ Channel changed to 0 ------------\n").encode("utf-8"))
                broadcast((nickname + " joined to the channel").encode("utf-8"), 0)
            elif message[len(nickname)+2:] == '/channel 1': # change the channel
                channel[index] = 1 # set channel
                client.send(("------------ Channel changed to 1 ------------\n").encode("utf-8"))
                broadcast((nickname + " joined to the channel").encode("utf-8"), 1)
            elif message[len(nickname)+2:] == '/channel 2': # change the channel
                channel[index] = 2 # set channel
                client.send(("------------ Channel changed to 2 ------------\n").encode("utf-8"))
                broadcast((nickname + " joined to the channel").encode("utf-8"), 2)
            elif message[len(nickname)+2:] == '/channel 3': # change the channel
                channel[index] = 2 # set channel
                client.send(("------------ Channel changed to 3 ------------\n").encode("utf-8"))
                broadcast((nickname + " joined to the channel").encode("utf-8"), 3)
            
            elif message[len(nickname)+2:].startswith("/private "):
                try:
                    parts = message.split(" ", 3) # split message
                    index_receiver = nicknames.index(parts[2]) # find receiver
                    clients[index_receiver].send((f"private from {nickname}:" + message[len(nickname)+2+9+len(nicknames[index]):]).encode("utf-8")) #send message
                except ValueError:
                    client.send(("user not found!").encode("utf-8")) # if an error occurs while finding the index
                except:
                    client.send(("error in sending a private message example:'/private user123 Hellooo!'").encode("utf-8")) # if error
            
            # send message to channel
            else:
                broadcast(message.encode("utf-8"), channel[index])
            
        except:
            index = clients.index(client) # find client index
            clients.remove(client) # remove old client
            client.close() # close connection
            print(f"{nickname} left the chat!".encode("utf-8")) # print server console
            broadcast(f"{nickname} left the chat!".encode("utf-8"), channel[index]) # send left message to channel
            del nicknames [index] # remove old nickname
            del channel [index] # remove old channel
            break
        
def receive():
    print("Server is running...")
    while True:
        # wait new connection...
        client, address = server.accept() # accept new connection /client = socket that can be used to communicate to client
        print(f"Connected with {str(address)}") # print new connection
        
        client.send('!NICKNAME!'.encode('utf-8')) # ask the client for nickname 
        nickname = client.recv(BUFFER_SIZE).decode('utf-8') # get nickname
        nicknames.append(nickname) # add to the list (name)
        clients.append(client) # add to the list (client socket)
        channel.append(0) # add channel
        
        print(f"Nickname of the client is {nickname}!") # print the new users nickname
        client.send("\n------------ Connected to the server ------------\n".encode("utf-8")) # send new user connected messsage
        client.send("If you need help type /help\n".encode("utf-8")) # send new user connected messsage
        client.send("\n".encode("utf-8"))
        broadcast(f"{nickname} joined the chat!".encode("utf-8"), 0) # use broadcast to send joined message
        
        
        thread = threading.Thread(target=handle_client, args=(client, nickname)) # make new thread to handle new client
        thread.start() # start thread
        
receive()