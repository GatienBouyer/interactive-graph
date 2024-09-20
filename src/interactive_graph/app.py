from networkx import DiGraph, Graph
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from interactive_graph import graphviz

templates = Jinja2Templates(directory="src/templates")

graph: Graph[str] = DiGraph()
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
graph.add_nodes_from(nodes)
graph.add_edges_from([
    (nodes[0], nodes[1]),
    (nodes[1], nodes[3]),
    (nodes[0], nodes[2]),
    (nodes[2], nodes[3]),
])


def homepage(request: Request) -> Response:
    return templates.TemplateResponse(request, "index.html", context={
        "paragraph": "Lorem ipsum dolor sit amet consectetur adipisicing elit."
    })


def generate(request: Request) -> Response:
    graph_svg = graphviz.generate_svg(graph)
    return templates.TemplateResponse(
        request,
        "generated.html",
        context={"diagram": graph_svg},
    )


app = Starlette(debug=True, routes=[
    Mount('/static', StaticFiles(directory='src/static'), name='static'),
    Route('/', homepage),
    Route('/generate', generate),
])
