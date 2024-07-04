#!/usr/bin/env python3
"""
Module pour la fonction element_length
Auteur SAID LAMGHARI
"""

from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Obtenir la longueur de chaque élément d'un itérable.

    Args:
    lst (Iterable[Sequence]): L'itérable à traiter.

    Returns:
    List[Tuple[Sequence, int]]: Une liste de tuples,
    chacun contenant un élément et sa longueur.
    """
    return [(i, len(i)) for i in lst]
