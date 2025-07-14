import unittest
from io import StringIO
from contextlib import redirect_stdout
import sys
from btree import BTree

class TestBTree(unittest.TestCase):
    """Unit tests for the BTree class."""

    def setUp(self):
        """Set up a BTree with sample keys before each test."""
        self.btree = BTree(3)
        for key in [10, 20, 5, 6, 12, 30, 7, 17]:
            self.btree.insert(key)

    def test_insert_and_traverse(self):
        """Test in-order traversal after multiple insertions."""
        captured_output = StringIO()
        sys.stdout = captured_output
        self.btree.traverse()
        sys.stdout = sys.__stdout__
        result = captured_output.getvalue().strip()
        self.assertEqual(result, "5 6 7 10 12 17 20 30")

    def test_search_found(self):
        """Test searching for an existing key."""
        self.assertIsNotNone(self.btree.search(6))

    def test_search_not_found(self):
        """Test searching for a non-existing key."""
        self.assertIsNone(self.btree.search(100))

    def test_delete_leaf(self):
        """Test deleting a leaf key."""
        self.btree.delete(6)
        self.assertIsNone(self.btree.search(6))

    def test_delete_internal(self):
        """Test deleting an internal (non-leaf) key."""
        self.btree.delete(10)
        self.assertIsNone(self.btree.search(10))

    def test_delete_root(self):
        """Test deleting all keys, resulting in an empty tree (root should be empty leaf node)."""
        for key in [5, 6, 7, 10, 12, 17, 20, 30]:
            self.btree.delete(key)
        self.assertIsNotNone(self.btree.root)
        self.assertTrue(self.btree.root.is_leaf)
        self.assertEqual(len(self.btree.root.keys), 0)

    def test_delete_nonexistent_key(self):
        """Test deleting a key that does not exist (should not raise error)."""
        captured_output = StringIO()
        try:
            self.btree.delete(999)
            with redirect_stdout(captured_output):
                self.btree.traverse()
        except Exception as e:
            self.fail(f"Deleting a non-existent key raised an exception: {e}")

        result = captured_output.getvalue().strip()
        self.assertEqual(result, "5 6 7 10 12 17 20 30")

    def test_minimum_degree_two(self):
        """Test BTree with minimum degree t=2."""
        btree2 = BTree(2)
        for key in [1, 2, 3, 4, 5]:
            btree2.insert(key)
        captured_output = StringIO()
        sys.stdout = captured_output
        btree2.traverse()
        sys.stdout = sys.__stdout__
        result = captured_output.getvalue().strip()
        self.assertEqual(result, "1 2 3 4 5")

    def test_delete_from_single_key_tree(self):
        """Test deleting the only key in the tree (root should be empty leaf node)."""
        btree_single = BTree(2)
        btree_single.insert(42)
        btree_single.delete(42)
        self.assertIsNotNone(btree_single.root)
        self.assertTrue(btree_single.root.is_leaf)
        self.assertEqual(len(btree_single.root.keys), 0)

    def test_invalid_min_degree(self):
        """Creating a tree with invalid minimum degree should raise ``ValueError``."""
        with self.assertRaises(ValueError):
            BTree(1)

    def test_delete_from_empty_tree(self):
        """Test deleting from an empty tree (should not raise error)."""
        empty_btree = BTree(2)
        try:
            empty_btree.delete(1)
        except Exception as e:
            self.fail(f"Deleting from an empty tree raised an exception: {e}")

    def test_insert_and_delete_negative_and_large_numbers(self):
        """Test inserting and deleting negative and large numbers."""
        special_btree = BTree(3)
        keys = [-100, 0, 9999999]
        for key in keys:
            special_btree.insert(key)
        for key in keys:
            self.assertIsNotNone(special_btree.search(key))
        for key in keys:
            special_btree.delete(key)
            # After all deletions, root may be an empty leaf node
            if special_btree.root is not None and len(special_btree.root.keys) == 0:
                self.assertTrue(special_btree.root.is_leaf)
            else:
                self.assertIsNone(special_btree.search(key))


    def test_root_split_on_insert(self):
        """Root should split when it becomes full on insertion."""
        split_tree = BTree(2)
        for key in [1, 2, 3, 4]:
            split_tree.insert(key)

        self.assertFalse(split_tree.root.is_leaf)
        self.assertEqual(split_tree.root.keys, [2])

        captured_output = StringIO()
        with redirect_stdout(captured_output):
            split_tree.traverse()
        self.assertEqual(captured_output.getvalue().strip(), "1 2 3 4")

if __name__ == '__main__':
    unittest.main()
