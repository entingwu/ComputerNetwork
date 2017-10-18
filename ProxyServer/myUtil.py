#!/usr/bin/python

import time
import urllib.parse


# Current time on the server.
def now():
    return time.ctime(time.time())


# Get the first line of the request data from the client side.
def getRequestLine(data):
    data_list = data.decode().split("\r\n")
    request_line = data_list[0]
    return request_line


# Take the first line of the request from client side.
# Returns the method, host, path, protocal (as reqeust_info) of the request.
def getRequestInfo(request_line):
    request_line_list = request_line.split(" ")
    method = request_line_list[0]
    url = request_line_list[1]
    url = urllib.parse.urlparse(url)
    path = url.path
    if path == "":
        path = "/"
    host = url.netloc
    protocol = request_line_list[2]
    return (method, host, path, protocol) # convert to a tuple


# Take the request data from the client side and the first line of that data.
# Returns the request from proxy sever to the real server.
def buildForwardRequest(data, request_info):
    data_list = data.decode().split("\r\n")
    first_line = request_info[0] + " " + request_info[2] + " " + request_info[3]
    data_list[0] = first_line
    close_connection = "Connection: close"
    foundField = False
    print("data_list ", data_list)
    for index, line in enumerate(data_list):
        if "Connection" in line:
            print("index ", index, "line ", line)
            foundField = True
            data_list[index] = close_connection
            break
    print("data_list update ", data_list)

    if not foundField:
        data_list.insert(-2, close_connection)
    forwardRequest = ("\r\n").join(data_list)
    return forwardRequest


