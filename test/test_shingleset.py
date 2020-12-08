import treesimi as ts


def test1():
    nested = [[1, 6, 0, 'A'], [2, 3, 1, 'B'], [4, 5, 1, 'C']]
    shingles = ts.shingleset(nested)
    assert [[1, 6, 0, 'A'], [2, 3, 1, 'B'], [4, 5, 1, 'C']] in shingles
    assert [[1, 2, 0, 'B']] in shingles
    assert [[1, 2, 0, 'C']] in shingles


def test2():
    nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'], [5, 6, 2, 'D']]
    shingles = ts.shingleset(nested)
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'],
            [4, 7, 1, 'C'], [5, 6, 2, 'D']] in shingles
    assert [[1, 4, 0, 'C'], [2, 3, 1, 'D']] in shingles
    assert [[1, 2, 0, 'D']] in shingles
    assert [[1, 2, 0, 'B']] in shingles
    assert len(shingles) == 4


def test3():
    nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'], [5, 6, 2, 'D']]
    cfg = {'use_trunc_leaves': True}
    shingles = ts.shingleset(nested, **cfg)
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'],
            [4, 7, 1, 'C'], [5, 6, 2, 'D']] in shingles
    assert [[1, 4, 0, 'C'], [2, 3, 1, 'D']] in shingles
    assert [[1, 2, 0, 'D']] in shingles
    assert [[1, 2, 0, 'B']] in shingles
    # trunced
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C']] in shingles
    assert len(shingles) == 5


def test4():
    nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'], [5, 6, 2, 'D']]
    cfg = {'use_drop_nodes': True}
    shingles = ts.shingleset(nested, **cfg)
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'],
            [4, 7, 1, 'C'], [5, 6, 2, 'D']] in shingles
    assert [[1, 4, 0, 'C'], [2, 3, 1, 'D']] in shingles
    assert [[1, 2, 0, 'D']] in shingles
    assert [[1, 2, 0, 'B']] in shingles
    # with dropped nodes 1/2
    assert [[1, 8, 0, 'A'], [4, 7, 1, 'C'], [5, 6, 2, 'D']] in shingles
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B']] in shingles
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C']] in shingles
    # with dropped nodes 2/2
    assert [[1, 4, 0, 'C']] in shingles
    assert len(shingles) == 8


def test5():
    nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'], [4, 7, 1, 'C'], [5, 6, 2, 'D']]
    cfg = {'use_replace_attr': True, 'placeholder': '😃'}
    shingles = ts.shingleset(nested, **cfg)
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'],
            [4, 7, 1, 'C'], [5, 6, 2, 'D']] in shingles
    assert [[1, 4, 0, 'C'], [2, 3, 1, 'D']] in shingles
    assert [[1, 2, 0, 'D']] in shingles
    assert [[1, 2, 0, 'B']] in shingles
    # replace 1/4
    assert [[1, 8, 0, '😃'], [2, 3, 1, 'B'],
            [4, 7, 1, 'C'], [5, 6, 2, 'D']] in shingles
    assert [[1, 8, 0, 'A'], [2, 3, 1, '😃'],
            [4, 7, 1, 'C'], [5, 6, 2, 'D']] in shingles
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'],
            [4, 7, 1, '😃'], [5, 6, 2, 'D']] in shingles
    assert [[1, 8, 0, 'A'], [2, 3, 1, 'B'],
            [4, 7, 1, 'C'], [5, 6, 2, '😃']] in shingles
    # replace 2/4
    assert [[1, 4, 0, '😃'], [2, 3, 1, 'D']] in shingles
    assert [[1, 4, 0, 'C'], [2, 3, 1, '😃']] in shingles
    # replace 3/4 and 4/4
    assert [[1, 2, 0, '😃']] in shingles
    assert len(shingles) == 11
