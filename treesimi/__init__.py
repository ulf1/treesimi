__version__ = '0.1.6'

from .convert import (
    adjac_to_nested,
    set_attr,
    get_subtree,
    adjac_to_nested_with_attr
)
from .extract import (
    remove_node_ids,
    extract_subtrees,
    trunc_leaves,
    drop_nodes,
    replace_attr
)
from .encode import (
    to_hash,
    unique_trees
)
from .shingleset import shingleset

from .utils_for_depparser import (
    to_adjac_from_spacy,
    to_adjac_from_stanza,
    to_adjac_from_trankit,
    examples_to_shingles
)
