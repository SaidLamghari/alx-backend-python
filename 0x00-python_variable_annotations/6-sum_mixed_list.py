#!/usr/bin/env python3
"""
Module pour la fonction sum_mixed_list
Auteur SAID LAMGHARI
"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Additionner une liste d'entiers et de flottants.

    Args:
    mxd_lst (List[Union[int, float]]):
    La liste d'entiers et de flottants à additionner.

    Returns:
    float: La somme des entiers et des flottants.
    """
    return sum(mxd_lst)
