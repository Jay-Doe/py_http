from app.http.types import HttpMethod
from app.http.types import HttpHeaders
from app.http.types import HttpRequestLine
from app.http.types import PROTOCOL
from app.http.types import HttpResponseLine
from app.http.types import HttpStatus
from app.http.types import HttpResponse
import socket  # noqa: F401
from .http.types import CLRF


def main():
     with socket.create_server(("localhost", 4221), reuse_port=True) as server_soc:
            not_found_line: HttpResponseLine = HttpResponseLine(HttpStatus(404), "Not Found")
            NOT_FOUND: HttpResponse = HttpResponse(not_found_line,HttpHeaders())
            while True:
                 print("ready for con")
                 con, _ = server_soc.accept()
                 print("Accepted con")
                 acc: bytearray = bytearray()
                 delimiter = (2 * CLRF).encode("ascii")
                 with con:
                    while delimiter not in acc:
                        data = con.recv(4096)
                        acc +=  data

                    print("Request Ided")
                    rawRequest = acc.decode("ascii")
                    raw_req_line, raw_headers = rawRequest.split(CLRF, maxsplit=1)
                    method, target, prot = raw_req_line.split(" ", maxsplit=2)
                    if prot !=  PROTOCOL:
                        print("Unsupported protocl")
                        con.close()
                    req_line: HttpRequestLine = HttpRequestLine(target, HttpMethod(method), PROTOCOL)
                    req_headers: HttpHeaders = HttpHeaders.parse(raw_headers)
                    if req_line.path != "/":
                        print("path not found")
                        con.sendall(str(NOT_FOUND).encode("ascii"))
                        con.close()
                    status = HttpStatus.OK
                    resp_line: HttpResponseLine = HttpResponseLine(status, status.name)
                    resp_headers: HttpHeaders = HttpHeaders()
                    resp: HttpResponse = HttpResponse(resp_line, resp_headers)
                    con.sendall(str(resp).encode("ascii"))















if __name__ == "__main__":
    main()
