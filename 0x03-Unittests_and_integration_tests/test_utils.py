#!/usr/bin/env python3
"""
0. Parameterize a unit test
1. Parameterize a unit test
Auteur SAID LAMGHARI
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Teste la fonction access_nested_map dans le module utils.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Teste que la fonction access_nested_map retourne le résultat attendu.

        :param nested_map: La carte imbriquée à tester.
        :param path: Le chemin pour accéder à la valeur.
        :param expected_result: Le résultat attendu.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), "KeyError"),
        ({"a": 1}, ("a", "b"), "KeyError"),
    ])
    def test_access_nested_map_exception(self, nested_map,
                                         path, expected_exception):
        """
        Teste que la fonction access_nested_map
        lève une exception KeyError avec le message attendu.

        :param nested_map: La carte imbriquée à tester.
        :param path: Le chemin pour accéder à la valeur.
        :param expected_exception: Le type d'exception attendu.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Vérifie que le message de l'exception est le message attendu
        self.assertEqual(str(context.exception), expected_exception)


if __name__ == "__main__":
    unittest.main()
