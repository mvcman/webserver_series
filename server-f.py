import socket
import os
import sys
import re
import yaml
from base64_encoding import *

HOST = sys.argv[1]
PORT = sys.argv[2]
REQUEST_QUEUE_SIZE = 5

userList = [
    "mandar:mandar",
    "mandar1:mandar1",
    "mandar2:mandar2",
]

host_headers = []

def create_response(file, connection, protocol, status):
    alldata = b''
    with open(file, 'r') as file:
        for i in file:
            print(i)
            alldata += str.encode(i)

    length = len(alldata)

    if status == 'not found':
        connection.sendall(bytes("HTTP/1.0 404 Not Found\nContent-Type: text/html\nContent-Length: {}\n".format(length), 'utf-8'))
    else:
        if 'HTTP/1.0' in protocol:
            connection.sendall(bytes("HTTP/1.0 200 OK\nContent-Type: text/html\nContent-Length: {}\n".format(length), 'utf-8'))
        else:
            connection.sendall(bytes("HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n".format(length), 'utf-8'))
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

def handle_request(client_connection):
    http_request = b''
    while True:
        response_file = ''
        request = client_connection.recv(1024)
        http_request += request
        print(http_request)
        if b'\r\n\r\n' in http_request:
            my_req = http_request.decode()
            print(request.decode())
            protocol = my_req.splitlines()[0]
            request_host = my_req.splitlines()[1]
            http_request = b''
            with open('config.yml') as data_file:
                config = yaml.safe_load(data_file)
                for v in config.items():
                    host_headers.append(v[1]['host'])
                    if v[1]['host'] in request_host:
                        response_file = v[1]['filename']
            if re.search('Authorization:', my_req):
                v = my_req.split('\n')
                print('Arrya of my_req', v)
                for l in range(len(v)):
                    if 'Authorization:' in v[l]:
                        b = v[l]
                print(b)
                value = re.split('[:]', b)
                print('Colon separated value', value)
                fo = value[1].split()
                print('decoded value ', decode_body(fo[1]))
                if decode_body(fo[1]) in userList:
                    print('found!')
                    isAuthenticated = 'yes'
                    send_response(request_host, response_file, my_req, client_connection, protocol, isAuthenticated)
                else:
                    isAuthenticated = 'no'
                    http_response = b"HTTP/1.1 401 Unauthorized\nWWW-Authenticate: Basic realm=Access to the web server\nContent-Type: text/html\nContent-Length: 13\n\nHello, World!"
                    client_connection.sendall(http_response)
            else:
                http_response = b"HTTP/1.1 401 Unauthorized\nWWW-Authenticate: Basic realm=Access to the web server\nContent-Type: text/html\nContent-Length: 13\n\nHello, World!"
                client_connection.sendall(http_response)


def serve_forever():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, int(PORT)))
    sock.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port}...'.format(port=PORT))

    while True:
        conn, address = sock.accept()
        pid = os.fork()
        if pid == 0:
            sock.close()
            handle_request(conn)
            conn.close()
            os._exit(0)
        else:
            conn.close()

if __name__ == '__main__':
    serve_forever()