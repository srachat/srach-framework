from core import Request
from router import url_patterns


def handle_request(request: Request):
    view = url_patterns.get(request.url)
    if view is None:
        return f"You try to open non existing page{request.url}".encode("utf-8")
    response = view(request).prepare()
    return response
