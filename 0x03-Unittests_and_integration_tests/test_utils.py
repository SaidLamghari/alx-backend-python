#!/usr/bin/env python3
"""
Ce module contient des tests unitaires pour la fonction utils.access_nested_map.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """
    Test case pour la fonction access_nested_map.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test la fonction access_nested_map avec différentes entrées.

        Args:
            nested_map (dict): La carte imbriquée à accéder.
            path (tuple): La séquence de clés pour accéder à la valeur.
            expected (Any): La valeur attendue à retourner.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "KeyError: 'a'"),
        ({"a": 1}, ("a", "b"), "KeyError: 'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception):
        """
        Test que la fonction access_nested_map lève une KeyError avec le message d'exception attendu.

        Args:
            nested_map (dict): La carte imbriquée à accéder.
            path (tuple): La séquence de clés pour accéder à la valeur.
            expected_exception (str): Le message d'exception attendu.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_exception)


class TestGetJson(unittest.TestCase):
    """
    Test case pour la fonction get_json.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test que la fonction get_json retourne le résultat attendu.

        Args:
            test_url (str): L'URL à tester.
            test_payload (dict): La charge utile attendue à retourner.
        """
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test case pour le décorateur memoize.
    """

    class TestClass:
        """
        Classe de test pour le décorateur memoize.
        """
        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    @patch.object(TestClass, 'a_method')
    def test_memoize(self, mock_a_method):
        """
        Test que le décorateur memoize met en cache le résultat de a_property.
        """
        mock_a_method.return_value = 42
        test_instance = self.TestClass()
        self.assertEqual(test_instance.a_property, 42)
        self.assertEqual(test_instance.a_property, 42)
        mock_a_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
