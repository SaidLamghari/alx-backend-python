#!/usr/bin/env python3
"""
Tests unitaires pour les fonctions utilitaires
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """
    Cas de test pour la fonction access_nested_map
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test que access_nested_map retourne la valeur correcte
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test que access_nested_map lève une KeyError pour des chemins invalides
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Vérifie que l'exception contient le message attendu
        self.assertEqual(cm.exception.args[0], path[-1])  # Supposons que la dernière clé dans le chemin est celle qui cause l'erreur


class TestGetJson(unittest.TestCase):
    """
    Cas de test pour la fonction get_json
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test que get_json retourne la charge utile correcte
        """
        with patch('utils.requests.get') as mock_get:
            # Simule la réponse JSON pour les tests
            mock_get.return_value = Mock(json=lambda: test_payload)
            result = get_json(test_url)
            # Vérifie que la charge utile retournée est correcte
            self.assertEqual(result, test_payload)
            # Vérifie que requests.get a été appelé avec l'URL correcte
            mock_get.assert_called_once_with(test_url)

    def test_get_json_http_error(self):
        """
        Test que get_json lève une exception HTTPError en cas d'erreur HTTP
        """
        with patch('utils.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.HTTPError("HTTP error")
            with self.assertRaises(requests.exceptions.HTTPError):
                get_json("http://example.com")


class TestMemoize(unittest.TestCase):
    """
    Cas de test pour le décorateur memoize
    """

    def test_memoize(self):
        """
        Test le décorateur memoize pour s'assurer qu'il met en cache les résultats
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            instance = TestClass()
            # Vérifie que la propriété memoized retourne la valeur correcte
            self.assertEqual(instance.a_property, 42)
            # Vérifie que la méthode a_method n'est appelée qu'une seule fois grâce au cache
            self.assertEqual(instance.a_property, 42)
            mock_method.assert_called_once()

    def test_memoize_different_inputs(self):
        """
        Test le décorateur memoize avec des entrées différentes pour vérifier le cache
        """
        class TestClass:
            @memoize
            def multiply(self, x, y):
                return x * y

        instance = TestClass()
        # Vérifie que la méthode memoized retourne la valeur correcte pour les entrées données
        self.assertEqual(instance.multiply(2, 3), 6)
        self.assertEqual(instance.multiply(2, 3), 6)  # Devrait utiliser le cache
