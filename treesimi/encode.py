import json
import hashlib


def to_hash(tree):
    return hashlib.sha512(json.dumps(tree).encode('utf-8'))


def unique_trees(trees):
    # store hash as key (dict keys are unique), and the orginal trees as value
    hashed = {to_hash(tree).hexdigest(): tree for tree in trees}
    # read the original trees
    return [tree for _, tree in hashed.items()]
