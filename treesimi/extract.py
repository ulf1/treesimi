import copy
from typing import List, Tuple, Union
DATA = Union[int, float, str, dict, list, tuple]


def extract_subtrees(nested: List[Tuple[int, int, int, int, DATA]]
                     ) -> List[Tuple[int, int, int, int, DATA]]:
    """Extracting full subtrees from a nested set tables is
        basically O(n) copy & paste
    """
    subtrees = []
    for _, lft0, rgt0, dep0, _ in nested:
        subtrees.append(
            [[lfti - lft0 + 1, rgti - lft0 + 1, depi - dep0, attr]
             for _, lfti, rgti, depi, attr in nested
             if (lfti >= lft0) and (rgti <= rgt0)])
    return subtrees


def trunc_leaves(nested: List[Tuple[int, int, int, int, DATA]]
                 ) -> List[Tuple[int, int, int, int, DATA]]:
    """Reduce depth level to truncate leaves to create (incomplete) trees
    """
    max_depth = max([d for _, _, _, d, _ in nested])
    subtrees = []
    for dmax in reversed(range(1, max_depth)):
        subtrees.append([node for node in nested if node[3] <= dmax])
    return subtrees


def drop_nodes(nested: List[Tuple[int, int, int, int, DATA]]
               ) -> List[Tuple[int, int, int, int, DATA]]:
    """Drop each node once
    """
    subtrees = []
    for _, lft0, rgt0, dep0, _ in nested:
        if lft0 > 1:
            subtrees.append([[i, l, r, d, a] for i, l, r, d, a in nested
                            if (l < lft0) and (r > rgt0)])
    return subtrees


def replace_attr(nested: List[Tuple[int, int, int, int, DATA]],
                 placeholder: str = '[MASK]',
                 ) -> List[Tuple[int, int, int, int, DATA]]:
    """Replace attribute field
    """
    subtrees = []
    for i in range(len(nested)):
        tmp = copy.deepcopy(nested)
        tmp[i][4] = placeholder
        subtrees.append(tmp)
    return subtrees
