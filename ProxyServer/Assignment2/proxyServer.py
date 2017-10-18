import socket
import _thread
from ProxyServer.Assignment2.myUtil import *

# Get host name, IP address, and port number.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8383

# Make a TCP socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to server IP and port number.
s.bind((host_ip, host_port))
print("Server started at: " + host_ip + "\nThe Port is: " + str(host_port))

# Listen allow 5 pending connects
s.listen(5)

bufsize = 1024
cache = {}

def handler(conn):
    raw_data = conn.recv(bufsize)
    data_list = raw_data.decode().split("\r\n")
    header_line = data_list[0]
    # ('GET', 'www.entingwu.me', '/', 'HTTP/1.1')
    method, host, path, protocol = getRequestInfo(header_line)

    response = b""
    if method != "GET":
        response = "HTTP/1.1 400 Bad request\r\nContent-Type:text/html \r\n\r\n"
        conn.sendall(response)
        conn.close()
        return

    if header_line in cache:
        response = cache[header_line]
        print("Get response from proxy cache ", response)



    conn.close()

while True:
    conn, addr = s.accept()
    print("Server connected by ", addr, "at ", now())
    _thread.start_new(handler, (conn,))