#!/usr/bin/env python3
"""Tests unitaires et d'intégration pour GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from typing import Dict, List


class TestGithubOrgClient(unittest.TestCase):
    """Classe de test pour Github Org Client."""

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, input: str, mock_get_json: unittest.mock.Mock) -> None:
        """Teste que GithubOrgClient.org retourne la valeur correcte."""
        test_class = GithubOrgClient(input)
        test_class.org()
        mock_get_json.assert_called_once_with(test_class.ORG_URL.format(org=input))

    def test_public_repos_url(self) -> None:
        """
        Teste que le résultat de _public_repos_url retourne la valeur correcte 
        basée sur le payload donné.
        """
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
            mock_org.return_value = payload
            test_class = GithubOrgClient('test')
            result = test_class._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: unittest.mock.Mock) -> None:
        """
        Teste que la liste des dépôts publics est correcte et que les mocks sont appelés une fois.
        """
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test/repos"
            test_class = GithubOrgClient('test')
            result = test_class.public_repos()
            expected = [repo["name"] for repo in payload]
            self.assertEqual(result, expected)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
        """Teste la méthode has_license pour différents scénarios."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Classe de tests d'intégration des fixtures pour GithubOrgClient."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Configure les patchs avant l'exécution des tests dans la classe."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()
        
        # Configuration de mock pour retourner des valeurs spécifiques selon l'URL
        mock_get.return_value.json.side_effect = [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        """Arrête les patchs après l'exécution des tests dans la classe."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Teste l'intégration des dépôts publics."""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])

    def test_public_repos_with_license(self) -> None:
        """Teste l'intégration des dépôts publics avec une licence spécifiée."""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
