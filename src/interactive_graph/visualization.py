"""
Functions to draw the graph.
"""

from io import BytesIO

from networkx import Graph
from networkx.drawing import nx_agraph
from pygraphviz import AGraph  # type: ignore[import-untyped]

from interactive_graph.work import NodeAttr, NodeState

status_to_colors = {
    NodeState.READY: ("#DDDDDD", "#DDDDDD"),
    NodeState.IN_PROGRESS: ("#3333DD", "#3333DD"),
    NodeState.DONE: ("#33DD33", "#33DD33"),
    NodeState.FAILED: ("#DD3333", "#DD3333"),
    NodeState.UNAVAILABLE: ("#888888", "#888888"),
}


def _prepare_node_attributes(agraph: AGraph) -> None:
    """Update the node attributes to customize the graphviz output."""
    for node in agraph.nodes():
        node.attr["id"] = node
        status = node.attr[NodeAttr.STATUS]
        node.attr["label"] = node.attr[NodeAttr.NAME]
        node.attr["style"] = "filled"
        fillcolor, bordercolor = status_to_colors[status]
        node.attr["fillcolor"] = fillcolor
        node.attr["color"] = bordercolor


def _agraph_to_svg(agraph: AGraph) -> str:
    """Generate the svg from the graph."""
    svg_io = BytesIO()
    agraph.draw(svg_io, format="svg", prog="dot", args="-Nshape=box")
    svg_document = svg_io.getvalue().decode()

    # Remove the xml and doctype headers
    svg_tag_start = svg_document.find("<svg ")
    svg_tag_end = svg_document.find("</svg>", svg_tag_start)
    svg = svg_document[svg_tag_start:svg_tag_end + len("</svg>") + 1]
    return svg


def generate_svg(graph: Graph) -> str:  # type: ignore[type-arg]
    """Generate the svg visualization of a networkx graph using graphviz."""
    agraph = nx_agraph.to_agraph(graph)
    _prepare_node_attributes(agraph)
    svg = _agraph_to_svg(agraph)
    return svg
