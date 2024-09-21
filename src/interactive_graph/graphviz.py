from io import BytesIO

from networkx import Graph
from networkx.drawing import nx_agraph
from pygraphviz import AGraph  # type: ignore[import-untyped]

status_to_color = {
    "done": "#33DD33",
    "failed": "#DD3333",
    "ready": "#DDDDDD",
    # "unavailable": "",
}


def prepare_node_attributes(graph: AGraph) -> None:
    for node in graph.nodes():
        node.attr["id"] = node
        status = node.attr["status"]
        if status != "unavailable":
            node.attr["style"] = "filled"
            node.attr["color"] = status_to_color[status]


def generate_svg(graph: Graph) -> str:  # type: ignore[type-arg]
    agraph = nx_agraph.to_agraph(graph)
    prepare_node_attributes(agraph)
    svg_io = BytesIO()
    agraph.draw(svg_io, format="svg", prog="dot", args="-Nshape=box")
    svg_document = svg_io.getvalue().decode()
    svg_tag_start = svg_document.find("<svg ")
    svg_tag_end = svg_document.find("</svg>", svg_tag_start)
    svg = svg_document[svg_tag_start:svg_tag_end + len("</svg>") + 1]
    return svg
