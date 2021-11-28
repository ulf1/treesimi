__version__ = '0.1.5'

from .convert import (
    adjac_to_nested, set_attr, get_subtree, adjac_to_nested_with_attr)
from .extract import (
    remove_node_ids, extract_subtrees, trunc_leaves, drop_nodes, replace_attr)
from .encode import (
    to_hash, unique_trees)
from .shingleset import shingleset
