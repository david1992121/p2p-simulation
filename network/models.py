from dataclasses import dataclass
from typing import List


def get_node_name(node_id: int) -> str:
    return f"N{node_id}"


@dataclass
class Node:
    '''
    A class represting a node
    A node in the network has the following properties.

    id        : an identifier of the nodes
    capacity  : a maximum number of child nodes, less than 3
    parent_id : an identifier of the parent node
    child_ids : a list of the identifiers of the child nodes
    tree_id   : an identifier of the tree it belongs to
    remaining : a number of nodes that can be further connected as a child
    '''

    id: int
    capacity: int
    parent_id: int
    child_ids: List[int]
    depth: int
    tree_id: int
    remaining: int

    def __str__(self):
        return f"{get_node_name(self.id)} (capacity:{self.capacity})"


@dataclass
class Tree:
    '''
    A class indicating a tree, a hierarchical structure of nodes
    The whold network has several trees, each of which has several nodes

    id         : an identifier of the trees
    node_ids   : identifiers of the nodes the tree has
    root_id    : an identifier of the root node of the tree
    '''

    id: int
    node_ids: List[int]
    root_id: int
