#!/usr/bin/env python3
"""
Module contenant une coroutine asynchrone pour
créer plusieurs tâches avec task_wait_random.
"""

import asyncio
from typing import List
# Importe la fonction task_wait_random du fichier 3-tasks.py
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Crée n tâches avec task_wait_random et retourne la liste des délais.

    Args:
        n (int): Nombre de tâches à créer.
        max_delay (int): Délai maximum à passer à
        chaque appel de task_wait_random.

    Returns:
        List[float]: Liste des délais générés par
        task_wait_random, triés par ordre croissant.
    """
    # Crée une liste de tâches asyncio avec task_wait_random
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    # Exécute toutes les tâches demanière
    # concurrente et attend leur achèvement
    delays = await asyncio.gather(*tasks)
    # Trie les délais générés par task_wait_random par ordre croissant
    return sorted(delays)
