#!/usr/bin/python

import _thread
import socket

from ProxyServer.myUtil import *

# Get host name, IP address, and port number.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8181

# Make a TCP socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to server IP and port number.
s.bind((host_ip, host_port))

print('Server started at: ' + host_ip + '\nThe Port is: ' + str(host_port))

# Listen allow 5 pending connects.
s.listen(5)

# dict, key is tuple
cached = {}
bufsize = 1024


def handler(conn):
    raw_data = ""
    #	while True:
    #		data = conn.recv(bufsize)
    #		if not data: break
    #		raw_data += data
    raw_data = conn.recv(bufsize)
    request_info = getRequestInfo(getRequestLine(raw_data))
    method, host, path, protocal = request_info
    if method != "GET":
        conn.sendall(b"HTTP/1.1 400 Bad request\r\nContent-Type:text/html \r\n\r\n")
        conn.close()
        return
    print(request_info)

    response = b""

    if request_info in cached:
        print("Get response from proxy cached.")
        # get a tuple from dict
        response = cached[request_info]
    else:
        print("Get response from real server.")
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.connect((host, 80))
        print("raw_data ", raw_data)
        print("request_info ", request_info)
        forward_request = buildForwardRequest(raw_data, request_info)
        new_socket.send(forward_request.encode())
        while True:
            data2 = new_socket.recv(bufsize)
            if not data2: break
            response += data2
            print("data2 ", data2)
        cached[request_info] = response
        print("response ", response)
        print("cached[request_info] ", cached)
        new_socket.close()

    conn.sendall(response)
    conn.close()
    return


while True:
    conn, addr = s.accept()
    print('Server connected by', addr)
    print('at', now())
    _thread.start_new(handler, (conn,))





