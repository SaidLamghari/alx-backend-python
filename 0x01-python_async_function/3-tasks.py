#!/usr/bin/env python3
"""
Module contenant une fonction pour créer
une tâche asyncio pour la coroutine wait_random.
"""

import asyncio
# Importe la coroutine wait_random du fichier 0-basic_async_syntax.py
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Crée et retourne une asyncio.Task pour la coroutine
    wait_random avec le délai maximum spécifié.

    Args:
        max_delay (int): Délai maximum à passer à wait_random.

    Returns:
        asyncio.Task: Tâche asyncio pour exécuter
        wait_random avec le délai maximum spécifié.
    """
    return asyncio.create_task(wait_random(max_delay))
