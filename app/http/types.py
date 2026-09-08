from collections.abc import Mapping
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Final


class HttpStatus(IntEnum):
    OK = 200
    NOT_FOUND = 404

class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"

PROTOCOL = "HTTP/1.1"

CLRF : Final = "\r\n"

@dataclass
class HttpResponseLine:
    status: HttpStatus
    phrase: str = "OK"
    protocol: str = PROTOCOL

    def __str__ (self) -> str:
        return f"{PROTOCOL} {self.status.value} {self.status.name}"

@dataclass(frozen=True)
class HttpRequestLine:
    path: str
    method: HttpMethod
    protocol: str = PROTOCOL

@dataclass()
class HttpRequest:
    line: HttpRequestLine
    headers: Mapping[str, str]
    body: bytes

@dataclass(frozen=True)
class HttpResponse:
    line: HttpRequestLine
    headers: dict[str, str]
    body: bytes = b""

    def __str__ (self) -> str:
        return f"{str(self.line)}{2*CLRF}"
