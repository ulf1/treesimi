from typing import List, Tuple, Optional, Union
DATA = Union[int, float, str, dict, list, tuple]


def adjac_to_nested_recur(adjac: List[Tuple[int, int]],
                          parent_id: Optional[int] = 0,
                          lft: Optional[int] = 1,
                          depth: Optional[int] = 0,
                          nested: List[Tuple[int, int, int, int]] = []
                          ) -> (int, List[Tuple[int, int, int, int]]):
    """Recursive function to traverse over an adjacency list model based
        tree to build the nested set model based tree

    Don't use this function directly. Please call `treesimi.adjac_to_nested`

    Parameters:
    -----------
    adjac : List[Tuple[int, int]]
        Adjacency list of the tree. The columns contain the following
          information:
            0: Node ID
            1: Parent ID of the node

    parent_id : int
        The current parent ID of the adjacency list

    lft : int
        The previous lft value of the nested set

    depth : int
        The current tree depth

    nested: List[Tuple[int, int, int, int]]
        see below

    Returns:
    --------
    rgt + 1 : int
        The next node's left value

    nested : List[Tuple[int, int, int, int]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Node ID
            1: Left value (root is 1)
            2: Right value
            3: Depth level (root is 0)

    Example:
    --------
        from treesimi.convert import adjac_to_nested_recur
        adjac = [(1, 0), (2, 1), (3, 1), (4, 2)]
        _, nested = adjac_to_nested_recur(
            adjac, parent_id=1, lft=1, depth=0, nested=[])
    """
    # The next "rgt" value is at least "lft+1"
    rgt = lft + 1
    # Lookup all direct children nodes of the current parent node
    #   from the adjacency list
    children = [nid for nid, pid in adjac if pid == parent_id]
    # Drill down till we reached each tree leaf
    for child in children:
        rgt, _ = adjac_to_nested_recur(adjac, child, rgt, depth + 1, nested)
    nested.append([parent_id, lft, rgt, depth])
    return rgt + 1, nested


def adjac_to_nested(adjac: List[Tuple[int, int]],
                    root_id: Optional[int] = 0
                    ) -> List[Tuple[int, int, int, int, int]]:
    """Convert Adjacancy List to Nested Set Table

    Parameters:
    -----------
    adjac : List[Tuple[int, int]]
        Adjacency list of the tree. The columns contain the following
          information:
            0: Node ID
            1: Parent ID of the node

    root_id : int = 0
        In CoNLL-U the root is usually "0"

    Return:
    -------
    nested : List[Tuple[int, int, int, int]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Node ID
            1: Left value (root is 1)
            2: Right value
            3: Depth level (root is 0)

    Example:
    --------
        import treesimi as ts
        adjac = [(1, 0), (2, 1), (3, 1), (4, 2)]
        nested = ts.adjac_to_nested(adjac)
    """
    # find the node ID marked as root
    for i, p in adjac:
        if p == root_id:
            parent_id = i
            break
    # start tree traversal
    _, nested = adjac_to_nested_recur(
        adjac, parent_id=parent_id, lft=1, depth=0, nested=[])
    # sorted nested set table
    nested = sorted(nested, key=lambda r: r[1])
    # done
    return nested


def get_subtree(nested, sub_id):
    if len(nested[0]) == 4:
        # find lft/rgt of sub_id
        for i, l, r, _ in nested:
            if i == sub_id:
                lft0, rgt0 = l, r
                break
        # fail if not found
        if 'lft0' not in vars():
            raise Exception(f"sub_id={sub_id} doesn't exist.")
        # iterate through list
        return [[i, l, r, d] for i, l, r, d in nested
                if (l >= lft0) and (r <= rgt0)]
    else:
        for i, l, r, _, _ in nested:
            if i == sub_id:
                lft0, rgt0 = l, r
                break
        if 'lft0' not in vars():
            raise Exception(f"sub_id={sub_id} doesn't exist.")
        return [[i, l, r, d, a] for i, l, r, d, a in nested
                if (l >= lft0) and (r <= rgt0)]


def set_attr(nested: List[Tuple[int, int, int, int]],
             attr: List[Tuple[int, DATA]]
             ) -> List[Tuple[int, int, int, int, DATA]]:
    """Join a data column to the nested set table

    Parameters:
    -----------
    nested : List[Tuple[int, int, int, int]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Node ID
            1: Left value (root is 1)
            2: Right value
            3: Depth level (root is 0)
        If an attribute column already exist, then it will be overwritten.

    attr : List[Tuple[int, DATA]]
        A list of node IDs and their data attributes. The columns contain the
          the following information:
            0: Node ID
            1: Attributes related to the node ID

    Returns:
    --------
    nested : List[Tuple[int, int, int, int, DATA]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Node ID
            1: Left value (root is 1)
            2: Right value
            3: Depth level (root is 0)
            4: Attributes related to the node ID

    Example:
    --------
        import treesimi as ts
        nested = [[1, None, None, None], [2, None, None, None]]
        attrs = [(1, 'A'), (2, 'B')]
        nested2 = ts.set_attr(nested, attrs)
        # [[1, None, None, None, 'A'], [2, None, None, None, 'B']]
    """
    # Add empty 4th column for attributes if not exist
    if len(nested[0]) == 4:
        nested = [[i, l, r, d, None] for i, l, r, d in nested]
    # add each attribute
    nid = [row[0] for row in nested]
    for i, dat in attr:
        nested[nid.index(i)][4] = dat
    return nested


def adjac_to_nested_with_attr(adjac: List[Tuple[int, int, DATA]]
                              ) -> List[Tuple[int, int, int, int, DATA]]:
    """Convert Adjacancy List to Nested Set Table with data column

    Parameters:
    -----------
    adjac : List[Tuple[int, int, DATA]]
        Adjacency list of the tree. The columns contain the following
          information:
            0: Node ID
            1: Parent ID of the node
            2: Attributes related to the node ID

    Return:
    -------
    nested : List[Tuple[int, int, int, int, DATA]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Node ID
            1: Left value (root is 1)
            2: Right value
            3: Depth level (root is 0)
            4: Attributes related to the node ID

    Example:
    --------
        import treesimi as ts
        adjac = [(1, 2, 'A'), (2, 0, 'B'), (3, 2, 'C'), (4, 3, 'D')]
        nested = ts.adjac_to_nested_with_attr(adjac)
    """
    nested = adjac_to_nested([(i, p) for i, p, _ in adjac])
    nested = set_attr(nested, [(i, d) for i, _, d in adjac])
    return nested
