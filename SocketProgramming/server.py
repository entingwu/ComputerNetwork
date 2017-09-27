import socket
import time
import _thread

# Get host name, IP address, and port number
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8181

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
    while True:
        data = conn.recv(bufsize)
        if not data: break
        print('Server received: ', data, 'from', addr)
        conn.sendall(str.encode('Echo ==> ') + data)
        time.sleep(10)
    conn.close()

while True:
    conn, addr = s.accept()
    print('Server connected by ', addr)
    print('at ', now())
    _thread.start_new_thread(handler, (conn, addr))