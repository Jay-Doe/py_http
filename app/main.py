from app.http.types import HttpResponseLine
from app.http.types import HttpStatus
from app.http.types import HttpResponse
import socket  # noqa: F401
from .http.types import CLRF


def main():
     with socket.create_server(("localhost", 4221), reuse_port=True) as server_soc:
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
                    responseLine = HttpResponseLine(HttpStatus.OK )
                    strResponse = str(HttpResponse(line=responseLine, headers={}))
                    print(strResponse)
                    response = strResponse.encode("ascii")
                    con.sendall(response)
                    con.close()











if __name__ == "__main__":
    main()
