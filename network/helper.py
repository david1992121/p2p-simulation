from typing import List, Union, Tuple
from .models import Node, Tree, get_node_name
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


def find_node_in_pool(node_id: int, pool: List[Node]) -> Tuple[int, Union[Node, None]]:
    for index, node_item in enumerate(pool):
        if node_item.id == node_id:
            return index, pool[index]
    return -1, None


def find_subtree_nodes(root_node_id: int, remaining_nodes: List[Node], all_nodes: List[Node]):
    ''' Find all the nodes of the subtree '''

    if len(remaining_nodes) == 0:
        return
    else:
        # get child nodes
        child_nodes = [
            x.id for x in remaining_nodes if x.parent_id == root_node_id]
        child_nodes.sort()

        if len(child_nodes) == 0:
            return

        # update remaining nodes
        updated_remaining_nodes = [
            x for x in remaining_nodes if x.id not in child_nodes]

        for child_node_id in child_nodes:
            _, child_node = find_node_in_pool(child_node_id, remaining_nodes)
            all_nodes.append(child_node)
            find_subtree_nodes(
                child_node_id, updated_remaining_nodes, all_nodes)


def get_max_index(values: List[int]):
    return np.argmax(values)


def sort_by_key(dict_array: Union[Node, Tree], key_name: str, reverse: bool):
    dict_array.sort(key=lambda x: getattr(x, key_name), reverse=reverse)


def get_total_remaining_capacity(nodes: List[Node]) -> bool:
    remainings = [x.remaining for x in nodes]
    return np.sum(remainings)


def update_depth(nodes: List[Node], offset: int):
    for node in nodes:
        node.depth += offset


def get_possible_nodes(nodes: List[Node]) -> List[Node]:
    return [x for x in nodes if x.remaining > 0]


def get_max_depth(nodes: List[Node]) -> int:
    depths = [x.depth for x in nodes]
    return np.max(depths)
