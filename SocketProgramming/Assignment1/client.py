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
message1 = ['3+12', '1+12/3', '6+7', '4*3+6', '5*8']
message2 = ['3+19', '1+12/4']
messages = [message1, message2]

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

# Take the response (a string) from server and decode the string to an array of
# the answers to the sent equations.
def decodeResponse(response):
    results = []
    numOfResponses = socket.ntohs(struct.unpack('h', response[:2])[0])
    pos = 2
    while numOfResponses > 0:
        lenOfAnswer = socket.ntohs(struct.unpack('h', response[pos: pos+2])[0])
        pos += 2
        answer = response[pos: pos + lenOfAnswer]
        pos += lenOfAnswer
        results.append(answer.decode())
        numOfResponses -= 1
    return results

# Take a string and return True if the string is one whole response from server otherwise return False.
def allReceived(data):
    numOfResponses = socket.ntohs(struct.unpack('h', data[:2])[0])
    pos = 2
    while numOfResponses > 0:
        if pos + 2 >= len(data):
            return False
        lenOfAnswer = socket.ntohs(struct.unpack('h', data[pos: pos+2])[0])
        pos += 2 + lenOfAnswer
        numOfResponses -= 1
    if pos == len(data):
        return True
    return False

# Send messages to server over socket
bufsize = 16
for msg in messages:
    request = createRequest(msg)
    print("request", request)
    s.sendall(request)
    response = b""
    while True:
        data = s.recv(bufsize)
        print('data', data)
        response += data
        # 16 bytes for once, receive multiple times to get a whole response
        if allReceived(response):
            print('Your equations are:\t\t', msg)
            print('The response from server is: ', repr(response))
            decode_response = decodeResponse(response)
            print('The result to show is:\t', decode_response, '\n')
            break

# Close socket to send EOF to server
s.close()