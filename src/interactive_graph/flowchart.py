from typing import Protocol


class Graph(Protocol):
    nodes: list[str]
    edges: list[tuple[int, int]]


def generate_script(graph: Graph) -> str:
    script = ""
    for i, node in enumerate(graph.nodes):
        script += f"node{i}=>operation: {node}\n"
    script += "\n"
    for source, target in graph.edges:
        script += f"node{source}{'(right)' if target == 2 else '(bottom)'}->node{target}\n"
    return script
