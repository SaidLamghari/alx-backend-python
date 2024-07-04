#!/usr/bin/env python3
"""
Module pour la fonction safely_get_value
Auteur SAID LAMGHARI
"""

from typing import Mapping, Any, Union, TypeVar
T = TypeVar('T')


def safely_get_value(dct: Mapping[Any, Any], key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """
    Obtenir une valeur d'un dictionnaire, avec
    une valeur par défaut si la clé n'est pas trouvée.

    Args:
    dct (Mapping[Any, Any]): Le dictionnaire à rechercher.
    key (Any): La clé à rechercher.
    default (Union[T, None]): La valeur par défaut si la clé n'est pas trouvée.

    Returns:
    Union[Any, T]: La valeur du dictionnaire, ou la valeur par défaut.
    """
    if key in dct:
        return dct[key]
    else:
        return default
