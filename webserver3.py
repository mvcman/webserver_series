import socket
import time
import re
import os
import sys
import yaml
from base64_encoding import *

# try:
#     from http_parser.parser import HttpParser
# except ImportError:
#     from http_parser.pyparser import HttpParser

ECHO = os.getenv('ECHO')
HOST = sys.argv[1]
PORT = sys.argv[2]
print(ECHO, sys.argv)

# p = HttpParser()

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 3)
listen_socket.bind((HOST, int(PORT)))
listen_socket.listen(3)
listen_socket.setblocking(0)
socketList=[]

userList = [
    "{ username: 'mandar', password: 'mandar' }",
    "{ username: 'mandar1', password: 'mandar1' }",
    "{ username: 'mandar2', password: 'mandar2' }",
]

print('Serving HTTP on port {0} ...'.format(PORT))

http_request = b''
host_headers = []

def create_response(file, connection, protocol, status):
    alldata = b''
    with open(file, 'r') as file:
        for i in file:
            print(i)
            alldata += str.encode(i)

    if status == 'not authorized':
        connection.sendall(b"HTTP/1.0 403 Not Authorized\nContent-Type: text/html\n")
    elif status == 'not found':
        connection.sendall(b"HTTP/1.0 404 Not Found\nContent-Type: text/html\n")
    else:
        if 'HTTP/1.0' in protocol:
            connection.sendall(b"HTTP/1.0 200 OK\nContent-Type: text/html\n")
        else:
            connection.sendall(b"HTTP/1.1 200 OK\nContent-Type: text/html\n")
    connection.sendall(b"\r\n")
    connection.sendall(alldata)


def connection_type(req, conn):
    if 'HTTP/1.0' in req:
        if 'Connection: keep-alive' in req:
            print("....")
        else:
            conn.close()
    if 'HTTP/1.1' in req and 'Connection: close' in req:
        conn.close()


def send_response(host, file, req, conn, protocol, isAuthenticated):
    print('requested data', host, file, req, isAuthenticated)
    status = ''
    if file != '':
        if isAuthenticated == 'no':
            if host in req:
                status = 'not authorized'
                create_response('templates/notauthorized.html', conn, protocol, status)
                connection_type(req, conn)
        else:
            if host in req:
                status = 'found'
                create_response(file, conn, protocol, status)
                connection_type(req, conn)
    else:
        status = 'not found'
        create_response('templates/error.html', conn, protocol, status)
        connection_type(req, conn)
        

while True:
    try:
        for i in range(0, len(socketList)):
            try:
                response_file = ''
                request_data = socketList[i].recv(1024)

                http_request += request_data
                my_req = http_request.decode()
                print('request', my_req)
                protocol = my_req.splitlines()[0]
                request_host = my_req.splitlines()[1]
                with open('config.yml') as data_file:
                    config = yaml.safe_load(data_file)
                    for v in config.items():
                        host_headers.append(v[1]['host'])
                        if v[1]['host'] in request_host:
                            response_file = v[1]['filename']  

                if b'\r\n\r\n' in http_request:
                    try:
                        if b'Authorization:' in http_request:
                            auth_value = my_req.splitlines()[4]
                            print('auth value', auth_value)
                            value = re.split('[:]', auth_value)
                            print('Colon separated value', value)
                            fo = value[1].split()
                            decoded_value = decode_body(fo[1])
                            print(str(decoded_value), userList[0])
                            if str(decoded_value) in userList:
                                print('Decode value is there')
                                isAuthenticated = 'yes'
                            else:
                                isAuthenticated = 'no'
                        else:
                            # socketList[i].sendall(b"HTTP/1.1 401 Unauthorized\nWWW-Authenticate: Basic realm=Access to the web server\nContent-Type: text/html\n")
                            isAuthenticated = 'never'
                            # break
                        print('inside loop', response_file)
                        send_response(request_host, response_file, my_req, socketList[i], protocol, isAuthenticated)
                        http_request = b''
                    except Exception as es:
                        print(es)
            except Exception as e:
                pass
        client_connection, client_addrress = listen_socket.accept() 
        print(client_connection, client_addrress)
        client_connection.setblocking(0)
        socketList.append(client_connection)
    except Exception as e:
        continue