import treesimi as ts


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
