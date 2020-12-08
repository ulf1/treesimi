import copy
from typing import List, Tuple, Union, Optional
DATA = Union[int, float, str, dict, list, tuple]


def remove_node_ids(nested: List[Tuple[int, int, int, int, DATA]],
                    nodeid_to_attr: Optional[bool] = False
                    ) -> List[Tuple[int, int, int, DATA]]:
    """Remove the node IDs in the 1st column from the nested set table

    Parameters:
    -----------
    nested : List[Tuple[int, int, int, int, DATA]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Node ID <= TO BE DELETED
            1: Left value (root is 1)
            2: Right value
            3: Depth level (root is 0)
            4: Attributes related to the node ID

    nodeid_to_attr : bool  (Default: False)
        Flag if the node IDs should be stored in the attr column.
          If the attribute column is not a dict object, the existing
          data is moved into {'data': data, 'nodeid': ...}
    Returns:
    --------
    nested : List[Tuple[int, int, int, int, DATA]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Left value (root is 1)
            1: Right value
            2: Depth level (root is 0)
            3: Attributes related to the node ID

    Example:
    --------
        import treesimi as ts
        nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'],
                  [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
        nested1 = ts.remove_node_ids(nested)
        nested2 = ts.remove_node_ids(nested, nodeid_to_attr=True)
    """
    if nodeid_to_attr:
        newlist = []
        for i, l, r, d, a in nested:
            if isinstance(a, dict):
                a['nodeid'] = i
            else:
                a = {'nodeid': i, 'data': a}
            newlist.append([l, r, d, a])
        return newlist
    else:
        return [[l, r, d, a] for _, l, r, d, a in nested]


def extract_subtrees(nested: List[Tuple[int, int, int, DATA]]
                     ) -> List[List[Tuple[int, int, int, DATA]]]:
    """Extracting full subtrees from a nested set tables is
        basically O(n) copy & paste

    Parameters:
    -----------
    nested : List[Tuple[int, int, int, int, DATA]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Left value (root is 1)
            1: Right value
            2: Depth level (root is 0)
            3: Attributes related to the node ID
        Please note, that you need to remove the node IDs beforehand,
          e.g. use `treesimi.remove_node_ids`

    Returns:
    --------
    List[List[Tuple[int, int, int, DATA]]]
        A list of nested set based trees

    Example:
    --------
        import treesimi as ts
        nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'],
                  [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
        nested = ts.remove_node_ids(nested)
        subtrees = ts.extract_subtrees(nested)
    """
    subtrees = []
    for lft0, rgt0, dep0, _ in nested:
        subtrees.append(
            [[lfti - lft0 + 1, rgti - lft0 + 1, depi - dep0, attr]
             for lfti, rgti, depi, attr in nested
             if (lfti >= lft0) and (rgti <= rgt0)])
    return subtrees


def trunc_leaves(nested: List[Tuple[int, int, int, DATA]]
                 ) -> List[List[Tuple[int, int, int, DATA]]]:
    """Reduce depth level to truncate leaves to create (incomplete) trees

    Parameters:
    -----------
    nested : List[Tuple[int, int, int, int, DATA]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Left value (root is 1)
            1: Right value
            2: Depth level (root is 0)
            3: Attributes related to the node ID
        Please note, that you need to remove the node IDs beforehand,
          e.g. use `treesimi.remove_node_ids`

    Returns:
    --------
    List[List[Tuple[int, int, int, DATA]]]
        A list of nested set based trees

    Example:
    --------
        import treesimi as ts
        nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'],
                  [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
        nested = ts.remove_node_ids(nested)
        subtrees = ts.trunc_leaves(nested)
    """
    max_depth = max([d for _, _, d, _ in nested])
    subtrees = []
    for dmax in reversed(range(1, max_depth)):
        subtrees.append([node for node in nested if node[2] <= dmax])
    return subtrees


def drop_nodes(nested: List[Tuple[int, int, int, DATA]]
               ) -> List[List[Tuple[int, int, int, DATA]]]:
    """Drop each node once

    Parameters:
    -----------
    nested : List[Tuple[int, int, int, int, DATA]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Left value (root is 1)
            1: Right value
            2: Depth level (root is 0)
            3: Attributes related to the node ID
        Please note, that you need to remove the node IDs beforehand,
          e.g. use `treesimi.remove_node_ids`

    Returns:
    --------
    List[List[Tuple[int, int, int, DATA]]]
        A list of nested set based trees

    Example:
    --------
        import treesimi as ts
        nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'],
                  [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
        nested = ts.remove_node_ids(nested)
        subtrees = ts.drop_nodes(nested)
    """
    subtrees = []
    for lft0, rgt0, _, _ in nested:
        if lft0 > 1:
            subtrees.append([[lft, rgt, d, a] for lft, rgt, d, a in nested
                            if (lft < lft0) or (rgt > rgt0)])
    return subtrees


def replace_attr(nested: List[Tuple[int, int, int, DATA]],
                 placeholder: Optional[str] = '\uFFFF',
                 ) -> List[List[Tuple[int, int, int, DATA]]]:
    """Replace attribute field

    Parameters:
    -----------
    nested : List[Tuple[int, int, int, int, DATA]]
        Nested set table of the tree. The columns contain the following
          information:
            0: Left value (root is 1)
            1: Right value
            2: Depth level (root is 0)
            3: Attributes related to the node ID
        Please note, that you need to remove the node IDs beforehand,
          e.g. use `treesimi.remove_node_ids`

    placeholder : str  (Default: '\uFFFF')
        The value to impute instead of the data attribute

    Returns:
    --------
    List[List[Tuple[int, int, int, DATA]]]
        A list of nested set based trees

    Example:
    --------
        import treesimi as ts
        nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'],
                  [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
        nested = ts.remove_node_ids(nested)
        subtrees = ts.replace_attr(nested, placeholder='[MASK]')
    """
    subtrees = []
    for i in range(len(nested)):
        tmp = copy.deepcopy(nested)
        tmp[i][3] = placeholder
        subtrees.append(tmp)
    return subtrees
