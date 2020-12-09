[![PyPI version](https://badge.fury.io/py/treesimi.svg)](https://badge.fury.io/py/treesimi)
[![DOI](https://zenodo.org/badge/318838452.svg)](https://zenodo.org/badge/latestdoi/318838452)

# treesimi
Compute similarity between trees, e.g. dependency trees


## Convert an Adjacency List into a Nested Set Table
For example, CoNLL-U's `['id', 'head']` fields form an adjacency list of a dependency tree.
Traversing an adjacency list is slower than reading a nested set.
Thus, converting a adjacency list to a nested set table once, makes sense if we need to read the three several times lateron.

```py
import treesimi as ts
adjac = [(1, 0), (2, 1), (3, 1), (4, 2)]
nested = ts.adjac_to_nested(adjac)
# columns: node id, left, right, depth
# [[1, 1, 8, 0], [2, 2, 5, 1], [4, 3, 4, 2], [3, 6, 7, 1]]
```

### Demo: Query a nested set table
To extract a subtree we just need to iterate through the list ($O(n)$)

```py
_, lft0, rgt0, _ = nested[1]
subtree = [(i, l, r, d) for i, l, r, d in nested if (l >= lft0) and (r <= rgt0)]
# [[2, 2, 5, 1], [4, 3, 4, 2]]
```

or `ts.get_subtree(nested, sub_id=2)`

### Set node attributes

```py
import treesimi as ts
nested = [[1, 1, 8, 0], [2, 2, 5, 1], [4, 3, 4, 2], [3, 6, 7, 1]]
attrs = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
nested = ts.set_attr(nested, attrs)
# columns: node id, left, right, depth, attributes
# [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'], [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
```

### Convert Adjacency List with attributes

```py
import treesimi as ts
adjac = [(1, 0, 'dat1'), (2, 1, 'dat2'), (3, 1, 'dat3'), (4, 2, 'dat3')]
nested = ts.adjac_to_nested_with_attr(adjac)
# columns: node id, left, right, depth
# [[1, 1, 8, 0, 'dat1'], [2, 2, 5, 1, 'dat2'], [4, 3, 4, 2, 'dat2'], [3, 6, 7, 1, 'dat4']]
```


## Extract subtree patterns
We can extract the following patterns from one tree:

* Depth dimension
    * Full subtrees
    * Truncate leaves
* Sibling dimension
    * All siblings
    * Drop siblings (and their subtree)
* Placeholder attribute field


### Full subtrees
The function `extract_subtrees` returns all subtrees of a tree.
The depth information is adjusted accordingly for each subtree.

```py
import treesimi as ts
nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'], [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
nested = ts.remove_node_ids(nested)
subtrees = ts.extract_subtrees(nested)
# [
#    [[1, 8, 0, 'a'], [2, 5, 1, 'b'], [3, 4, 2, 'd'], [6, 7, 1, 'c']],
#    [[1, 4, 0, 'b'], [2, 3, 1, 'd']],
#    [[1, 2, 0, 'd']],
#    [[1, 2, 0, 'c']]
# ]
```

### Truncate leaves
In the first step, the function `trunc_leaves` removes leaves of the largest depth level.
The result is always an incomplete tree, and the `lft` and `rgt` values are **not adjusted** to indicate that **there is a missing node**.
In the next steps, the depth level is further removed down to `depth=1`.

```py
import treesimi as ts
nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'], [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
nested = ts.remove_node_ids(nested)
subtrees = ts.trunc_leaves(nested)
# [
#   [[1, 8, 0, 'a'], [2, 5, 1, 'b'], [6, 7, 1, 'c']]
# ]
```

Hint: Run `trunc_leaves` for each subtree extracted by `extract_subtrees`. Call `unique_trees` after each step.


### Drop sibling nodes
Generate variants of a tree by dropping each node once.
Again, the result is always an incomplete tree, and the `lft` and `rgt` values are **not adjusted** to indicate that **there is a missing node**.

```py
import treesimi as ts
nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'], [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
nested = ts.remove_node_ids(nested)
subtrees = ts.drop_nodes(nested)
# [
#   [[1, 8, 0, 'a']],
#   [[1, 8, 0, 'a'], [2, 5, 1, 'b']],
#   [[1, 8, 0, 'a']]
# ]
```

Hints: Create subtrees with `extract_subtrees` and `trunc_leaves`, and run `drop_nodes` on these subtrees. If you want to drop N nodes/leaves of a tree, then call the function twice, e.g. `drop_nodes(drop_nodes(...))`.


### Placeholder attribute field
The `replace_attr` removes the data attribute of a node with a generic placeholder.

```py
import treesimi as ts
nested = [[1, 1, 8, 0, 'a'], [2, 2, 5, 1, 'b'], [4, 3, 4, 2, 'd'], [3, 6, 7, 1, 'c']]
nested = ts.remove_node_ids(nested)
subtrees = ts.replace_attr(nested, placeholder='[MASK]')
# [
#   [[1, 8, 0, '[MASK]'], [2, 5, 1, 'b'], [3, 4, 2, 'd'], [6, 7, 1, 'c']],
#   [[1, 8, 0, 'a'], [2, 5, 1, '[MASK]'], [3, 4, 2, 'd'], [6, 7, 1, 'c']], 
#   [[1, 8, 0, 'a'], [2, 5, 1, 'b'], [3, 4, 2, '[MASK]'], [6, 7, 1, 'c']], 
#   [[1, 8, 0, 'a'], [2, 5, 1, 'b'], [3, 4, 2, 'd'], [6, 7, 1, '[MASK]']]
# ]
```

## Demo Notebooks about Shingling for MinHash
- [Create subtrees as shingle sets](https://github.com/ulf1/treesimi/blob/master/demo/Create%20subtrees%20as%20shingle%20sets.ipynb)
- [Jaccard Similarity between Dependency Trees](https://github.com/ulf1/treesimi/blob/master/demo/Jaccard%20Similarity%20between%20Dependency%20Trees.ipynb)
- [Shingle Dependency Trees for datasketch's Minhash](https://github.com/ulf1/treesimi/blob/master/demo/Shingle%20Dependency%20Trees%20for%20datasketch's%20Minhash.ipynb)

Start jupyter to run the demo notebook

```
source .venv/bin/activate
jupyter lab
```

## Appendix

### Installation
The `treesimi` [git repo](http://github.com/ulf1/treesimi) is available as [PyPi package](https://pypi.org/project/treesimi)

```
pip install treesimi
pip install git+ssh://git@github.com/ulf1/treesimi.git
```

### Commands
Install a virtual environment

```sh
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

Python commands

* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Support
Please [open an issue](https://github.com/ulf1/treesimi/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/treesimi/compare/).
