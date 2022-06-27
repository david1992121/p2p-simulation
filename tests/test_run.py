import unittest
from network.crud import P2PNetwork
import pathlib
import json
import os
from glob import glob
from network.models import Node, Tree


class TestP2PNetwork(unittest.TestCase):
    '''
    A class for unit testing the P2PNetwork
    '''

    def setUp(self):
        ''' Executes initialization before every test '''

        self.initialize_network()

    def initialize_network(self):
        ''' Initialize with an empty network '''

        self.network = P2PNetwork()

    def test_cases(self):
        ''' Test the sample cases defined in the JSON files '''

        test_cases = []
        folder_path = pathlib.Path(__file__).parent.resolve()
        folder_path = os.path.join(folder_path, "cases")
        test_files = glob(folder_path + r"\*.json")

        for test_file in test_files:
            with open(test_file) as f:
                case_data = json.load(f)
                test_cases.append(case_data)

        for case_data in test_cases:
            self.initialize_network()
            simulation = case_data.get("case", None)
            expected = case_data.get("result", None)
            if simulation:
                for action_item in simulation:
                    if "join" in action_item.keys():
                        self.network.join(
                            action_item["join"].get("capacity", 0))
                    if "leave" in action_item.keys():
                        self.network.leave(action_item["leave"].get("id", 0))

            network_structure = json.dumps(self.network.info())
            expected_structure = json.dumps(expected)
            assert network_structure == expected_structure

    def test_minimal_case(self):
        ''' Test the minimal case with two nodes '''

        # Add the first node with the capacity of 1

        self.network.join(1)

        assert len(self.network.trees) == 1
        assert len(self.network.nodes) == 1

        tree = self.network.trees[0]
        node = self.network.nodes[0]

        assert tree.id == 1
        assert tree.root_id == node.id
        assert tree.node_ids == [node.id]

        assert node.id == 1
        assert node.parent_id == 0
        assert node.tree_id == tree.id
        assert node.capacity == 1
        assert node.remaining == 1

        # Add the second node with the capacity of 0

        self.network.join(0)

        assert len(self.network.trees) == 1
        assert len(self.network.nodes) == 2
        tree = self.network.trees[0]

        assert tree.node_ids == [1, 2]

        _, second_node = self.network.find_node(2)
        _, first_node = self.network.find_node(1)
        assert second_node.parent_id == first_node.id
        assert first_node.child_ids == [second_node.id]
        assert first_node.remaining == 0

        assert second_node.capacity == 0
        assert second_node.remaining == 0

    def test_add_node(self):
        new_node = Node(1, 0, 0, [], 1, 0)
        self.network.add_node(new_node)
        assert len(self.network.nodes) == 1

    def test_add_tree(self):
        new_node = Node(1, 0, 0, [], 1, 0)
        self.network.add_node(new_node)
        new_tree = Tree(1, [1], 1)
        self.network.add_tree(new_tree)
        assert len(self.network.trees) == 1

    def test_find_tree(self):
        tree_index, tree = self.network.find_tree(1)
        assert tree_index == -1
        assert tree is None

    def test_find_node(self):
        node_index, node = self.network.find_node(1)
        assert node_index == -1
        assert node is None

    def test_get_all_nodes(self):
        self.network.join(1)
        all_nodes = self.network.get_all_nodes([1])
        assert "N1" in all_nodes.keys()
        assert all_nodes["N1"] == 1

    def test_get_all_edges(self):
        self.network.join(1)
        assert len(self.network.trees) == 1
        all_nodes = self.network.get_all_edges(self.network.trees[0])
        assert len(all_nodes) == 0
