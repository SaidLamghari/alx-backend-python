#!/usr/bin/env python3
"""
Tests unitaires pour les fonctions utilitaires.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """
    Cas de test pour la fonction access_nested_map.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: any):
        """
        Teste que access_nested_map retourne la valeur correcte.

        Paramètres:
        nested_map (dict): Le dictionnaire à rechercher.
        path (tuple): La séquence de clés pour parcourir le dictionnaire.
        expected (any): Le résultat attendu à partir du dictionnaire imbriqué.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple):
        """
        Teste que access_nested_map lève une KeyError pour des chemins invalides.

        Paramètres:
        nested_map (dict): Le dictionnaire à rechercher.
        path (tuple): La séquence de clés pour parcourir le dictionnaire.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), str(path))


class TestGetJson(unittest.TestCase):
    """
    Cas de test pour la fonction get_json.
    """
    
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: dict):
        """
        Teste que get_json retourne la charge utile correcte.

        Paramètres:
        test_url (str): L'URL à requêter.
        test_payload (dict): La réponse JSON attendue.
        """
        with patch('utils.requests.get') as mock_get:
            mock_get.return_value = Mock(json=lambda: test_payload)
            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Cas de test pour le décorateur memoize.
    """

    def test_memoize(self):
        """
        Teste le décorateur memoize pour s'assurer que la méthode est appelée une seule fois.

        Ce test vérifie que la méthode mémorisée retourne le résultat correct
        mais que la méthode originale est appelée une seule fois.
        """

        class TestClass:
            """
            Classe pour tester le décorateur memoize.
            """
            def a_method(self) -> int:
                """
                Méthode qui retourne une valeur fixe.

                Retourne:
                int: La valeur fixe 42.
                """
                return 42

            @memoize
            def a_property(self) -> int:
                """
                Propriété qui utilise la mémorisation pour retourner le résultat de a_method.

                Retourne:
                int: Le résultat de a_method.
                """
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            instance = TestClass()
            self.assertEqual(instance.a_property, 42)
            self.assertEqual(instance.a_property, 42)
            mock_method.assert_called_once()

if __name__ == '__main__':
    unittest.main()
