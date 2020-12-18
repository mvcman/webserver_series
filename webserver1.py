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

def create_response(file, connection, protocol):
    alldata = b''
    with open(file, 'r') as file:
            for i in file:
                print(i)
                alldata += str.encode(i)
    if 'HTTP/1.0' in protocol:
        connection.sendall(b"HTTP/1.0 200 OK\nContent-Type: text/html\n")
    else:
        connection.sendall(b"HTTP/1.1 200 OK\nContent-Type: text/html\n")
    connection.sendall(b"\r\n")
    connection.sendall(alldata)

def send_response(host, file, req, conn, protocol):
    print('requested data', host, file, req)
    if host in req:
        print('condition true')
        create_response(file, conn, protocol)
        if 'HTTP/1.0' in req:
            if 'Connection: keep-alive' in req:
                print("....")
            else:
                conn.close()

while True:
    try:
        for i in range(0,len(socketList)):
            try:
                request_data = socketList[i].recv(1024)
                http_request += request_data
                my_req = http_request.decode()
                protocol = my_req.splitlines()[0]
                request_host = my_req.splitlines()[1]
                print('request host', request_host, protocol)
                with open('config.yml') as data_file:
                    config = yaml.safe_load(data_file)
                    for v in config.items():
                        if v[1]['host'] in request_host:
                            response_file = v[1]['filename']
                if b'\r\n\r\n' in http_request:
                    send_response(request_host, response_file, my_req, socketList[i], protocol)
                    http_request = b''
            except Exception as e:
                pass
        client_connection, client_addrress = listen_socket.accept() 
        print(client_connection, client_addrress)
        client_connection.setblocking(0)
        socketList.append(client_connection)
    except Exception as e:
        continue