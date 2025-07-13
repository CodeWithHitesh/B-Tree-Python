import bisect

class BTreeNode:
    def __init__(self, min_degree: int, is_leaf: bool) -> None:
        """
        Initialize a B-Tree node.

        :param min_degree: Minimum degree (defines the range for number of keys)
        :param is_leaf: Boolean, True if node is a leaf. Otherwise, False.
        """
        self.keys = []
        self.min_degree = min_degree
        self.children = []
        self.is_leaf = is_leaf

    def insert_non_full(self, key: int) -> None:
        """
        Insert a key into this non-full node using binary search.
        If the node is a leaf, it inserts the key directly.
        If the node is not a leaf, it finds the appropriate child to insert the key into.
        If the child is full, it splits the child and then inserts the key.
        This method maintains the B-Tree properties.

        :param key: The key to insert.
        :return: None
        """
        if self.is_leaf:
            key_index = self.get_key_index(key)
            self.keys.insert(key_index, key)
        else:
            child_index = self.get_key_index(key)
            if self.children[child_index].is_full():
                self.split_child(child_index)
                if key > self.keys[child_index]:
                    child_index += 1
            self.children[child_index].insert_non_full(key)

    def is_full(self) -> bool:
        """
        Check if the node is full (i.e., contains 2*min_degree - 1 keys).

        :return: True if node is full, False otherwise.
        """
        return len(self.keys) == (2 * self.min_degree) - 1

    def split_child(self, child_index: int) -> None:
        """
        Split the full child at 'child_index' into two nodes and move the middle key up.

        :param child_index: Index of the child to split.
        :return: None
        """
        # make a new sibling node which will hold the right half of the keys
        existing_child = self.children[child_index]
        new_child = BTreeNode(self.min_degree, existing_child.is_leaf)
        
        # Move the last min_degree - 1 keys from existing_child to new_child
        middle_key = existing_child.keys[self.min_degree - 1]
        new_child.keys = existing_child.keys[self.min_degree:]
        existing_child.keys = existing_child.keys[:self.min_degree - 1]
        
        # If existing_child is not a leaf, move the last min_degree children to new_child
        if not existing_child.is_leaf:
            new_child.children = existing_child.children[self.min_degree:]
            existing_child.children = existing_child.children[:self.min_degree]
        
        # Insert the new child into the parent node
        self.children.insert(child_index + 1, new_child)
        
        # Insert the middle key into the parent node        
        self.keys.insert(child_index, middle_key)

    def traverse(self) -> None:
        """
        Traverse the subtree rooted at this node and print keys in order.

        :return: None
        """
        if self.is_leaf:
            for key in self.keys:
                print(key, end=' ')
        else:
            for i in range(len(self.keys)):
                self.children[i].traverse()
                print(self.keys[i], end=' ')
            self.children[len(self.keys)].traverse()  # Last child traversal

    def search(self, key: int) -> "BTreeNode":
        """
        Search for a key in the subtree rooted at this node using binary search.

        :param key: The key to search for.
        :return: The node containing the key, or None if not found.
        """
        if not self.keys:
            return None

        idx = self.get_key_index(key)

        if idx < len(self.keys) and self.keys[idx] == key:
            return self  # Key found

        if self.is_leaf:
            return None  # Not found in leaf

        return self.children[idx].search(key)  # Recurse into child

    def get_key_index(self, key: int) -> int:
        """
        Get the first index in self.keys where key >= self.keys[idx].

        :param key: The key to find.
        :return: Index of the key or where it should be.
        """
        return bisect.bisect_left(self.keys, key)

    def get_predecessor(self) -> int:
        """
        Get the predecessor key (rightmost key) from the subtree rooted at this node.

        :return: The predecessor key.
        """
        node = self
        while not node.is_leaf:
            node = node.children[-1]
        return node.keys[-1]

    def get_successor(self) -> int:
        """
        Get the successor key (leftmost key) from the subtree rooted at this node.

        :return: The successor key.
        """
        node = self
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]

    def borrow_from_prev(self, idx: int) -> None:
        """
        Borrow a key from the previous sibling and move it to the child at idx.

        :param idx: Index of the child to borrow for.
        :return: None
        """
        child = self.children[idx]
        sibling = self.children[idx - 1]
        
        child.keys.insert(0, self.keys[idx - 1])
        
        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())
        
        self.keys[idx - 1] = sibling.keys.pop()

    def borrow_from_next(self, idx: int) -> None:
        """
        Borrow a key from the next sibling and move it to the child at idx.

        :param idx: Index of the child to borrow for.
        :return: None
        """
        child = self.children[idx]
        sibling = self.children[idx + 1]
        
        child.keys.append(self.keys[idx])
        
        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))
        
        self.keys[idx] = sibling.keys.pop(0)

    def merge(self, idx: int) -> None:
        """
        Merge the child at idx with its next sibling.

        :param idx: Index of the child to merge.
        :return: None
        """
        child = self.children[idx]
        sibling = self.children[idx + 1]
        
        child.keys.append(self.keys.pop(idx))
        child.keys.extend(sibling.keys)
        
        if not child.is_leaf:
            child.children.extend(sibling.children)
        
        self.children.pop(idx + 1)

    def fill(self, idx: int) -> None:
        """
        Ensure that the child node at idx has at least t keys.

        :param idx: Index of the child to fill.
        :return: None
        """
        if idx != 0 and len(self.children[idx - 1].keys) >= self.min_degree:
            self.borrow_from_prev(idx)
        
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= self.min_degree:
            self.borrow_from_next(idx)
        
        else:
            if idx != len(self.keys):
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def remove_from_leaf(self, idx: int) -> None:
        """
        Remove the key at idx from a leaf node.

        :param idx: Index of the key to remove.
        :return: None
        """
        self.keys.pop(idx)

    def remove_from_non_leaf(self, idx: int) -> None:
        """
        Remove the key at idx from a non-leaf node.

        :param idx: Index of the key to remove.
        :return: None
        """
        key = self.keys[idx]
        
        if len(self.children[idx].keys) >= self.min_degree:
            pred = self.children[idx].get_predecessor()
            self.keys[idx] = pred
            self.children[idx].delete(pred)
        
        elif len(self.children[idx + 1].keys) >= self.min_degree:
            succ = self.children[idx + 1].get_successor()
            self.keys[idx] = succ
            self.children[idx + 1].delete(succ)
        
        else:
            self.merge(idx)
            self.children[idx].delete(key)

    def delete(self, key: int) -> None:
        """
        Delete a key from the subtree rooted at this node.

        :param key: The key to delete.
        :return: None
        """
        idx = self.get_key_index(key)

        if idx < len(self.keys) and self.keys[idx] == key:
            if self.is_leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        
        else:
            if self.is_leaf:
                return  # Key not found
            
            flag = (idx == len(self.keys))
            
            if len(self.children[idx].keys) < self.min_degree:
                self.fill(idx)
            
            # If the last child was merged, it may have moved, so recurse accordingly
            if flag and idx > len(self.keys):
                self.children[idx - 1].delete(key)
            
            else:
                self.children[idx].delete(key)

