from lib import Trie
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