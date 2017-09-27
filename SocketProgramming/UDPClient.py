import socket

serverName = socket.gethostname()
serverPort = 12000

# creates the client's socket.
# SOCK_DGRAM means it is a UDP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "Zhi Dong"

# sendto() attaches the destination address to the message and sends the resulting packet into the clientSocket
clientSocket.sendto(message, (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage)
clientSocket.close()