from networkx import DiGraph
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from interactive_graph import graphviz

templates = Jinja2Templates(directory="src/templates")

graph: DiGraph = DiGraph()  # type: ignore[type-arg]
"""Diamond diagram
  A
// \\
B   C
\\ //
  D
"""
nodes = [
    ("My first operation", {"description": "Operation that initialize the workflow."}),
    ("My second operation", {"description": "Compute alpha"}),
    ("My third operation", {"description": "Arrange, organise, sort and filter the data."}),
    ("My fourth operation", {"description": "Present the data to the user."}),
]
graph.add_nodes_from(nodes)
graph.add_edges_from([
    (nodes[0][0], nodes[1][0]),
    (nodes[1][0], nodes[3][0]),
    (nodes[0][0], nodes[2][0]),
    (nodes[2][0], nodes[3][0]),
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


async def node(request: Request) -> Response:
    node_id = request.query_params.get("element")
    if node_id not in graph:
        raise HTTPException(404, "Node not found")
    node = graph.nodes[node_id]
    return templates.TemplateResponse(request, "node_details.html", context={
        "node_info": node.get("description"),
        "predecessors": tuple(graph.predecessors(node_id)),
        "successors": tuple(graph.successors(node_id)),
    })


app = Starlette(debug=True, routes=[
    Mount('/static', StaticFiles(directory='src/static'), name='static'),
    Route('/', homepage),
    Route('/generate', generate),
    Route('/node', node),
])
