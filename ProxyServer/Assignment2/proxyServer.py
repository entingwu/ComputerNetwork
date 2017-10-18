import socket
import _thread
from ProxyServer.Assignment2.myUtil import *

# Get host name, IP address, and port number.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8383

# Make a TCP socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to server IP and port number.
s.bind((host_ip, host_port))
print("Server started at: " + host_ip + "\nThe Port is: " + str(host_port))

# Listen allow 5 pending connects
s.listen(5)

bufsize = 1024
# dict, key is tuple
cache = {}


def handler(conn):
    raw_data = conn.recv(bufsize)
    # Examine the first line
    request_line = getRequestLine(raw_data)
    # ('GET', 'www.entingwu.me', '/', 'HTTP/1.1')
    request_info = getRequestInfo(request_line)
    method, host, path, protocol = request_info

    response = b""
    if method != "GET":
        conn.sendall(b"HTTP/1.1 400 Bad request\r\nContent-Type:text/html \r\n\r\n")
        conn.close()
        return

    if request_info in cache:
        # get a tuple from dict
        response = cache[request_info]
        print("Get response from proxy cache ", response)
    else:
        print("Get response from real server.")
        # Make TCP connection to the real web server
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 'www.entingwu.me' 80
        new_socket.connect((host, 80))
        print("request_info ", request_info)
        forward_request = buildForwardRequest(raw_data, request_info)
        # Send over an HTTP request
        new_socket.send(forward_request.encode())
        while True:
            data = new_socket.recv(bufsize)
            if not data: break
            response += data
            print("data ", data)
        cache[request_info] = response
        # Close the TCP connection to the server
        new_socket.close()

    # Send the server's response back to the client
    conn.sendall(response)
    # Close the connection socket to the client
    conn.close()
    return

while True:
    conn, addr = s.accept()
    print("Server connected by ", addr, "at ", now())
    _thread.start_new(handler, (conn,))