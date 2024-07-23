from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable

T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: dict[T, int] = field(default_factory=dict)
    is_end: bool = False

class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))
        self.unique_nodes = 1  # Start counting from the root node

    def push(self, seq: Iterable[T]) -> None:
        current_node_index = 0

        for element in seq:
            if element in self[current_node_index].children:
                current_node_index = self[current_node_index].children[element]
            else:
                new_node_index = len(self)
                new_node = TrieNode(body=element)
                self.append(new_node)
                self[current_node_index].children[element] = new_node_index
                current_node_index = new_node_index
                self.unique_nodes += 1  # Increase count of unique nodes

        self[current_node_index].is_end = True

    def search(self, seq: Iterable[T]) -> bool:
        current_node_index = 0

        for element in seq:
            if element not in self[current_node_index].children:
                return False
            current_node_index = self[current_node_index].children[element]

        return self[current_node_index].is_end

    def starts_with(self, prefix: Iterable[T]) -> bool:
        current_node_index = 0

        for element in prefix:
            if element not in self[current_node_index].children:
                return False
            current_node_index = self[current_node_index].children[element]

        return True

    def __repr__(self) -> str:
        def node_repr(node_index: int, level: int = 0) -> str:
            node = self[node_index]
            indent = "  " * level
            children_repr = ''.join(node_repr(child_index, level + 1) for child_index in node.children.values())
            return f"{indent}Node(body={node.body}, is_end={node.is_end})\n{children_repr}"

        return node_repr(0)


import sys

def main() -> None:
    input = sys.stdin.read
    data = input().split()
    
    num_words = int(data[0])
    words = data[1:]
    
    trie = Trie[str]()
    
    for word in words:
        trie.push(word)
    
    print(trie.unique_nodes)
    

if __name__ == "__main__":
    main()