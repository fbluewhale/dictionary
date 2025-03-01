class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end_of_word = True

    def search_prefix(self, prefix: str):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def collect_words(self, node, prefix: str):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for ch, child in node.children.items():
            words.extend(self.collect_words(child, prefix + ch))
        return words

    def starts_with(self, prefix: str):
        node = self.search_prefix(prefix)
        if not node:
            return []
        return self.collect_words(node, prefix)
