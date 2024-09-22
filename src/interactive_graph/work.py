"""
Define the graph and the methods to interact with the graph.
"""

from enum import StrEnum
from pathlib import Path
from random import random
from time import sleep

import yaml
from networkx import DiGraph
from networkx.readwrite import json_graph

GRAPH_YAML = Path(__file__).parent / "graph.yaml"


class NodeAttr(StrEnum):
    """Attributes of nodes."""
    STATUS = "status"
    NAME = "name"
    DESC = "description"


class NodeState(StrEnum):
    """Values of the status attribute of nodes."""
    READY = "ready"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
    UNAVAILABLE = "unavailable"


def import_graph() -> "DiGraph[str]":
    """Load graph from the yaml file."""
    with GRAPH_YAML.open() as file:
        graph_data = yaml.safe_load(file)
    digraph: "DiGraph[str]" = json_graph.node_link_graph(graph_data)
    return digraph


graph = import_graph()


class NotReadyError(Exception):
    """Error raised when an operation can't be run because of its state."""


def can_do_operation(node_id: str) -> bool:
    """Check if the node state allows starting the operation of the node."""
    ok_states = (NodeState.READY, NodeState.DONE, NodeState.FAILED)
    return graph.nodes[node_id][NodeAttr.STATUS] in ok_states


def do_operation(node_id: str) -> None:
    """Do the operation associate with the node and update its status.
    If the node isn't ready, raise NotReadyError.
    """
    node = graph.nodes[node_id]
    if not can_do_operation(node_id):
        raise NotReadyError()
    node[NodeAttr.STATUS] = NodeState.IN_PROGRESS
    invalidate_all_successors(node_id)
    sleep(2)
    if random() < 0.85:
        node[NodeAttr.STATUS] = NodeState.DONE
        update_node_done(node_id)
        print(f"Success for the operation of the node {node_id}.")
    else:
        node[NodeAttr.STATUS] = NodeState.FAILED
        print(f"Operation for node {node_id} failed.")


def update_node_done(node_id: str) -> None:
    """Mark ready the successors that can be,
    i.e. no more of their predecessors are not done.
    """
    for successor in graph.successors(node_id):
        if all(
            graph.nodes[pred][NodeAttr.STATUS] == NodeState.DONE
            for pred in graph.predecessors(successor)
        ):
            graph.nodes[successor][NodeAttr.STATUS] = NodeState.READY


def invalidate_all_successors(node_id: str) -> None:
    """Mark unavailable all successors (recursive) of the node."""
    for successor in graph.successors(node_id):
        graph.nodes[successor][NodeAttr.STATUS] = NodeState.UNAVAILABLE
        invalidate_all_successors(successor)
