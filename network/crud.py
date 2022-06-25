from typing import List
from .models import Node, Tree, get_node_name
from .helper import find_edges
from copy import deepcopy


class P2PNetwork():
    '''
    A network of the system
    It has a list of all the nodes, and a list of all the trees
    It has the following three main methods

    join  :  deals with a new connection of a node
    leave :  removes the node, and rebuild the network
    info  :  returns the whole structure of the current network
    '''

    def __init__(self):
        self.nodes: List[Node] = []
        self.trees: List[Tree] = []
        self.max_node_id = 0
        self.max_tree_id = 0

    def join(self, capacity: int):
        ''' Add a new node with capacity into the network '''

        # default node to be created
        new_node = Node(
            id=self.max_node_id + 1,
            capacity=capacity,
            parent_id=0,
            child_ids=[],
            tree_id=self.max_tree_id + 1,
            remaining=capacity
        )

        # default tree to be created
        new_tree = Tree(
            id=self.max_tree_id + 1,
            node_ids=[new_node.id],
            root_id=new_node.id
        )

        # if there's no node in the network, just add a new node and tree
        if len(self.nodes) == 0:
            self.add_tree(new_tree)
        else:
            # take the best fitting node
            best_fitting_node = self.nodes[0]

            if best_fitting_node.remaining == 0:
                # if the best fitting node has no capacity, add a new node and tree
                self.add_tree(new_tree)
            else:
                # if the best fitting node has capacity, set a new node as it's child
                new_node.parent_id = best_fitting_node.id
                new_node.tree_id = best_fitting_node.tree_id

                # update best_fitting_node
                best_fitting_node.child_ids.append(new_node.id)
                best_fitting_node.remaining -= 1

                cur_tree_index = self.find_tree_index(new_node.tree_id)
                self.trees[cur_tree_index].node_ids.append(new_node.id)

        # add a node
        self.add_node(new_node)
        # print("Before sorting...")
        # print(self.nodes)

        # sort the nodes in the descending based on the remaining capacity
        self.sort_by_key("remaining", True)
        # print("After sorting...")
        # print(self.nodes)

    def leave(self, node_id: int):
        ''' Remove the node from the network, rebuild '''

        pass

    def info(self) -> List[dict]:
        ''' Outputs the current network info '''

        network_info = []
        for tree in self.trees:
            tree_info = {}

            # get all nodes
            tree_info["nodes"] = self.get_all_nodes(tree.node_ids)

            # get all edges
            tree_info["edges"] = self.get_all_edges(tree)

            network_info.append(tree_info)
        return network_info

    def add_tree(self, new_tree: Tree):
        self.trees.append(new_tree)
        self.max_tree_id += 1

    def add_node(self, new_node: Node):
        self.nodes.append(new_node)
        self.max_node_id += 1

    def sort_by_key(self, key_name: str, reverse: bool):
        self.nodes.sort(key=lambda x: getattr(x, key_name), reverse=reverse)

    def find_tree_index(self, tree_id: int) -> int:
        for index, tree_item in enumerate(self.trees):
            if tree_item.id == tree_id:
                return index
        return -1

    def find_node_index(self, node_id: int) -> int:
        for index, node_item in enumerate(self.nodes):
            if node_item.id == node_id:
                return index
        return -1

    def get_all_nodes(self, node_ids: List[int]) -> dict:
        node_ids.sort()
        nodes_info = {}
        for node_id in node_ids:
            nodes_info[get_node_name(node_id)] = self.nodes[self.find_node_index(
                node_id)].capacity
        return nodes_info

    def get_all_edges(self, tree: Tree) -> List[List]:
        node_ids = tree.node_ids.copy()
        node_ids.remove(tree.root_id)
        remaining_nodes: List[Node] = [
            deepcopy(self.nodes[self.find_node_index(x)]) for x in node_ids]
        all_edges = []
        find_edges(tree.root_id, remaining_nodes, all_edges)
        return all_edges
