from core import Request, Response


def index_view(request: Request) -> Response:
    content = f"<h1>Your user agent is {request.headers['User-Agent']}</h1>"
    return Response(request, 200, "OK", content=content, content_type="text/html")


url_patterns = {
    "/": index_view
}
