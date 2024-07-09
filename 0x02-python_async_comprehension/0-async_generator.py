#!/usr/bin/env python3
""" Auteur SAID LAMGHARI """

import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    """
    Générateur asynchrone qui génère des nombres aléatoires
    entre 0 et 10 après chaque attente d'une seconde, répété 10 fois.

    Yields:
        float: Nombre aléatoire généré entre 0 et 10.
    """
    for _ in range(10):
        # Attendre 1 seconde de manière asynchrone
        await asyncio.sleep(1)
        # Générer un nombre aléatoire entre 0 et 10
        yield random.uniform(0, 10)
