from dataclasses import dataclass
from enum import IntEnum, StrEnum

from .constants import PROTOCOL
from .headers import Headers


class HttpStatus(IntEnum):
    OK = 200
    NOT_FOUND = 404

    def __str__(self) -> str:
        if self.value == 404:
            return "Not Found"
        return self.name


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"


@dataclass(frozen=True)
class ResponseLine:
    status: HttpStatus
    phrase: str
    protocol: str = PROTOCOL

    def __str__(self) -> str:
        return f"{PROTOCOL} {self.status.value} {self.status}"


@dataclass(frozen=True)
class RequestLine:
    path: str
    method: HttpMethod
    protocol: str = PROTOCOL


@dataclass(frozen=True)
class Request:
    line: RequestLine
    headers: Headers
    body: bytes


@dataclass(frozen=True)
class Response:
    line: ResponseLine
    headers: Headers
    body: bytes | None = None
