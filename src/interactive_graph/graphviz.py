from io import BytesIO

from networkx import Graph
from networkx.drawing import nx_agraph


def generate_svg(graph: Graph) -> str:  # type: ignore[type-arg]
    agraph = nx_agraph.to_agraph(graph)
    for node in agraph.nodes():
        node.attr["id"] = node
    svg_io = BytesIO()
    agraph.draw(svg_io, format="svg", prog="dot", args="-Nshape=box")
    svg_document = svg_io.getvalue().decode()
    svg_tag_start = svg_document.find("<svg ")
    svg_tag_end = svg_document.find("</svg>", svg_tag_start)
    svg = svg_document[svg_tag_start:svg_tag_end + len("</svg>") + 1]
    return svg
