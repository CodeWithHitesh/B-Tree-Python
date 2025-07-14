# B-Tree Implementation in Python

A clean, production-ready B-Tree implementation in Python.  
Supports insertion, deletion, search, and in-order traversal.

## Features

- Generic B-Tree with configurable minimum degree (`min_degree`)
- Efficient insert, delete, and search operations
- Well-documented and modular code
- Comprehensive unit tests, including edge cases

## Requirements

- Python 3.7 or higher
- `min_degree` must be **at least 2** for a valid B-Tree

## Installation

```sh
pip install btree
```

## Usage

```python
from btree import BTree

btree = BTree(min_degree=3)
for key in [10, 20, 5, 6, 12, 30, 7, 17]:
    btree.insert(key)

print("In-order traversal:")
btree.traverse()
print()

print("Search 6:", "Found" if btree.search(6) else "Not found")
print("Search 15:", "Found" if btree.search(15) else "Not found")

btree.delete(6)
print("After deleting 6:")
btree.traverse()
print()
```

## Run Tests

```sh
python -m unittest test_btree.py
```

## Test Coverage

- Insertion and in-order traversal
- Search (existing and non-existing keys)
- Deletion (leaf, internal, root, all keys, non-existent keys)
- Edge cases: minimum degree 2, negative and large numbers, empty tree, single-key tree, duplicate keys

## Continuous Integration

Pull requests run a GitHub Actions workflow that executes `python -m unittest`.
After the tests pass, the PR can be merged once it has been approved.

Merged commits on `master` are scanned for Conventional Commit messages.
A separate workflow uses a public GitHub Action to calculate the next semantic
version and automatically push the corresponding `vX.Y.Z` tag.
Whenever a tag is created, another step builds the package and publishes it to
the configured Artifactory PyPI repository.

## License

[MIT](LICENSE)
