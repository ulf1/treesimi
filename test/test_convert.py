import treesimi as ts


def test1():
    adjac = [(1, 2), (2, 0), (3, 2), (4, 3)]
    nested = ts.adjac_to_nested(adjac)
    assert nested == [[2, 1, 8], [1, 2, 3], [3, 4, 7], [4, 5, 6]]

    subtree = ts.get_subtree(nested, 3)
    assert subtree == [[3, 4, 7], [4, 5, 6]]

    attrs = [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')]
    nested2 = ts.set_attr(nested, attrs)
    assert nested2 == [
        [2, 1, 8, 'B'], [1, 2, 3, 'A'], [3, 4, 7, 'C'], [4, 5, 6, 'D']]

    subtree = ts.get_subtree(nested2, 3)
    assert subtree == [[3, 4, 7, 'C'], [4, 5, 6, 'D']]


def test2():
    nested = [[1, 1, 8, 'a'], [2, 2, 5, 'b'], [4, 3, 4, 'd'], [3, 6, 7, 'c']]
    subtrees = ts.extract_all_subtrees(nested)
    assert subtrees == [
        [(1, 8, 'a'), (2, 5, 'b'), (3, 4, 'd'), (6, 7, 'c')],
        [(1, 4, 'b'), (2, 3, 'd')], [(1, 2, 'd')], [(1, 2, 'c')]]
