import socket
import time
import requests
import os
import sys
import yaml


ECHO = os.getenv('ECHO')
HOST = sys.argv[1]
PORT = sys.argv[2]
print(ECHO, sys.argv)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, int(PORT)))
sock.listen(5)
sock.setblocking(0)
sock_list=[]

# def read_yaml():
#     """ A function to read YAML file"""
#     with open('config.yml') as f:
#         # config = yaml.safe_load(f)
#         documents = yaml.full_load(file)
#         for item, doc in documents.items():
#             print(item, ":", doc)
 
    # return config

print('Serving HTTP on port {0} ...'.format(PORT))
http_request = b''
while True:
    try:
        for i in range(0,len(sock_list)):
            try:
                data = sock_list[i].recv(1024)
                
                http_request += data
                print("http_request: ", http_request)
                request = http_request.decode()
                print("my req: ", request)
                response_data = b''
                if '\r\n\r\n' in request:
                    if 'Host: www.mandar.com' in request or 'Host: www.mandar.com:8000' in request:
                        # f = open('templates/mandar.html', 'r')
                        # print('openin madnar.com')
                        # for i in f.readlines():
                        #     print(i)
                        #     response_data = str.encode(i)
                        #     conn.sendall(response_data)
                        #     i = f.read(1024)
                        # http_request = b''
                        with open('templates/mandar.html', 'r') as file:
                            for i in file:
                                response_data += str.encode(i)
                        conn.sendall(b'HTTP/1.1 200 OK\n')
                        conn.sendall(b'Content-Type: text/html\n')
                        conn.sendall(b'\r\n')
                        conn.sendall(response_data)
                        
                        if 'HTTP/1.0' in request:
                            if 'Connection: keep-alive' in request:
                                http_request = b''
                                print("....")
                            else:
                                http_request = b''
                                conn.close()
                    elif 'Host: www.aniket.com' in request or 'Host: www.aniket.com:8000' in request:
                        # print("Host: aniket/1.1")
                        f = open('templates/aniket.html', 'r')
                        # conn.sendall(b'HTTP/1.1 200 OK')
                        for i in f.readlines():
                            response_data = str.encode(i)
                            conn.sendall(response_data)
                            i = f.read(1024)
                        f.close()
                        if 'HTTP/1.0' in request:
                            if 'Connection: keep-alive' in request:
                                http_request = b''
                                print("....")
                            else:
                                http_request = b''
                                conn.close()
                    elif 'Host: www.shreya.com' in request or 'Host: www.shreya.com:8000' in request:
                        # print("Host: shreya/1.1")
                        f = open('templates/shreya.html', 'r')
                        # conn.sendall(b'HTTP/1.1 200 OK')
                        for i in f.readlines():
                            response_data = str.encode(i)
                            conn.sendall(response_data)
                            i = f.read(1024)
                        f.close()
                        if 'HTTP/1.0' in request:
                            if 'Connection: keep-alive' in request:
                                http_request = b''
                                print("....")
                            else:
                                http_request = b''
                                conn.close()
                    else:
                        conn.sendall('Didnt\' receive header!')
                        http_request = b''
                        conn.close()
            except Exception as e:
                pass
        
        conn, addr = sock.accept() 
        # read_yaml()
        conn.setblocking(0)
        sock_list.append(conn)
    except Exception as e:
        continue