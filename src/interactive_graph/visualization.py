from io import BytesIO

from networkx import Graph
from networkx.drawing import nx_agraph
from pygraphviz import AGraph  # type: ignore[import-untyped]

from interactive_graph.work import NodeState

status_to_colors = {
    NodeState.READY: ("#DDDDDD", "#DDDDDD"),
    NodeState.IN_PROGRESS: ("#3333DD", "#3333DD"),
    NodeState.DONE: ("#33DD33", "#33DD33"),
    NodeState.FAILED: ("#DD3333", "#DD3333"),
    NodeState.UNAVAILABLE: ("#888888", "#888888"),
}


def prepare_node_attributes(graph: AGraph) -> None:
    for node in graph.nodes():
        node.attr["id"] = node
        status = node.attr["status"]
        node.attr["style"] = "filled"
        fillcolor, bordercolor = status_to_colors[status]
        node.attr["fillcolor"] = fillcolor
        node.attr["color"] = bordercolor


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
