from typing import List, Tuple, Union
from .models import Node, Tree, get_node_name
from .helper import find_edges, find_subtree_nodes, get_max_index, sort_by_key
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
            # find the best fitting node
            remainings = [node_item.remaining for node_item in self.nodes]
            best_fitting_index = get_max_index(remainings)

            # take the best fitting node
            best_fitting_node = self.nodes[best_fitting_index]

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

                _, cur_tree = self.find_tree(new_node.tree_id)
                cur_tree.node_ids.append(new_node.id)

        # add a node
        self.add_node(new_node)

    def leave(self, node_id: int) -> bool:
        ''' Remove the node from the network, rebuild '''

        cur_node_index, cur_node = self.find_node(node_id)
        if cur_node is None:
            return False

        number_of_childs = len(cur_node.child_ids)
        cur_tree_id = cur_node.tree_id
        cur_tree_index, cur_tree = self.find_tree(cur_tree_id)
        is_root = node_id == cur_tree.root_id

        if is_root:
            # if the root has no child, remove the tree
            if number_of_childs == 0:
                self.trees.pop(cur_tree_index)
            else:
                # if the root has one child node
                if number_of_childs == 1:
                    child_node_id = cur_node.child_ids[0]
                    _, child_node = self.find_node(child_node_id)

                    # set the child as the root of the current tree
                    child_node.parent_id = 0
                    cur_tree.root_id = child_node_id

                # if the root has two child nodes
                elif number_of_childs == 2:
                    cur_node.child_ids.sort()
                    _, first_c_node = self.find_node(cur_node.child_ids[0])
                    _, second_c_node = self.find_node(cur_node.child_ids[1])

                    cur_tree_nodes: List[Node] = [
                        deepcopy(self.nodes[self.find_node(x)[0]]) for x in cur_tree.node_ids]
                    second_sub_tree_nodes: List[int] = []
                    find_subtree_nodes(
                        second_c_node, cur_tree_nodes, second_sub_tree_nodes)

                    first_sub_tree_nodes: List[int] = []
                    find_subtree_nodes(
                        second_c_node, cur_tree_nodes, first_sub_tree_nodes)

                    # if the two child nodes have no remaining capacity, divide the tree into two
                    if first_c_node.remaining == 0 and second_c_node.remaining == 0:
                        # update the current tree
                        cur_tree.root_id = first_c_node.id
                        cur_tree.node_ids = first_sub_tree_nodes

                        # create a new tree with the second node as a root
                        new_tree = Tree(
                            id=self.max_tree_id + 1,
                            node_ids=second_sub_tree_nodes,
                            root_id=second_c_node.id
                        )
                        self.add_tree(new_tree)

                    else:
                        # if the first child has the remaining capacity, make it a root
                        if first_c_node.remaining > 0:
                            cur_tree.root_id = first_c_node.id
                            first_c_node.parent_id = 0
                            second_c_node.parent_id = first_c_node.id
                            first_c_node.remaining -= 1
                        # if the second child has the remaining capacity, make it a root
                        else:
                            cur_tree.root_id = second_c_node.id
                            second_c_node.parent_id = 0
                            first_c_node.parent_id = second_c_node.id
                            second_c_node.remaining -= 1

                # if the root has three child nodes
                else:
                    # TODO: add the logic
                    pass

                # remove the node from the tree
                cur_tree.node_ids.remove(node_id)
        else:
            # get the parent of the current node
            p_node_index, p_node = self.find_node(cur_node.parent_id)

            if number_of_childs == 0:
                p_node.child_ids.remove(node_id)
                p_node.remaining += 1
            else:
                if number_of_childs == 1:
                    _, parent_node = self.find_node(cur_node.parent_id)
                    _, child_node = self.find_node(cur_node.child_ids[0])
                    parent_node.child_ids.remove(cur_node.id)
                    parent_node.child_ids.append(child_node.id)
                    child_node.parent_id = parent_node.id
                elif number_of_childs == 2:
                    # TODO: add the logic
                    pass
                else:
                    # TODO: add the logic
                    pass

            # remove the node from the tree
            cur_tree.node_ids.remove(node_id)

        self.nodes.pop(cur_node_index)
        return True

    def info(self) -> List[dict]:
        ''' Outputs the current network info '''

        network_info = []
        trees = deepcopy(self.trees)
        sort_by_key(trees, "root_id", False)

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

    def find_tree(self, tree_id: int) -> Tuple[int, Union[Tree, None]]:
        for index, tree_item in enumerate(self.trees):
            if tree_item.id == tree_id:
                return index, self.trees[index]
        return -1, None

    def find_node(self, node_id: int) -> Tuple[int, Union[Node, None]]:
        for index, node_item in enumerate(self.nodes):
            if node_item.id == node_id:
                return index, self.nodes[index]
        return -1, None

    def get_all_nodes(self, node_ids: List[int]) -> dict:
        node_ids.sort()
        nodes_info = {}
        for node_id in node_ids:
            _, cur_node = self.find_node(node_id)
            nodes_info[get_node_name(node_id)] = cur_node.capacity
        return nodes_info

    def get_all_edges(self, tree: Tree) -> List[List]:
        node_ids = tree.node_ids.copy()
        node_ids.remove(tree.root_id)
        remaining_nodes: List[Node] = [
            deepcopy(self.nodes[self.find_node(x)[0]]) for x in node_ids]
        all_edges = []
        find_edges(tree.root_id, remaining_nodes, all_edges)
        return all_edges
