from sqlite3 import connect
from typing import List, Tuple, Union
from .models import Node, Tree, get_node_name
from .helper import find_edges, find_node_in_pool, find_subtree_nodes, get_max_depth, get_max_index, get_possible_nodes, sort_by_key, get_total_remaining_capacity, update_depth
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
            depth=0,
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
                new_node.depth = best_fitting_node.depth + 1

                # update best_fitting_node
                best_fitting_node.child_ids.append(new_node.id)
                best_fitting_node.remaining -= 1

                _, cur_tree = self.find_tree(new_node.tree_id)
                cur_tree.node_ids.append(new_node.id)

        # add a node
        self.add_node(new_node)

    def leave(self, node_id: int) -> bool:
        ''' Remove the node from the network, rebuild '''

        # get the current node
        cur_node_index, cur_node = self.find_node(node_id)
        if cur_node is None:
            return False

        # get the number of children of the current node
        number_of_childs = len(cur_node.child_ids)

        # get the tree that has the current node
        cur_tree_id = cur_node.tree_id
        cur_tree_index, cur_tree = self.find_tree(cur_tree_id)

        # check if the current node is the root or not
        is_root = node_id == cur_tree.root_id

        # get all the nodes of the tree
        cur_tree.node_ids.sort()
        cur_tree_nodes: List[Node] = [
            self.nodes[self.find_node(x)[0]] for x in cur_tree.node_ids]

        # divide the tree
        sub_trees = self.divide_tree(cur_node, cur_tree_nodes, is_root)

        # execute the combination
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

                # if the root has more than one child node
                else:
                    self.combine_trees(cur_tree, sub_trees)

                # remove the node from the tree
                cur_tree.node_ids.remove(node_id)
        else:
            # get the parent of the current node
            _, p_node = self.find_node(cur_node.parent_id)
            p_node.child_ids.remove(node_id)

            if number_of_childs == 0:
                p_node.remaining += 1
            else:
                self.combine_trees(cur_tree, sub_trees)

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
        ''' Add a new tree to the network '''

        self.trees.append(new_tree)
        self.max_tree_id += 1

    def add_node(self, new_node: Node):
        ''' Add a new node to the network '''

        self.nodes.append(new_node)
        self.max_node_id += 1

    def find_tree(self, tree_id: int) -> Tuple[int, Union[Tree, None]]:
        ''' Find a tree with a specific identifer '''

        for index, tree_item in enumerate(self.trees):
            if tree_item.id == tree_id:
                return index, self.trees[index]
        return -1, None

    def find_node(self, node_id: int, nodes: List[Node] = []) -> Tuple[int, Union[Node, None]]:
        ''' Find a node in the network or in the list of nodes '''

        if len(nodes) > 0:
            return find_node_in_pool(node_id, nodes)
        else:
            return find_node_in_pool(node_id, self.nodes)

    def get_all_nodes(self, node_ids: List[int]) -> dict:
        ''' Get the information of the nodes '''

        node_ids.sort()
        nodes_info = {}
        for node_id in node_ids:
            _, cur_node = self.find_node(node_id)
            nodes_info[get_node_name(node_id)] = cur_node.capacity
        return nodes_info

    def get_all_edges(self, tree: Tree) -> List[List]:
        ''' Get the list of all the direct edges in the tree '''

        node_ids = tree.node_ids.copy()
        node_ids.remove(tree.root_id)
        remaining_nodes: List[Node] = [
            deepcopy(self.nodes[self.find_node(x)[0]]) for x in node_ids]
        all_edges = []
        find_edges(tree.root_id, remaining_nodes, all_edges)
        return all_edges

    def divide_tree(self, p_node: Node, nodes: List[Node], is_root: bool = True) -> List[List[Node]]:
        ''' Divide the tree after removing the specific node '''

        tree_set = []
        all_descendants = [p_node.id]
        for child_node_id in p_node.child_ids:
            _, child_node = self.find_node(child_node_id, nodes)
            temp_sub_tree = [child_node]
            find_subtree_nodes(child_node_id, nodes, temp_sub_tree)
            tree_set.append(temp_sub_tree)

            for sub_node in temp_sub_tree:
                all_descendants.append(sub_node.id)

        if not is_root:
            remainings = [x for x in nodes if x.id not in all_descendants]
            if len(remainings) > 0:
                tree_set.insert(0, remainings)

        return tree_set

    def combine_trees(self, cur_tree: Tree, sub_trees: List[List[Node]]):
        '''
        Combine the subtrees
        The number of subtrees could be either of 2, 3, and 4.
        But for now, just consider the case that there are two subtrees.
        '''

        if len(sub_trees) == 1:
            return
        else:
            if len(sub_trees) == 2:
                self.combine_two_trees(cur_tree, sub_trees[0], sub_trees[1])
            else:
                # TODO: implement the combination of 3 or 4 sub trees
                pass

    def combine_two_trees(self, cur_tree: Tree, left: List[Node], right: List[Node]):
        ''' Combine the two trees'''

        update_depth(left, left[0].depth)
        update_depth(right, right[0].depth)
        left_node_ids = [x.id for x in left]
        right_node_ids = [x.id for x in right]

        # check if there are any node that has a remaining capacity
        if get_total_remaining_capacity(left) + get_total_remaining_capacity(right) == 0:
            # update the current tree
            cur_tree.root_id = left[0].id
            cur_tree.node_ids = left_node_ids

            # create a new tree
            new_tree = Tree(
                id=self.max_tree_id + 1,
                node_ids=right_node_ids,
                root_id=right[0].id
            )
            self.add_tree(new_tree)
        else:
            # find the connecting node with the smallest depth after combined
            left_connectable_nodes = get_possible_nodes(left)
            update_depth(left_connectable_nodes, get_max_depth(right))
            right_connectable_nodes = get_possible_nodes(right)
            update_depth(right_connectable_nodes, get_max_depth(left))

            left_connectable_nodes.extend(right_connectable_nodes)
            sort_by_key(left_connectable_nodes, "depth", False)

            connecting_node = left_connectable_nodes[0]

            # combine the two
            if connecting_node.id in left_node_ids:
                cur_tree.root_id = left[0].id
                left[0].parent_id = 0
                right[0].parent_id = connecting_node.id
                update_depth(right, connecting_node.depth)
            else:
                cur_tree.root_id = right[0].id
                right[0].parent_id = 0
                left[0].parent_id = connecting_node.id
                update_depth(left, connecting_node.depth)

            connecting_node.remaining -= 1
