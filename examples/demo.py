from btree import BTree

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
