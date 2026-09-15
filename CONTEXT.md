# HTTP Server Context

This project models the small set of HTTP/1.1 messages needed by the current
challenge stage and keeps message interpretation separate from socket I/O.

## HTTP messages

**Request**:
An inbound HTTP message made of a request line, headers, and a body.
_Avoid_: `HttpRequest`

**Response**:
An outbound HTTP message made of a response line, headers, and an optional
body.
_Avoid_: `HttpResponse`

**Headers**:
The named metadata entries belonging to a request or response.
_Avoid_: `HttpHeaders`

**Request line**:
The method, target path, and protocol at the start of a request.
_Avoid_: `RqLine`, `HttpRequestLine`

**Response line**:
The status and reason phrase at the start of a response.
_Avoid_: `RpLine`, `HttpResponseLine`
