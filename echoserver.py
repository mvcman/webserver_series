import socket
import os
import sys

ECHO = os.getenv('ECHO')
HOST = sys.argv[1]
PORT = sys.argv[2]
print(ECHO, sys.argv)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, int(PORT)))
server.listen(5)
server.setblocking(0)
arr = [] 


# def handle_request(client_connection):
#     if (client_connection):
#         while True:
#             print(client_connection)
#             dir(client_connection)
#             request = client_connection.recv(1024)
#             print(request.decode())
#             http_response = b"""\
#         HTTP/1.1 200 ok

#         Hello, World!
#             """
#             client_connection.sendall(http_response)
#     else:
#         client_connection.close()

# while True:
#     conn, address = server.accept()
#     handle_request(conn)
#     server.close()
#     # conn.close()
#     os._exit(0)

while True:
    try:
        for i in range(0, len(arr)):
            try:
                data = arr[i].recv(1024)
                if int(ECHO) == 0:
                    response = """\
                HTTP/1.1 200 OK

                Welcome Webserver
                    """
                    arr[i].send(response)
                else:
                    arr[i].send(data)
            except Exception as e:
                pass
        conn, address = server.accept()
        conn.setblocking(0)
        arr.append(conn)
        
    except Exception as e:
        continue
