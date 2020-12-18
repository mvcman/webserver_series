import socket

HOST, PORT = '', 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# didn't get the below line
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((HOST, PORT))

sock.listen(1)

print('Serving HTTP on Port {0}'.format(PORT))

while True:
    conn, address = sock.accept()
    print(conn, address)
    request_data = conn.recv(1024)
    print(request_data)

# Creating response string
# Even when we do telnet we have to enter the key twice for /r/n but here we enter  it once
    responseM = b"""\
HTTP/1.1 200 OK

Welcome to Mandar.com
"""
    responseA = b"""\
HTTP/1.1 200 OK

Welcome to Aniket.com
""" 
    responseS = b"""\
HTTP/1.1 200 OK

Welcome to Shreya.com
""" 
    if 'Host: www.mandar.com:8888' in request_data:
        conn.sendall(responseM)
    elif 'Host: www.aniket.com:8888' in request_data:
        conn.sendall(responseA)
    elif 'Host: www.shreya.com:8888' in request_data:
        conn.sendall(responseS)
    print(request_data)
    conn.sendall(responseM)
    # conn.close()