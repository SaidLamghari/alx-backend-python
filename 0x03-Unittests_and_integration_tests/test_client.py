#!/usr/bin/env python3
"""
Tests unitaires pour le module client
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Cas de test pour GithubOrgClient
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Teste que la méthode org de
        GithubOrgClient retourne la valeur correcte
        """
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assrt_cd_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Teste que _public_repos_url retourne la valeur
        correcte en fonction de l'organisation simulée
        """
        mock_org.return_value = {"repos_url": "http://example.com/repos"}
        client = GithubOrgClient("test")
        self.assertEqual(client._public_repos_url, "http://example.com/repos")

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Teste la méthode public_repos
        """
        mock_public_repos_url.return_value = "http://example.com/repos"
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("test")
        self.assertEqual(client.pc_repos(), ["repo1", "repo2"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assrt_cd_with("http://example.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Teste la méthode has_license
        """
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Cas de test d'intégration pour GithubOrgClient
    """

    @classmethod
    def setUpClass(cls):
        """
        Configuration des fixtures de classe
        """
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            cls.mock_response(org_payload),
            cls.mock_response(repos_payload)
        ]

    @classmethod
    def tearDownClass(cls):
        """
        Nettoyage des fixtures de classe
        """
        cls.get_patcher.stop()

    @staticmethod
    def mock_response(payload):
        """
        Fonction utilitaire pour simuler une réponse HTTP
        """
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = payload
        return mock_response

    def test_public_repos(self):
        """
        Teste la méthode public_repos
        """
        client = GithubOrgClient("test")
        self.assertEqual(client.pc_repos(), expected_repos)

    def test_public_repos_with_license(self):
        """
        Teste public_repos avec l'argument license
        """
        client = GithubOrgClient("test")
        self.assertEqual(client.pc_repos(license="apache-2.0"), apache2_repos)
