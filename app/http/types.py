from dataclasses import field
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

@dataclass(frozen=True)
class HttpResponseLine:
    status: HttpStatus
    phrase: str
    protocol: str = PROTOCOL

    def __str__ (self) -> str:
        return f"{PROTOCOL} {self.status.value} {self.status.name}"

@dataclass(frozen=True)
class HttpRequestLine:
    path: str
    method: HttpMethod
    protocol: str = PROTOCOL

@dataclass(frozen=True)
class HttpRequest:
    line: HttpRequestLine
    headers: HttpHeaders
    body: bytes

@dataclass(frozen=True)
class HttpResponse:
    line: HttpResponseLine
    headers: HttpHeaders
    body: bytes = b""

    def __str__ (self) -> str:
        return f"{str(self.line)}{2*CLRF}"

@dataclass
class HttpHeaders:
    entries: list[tuple[str,str]] = field(default_factory=list)

    @classmethod
    def parse(cls, raw_block: str) -> HttpHeaders:
        header_lines =raw_block.lstrip().split(CLRF)
        if not header_lines:
            return HttpHeaders()
        y = HttpHeaders()
        for line in header_lines:
            if not line:
                continue
            k, v = line.split(": ", maxsplit=1)
            y.set_header(key=k, value=v)
        return y


    def get(self, key) -> str:
        for k,v in self.entries:
            if key == k:
                return v
        return ""
    def set_header(self, key: str, value: str) -> None:
        self.entries.append((key,value))
    def __str__(self) -> str:
        return f"{CLRF.join(f"{k}: {v}" for k, v in self.entries) + CLRF}"
