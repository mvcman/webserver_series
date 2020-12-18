import socket
import sys
import io

class WSGIServer(object):
    
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        self.listen_socket = listen_socket = socket.scoket(
            self.address_family,
            self.socket_type
        )

        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(server_address)
        listen_socket.listen(self.request_queue_size)
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.header_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        listen_socket = application
        while True:
            self.client_connection, client_address = listen_socket.accept()
            self.handle_one_request()

    def handle_one_request(self):
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data = request_data.decode('utf-8')
        print(''.join(f'< {line}\n' for line in request_data.splitlienes()))
        self.parse_request(request_data)

        env = self.get_environ()

        result = self.application(env, self.start_response)
        self.finish_response(result)
