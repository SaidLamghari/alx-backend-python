#!/usr/bin/env python3
"""
Tests unitaires pour les fonctions utilitaires
Auteur: SAID LAMGHARI
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
        ({"a": 1}, ("a",), 1),  # Teste avec un dictionnaire simple et un chemin direct
        ({"a": {"b": 2}}, ("a",), {"b": 2}),  # Teste avec un dictionnaire imbriqué et un chemin partiel
        ({"a": {"b": 2}}, ("a", "b"), 2)  # Teste avec un dictionnaire imbriqué et un chemin complet
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Teste que access_nested_map retourne la valeur correcte pour des chemins valides.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),  # Dictionnaire vide avec un chemin invalide
        ({"a": 1}, ("a", "b"))  # Dictionnaire avec un chemin inexistant
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Teste que access_nested_map lève une KeyError pour des chemins invalides.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Vérifie que le message d'exception correspond à la clé qui a causé l'erreur
        self.assertEqual(str(cm.exception), str(path[-1]))


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
        Teste que get_json retourne le payload correct pour une URL donnée.
        """
        with patch('utils.requests.get') as mock_get:
            # Configure le mock pour retourner le payload de test
            mock_get.return_value = Mock(json=lambda: test_payload)
            
            # Appelle get_json et vérifie le résultat
            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            
            # Vérifie que requests.get a été
            # appelé une seule fois avec l'URL correcte
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Cas de test pour le décorateur memoize
    """

    def test_memoize(self):
        """
        Teste que le décorateur memoize met en cache
        les résultats et appelle la méthode uniquement une fois.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Utilise patch.object pour mocker la méthode a_method
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            instance = TestClass()
            # Accède à la propriété mémoïsée deux fois
            self.assertEqual(instance.a_property, 42)
            self.assertEqual(instance.a_property, 42)
            # Vérifie que a_method a été appelé une
            # seule fois en raison de la mise en cache
            mock_method.assert_called_once()
