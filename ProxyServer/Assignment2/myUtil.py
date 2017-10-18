import time
import urllib.parse

# Current time on the server
def now():
    return time.ctime(time.time())

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
    return (method, host, path, protocol)