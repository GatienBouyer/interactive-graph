from starlette import status
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from interactive_graph import visualization, work

templates = Jinja2Templates(directory="src/templates")


def homepage(request: Request) -> Response:
    return templates.TemplateResponse(request, "index.html", context={
        "paragraph": "Lorem ipsum dolor sit amet consectetur adipisicing elit."
    })


def generate(request: Request) -> Response:
    graph_svg = visualization.generate_svg(work.graph)
    return templates.TemplateResponse(
        request,
        "generated.html",
        context={"diagram": graph_svg},
    )


def get_node_id(request: Request) -> str:
    node_id = request.query_params["element"]
    if node_id not in work.graph:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Node not found")
    return node_id


def node(request: Request) -> Response:
    node_id = get_node_id(request)
    node = work.graph.nodes[node_id]
    return templates.TemplateResponse(request, "node_details.html", context={
        "node_id": node_id,
        "node_info": node.get("description"),
        "predecessors": tuple(work.graph.predecessors(node_id)),
        "successors": tuple(work.graph.successors(node_id)),
    })


def run(request: Request) -> Response:
    node_id = get_node_id(request)
    if not work.can_do_operation(node_id):
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    task = BackgroundTask(work.do_operation, node_id)
    return Response("", headers={"HX-Refresh": "true"}, background=task)


app = Starlette(debug=True, routes=[
    Mount('/static', StaticFiles(directory='src/static'), name='static'),
    Route('/', homepage),
    Route('/generate', generate),
    Route('/node', node),
    Route('/run', run),
])
