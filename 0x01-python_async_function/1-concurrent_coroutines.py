#!/usr/bin/env python3
"""
Module contenant une coroutine asynchrone pour
attendre plusieurs délais aléatoires simultanément.
"""

import asyncio
from typing import List
# Importe la coroutine wait_random du fichier 0-basic_async_syntax.py
from 0-basic_async_syntax import wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Coroutine asynchrone qui appelle wait_random
    n fois avec un délai maximum spécifié
    et retourne la liste des délais dans l'ordre croissant.

    Args:
        n (int): Nombre de fois où wait_random doit être appelé.
        max_delay (int): Délai maximum à passer à chaque appel de wait_random.

    Returns:
        List[float]: Liste des délais générés
        par wait_random, triés par ordre croissant.
    """
    # Crée une liste de tâches à exécuter, où chaque tâche
    # est une invocation de wait_random avec max_delay spécifié
    valtasks = [wait_random(max_delay) for _ in range(n)]

    # Exécute toutes les tâches de manière
    # concurrente et attend leur achèvement
    valdelays = await asyncio.gather(*valtasks)

    # Trie les délais générés par wait_random par ordre croissant
    return sorted(valdelays)
