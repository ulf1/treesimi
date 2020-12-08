import treesimi as ts
import hashlib


def test1():
    tree = [[1, 2, 3], [4, 5, 6]]
    target = hashlib.sha512("[[1, 2, 3], [4, 5, 6]]".encode('utf-8'))
    hashed = ts.to_hash(tree)
    assert hashed.hexdigest() == target.hexdigest()


def test2():
    trees = [1, 1, 1, 2, 2, 'A', 'A', [2, 3, 4], [2, 3, 4]]
    utrees = ts.unique_trees(trees)
    assert utrees == [1, 2, 'A', [2, 3, 4]]
