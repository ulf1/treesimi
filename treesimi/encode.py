import json
import hashlib
from typing import List, Union
ELEMENT = Union[int, float, str, dict, list, tuple]


def to_hash(tree: ELEMENT) -> hashlib.sha512:
    """Stringify and hash a python list"""
    return hashlib.sha512(json.dumps(tree).encode('utf-8'))


def unique_trees(trees: List[ELEMENT]) -> List[ELEMENT]:
    """Filters unique elements of any data type
         (Basically `set` for list objects)
    """
    # store hash as key (dict keys are unique), and the orginal trees as value
    hashed = {to_hash(tree).hexdigest(): tree for tree in trees}
    # read the original trees
    return [tree for _, tree in hashed.items()]
