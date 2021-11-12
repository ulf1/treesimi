import treesimi as ts
from treesimi.convert import adjac_to_nested_recur


def test1():
    adjac = [(1, 2), (2, 0), (3, 2), (4, 3)]
    nested = ts.adjac_to_nested(adjac)
    assert nested == [[2, 1, 8, 0], [1, 2, 3, 1], [3, 4, 7, 1], [4, 5, 6, 2]]

    subtree = ts.get_subtree(nested, 3)
    assert subtree == [[3, 4, 7, 1], [4, 5, 6, 2]]

    attrs = [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')]
    nested2 = ts.set_attr(nested, attrs)
    assert nested2 == [
        [2, 1, 8, 0, 'B'], [1, 2, 3, 1, 'A'],
        [3, 4, 7, 1, 'C'], [4, 5, 6, 2, 'D']]

    subtree = ts.get_subtree(nested2, 3)
    assert subtree == [[3, 4, 7, 1, 'C'], [4, 5, 6, 2, 'D']]


def test2():
    adjac = [(1, 0), (2, 1), (3, 1), (4, 2)]
    _, nested = adjac_to_nested_recur(
        adjac, nested=[], parent_id=1, lft=1, depth=0)
    assert [4, 3, 4, 2] in nested
    assert [2, 2, 5, 1] in nested
    assert [3, 6, 7, 1] in nested
    assert [1, 1, 8, 0] in nested
    assert len(nested) == 4


def test3():
    adjac = [(1, 0), (2, 1), (3, 1), (4, 2)]
    nested = ts.adjac_to_nested(adjac)
    assert [1, 1, 8, 0] in nested
    assert [2, 2, 5, 1] in nested
    assert [4, 3, 4, 2] in nested
    assert [3, 6, 7, 1] in nested
    assert len(nested) == 4


def test4():
    nested = [[i, None, None, None] for i in range(1, 5)]
    attrs = [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')]
    nested2 = ts.set_attr(nested, attrs)
    assert [1, None, None, None, 'A'] in nested2
    assert [2, None, None, None, 'B'] in nested2
    assert [3, None, None, None, 'C'] in nested2
    assert [4, None, None, None, 'D'] in nested2
    assert len(nested2) == 4


def test5():
    adjac = [(1, 2, 'A'), (2, 0, 'B'), (3, 2, 'C'), (4, 3, 'D')]
    nested = ts.adjac_to_nested_with_attr(adjac)
    assert [2, 1, 8, 0, 'B'] in nested
    assert [1, 2, 3, 1, 'A'] in nested
    assert [3, 4, 7, 1, 'C'] in nested
    assert [4, 5, 6, 2, 'D'] in nested
    assert len(nested) == 4


def test6():
    adjac = [(1, 2, 'A'), (2, 0, 'B'),
             ((2, "-", 3), None, "mwe"),
             (3, 2, 'C'), (4, 3, 'D')]
    nested = ts.adjac_to_nested_with_attr(adjac)
    assert [2, 1, 8, 0, 'B'] in nested
    assert [1, 2, 3, 1, 'A'] in nested
    assert [3, 4, 7, 1, 'C'] in nested
    assert [4, 5, 6, 2, 'D'] in nested
    assert len(nested) == 4
