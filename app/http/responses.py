from .constants import CRLF
from .headers import Headers
from .models import HttpStatus, Request, Response, ResponseLine
from .protocols import Serializable


def make_response(
    line: ResponseLine,
    headers: Headers,
    body: Serializable | bytes | None = None,
) -> Response:
    if isinstance(body, bytes):
        body_bytes = body
    elif body is not None:
        body_bytes = body.serialize()
    else:
        body_bytes = None

    if body_bytes is not None:
        headers.add_header("Content-length", f"{len(body_bytes)}")

    return Response(line, headers, body_bytes)


def response_for(request: Request) -> Response:
    match(request.line.path):
        case path if path.startswith("/echo"):
            echo = path.lstrip("/echo").split("/", maxsplit=1)[0]
            status = HttpStatus.OK
            line = ResponseLine(status, status.name)
            head = Headers()
            head.add_header("Content-type", "text/plain")
            return make_response(line, headers=head, body=echo.encode("utf-8"))
        case path if path.startswith("/user-agent"):
            status = HttpStatus.OK
            line = ResponseLine(status, status.name)
            head = Headers()
            head.add_header("Content-type", "text/plain")
            return make_response(line, headers=head, body=request.headers.get_header("User-Agent").encode("utf-8"))
        case "/":
            status = HttpStatus.OK
            line = ResponseLine(status, status.name)
            return make_response(line, Headers())
        case _:
            pass

    line = ResponseLine(HttpStatus.NOT_FOUND, "Not Found")
    return make_response(line, Headers(), b"")

def serialize_response(response: Response) -> bytes:
    head = f"{response.line}{CRLF}{response.headers}".encode("ascii")
    if response.headers.entries:
        head += CRLF.encode("ascii")
    body = response.body or b""
    return head + body
