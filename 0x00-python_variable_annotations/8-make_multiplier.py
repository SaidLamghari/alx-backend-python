#!/usr/bin/env python3
"""
Module pour la fonction make_multiplier
Auteur SAID LAMGHARI
"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Créer une fonction de multiplication.

    Args:
    multiplier (float): Le multiplicateur.

    Returns:
    Callable[[float], float]: Une fonction qui
    multiplie un flottant par le multiplicateur.
    """
    def multiplier_function(vle: float) -> float:
        return vle * multiplier
    return multiplier_function
