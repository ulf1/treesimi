import copy
from .extract import (
    remove_node_ids, extract_subtrees, trunc_leaves, drop_nodes, replace_attr)
from .encode import  unique_trees
from typing import List, Tuple, Union, Optional
DATA = Union[int, float, str, dict, list, tuple]


def shingleset(nested: List[Tuple[int, int, int, DATA]],
               placeholder: Optional[str] = '\uFFFF',
               ) -> List[List[Tuple[int, int, int, DATA]]]:
    if len(nested[0]) == 5:
        nested = remove_node_ids(nested)

    # Extract full subtrees
    trees = extract_subtrees(nested)
    trees.append(nested)  # add original tree
    trees = unique_trees(trees)

    # Truncate leaves
    for tmp in copy.deepcopy(trees):
        trees.extend(trunc_leaves(tmp))
    trees = unique_trees(trees)

    # Drop nodes
    for tmp in copy.deepcopy(trees):
        trees.extend(drop_nodes(tmp))
    trees = unique_trees(trees)

    # Mask data attributes
    for tmp in copy.deepcopy(trees):
        trees.extend(replace_attr(tmp, placeholder=placeholder))
    trees = unique_trees(trees)

    # done
    return trees
