from typing import List
from .models import Node, get_node_name
import numpy as np


def find_edges(parent_node_id: int, remaining_nodes: List[Node], all_edges: List[List]):
    ''' Find all the edges from the tree '''

    if len(remaining_nodes) == 0:
        return
    else:
        # get child nodes
        child_nodes = [
            x.id for x in remaining_nodes if x.parent_id == parent_node_id]
        child_nodes.sort()

        # update remaining nodes
        updated_remaining_nodes = [
            x for x in remaining_nodes if x.id not in child_nodes]

        # loop over the child nodes, call the function recursively
        for child_node_id in child_nodes:
            all_edges.append([get_node_name(parent_node_id),
                             get_node_name(child_node_id)])
            find_edges(child_node_id, updated_remaining_nodes, all_edges)


def get_max_index(values: List[int]):
    return np.argmax(values)


def sort_by_key(dict_array: List[dict], key_name: str, reverse: bool):
    dict_array.sort(key=lambda x: getattr(x, key_name), reverse=reverse)
