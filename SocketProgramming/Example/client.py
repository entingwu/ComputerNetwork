#!/usr/bin/python

import socket
import struct

# Specify server name and port number to connect to.
#
# API: gethostname()
#   returns a string containing the hostname of the
#   machine where the Python interpreter is currently
#   executing.
server_name = socket.gethostname()
print('Hostname: ', server_name)
server_port = 8182

# Make a TCP socket object.
#
# API: socket(address_family, socket_type)
#
# Address family
#   AF_INET: IPv4
#   AF_INET6: IPv6
#
# Socket type
#   SOCK_STREAM: TCP socket
#   SOCK_DGRAM: UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server machine and port.
#
# API: connect(address)
#   connect to a remote socket at the given address.
s.connect((server_name, server_port))
print('Connected to server ', server_name)


# Take a list of message(equations) and return a formated request string.
def createRequest(messages):
    numOfEquations = len(messages)
    result = struct.pack('h', socket.htons(numOfEquations))
    print("result ", result)
    for message in messages:
        messageLength = len(message)
        print("msg ", message, "len", messageLength)
        result = result + struct.pack('h', socket.htons(messageLength)) + message.encode()
        print("result ", result)
    return result


# Take the response (a string) from server and decode the string to an array of
# the answers to the sent equations.
def decodeResponse(response):
    result = []
    numOfAnswers = socket.ntohs(struct.unpack('h', response[:2])[0])
    currentPosition = 2
    while numOfAnswers > 0:
        answerLength = socket.ntohs(struct.unpack('h', (response[currentPosition: currentPosition + 2]))[0])
        currentPosition += 2
        result.append(int(response[currentPosition: currentPosition + answerLength]))
        currentPosition += answerLength
        numOfAnswers -= 1
    return result


# Take a string and return True if the string is one whole response from server otherwise return False.	
def allReceived(data):
    numOfEquations = socket.ntohs(struct.unpack('h', data[:2])[0])
    currentPosition = 2
    while numOfEquations > 0:
        if currentPosition + 2 >= len(data):
            return False
        length = socket.ntohs(struct.unpack('h', data[currentPosition:currentPosition + 2])[0])
        currentPosition += length + 2
        numOfEquations -= 1
    if currentPosition == len(data):
        return True
    return False


# Send messages to server over socket.
#
# API: send(string)
#   Sends data to the connected remote socket.
#   Returns the number of bytes sent. Applications
#   are responsible for checking that all data
#   has been sent
#
# API: recv(bufsize)
#   Receive data from the socket. The return value is
#   a string representing the data received. The
#   maximum amount of data to be received at once is
#   specified by bufsize
#
# API: sendall(string)
#   Sends data to the connected remote socket.
#   This method continues to send data from string
#   until either all data has been sent or an error
#   occurs.

bufsize = 16
# messages to send to server.
message1 = ['3+12', '1+12/3', '1+1']
message2 = ['3+19', '1+12/4']
message3 = ['32+323', '32/3+387', '644/32+645*32', '656/22+237-23/4+32*94', '4*3+26', '493*10+35-67']
messages = [message1, message2, message3]

for message in messages:
    request = createRequest(message)
    s.sendall(request)
    response = b""
    while True:
        data = s.recv(bufsize)
        response += data
        if allReceived(response):
            print("Your equations are:\t\t", message)
            print("The response from server is:\t", repr(response))
            response_to_show = decodeResponse(response)
            print("The result to show is:\t", response_to_show, '\n')
            break

# Close socket to send EOF to server.
s.close()
