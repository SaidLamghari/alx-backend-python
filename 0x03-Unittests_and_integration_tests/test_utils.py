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
        Teste que access_nested_map retourne la valeur correcte pour un chemin donné.
        
        Args:
            nested_map (dict): Dictionnaire imbriqué à tester.
            path (tuple): Chemin pour accéder à la valeur dans le dictionnaire.
            expected (any): Valeur attendue à obtenir.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Teste que access_nested_map lève une KeyError pour des chemins invalides.
        
        Args:
            nested_map (dict): Dictionnaire imbriqué à tester.
            path (tuple): Chemin pour accéder à la valeur dans le dictionnaire.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Vérifie que le message d'exception correspond au chemin recherché
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
        Teste que get_json retourne le payload correct pour une URL donnée.
        
        Args:
            test_url (str): URL pour tester la fonction get_json.
            test_payload (dict): Payload attendu en réponse à l'URL.
        """
        with patch('utils.requests.get') as mock_get:
            # Configure le mock pour que la méthode json() retourne le payload de test
            mock_get.return_value = Mock(json=lambda: test_payload)
            result = get_json(test_url)
            # Vérifie que le résultat de get_json est celui attendu
            self.assertEqual(result, test_payload)
            # Vérifie que requests.get a été appelé exactement une fois avec l'URL donnée
            mock_get.assert_called_once_with(test_url)

class TestMemoize(unittest.TestCase):
    """
    Cas de test pour le décorateur memoize
    """

    def test_memoize(self):
        """
        Teste le décorateur memoize pour s'assurer qu'il met en cache les résultats.
        
        Vérifie que a_method est appelé une seule fois même si a_property est accédé plusieurs fois.
        """
        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            instance = TestClass()
            # Appelle a_property deux fois
            result_first_call = instance.a_property()
            result_second_call = instance.a_property()
            # Vérifie que a_method a été appelé une seule fois
            mock_method.assert_called_once()
            # Vérifie que les deux appels retournent le même résultat
            self.assertEqual(result_first_call, 42)
            self.assertEqual(result_second_call, 42)
