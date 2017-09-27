import socket

# Specify server name and port number to connect to.
server_name = socket.gethostname()
print('Hostname: ', server_name)
server_port = 8181

# Make a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server machine and port
s.connect((server_name, server_port))
print('Connected to server ', server_name)

# messages to send to server
message = ['Hello network world', 'This is Enting Wu']

# Send messages to server over socket
bufsize = 1024
for line in message:
    s.sendall(str.encode(line))
    data = s.recv(bufsize)
    print('Client received: ', data)

# Close socket to send EOF to server
s.close()