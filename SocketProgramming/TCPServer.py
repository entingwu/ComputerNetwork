#!/usr/bin/python
import socket

serverName = socket.gethostname()
serverIP = socket.gethostbyname(serverName)
serverPort = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Establish a welcoming door, we will wait and listen for some client to knock on the door
serverSocket.bind((serverIP, serverPort))
# This line has the server listen for TCP connection requests from the client.
# The parameter specifies the maximum number of queued connections.
serverSocket.listen(1)
print('The server is ready to receive')

while 1:
    # When a client knocks on this door, the program invokes the accept() method for serverSocket
    # which creates a new socket in the server, called connectionSocket, dedicated to this particular client.
    # The client and server complete the handshaking, creating a TCP connection between the client's clientSocket
    # and the server's connectionSocket. Arrive in order
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    capitalizeSentence = sentence.upper()

    connectionSocket.send(capitalizeSentence)
    connectionSocket.close()