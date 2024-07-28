#!/usr/bin/env python3
"""
Tests unitaires pour les fonctions utilitaires
Auteur SAID LAMGHARI
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
        Teste que access_nested_map retourne
        la valeur correcte en fonction du chemin
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Teste que access_nested_map lève
        une KeyError pour des chemins invalides
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Vérifie que le message d'exception
        # correspond au chemin recherché
        self.assertEqual(str(cm.exception), str(path))


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
        Teste que get_json retourne
        le payload correct pour une URL donnée
        """
        with patch('utils.requests.get') as mock_get:
            # Configure le mock pour que
            # la méthode json() retourne le payload de test
            mock_get.return_value = Mock(json=lambda: test_payload)
            result = get_json(test_url)
            # Vérifie que le résultat de get_json est celui attendu
            self.assertEqual(result, test_payload)
            # Vérifie que requests.get a été
            # appelé exactement une fois avec l'URL donnée
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Cas de test pour le décorateur memoize
    """

    def test_memoize(self):
        """
        Teste le décorateur memoize pour
        s'assurer qu'il met en cache les résultats
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Crée une instance de TestClass et remplace a_method par un mock
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_mthd:
            instance = TestClass()
            # Appelle a_property deux fois
            self.assertEqual(instance.a_property, 42)
            self.assertEqual(instance.a_property, 42)
            # Vérifie que a_method n'a été appelé qu'une seule fois
            mock_mthd.assert_called_once()
