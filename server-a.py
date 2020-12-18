import socket
import os

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def handle_request(client_connection):
    while True:
        request = client_connection.recv(1024)
        print(request.decode())
        http_response = b"""\
    HTTP/1.1 200 ok

    Hello, World!
        """
        client_connection.sendall(http_response)
        # client_connection.sendall(request)


def serve_forever():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(SERVER_ADDRESS)
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