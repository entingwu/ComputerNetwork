#!/usr/bin/python
import socket

serverName = socket.gethostname()
print('TCP Client Hostname: ', serverName)
serverPort = 12000
# AF_INET: the underlying network is using IPv4
# SOCK_STREAM indicates that the socket is of type SOCK_STREAM
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
sentence = "Enting Wu"
clientSocket.send(sentence)

modifiedSentence = clientSocket.recv(2048)
print('From TCP Server: ', modifiedSentence)
clientSocket.close()