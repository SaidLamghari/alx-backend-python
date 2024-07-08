#!/usr/bin/env python3
"""
Module pour mesurer le temps d'exécution de
la coroutine wait_n avec différents paramètres.
"""

import time
import asyncio
# Importe la coroutine wait_n du fichier 1-concurrent_coroutines.py
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Mesure le temps total d'exécution de wait_n(n, max_delay)
    et retourne le temps moyen par coroutine.

    Args:
        n (int): Nombre de coroutines à exécuter
        simultanément avec wait_n.
        max_delay (int): Délai maximum
        à passer à chaque appel de wait_n.

    Returns:
        float: Temps moyen d'exécution par coroutine, en secondes.
    """
    # Temps de début de l'exécution
    strt_time = time.time()
    # Exécute la coroutine wait_n avec les paramètres donnés
    asyncio.run(wait_n(n, max_delay))
    # Calcul du temps total d'exécution
    ttl_time = time.time() - strt_time
    # Retourne le temps moyen par coroutine
    return ttl_time / n
