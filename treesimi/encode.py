import json
import hashlib
from typing import List, Union
import struct
ELEMENT = Union[int, float, str, dict, list, tuple]


def to_hash(subtree: ELEMENT) -> hashlib.sha512:
    """Stringify and hash a python list"""
    stringified = json.dumps(subtree).encode('utf-8')
    return hashlib.sha512(stringified)


def unique_trees(trees: List[ELEMENT]) -> List[ELEMENT]:
    """Filters unique elements of any data type
         (Basically `set` for list objects)
    """
    # store hash as key (dict keys are unique), and the orginal trees as value
    hashed = {to_hash(tree).hexdigest(): tree for tree in trees}
    # read the original trees
    return [tree for _, tree in hashed.items()]


def uint32_to_int32(i):  # i: np.uint32 -> np.int32
    return struct.unpack('<l', struct.pack('<I', i))[0]
