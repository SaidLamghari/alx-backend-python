#!/usr/bin/env python3
"""
Tests unitaires et d'intégration pour la classe GithubOrgClient.
Ce module utilise unittest, parameterized,
et unittest.mock pour tester les fonctionnalités.
Auteur SAID LAMGHARI
"""
from fixtures import TEST_PAYLOAD
from client import GithubOrgClient
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """
    Classe de tests pour la classe GithubOrgClient.

    Cette classe contient des tests unitaires
    pour vérifier le comportement des méthodes
    de la classe GithubOrgClient. Elle utilise
    le décorateur @parameterized.expand pour
    tester des cas multiples et @patch pour
    simuler les dépendances externes.
    """

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Teste que la méthode org retourne les
        bonnes informations pour une organisation.

        Paramètres :
        - org_name : Nom de l'organisation à tester.
        - mock_get_json : Mock de la fonction
        get_json pour empêcher les appels HTTP réels.
        """
        # URL attendue pour l'organisation donnée
        expected_url = f"https://api.github.com/orgs/{org_name}"
        # Mock de la réponse de get_json
        mock_get_json.return_value = {"login": org_name}

        # Initialisation du client et appel de la méthode org
        client = GithubOrgClient(org_name)
        result = client.org

        # Vérification que le résultat et l'appel au mock sont corrects
        self.assertEqual(result["login"], org_name)
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        Teste que _public_repos_url retourne
        la bonne URL des dépôts publics.

        Utilise un mock pour la méthode org
        pour simuler une réponse de l'API GitHub.
        """
        # Mock de la méthode org pour
        # retourner une URL de dépôt connue
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            expected_repos_url = "https://api.github.com/orgs/test/repos"
            mock_org.return_value = {"repos_url": expected_repos_url}

            # Initialisation du client et vérification de _public_repos_url
            client = GithubOrgClient('test')
            result = client._public_repos_url
            self.assertEqual(result, expected_repos_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Teste la méthode public_repos pour
        retourner la liste des dépôts publics.

        Paramètres :
        - mock_get_json : Mock de la fonction
        get_json pour retourner un payload de test.
        """
        # Payload fictif pour simuler des dépôts publics
        repos_payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_get_json.return_value = repos_payload

        # Mock de _public_repos_url pour éviter les appels réseau
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            link = "https://api.github.com/orgs/test/repos"
            mock_public_repos_url.return_value = link

            # Initialisation du client et vérification de public_repos
            client = GithubOrgClient('test')
            result = client.public_repos()
            self.assertEqual(result, [repo["name"] for repo in repos_payload])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Teste la méthode has_license pour vérifier la présence d'une licence.

        Paramètres :
        - repo : Dictionnaire représentant un dépôt.
        - license_key : Clé de licence à vérifier.
        - expected : Résultat attendu (True ou False).
        """
        # Vérification que le résultat de has_license est comme
        rslt = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(rslt, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Tests d'intégration pour la classe GithubOrgClient avec des fixtures.

    Cette classe de tests utilise les fixtures
    fournies dans TEST_PAYLOAD pour vérifier
    les méthodes de la classe GithubOrgClient
    sans effectuer d'appels externes réels.
    """

    @classmethod
    def setUpClass(cls):
        """
        Prépare le test en simulant requests.get.

        Cette méthode est appelée une fois
        avant tous les tests de la classe.
        """
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()
        mock_get.return_value.json.side_effect = [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload
        ]

    def test_public_repos(self):
        """
        Teste la méthode public_repos pour vérifier les dépôts publics.

        Utilise les données simulées de org_payload
        et repos_payload pour les assertions.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.org, self.org_payload)
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("XLICENSE"), [])

    def test_public_repos_with_license(self):
        """
        Teste public_repos avec un filtre de licence spécifique.

        Vérifie que seuls les dépôts avec
        la licence apache-2.0 sont retournés.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("XLICENSE"), [])
        self.assertEqual(client.public_repos("apache-2.0"),
                         self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """
        Nettoie après les tests en arrêtant le patcher.

        Cette méthode est appelée une fois
        après tous les tests de la classe.
        """
        cls.get_patcher.stop()
