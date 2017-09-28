#!/usr/bin/python

import socket
import _thread
import time
import struct
import re
import operator

# Get host name, IP address, and port number.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8182

# Make a TCP socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to server IP and port number.
s.bind((host_ip, host_port))

# Listen allow 5 pending connects.
s.listen(5)


# Current time on the server.
def now():
    return time.ctime(time.time())


bufsize = 16


def handler(conn):
    received = b""
    while True:
        data = conn.recv(bufsize)
        if not data: break
        received += data
        if allReceived(received):
            print('Server received:', repr(received))
            response = answerRequest(received)
            print('Server respond:\t', repr(response), '\n')
            conn.sendall(response)
            received = b""
    conn.close()


# Take a string and return True if the string is one whole request from client otherwise return False.
def allReceived(request):
    numOfEquations = socket.ntohs(struct.unpack('h', request[:2])[0])
    currentPosition = 2
    while numOfEquations > 0:
        if currentPosition + 2 >= len(request):
            return False
        length = socket.ntohs(struct.unpack('h', request[currentPosition:currentPosition + 2])[0])
        currentPosition += length + 2
        numOfEquations -= 1
    if currentPosition == len(request):
        return True
    return False


# Take one formated request and return a formated response with answers.
def answerRequest(request):
    numOfEquations = socket.ntohs(struct.unpack('h', request[:2])[0])
    result = request[:2]
    print("result", result)
    currentPosition = 2
    while numOfEquations > 0:
        numOfEquations -= 1
        length = socket.ntohs(struct.unpack('h', request[currentPosition: currentPosition + 2])[0])
        currentPosition += 2

        answer = calculate(request[currentPosition: currentPosition + length])
        currentPosition += length
        string_answer = str(answer).encode()
        result += struct.pack('h', socket.htons(len(string_answer)))
        result += string_answer
    return result


# Take a string expression and return the answer(int) of the given string.
def calculate(s):
    s = re.sub(r'\d+', ' \g<0> ', s.decode())
    op = {'+': operator.add, '-': operator.sub,
          '*': operator.mul, '/': operator.floordiv}
    expression = s.split()
    total = d = idx = 0
    func = op['+']
    while idx < len(expression):
        e = expression[idx]
        if e in '+-':
            total = func(total, d)
            func = op[e]
        elif e in '*/':
            idx += 1
            d = op[e](d, int(expression[idx]))
        else:
            d = int(e)
        idx += 1
    return func(total, d)


while True:
    conn, addr = s.accept()
    print('Server connected by', addr, )
    print('at', now())
    _thread.start_new(handler, (conn,))
