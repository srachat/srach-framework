from core import Request
from router import url_patterns


def handle_request(request: Request):
    view = url_patterns.get(request.url)
    response = view(request)
    return response
