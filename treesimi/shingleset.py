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
    if len(nested[0]) == 5:
        nested = remove_node_ids(nested)

    # Extract full subtrees
    trees = extract_subtrees(nested)
    trees.append(nested)  # add original tree
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
