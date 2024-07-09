#!/usr/bin/env python3
"""
Auteur SAID LAMGHARI
"""
import time
import asyncio
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Mesure le temps total d'exécution
    de async_comprehension
    lorsqu'il est exécuté quatre fois en parallèle.

    Returns:
        float: Temps total d'exécution en secondes.
    """
    start_tme = time.perf_counter()
    val_tsk = [async_comprehension() for i in range(4)]
    await asyncio.gather(*val_tsk)
    end_tme = time.perf_counter()
    return (end_tme - start_tme)
