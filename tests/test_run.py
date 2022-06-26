from network.crud import P2PNetwork
import pathlib
import json
import os
from glob import glob


def read_test_cases():
    ''' Read JSON files from the directory and return data for testing '''

    test_cases = []
    folder_path = pathlib.Path(__file__).parent.resolve()
    folder_path = os.path.join(folder_path, "cases")
    test_files = glob(folder_path + r"\*.json")

    for test_file in test_files:
        with open(test_file) as f:
            case_data = json.load(f)
            test_cases.append(case_data)
    return test_cases


class TestP2PNetwork:
    '''
    A class for unit testing the P2PNetwork
    '''

    def setup_method(self, method):
        ''' Executes initialization before every test '''

        self.initialize_network()

    def initialize_network(self):
        ''' Initialize with an empty network '''

        self.network = P2PNetwork()

    def test_cases(self):
        ''' Test the sample cases defined in the JSON files '''

        test_cases = read_test_cases()
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

        # network_data = self.execute_multiple_join([1, 0, 2, 1, 3, 2])
        # print(json.dumps(network_data))

    def test_minimal_case(self):
        ''' Test the minimal case with two nodes '''

        self.first_join()
        self.second_join()

    def first_join(self):
        ''' Add the first node with the capacity of 1 '''

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

        self.network.info()

    def second_join(self):
        ''' Add the second node with the capacity of 0 '''

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
