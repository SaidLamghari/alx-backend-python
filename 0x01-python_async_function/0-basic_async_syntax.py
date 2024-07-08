#!/usr/bin/env python3
"""
Coroutine asynchrone `wait_random` qui attend
un délai aléatoire entre 0 et max_delay secondes.

Utilisation :
    import asyncio

    wait_random = __import__('0-basic_async_syntax').wait_random

    print(asyncio.run(wait_random())# Exécute avec max_delay par défaut = 10
    print(asyncio.run(wait_random(5)))# Exécute avec max_delay = 5
    print(asyncio.run(wait_random(15)))# Exécute avec max_delay = 15
"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Coroutine asynchrone qui attend un délai
    aléatoire entre 0 et max_delay secondes.

    Args:
        max_delay (float): Nombre maximum de
        secondes à attendre (par défaut 10).

    Returns:
        float: Le délai aléatoire qui a été attendu.
    """
    # Génère un délai aléatoire
    valdelay = random.uniform(0, max_delay)
    # Attend de manière asynchrone le délai
    await asyncio.sleep(valdelay)
    # Retourne le délai une fois complété
    return valdelay
