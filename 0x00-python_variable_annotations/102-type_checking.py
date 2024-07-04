#!/usr/bin/env python3
"""
Module pour la fonction zoom_array
Auteur SAID LAMGHARI
"""

from typing import List, Tuple


def zoom_array(lst: Tuple[int, ...], factor: int = 2) -> List[int]:
    """
    Zoomer sur un tableau en répétant
    chaque élément un certain nombre de fois.

    Args:
    lst (Tuple[int, ...]): Le tableau à zoomer.
    factor (int): Le facteur de zoom.

    Returns:
    List[int]: Le tableau zoomé.
    """
    zoomed_in: List[int] = [
        item for item in lst
        for _ in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
