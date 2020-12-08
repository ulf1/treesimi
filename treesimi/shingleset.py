import copy
from .extract import (
    remove_node_ids, extract_subtrees, trunc_leaves, drop_nodes, replace_attr)
from .encode import unique_trees
from typing import List, Tuple, Union, Optional
DATA = Union[int, float, str, dict, list, tuple]


def shingleset(nested: List[Tuple[int, int, int, DATA]],
               use_trunc_leaves: Optional[bool] = False,
               use_drop_nodes: Optional[bool] = False,
               use_replace_attr: Optional[bool] = False,
               placeholder: Optional[str] = '\uFFFF',
               ) -> List[List[Tuple[int, int, int, DATA]]]:
    """Extract unique subtrees or incomplete tree segments that can
         be stringified as shingles for MinHashing

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

    use_trunc_leaves : bool  (Default: False)
        Flag to apply `trunc_leaves` after `extract_subtrees`

    use_drop_nodes : bool  (Default: False)
        Flag to apply `drop_nodes` after `trunc_leaves`

    use_replace_attr : bool  (Default: False)
        Flag to apply `replace_attr` after `drop_nodes`

    placeholder : str  (Default: '\uFFFF')
        The data impute with `replace_attr`

    Returns:
    --------
    List[List[Tuple[int, int, int, DATA]]]
        A list of nested set based trees

    Example:
    --------
        import treesimi as ts
        cfg = {'use_trunc_leaves': False, 'use_drop_nodes': False,
               'use_replace_attr': True}
        nested = [[1, 8, 0, 'A'], [2, 3, 1, 'B'],
                  [4, 7, 1, 'C'], [5, 6, 2, 'D']]
        shingles = ts.shingleset(nested, **cfg)
    """
    if len(nested[0]) == 5:
        nested = remove_node_ids(nested)

    # Extract full subtrees
    trees = extract_subtrees(nested)
    trees = unique_trees(trees)

    # Truncate leaves
    if use_trunc_leaves:
        for tmp in copy.deepcopy(trees):
            trees.extend(trunc_leaves(tmp))
        trees = unique_trees(trees)

    # Drop nodes
    if use_drop_nodes:
        for tmp in copy.deepcopy(trees):
            trees.extend(drop_nodes(tmp))
        trees = unique_trees(trees)

    # Mask data attributes
    if use_replace_attr:
        for tmp in copy.deepcopy(trees):
            trees.extend(replace_attr(tmp, placeholder=placeholder))
        trees = unique_trees(trees)

    # done
    return trees
