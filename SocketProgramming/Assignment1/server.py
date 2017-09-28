import operator
import re
import socket
import time
import _thread

# Get host name, IP address, and port number
import struct

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8383

# Make a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to server IP and port number
s.bind((host_ip, host_port))
print('Server started. Waiting for connection...')

# Listen allow 5 pending connects
s.listen()

# Current time on the server
def now():
    return time.ctime(time.time())

bufsize = 16
def handler(conn, addr):
    received = b""
    while True:
        data = conn.recv(bufsize)
        if not data: break
        received += data
        if allReceived(received):
            print('Server received: ', repr(received), 'from', addr)
            response = answerRequest(received)
            #print('Server respond: ', repr(response), '\n')
            conn.sendall(str.encode('Echo ==> ') + data)
            received = b""
    conn.close()

# Take a string and return True if the string is one whole request from client, otherwise return False
def allReceived(request):
    # get first two bytes, (2,):
    # struct.unpack('h', request[:2])[0]
    numOfEquations = socket.ntohs(struct.unpack('h', request[:2])[0])
    pos = 2

    while numOfEquations > 0:
        if pos + 2 >= len(request):
            return False
        # get next 2 bytes: request[pos: pos+2]
        lenOfEquation = socket.ntohs(struct.unpack('h', request[pos: pos+2])[0])
        pos += 2 + lenOfEquation
        # pos is at next exp
        numOfEquations -= 1
    if pos == len(request):
        return True
    return False

# Take one formatted request and return a formatted response with answers
# 3 2 "15" 1 "5" 1 "2"
def answerRequest(request):
    numOfEquations = socket.ntohs(struct.unpack('h', request[:2])[0])
    result = request[:2] #byte
    pos = 2

    while numOfEquations > 0:
        lenOfEquation = socket.ntohs(struct.unpack('h', request[pos: pos+2])[0])
        pos += 2
        equation = request[pos: pos+lenOfEquation]
        pos += lenOfEquation
        print("equation ", equation)
        tmp = caculate(equation)
        #result = result + len(tmp) + tmp
        numOfEquations -= 1
    return result

# Take a string expression and return the answer(int) of the given string
def caculate(bytes):
    # 1 + 12 / 3
    str = re.sub(r'\d+', " \g<0> ", bytes.decode())
    oper = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv}
    expressions = str.split()
    i = d = tmp = 0
    func = oper['+']
    while i < len(expressions):
        exp = expressions[i]
        if exp in '+-':
            tmp = func(tmp, d) # tmp = func(0,1) = 1
            func = exp # +
        elif exp in '*/':
            i += 1
            tmp += oper[exp](d, expressions[i]) # 1 + 4
        else:
            d = int(exp) # 1 12
        i += 1
    return func(tmp, d)

while True:
    conn, addr = s.accept()
    print('Server connected by ', addr, 'at', now())
    _thread.start_new_thread(handler, (conn, addr))