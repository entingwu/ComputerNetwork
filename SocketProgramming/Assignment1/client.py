import socket

# Specify server name and port number to connect to.
import struct

server_name = socket.gethostname()
print('Hostname: ', server_name)
server_port = 8383

# Make a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server machine and port
s.connect((server_name, server_port))
print('Connected to server ', server_name)

# messages to send to server
message1 = ['3+12', '1+12/3', '1+1']
messages = [message1]

# Take a list of message(equations) and return a formatted request string.
# 2 4 '3+12' 6 '1+12/3'
def createRequest(messages):
    numOfEquations = len(messages)
    result = struct.pack('h', socket.htons(numOfEquations))
    for msg in messages:
        lenOfEquations = len(msg)
        result += struct.pack('h', socket.htons(lenOfEquations))
        result += msg.encode()
    return result

# Send messages to server over socket
bufsize = 16
for msg in messages:
    print("msg", msg)
    request = createRequest(msg)
    print("request", request)
    s.sendall(request)
    response = b""
    while True:
        data = s.recv(bufsize)
        response += data
        print('The response from server is: ', repr(response))

# Close socket to send EOF to server
s.close()