class BTree:
    def __init__(self, min_degree: int) -> None:
        """
        Initialize a B-Tree.

        :param min_degree: Minimum degree (defines the range for number of keys)
        :raises ValueError: If ``min_degree`` is less than 2.
        """
        if min_degree < 2:
            raise ValueError("min_degree must be at least 2")

        self.root = BTreeNode(min_degree, True)
        self.min_degree = min_degree

    def traverse(self) -> None:
        """
        Traverse the entire B-Tree and print all keys in order.

        :return: None
        """
        if self.root:
            self.root.traverse()

    def search(self, key: int) -> "BTreeNode":
        """
        Search for a key in the B-Tree.

        :param key: The key to search for.
        :return: The node containing the key, or None if not found.
        """
        if not self.root:
            return None
        return self.root.search(key)

    def insert(self, key: int) -> None:
        """
        Insert a new key into the B-Tree, handling root splits if necessary.

        :param key: The key to insert.
        :return: None
        """
        if self.root.is_full():
            new_root = BTreeNode(self.min_degree, False)
            new_root.children.append(self.root)
            new_root.split_child(0)
            new_root.insert_non_full(key)
            self.root = new_root
        else:
            self.root.insert_non_full(key)

    def delete(self, key: int) -> None:
        """
        Delete a key from the B-Tree.

        :param key: The key to delete.
        :return: None
        """
        if not self.root:
            return
        self.root.delete(key)
        # Shrink the height of the tree if the root has no keys and is not a leaf
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]
        # If the root is a leaf and has no keys, keep the empty root node

# Driver program
if __name__ == '__main__':
    t = BTree(3)
    print("=== B-Tree Demo ===\n")

    print("Inserting keys: 10, 20, 5, 6, 12, 30, 7, 17")
    for key in [10, 20, 5, 6, 12, 30, 7, 17]:
        t.insert(key)

    print("\nTraversal of the constructed tree:")
    t.traverse()
    print("\n")

    for k_to_find in [6, 15]:
        result = "Present" if t.search(k_to_find) else "Not Present"
        print(f"Search for {k_to_find}: {result}")

    print("\nDeleting key 6...")
    t.delete(6)
    print("Traversal after deletion:")
    t.traverse()
    print()