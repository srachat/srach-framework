import json
from typing import Iterator, Optional, Dict


class Request:
    def __init__(self, data: bytes):
        self.method = None
        self.url = None
        self.version = None
        self.headers = {}
        self.body = None

        self._parse_data(data)

    def _parse_data(self, data: bytes):
        data_iterator = iter(data.decode().split("\r\n"))

        try:
            self._parse_request_header(data_iterator)
            self._parse_headers(data_iterator)
            self._parse_body(data_iterator)
        except StopIteration:
            pass

    def _parse_request_header(self, data_iterator: Iterator[str]):
        split_header = next(data_iterator).split(" ")

        if len(split_header) != 3:
            raise ValueError("Incorrect value of lines")

        self.method, self.url, self.version = split_header

    def _parse_headers(self, data_iterator: Iterator[str]):
        header = next(data_iterator)

        while header != "":
            key, value = header.split(":", 1)
            self.headers[key] = value.strip()
            header = next(data_iterator)

    def _parse_body(self, data_iterator: Iterator[str]):
        body = next(data_iterator)
        content_type = self.headers.get("Content-Type")
        if content_type is None:
            raise TypeError("Incorrect type")

        if content_type == "application/json":
            self.body = json.loads(body)


class Response:
    def __init__(self,
                 request: Request,
                 status_code: int,
                 status_text: str,
                 headers: Optional[Dict[str, str]] = None,
                 content: Optional[str] = None,
                 content_type: Optional[str] = None):
        self.request = request
        self.status_code = status_code
        self.status_text = status_text
        self.headers = headers or {}
        self.content = content
        self.content_type = content_type

    def prepare(self) -> bytes:
        status_line = f"{self.request.version} {self.status_code} {self.status_text}\r\n"
        headers = "\r\n".join(f"{name}: {value}" for name, value in self.headers.items()) + "\r\n"

        result = status_line + headers

        if self.content:
            result += f"\r\n{self.content}"

        return result.encode("utf-8")
