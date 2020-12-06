from typing import List, Tuple, Optional, Union
DATA = Union[int, float, str, dict, list, tuple]


def adjac_to_nested_recur(adjac: List[Tuple[int, int]],
                          parent_id: Optional[int]=0,
                          lft: Optional[int]=1,
                          nested: List[Tuple[int, int, int]]=[]
                         ) -> (int, List[Tuple[int, int, int]]):
    """Recursive function to traverse over an adjacency list model based
        tree to build the nested set model based tree

    adjac : List[Tuple[int, int]]
        Adjacency list of the tree. The 1st column contains the
          node IDs, and the 2nd column the parent's ID of the node

    parent_id : int
        The current parent ID of the adjacency list

    lft : int
        The previous lft value of the nested set

    nested : List[Tuple[int, int, int]]
        Nested set table of the tree. The 1st column hold the node
          IDs, the 2nd column are the "left" values, and the 3rd
          column are the "right" values.
    """
    # The next "rgt" value is at least "lft+1"
    rgt = lft + 1
    # Lookup all direct children nodes of the current parent node
    #   from the adjacency list
    children = [nid for nid, pid in adjac if pid == parent_id]
    # Drill down till we reached each tree leaf
    for child in children:
        rgt, _ = adjac_to_nested_recur(adjac, child, rgt, nested)
    nested.append([parent_id, lft, rgt])
    return rgt + 1, nested


def adjac_to_nested(adjac: List[Tuple[int, int]],
                    root_id: Optional[int] = 0
                   ) -> List[Tuple[int, int, int]]:
    """Convert Adjacancy List to Nested Set Table

    adjac : List[Tuple[int, int]]
        Adjacency list of the tree. The 1st column contains the
          node IDs, and the 2nd column the parent's ID of the node

    root_id : int = 0
        In CoNLL-U the root is usually "0"

    Return:
    -------
    nested : List[Tuple[int, int, int]]
        Nested set table of the tree. The 1st column hold the node
          IDs, the 2nd column are the "left" values, and the 3rd
          column are the "right" values.

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
    _, nested = adjac_to_nested_recur(adjac, parent_id=parent_id, lft=1)
    # sorted nested set table
    nested = sorted(nested, key=lambda r: r[1])
    # done
    return nested


def get_subtree(nested, sub_id):
    if len(nested[0]) == 3:
        # find lft/rgt of sub_id
        for i, l, r in nested:
            if i == sub_id:
                lft0, rgt0 = l, r
                break
        # fail if not found
        if 'lft0' not in vars():
            raise Exception(f"sub_id={sub_id} doesn't exist.")
        # iterate through list
        return [[i, l, r] for i, l, r in nested
                if (l >= lft0) and (r <= rgt0)]
    else:
        for i, l, r, _ in nested:
            if i == sub_id:
                lft0, rgt0 = l, r
                break
        if 'lft0' not in vars():
            raise Exception(f"sub_id={sub_id} doesn't exist.")
        return [[i, l, r, a] for i, l, r, a in nested
                if (l >= lft0) and (r <= rgt0)]


def set_attr(nested: List[Tuple[int, int, int]],
             attr: List[Tuple[int, DATA]]
             ) -> List[Tuple[int, int, int, DATA]]:
    """
    """
    # Add empty 4th column for attributes if not exist
    if len(nested[0]) == 3:
        nested = [[i, l, r, None] for i, l, r in nested]
    # add each attribute
    nid = [row[0] for row in nested]
    for i, dat in attr:
        nested[nid.index(i)][3] = dat
    return nested


def extract_all_subtrees(nested):
    """Extracting subtrees from a nested set tables is
        basically O(n) copy & paste
    """
    subtrees = []
    for _, lft0, rgt0, _ in nested:
        subtrees.append(
            [(lfti - lft0 + 1, rgti - lft0 + 1, attr)
             for _, lfti, rgti, attr in nested
             if (lfti >= lft0) and (rgti <= rgt0)])
    return subtrees

