from .constants import CRLF
from .headers import Headers
from .models import HttpMethod, Request, RequestLine


def read_request(connection) -> str:
    received = bytearray()
    delimiter = (2 * CRLF).encode("ascii")

    while delimiter not in received:
        data = connection.recv(4096)
        received += data

    return received.decode("ascii")


def parse_request(raw_request: str) -> Request:
    raw_request_line, raw_headers = raw_request.split(CRLF, maxsplit=1)
    method, target, protocol = raw_request_line.split(" ", maxsplit=2)
    request_line = RequestLine(target, HttpMethod(method), protocol)
    headers = Headers.parse(raw_headers)
    return Request(request_line, headers, b"")

