#!/usr/bin/env python3
"""
Auteur SAID LAMGHARI
"""

import asyncio
from typing import List
# Assurez-vous que le chemin d'importation est correct
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Utilise une compréhension asynchrone pour collecter
    10 nombres aléatoires générés par async_generator.

    Returns:
        List[float]: Liste de 10 nombres aléatoires.
    """
    # Utilisation de la compréhension asynchrone
    # pour collecter les résultats de async_generator
    return [ik async for ik in async_generator()]
