from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    id: int
    capacity: int
    parent_id: int
    child_ids: List[int]
    remaining: int


@dataclass
class Tree:
    id: int
    nodes: List[int]
    root_id: int
