from pathlib import Path

import yaml
from networkx import DiGraph
from networkx.readwrite import json_graph

GRAPH_YAML = Path(__file__).parent / "graph.yaml"


def import_graph() -> "DiGraph[str]":
    with GRAPH_YAML.open() as file:
        graph_data = yaml.safe_load(file)
    graph: "DiGraph[str]" = json_graph.node_link_graph(graph_data)
    return graph
