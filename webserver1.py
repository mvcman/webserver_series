import socket
import time
import os
import sys
import yaml


ECHO = os.getenv('ECHO')
HOST = sys.argv[1]
PORT = sys.argv[2]
print(ECHO, sys.argv)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 3)
listen_socket.bind((HOST, int(PORT)))
listen_socket.listen(3)
listen_socket.setblocking(0)
socketList=[]

print('Serving HTTP on port {0} ...'.format(PORT))

http_request = b''
host_headers = []

def create_response(file, connection, protocol, status):
    alldata = b''
    with open(file, 'r') as file:
        for i in file:
            print(i)
            alldata += str.encode(i)

    length = len(alldata)
    print(length)
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


def send_response(host, file, req, conn, protocol):
    print('requested data', host, file, req)
    status = ''
    if file != '':
        if host in req:
            status = 'found'
            print('condition true')
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
                        print('inside loop', response_file)
                        send_response(request_host, response_file, my_req, socketList[i], protocol)
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