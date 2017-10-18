import time
import urllib.parse

# Current time on the server
def now():
    return time.ctime(time.time())

# Get the first line of the request data from the client side.
def getRequestLine(data):
    # decode(): binary to string
	data_list = data.decode().split("\r\n")
	request_line = data_list[0]
	return request_line

# Take the first line of the request from client side.
# Returns the method, host, path, protocol (as reqeust_info) of the request.
def getRequestInfo(header_line):
    header_list = header_line.split(" ")
    method = header_list[0]
    # url ParseResult(scheme='http', netloc='www.entingwu.me', path='/', params='', query='', fragment='')
    url = urllib.parse.urlparse(header_list[1])
    path = url.path
    if path == "":
        path = "/"
    host = url.netloc
    protocol = header_list[2]
    return (method, host, path, protocol) # tuple

# Take the request data from the client side and the first line of that data.
# Returns the request from proxy sever to the real server.
def buildForwardRequest(data, request_info):
    data_list = data.decode().split("\r\n")
    # request_info ('GET', 'www.entingwu.me', '/', 'HTTP/1.1')
    # request_header 'GET / HTTP/1.1'
    first_line = request_info[0] + " " + request_info[2] + " " + request_info[3]
    data_list[0] = first_line

    is_found = False
    close_connection = "Connection: close"
    print("data_list ", data_list)
    # 2 Proxy - Connection: keep - alive
    for index, line in enumerate(data_list):
        if "Connection" in line:
            is_found = True
            print("index ", index, "line ", line)
            data_list[index] = close_connection
            break
    if not is_found:
        data_list.insert(-2, close_connection)

    # Insert "\r\n" into each pair in data_list
    forward_request = ("\r\n").join(data_list)
    return forward_request