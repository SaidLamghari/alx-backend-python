#!/usr/bin/env python3
"""
Auteur SAID LAMGHARI
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize  # Ajustez les chemins d'importation si nécessaire

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Teste la fonction access_nested_map avec divers inputs.
        
        Args:
            nested_map (dict): Le dictionnaire imbriqué à tester.
            path (tuple): Le chemin pour accéder à la valeur dans le dictionnaire.
            expected (any): Le résultat attendu.
        """
        # Vérifie si le résultat de la fonction correspond au résultat attendu
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Teste que KeyError est levée avec des inputs invalides.

        Args:
            nested_map (dict): Le dictionnaire imbriqué à tester.
            path (tuple): Le chemin pour accéder à la valeur dans le dictionnaire.
        """
        # Vérifie si une KeyError est levée lorsqu'on appelle access_nested_map avec des inputs invalides
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        
        # Vérifie que le message d'exception correspond à celui attendu
        self.assertEqual(str(context.exception), str(KeyError(path[-1])))

class TestGetJson(unittest.TestCase):
    @patch('utils.requests.get')  # Remplace requests.get utilisé dans la fonction get_json
    def test_get_json(self, mock_get):
        """
        Teste que la fonction get_json retourne le résultat attendu et fonctionne correctement.
        
        Args:
            mock_get (Mock): La méthode requests.get mockée.
        """
        # Définir les cas de test
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            # Configure le mock pour retourner le test_payload
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response
            
            # Appelle la fonction avec l'URL de test
            result = get_json(test_url)
            
            # Vérifie si requests.get a été appelé avec l'URL de test
            mock_get.assert_called_once_with(test_url)
            
            # Vérifie que le résultat correspond au test_payload
            self.assertEqual(result, test_payload)

            # Réinitialise le mock pour le prochain cas de test
            mock_get.reset_mock()

class TestMemoize(unittest.TestCase):
    @patch('utils.TestClass.a_method')  # Remplace a_method dans TestClass
    def test_memoize(self, mock_a_method):
        """
        Teste que le décorateur memoize met en cache correctement les résultats.
        
        Args:
            mock_a_method (MagicMock): La méthode a_method mockée.
        """
        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        # Crée une instance de TestClass
        instance = TestClass()
        
        # Configure le mock pour retourner une valeur spécifique
        mock_a_method.return_value = 42
        
        # Appelle la propriété mémoisée deux fois
        result_first_call = instance.a_property()
        result_second_call = instance.a_property()
        
        # Vérifie que a_method a été appelé une seule fois
        mock_a_method.assert_called_once()
        
        # Vérifie que les deux appels retournent le même résultat
        self.assertEqual(result_first_call, 42)
        self.assertEqual(result_second_call, 42)
