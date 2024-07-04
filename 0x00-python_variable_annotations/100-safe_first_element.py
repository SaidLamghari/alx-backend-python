#!/usr/bin/env python3
"""
Module pour la fonction safe_first_element
Auteur SAID LAMGHARI
"""

from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Obtenir le premier élément d'une séquence, s'il existe.

    Args:
    lst (Sequence[Any]): La séquence à traiter.

    Returns:
    Union[Any, None]: Le premier élément, ou None si la séquence est vide.
    """
    if lst:
        return lst[0]
    else:
        return None
