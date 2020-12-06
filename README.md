# treesimi
Compute similarity between trees, e.g. dependency trees


## Usage

### Convert an Adjacency List into a Nested Set Table
For example, CoNLL-U's `['id', 'head']` fields form an adjacency list of a dependency tree.
Traversing an adjacency list is slower than reading a nested set.
Thus, converting a adjacency list to a nested set table once, makes sense if we need to read the three several times lateron.

```py
import treesimi as ts
adjac = [(1, 0), (2, 1), (3, 1), (4, 2)]
nested = ts.adjac_to_nested(adjac)
# [[1, 1, 8], [2, 2, 5], [4, 3, 4], [3, 6, 7]]
```

To extract a subtree we just need to iterate through the list ($O(n)$)

```py
_, lft0, rgt0 = nested[1]
subtree = [(i, l, r) for i, l, r in nested if (l >= lft0) and (r <= rgt0)]
# [[2, 2, 5], [4, 3, 4]]
```

or `ts.get_subtree(nested, sub_id=2)`


### Set node attributes

```py
import treesimi as ts
nested = [[1, 1, 8], [2, 2, 5], [4, 3, 4], [3, 6, 7]]
attrs = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
nested = ts.set_attr(nested, attrs)
# [[1, 1, 8, 'a'], [2, 2, 5, 'b'], [4, 3, 4, 'd'], [3, 6, 7, 'c']]
```


### Extract all subtrees

```py
import treesimi as ts
nested = [[1, 1, 8, 'a'], [2, 2, 5, 'b'], [4, 3, 4, 'd'], [3, 6, 7, 'c']]
subtrees = ts.extract_all_subtrees(nested)
# [
#   [(1, 8, 'a'), (2, 5, 'b'), (3, 4, 'd'), (6, 7, 'c')],
#   [(1, 4, 'b'), (2, 3, 'd')],
#   [(1, 2, 'd')],
#   [(1, 2, 'c')]
# ]
```


### Count unique trees


### Hash trees



## Appendix

### Installation
The `treesimi` [git repo](http://github.com/ulf1/treesimi) is available as [PyPi package](https://pypi.org/project/treesimi)

```
pip install treesimi
pip install git+ssh://git@github.com/ulf1/treesimi.git
```

### Commands
Install a virtual environment

```
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
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
