from app.http.responses import make_response
import socket
from pathlib import Path

from .constants import PROTOCOL
from .parsing import parse_request, read_request
from .responses import response_for, serialize_response
from .models import HttpStatus, ResponseLine
from .headers import Headers


def handle_connection(connection: socket.socket) -> None:
    raw_request = read_request(connection)
    print("Request Ided")
    request = parse_request(raw_request)

    if request.line.protocol != PROTOCOL:
        print("Unsupported protocol")
        return

    if not request.line.path.startswith("/"):
        print("path not found")
        resp_line = ResponseLine(HttpStatus.NOT_FOUND, "Not Found")
        resp = make_response(resp_line, headers=Headers())
        connection.sendall(serialize_response(resp))
        connection.close()
        return

    response = response_for(request)
    connection.sendall(serialize_response(response))


def serve(host: str = "localhost", port: int = 4221) -> None:
    with socket.create_server((host, port), reuse_port=True) as server_socket:
        while True:
            print("ready for con")
            connection, _ = server_socket.accept()
            print("Accepted con")
            with connection:
                handle_connection(connection)
