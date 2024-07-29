#!/usr/bin/env python3
"""
Tests pour les fonctions du module utils.
Auteur SAID LAMGHARI
"""
from unittest.mock import patch
import unittest
import requests
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Classe de tests pour la
    fonction access_nested_map.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map,
                               path, expected):
        """
        Teste la fonction access_nested_map avec différentes entrées.
        Args:
            nested_map (Dict): Un dictionnaire qui peut
            contenir des dictionnaires imbriqués.
            path (List, tuple): Clés pour accéder à la valeur
            souhaitée dans le dictionnaire imbriqué.
            expected (Any): La valeur attendue après
            avoir accédé au chemin dans le dictionnaire.
        """
        rps = access_nested_map(nested_map, path)
        self.assertEqual(rps, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map,
                                         path):
        """
        Teste que la fonction access_nested_map lève
        une exception lorsque le chemin est invalide.
        Args:
            nested_map (Dict): Un dictionnaire qui
            peut contenir des dictionnaires imbriqués.
            path (List, tuple): Clés pour accéder à la
            valeur souhaitée dans le dictionnaire imbriqué.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Classe de tests pour
    la fonction get_json.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_requests_get):
        """
        Teste que la fonction get_json retourne les données JSON attendues.
        Args:
            test_url (str): URL vers laquelle envoyer la requête HTTP.
            test_payload (dict): La réponse JSON attendue.
            mock_requests_get (patch): Mock pour requests.get.
        """
        # Configuration du mock pour retourner une réponse spécifique
        mock_requests_get.return_value.json.return_value = test_payload

        # Appel de la fonction testée
        rslt = get_json(test_url)

        # Vérification que le résultat est celui attendu
        self.assertEqual(rslt, test_payload)

        # Vérification que requests.get a été
        # appelé une fois avec l'URL correcte
        mock_requests_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Classe de tests pour le décorateur memoize.
    """
    def test_memoize(self):
        """
        Teste que le décorateur memoize fonctionne
        correctement en mémorisant le résultat d'une méthode.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_method:
            test_instance = TestClass()

            # Premier appel devrait appeler a_method
            rslto = test_instance.a_property()
            # Deuxième appel ne
            # devrait pas rappeler a_method
            rslts = test_instance.a_property()

            # Vérification des résultats
            self.assertEqual(rslto, 42)
            self.assertEqual(rslts, 42)

            # Vérification que a_method n'a
            # été appelé qu'une seule fois
            mock_method.assert_called_once()
