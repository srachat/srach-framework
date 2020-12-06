from core import Request


def index_view(request: Request):
    return f"Your user agent is {request.headers['User-Agent']}".encode("utf-8")


url_patterns = {
    "/": index_view
}
