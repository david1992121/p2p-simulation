import unittest
from typing import List
from network.models import Node
from network.helper import *


class TestHelper(unittest.TestCase):
    def setUp(self):
        self.nodes: List[Node] = [
            Node(1, 3, 0, [2, 3, 4], 1, 1),
            Node(2, 1, 1, [4], 1, 0),
            Node(3, 0, 1, [], 1, 0),
            Node(4, 1, 2, [], 1, 0)
        ]

    def test_find_edges(self):
        all_edges = []
        find_edges(1, self.nodes, all_edges)
        assert len(all_edges) == 3
        assert ["N1", "N2"] in all_edges
        assert ["N1", "N3"] in all_edges
        assert ["N2", "N4"] in all_edges

    def test_subtree_nodes(self):
        all_nodes = []
        find_subtree_nodes(1, self.nodes, all_nodes)
        assert len(all_nodes) == 3
        assert all_nodes == [2, 4, 3]

    def test_get_max_index(self):
        assert get_max_index([2, 4, 5, 1]) == 2
        assert get_max_index([2, 4, 4, 1]) == 1

    def test_sort_by_key(self):
        sort_by_key(self.nodes, "capacity", False)
        assert self.nodes[0].id == 3
        assert self.nodes[-1].id == 1
