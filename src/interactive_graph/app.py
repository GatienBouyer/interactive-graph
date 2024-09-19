from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from interactive_graph import flowchart

templates = Jinja2Templates(directory="src/templates")


class Graph:
    """Diamond diagram
      A
    // \\
    B   C
    \\ //
      D
    """
    nodes = [
        "My first operation",
        "My second operation",
        "My third operation",
        "My fourth operation",
    ]
    edges = [
        (0, 1),
        (1, 3),
        (0, 2),
        (2, 3),
    ]


graph = Graph()


def homepage(request: Request) -> Response:
    return templates.TemplateResponse(request, "index.html", context={
        "paragraph": "Lorem ipsum dolor sit amet consectetur adipisicing elit."
    })


def generate(request: Request) -> Response:
    flowchart_script = flowchart.generate_script(graph)
    return templates.TemplateResponse(
        request,
        "generated.html",
        context={"diagram": flowchart_script},
    )


app = Starlette(debug=True, routes=[
    Mount('/static', StaticFiles(directory='src/static'), name='static'),
    Route('/', homepage),
    Route('/generate', generate),
])
