from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/templates")


def homepage(request: Request) -> Response:
    return templates.TemplateResponse(request, "index.html", context={
        "paragraph": "Lorem ipsum dolor sit amet consectetur adipisicing elit."
    })


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
