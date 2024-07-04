#!/usr/bin/env python3
"""
Module pour la fonction to_kv
Auteur SAID LAMGHARI
"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Créer un tuple à partir d'une chaîne de caractères
    et d'un nombre, avec le nombre au carré.

    Args:
    k (str): La chaîne de caractères.
    v (Union[int, float]): Le nombre à mettre au carré.

    Returns:
    Tuple[str, float]: Un tuple avec la chaîne
    de caractères et le nombre au carré.
    """
    return (k, float(v ** 2))
