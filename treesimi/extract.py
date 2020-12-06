from typing import List, Tuple, Union, Optional
DATA = Union[int, float, str, dict, list, tuple]


def remove_node_ids(nested: List[Tuple[int, int, int, int, DATA]]
                    ) -> List[Tuple[int, int, int, DATA]]:
    return [[l, r, d, a] for _, l, r, d, a in nested]


def extract_subtrees(nested: List[Tuple[int, int, int, DATA]]
                     ) -> List[List[Tuple[int, int, int, DATA]]]:
    """Extracting full subtrees from a nested set tables is
        basically O(n) copy & paste
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
    """
    max_depth = max([d for _, _, d, _ in nested])
    subtrees = []
    for dmax in reversed(range(1, max_depth)):
        subtrees.append([node for node in nested if node[2] <= dmax])
    return subtrees


def drop_nodes(nested: List[Tuple[int, int, int, DATA]]
               ) -> List[List[Tuple[int, int, int, DATA]]]:
    """Drop each node once
    """
    subtrees = []
    for lft0, rgt0, _, _ in nested:
        if lft0 > 1:
            subtrees.append([[lft, rgt, d, a] for lft, rgt, d, a in nested
                            if (lft < lft0) and (rgt > rgt0)])
    return subtrees


def replace_attr(nested: List[Tuple[int, int, int, DATA]],
                 placeholder: Optional[str] = '[MASK]',
                 ) -> List[List[Tuple[int, int, int, DATA]]]:
    """Replace attribute field
    """
    subtrees = []
    for i in range(len(nested)):
        tmp = copy.deepcopy(nested)
        tmp[i][3] = placeholder
        subtrees.append(tmp)
    return subtrees
