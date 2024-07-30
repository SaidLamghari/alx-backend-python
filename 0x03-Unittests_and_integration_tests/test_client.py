#!/usr/bin/env python3
""" Tests unitaires pour la classe GithubOrgClient """

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD  # Importation des données de test
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class


class TestGithubOrgClient(TestCase):
    """ Classe pour tester le client GitHub Org """

    @parameterized.expand([
        ('google',),  # Paramètre pour le test avec l'organisation 'google'
        ('abc',)      # Paramètre pour le test avec l'organisation 'abc'
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json) -> None:
        """ Test que GithubOrgClient.org renvoie la valeur correcte """
        test_class = GithubOrgClient(org_name)
        org_value = test_class.org()

        # Vérification que get_json a été appelé avec l'URL attendue
        mock_get_json.assert_called_once_with(test_class.ORG_URL.format(org=org_name))
        self.assertEqual(org_value, org_name)  # Vérifie que la valeur renvoyée est correcte

    def test_public_repos_url(self) -> None:
        """ Test que _public_repos_url renvoie la bonne valeur basée sur la propriété org mockée """
        mock_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_payload  # Mock de la propriété org
            test_class = GithubOrgClient('test')
            result = test_class._public_repos_url  # Appel de la méthode à tester

            # Vérifie que le résultat correspond à l'URL de repos mockée
            self.assertEqual(result, mock_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        """ Test que GithubOrgClient.public_repos renvoie la liste attendue de repos """
        mock_repos_payload = [{"name": "Repo1"}, {"name": "Repo2"}]
        mock_get_json.return_value = mock_repos_payload  # Mock de la réponse de get_json

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test/repos"  # Mock de l'URL de repos
            test_class = GithubOrgClient('test')
            result = test_class.public_repos()  # Appel de la méthode à tester

            expected = [repo["name"] for repo in mock_repos_payload]  # Liste des noms de repos attendue
            self.assertEqual(result, expected)  # Vérifie que le résultat est conforme à l'attendu
            mock_public_repos_url.assert_called_once()  # Vérifie que la propriété a été appelée une fois
            mock_get_json.assert_called_once()  # Vérifie que get_json a été appelé une fois

    @parameterized_class(
        ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
        TEST_PAYLOAD  # Charge les données de test à partir de fixtures
    )
    class TestIntegrationGithubOrgClient(TestCase):
        """ Classe pour les tests d'intégration du GithubOrgClient """

        @classmethod
        def setUpClass(cls) -> None:
            """ Méthode d'installation appelée avant les tests d'intégration """
            cls.get_patcher = patch('requests.get')  # Patch de la méthode requests.get
            cls.mock_get = cls.get_patcher.start()  # Démarrage du patch

            # Configuration du comportement du mock
            cls.mock_get.side_effect = lambda url: {
                "https://api.github.com/orgs/Google": cls.org_payload,
                "https://api.github.com/orgs/Google/repos": cls.repos_payload,
            }[url]

        @classmethod
        def tearDownClass(cls) -> None:
            """ Méthode d'arrêt appelée après les tests d'intégration """
            cls.get_patcher.stop()  # Arrête le patch

        def test_public_repos(self) -> None:
            """ Test d'intégration pour public_repos """
            test_class = GithubOrgClient("Google")  # Création d'une instance de GithubOrgClient

            # Vérifie que les valeurs récupérées sont celles attendues
            self.assertEqual(test_class.org, self.org_payload)
            self.assertEqual(test_class.repos_payload, self.repos_payload)
            self.assertEqual(test_class.public_repos(), self.expected_repos)  # Vérifie les repos
            self.assertEqual(test_class.public_repos("XLICENSE"), [])  # Vérifie le comportement sans licence

        def test_public_repos_with_license(self) -> None:
            """ Test d'intégration pour les repos publics avec licence spécifiée """
            test_class = GithubOrgClient("Google")  # Création d'une instance de GithubOrgClient

            # Vérifie les repos retournés avec et sans filtre de licence
            self.assertEqual(test_class.public_repos(), self.expected_repos)
            self.assertEqual(test_class.public_repos("XLICENSE"), [])
            self.assertEqual(test_class.public_repos("apache-2.0"), self.apache2_repos)  # Vérifie la liste filtrée
