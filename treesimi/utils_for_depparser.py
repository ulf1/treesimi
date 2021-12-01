from typing import List, Tuple
# import spacy
# import stanza
# import trankit
from .convert import adjac_to_nested_with_attr
from .extract import remove_node_ids
from .shingleset import shingleset
import json


def to_adjac_from_spacy(corpus: str,
                        model  #: spacy.lang
                        ) -> List[List[Tuple[int, int, str]]]:
    """ Parse all sentences with SpaCy, and extract parent-child relations
          from the dependency tree as adjacency list.
    """
    # parse string into sentences
    docs = model(corpus)
    # extract adjacency list of dependency tree
    all_adjac = []
    for snt in docs.sents:
        adjac = [(t.i + 1, 0 if t.dep_ == 'ROOT' else (t.head.i + 1), t.dep_)
                 for t in snt
                 if isinstance(t.i, int)]
        # adjust ids
        d = min([c for c, _, __ in adjac]) - 1
        adjac = [(c - d, max(0, p - d), m) for c, p, m in adjac]
        # store it
        all_adjac.append(adjac)
    # done
    return all_adjac


def to_adjac_from_stanza(corpus: str,
                         model  #: stanza.pipeline.core.Pipeline
                         ) -> List[List[Tuple[int, int, str]]]:
    """ Parse all sentences with Stanza, and extract parent-child relations
          from the dependency tree as adjacency list.
    """
    # parse string into sentences
    docs = model(corpus)
    # extract adjacency list of dependency tree
    all_adjac = []
    for snt in docs.sentences:
        adjac = [(t.id, t.head, t.deprel)
                 for t in snt.words
                 if isinstance(t.id, int)]
        # adjust ids
        d = min([c for c, _, __ in adjac]) - 1
        adjac = [(c - d, max(0, p - d), m) for c, p, m in adjac]
        # store it
        all_adjac.append(adjac)
    # done
    return all_adjac


def to_adjac_from_trankit(corpus: str,
                          model  # : trankit.pipeline.Pipeline
                          ) -> List[List[Tuple[int, int, str]]]:
    """ Parse all sentences with Trankit, and extract parent-child relations
          from the dependency tree as adjacency list.
    """
    # parse string into sentences
    docs = model(corpus)
    # extract adjacency list of dependency tree
    all_adjac = []
    for snt in docs.get("sentences"):
        adjac = [(t.get("id"), t.get("head"), t.get("deprel"))
                 for t in snt.get("tokens")
                 if isinstance(t.get("id"), int)]
        # adjust ids
        d = min([c for c, _, __ in adjac]) - 1
        adjac = [(c - d, max(0, p - d), m) for c, p, m in adjac]
        # store it
        all_adjac.append(adjac)
    # done
    return all_adjac


def examples_to_shingles(examples: List[str], model, cfg=None) -> List[str]:
    if cfg is None:
        cfg = {
            'use_trunc_leaves': True,
            'use_drop_nodes': False,
            'use_replace_attr': False}
    # get model name
    model_name = str(type(model))
    # loop over text examples
    stringified = []
    for text in examples:
        # extract adjacency lists for each identified sentence
        if "spacy" in model_name:
            all_adjac = to_adjac_from_spacy(text, model)
        elif "stanza" in model_name:
            all_adjac = to_adjac_from_stanza(text, model)
        elif "trankit" in model_name:
            all_adjac = to_adjac_from_trankit(text, model)
        else:
            raise Exception(f"Unsupported type(model)={model_name}")
        # shingle all identified sentences of the example
        shingled = []
        for adjac in all_adjac:
            nested = adjac_to_nested_with_attr(adjac)
            nested = remove_node_ids(nested)
            shingled.extend(shingleset(nested, **cfg))
        # convert subtrees in `shingled` to strings.
        stringified.append(
            [json.dumps(tree).encode('utf-8') for tree in shingled])
    # done
    return stringified
