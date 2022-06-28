import unittest
from typing import List
from network.models import Node
from network.helper import *


class TestHelper(unittest.TestCase):
    def setUp(self):
        self.nodes: List[Node] = [
            Node(1, 3, 0, [2, 3], 0, 1, 1),
            Node(2, 1, 1, [4], 1, 1, 0),
            Node(3, 0, 1, [], 1, 1, 0),
            Node(4, 1, 2, [], 2, 1, 0)
        ]

    def test_find_edges(self):
        all_edges = []
        find_edges(1, self.nodes, all_edges)
        assert len(all_edges) == 3
        assert ["N1", "N2"] in all_edges
        assert ["N1", "N3"] in all_edges
        assert ["N2", "N4"] in all_edges

    def test_find_node_in_pool(self):
        index, node = find_node_in_pool(2, self.nodes)
        assert index == 1
        assert node.id == 2

    def test_subtree_nodes(self):
        all_nodes: List[Node] = []
        find_subtree_nodes(1, self.nodes, all_nodes)
        assert len(all_nodes) == 3
        all_node_ids = [x.id for x in all_nodes]
        assert all_node_ids == [2, 4, 3]

    def test_get_max_index(self):
        assert get_max_index([2, 4, 5, 1]) == 2
        assert get_max_index([2, 4, 4, 1]) == 1

    def test_sort_by_key(self):
        sort_by_key(self.nodes, "capacity", False)
        assert self.nodes[0].id == 3
        assert self.nodes[-1].id == 1

    def test_check_capacity(self):
        assert get_total_remaining_capacity(self.nodes) == 1

    def test_get_possible_nodes(self):
        assert len(get_possible_nodes(self.nodes)) == 1

    def test_get_max_depth(self):
        assert get_max_depth(self.nodes) == 2
