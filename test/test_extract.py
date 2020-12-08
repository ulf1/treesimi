import treesimi as ts


def test1():
    nested = [[1, 1, 4, 0, 'A'], [2, 2, 3, 1, 'B']]

    nested2 = ts.remove_node_ids(nested)
    assert nested2 == [[1, 4, 0, 'A'], [2, 3, 1, 'B']]

    nested3 = ts.remove_node_ids(nested, nodeid_to_attr=True)
    assert nested3 == [[1, 4, 0, {'nodeid': 1, 'data': 'A'}],
                       [2, 3, 1, {'nodeid': 2, 'data': 'B'}]]


def test2():
    nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'], [5, 6, 2, 'D']]
    subtrees = ts.extract_subtrees(nested)
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'],
            [4, 7, 1, 'C'], [5, 6, 2, 'D']] in subtrees
    assert [[1, 4, 0, 'C'], [2, 3, 1, 'D']] in subtrees
    assert [[1, 2, 0, 'D']] in subtrees
    assert [[1, 2, 0, 'B']] in subtrees
    assert len(subtrees) == 4


def test3():
    nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'], [5, 6, 2, 'D']]
    subtrees = ts.trunc_leaves(nested)
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C']] in subtrees
    assert len(subtrees) == 1


def test4():
    nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'], [5, 6, 2, 'D']]
    subtrees = ts.drop_nodes(nested)
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C']] in subtrees
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B']] in subtrees
    assert [[1, 8, 0, 'A'], [4, 7, 1, 'C'], [5, 6, 2, 'D']] in subtrees
    assert len(subtrees) == 3


def test5():
    nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'], [5, 6, 2, 'D']]
    subtrees = ts.replace_attr(nested, placeholder='😃')
    assert [[1, 8, 0, '😃'], [2, 3, 1, 'B'], [4, 7, 1, 'C'],
            [5, 6, 2, 'D']] in subtrees
    assert [[1, 8, 0, 'A'], [2, 3, 1, '😃'], [4, 7, 1, 'C'],
            [5, 6, 2, 'D']] in subtrees
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, '😃'],
            [5, 6, 2, 'D']] in subtrees
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'],
            [5, 6, 2, '😃']] in subtrees
    assert len(subtrees) == 4
