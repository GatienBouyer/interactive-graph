from enum import StrEnum
from pathlib import Path
from random import random
from time import sleep

import yaml
from networkx import DiGraph
from networkx.readwrite import json_graph

GRAPH_YAML = Path(__file__).parent / "graph.yaml"


class NodeState(StrEnum):
    READY = "ready"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
    UNAVAILABLE = "unavailable"


def import_graph() -> "DiGraph[str]":
    """Load graph from the yaml file."""
    with GRAPH_YAML.open() as file:
        graph_data = yaml.safe_load(file)
    graph: "DiGraph[str]" = json_graph.node_link_graph(graph_data)
    return graph


graph = import_graph()


class NotReadyError(Exception):
    pass


def can_do_operation(node_id: str) -> bool:
    return graph.nodes[node_id]["status"] in (NodeState.READY, NodeState.DONE, NodeState.FAILED)


def do_operation(node_id: str) -> None:
    """Do the operation associate with the node and update its status.

    If the node isn't ready, raise NotReadyError.
    """
    node = graph.nodes[node_id]
    if not can_do_operation(node_id):
        raise NotReadyError()
    node["status"] = NodeState.IN_PROGRESS
    invalidate_all_successors(node_id)
    sleep(2)
    if random() < 0.85:
        node["status"] = NodeState.DONE
        update_node_done(node_id)
        print(f"Success for the operation of the node {node_id}.")
    else:
        node["status"] = NodeState.FAILED
        print(f"Operation for node {node_id} failed.")


def update_node_done(node_id: str) -> None:
    """Mark ready the successors that can be,
    i.e. no more of their predecessors are not done."""
    for successor in graph.successors(node_id):
        if all(graph.nodes[pred]["status"] == NodeState.DONE for pred in graph.predecessors(successor)):
            graph.nodes[successor]["status"] = NodeState.READY


def invalidate_all_successors(node_id: str) -> None:
    for successor in graph.successors(node_id):
        graph.nodes[successor]["status"] = NodeState.UNAVAILABLE
        invalidate_all_successors(successor)
