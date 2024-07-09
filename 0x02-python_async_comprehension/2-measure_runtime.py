#!/usr/bin/env python3
"""
Auteur SAID LAMGHARI
"""

import asyncio
import time
# Assurez-vous que le chemin d'importation est correct
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Mesure le temps total d'exécution de async_comprehension
    lorsqu'il est exécuté quatre fois en parallèle.

    Returns:
        float: Temps total d'exécution en secondes.
    """
    start_tme = time.perf_counter()
    # Utilisation de asyncio.gather pour exécuter
    # async_comprehension quatre fois en parallèle
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )

    return time.perf_counter() - start_tme
