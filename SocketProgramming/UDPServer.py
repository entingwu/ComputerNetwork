import socket

serverName = socket.gethostname()
serverIP = socket.gethostbyname(serverName)
serverPort = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# assign a port number to the socket.
# When anyone sends a packet to port 12000 at the IP address of the server,
# that packet will be directed to this socket
serverSocket.bind((serverIP, serverPort))
print("The server is ready to receive")

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.upper()
    # attaches the client's address (IP address and port number) to the capitalized message
    # and sends the resulting packet into the server's socket.
    serverSocket.sendto(modifiedMessage, clientAddress)