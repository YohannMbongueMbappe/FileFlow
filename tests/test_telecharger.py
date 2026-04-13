import os
import unittest
from unittest.mock import patch, MagicMock
from app_cli.telecharger import telecharger_fichier, recuperer_api_json
from app_cli.exceptions import AppError

class TestTelecharger(unittest.TestCase):

    def setUp(self):
        """Prépare les dossiers de test."""
        self.dossier_test = "test_downloads"
        self.fichier_json = "test_api.json"
        if not os.path.exists(self.dossier_test):
            os.makedirs(self.dossier_test)

    def tearDown(self):
        """Nettoie les fichiers créés."""
        if os.path.exists(self.fichier_json):
            os.remove(self.fichier_json)
        if os.path.exists(self.dossier_test):
            for f in os.listdir(self.dossier_test):
                os.remove(os.path.join(self.dossier_test, f))
            os.rmdir(self.dossier_test)

    @patch('requests.get')
    def test_telecharger_fichier_success(self, mock_get):
        """Vérifie le téléchargement d'un fichier (simulé par mock)."""
        # Configuration du mock pour simuler un téléchargement réussi
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"donnees_de_test"]
        mock_get.return_value = mock_response

        url = "https://exemple.com/testfile.png"
        succes = telecharger_fichier(url, self.dossier_test)

        self.assertTrue(succes)
        self.assertTrue(os.path.exists(os.path.join(self.dossier_test, "testfile.png")))

    def test_recuperer_api_json_reel(self):
        """Vérifie la récupération de données JSON sur une API réelle de test."""
        # On utilise une API de test très stable
        url = "https://jsonplaceholder.typicode.com/posts/1"
        succes = recuperer_api_json(url, self.fichier_json)
        
        self.assertTrue(succes)
        self.assertTrue(os.path.exists(self.fichier_json))
        
        # Vérifie que le contenu est bien chargé
        import json
        with open(self.fichier_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data["id"], 1)
            self.assertIn("title", data)

    def test_api_introuvable(self):
        """Vérifie que le système lève AppError pour une URL d'API invalide."""
        url = "https://jsonplaceholder.typicode.com/cette_page_n_existe_pas"
        with self.assertRaises(AppError):
            recuperer_api_json(url, self.fichier_json)


if __name__ == '__main__':
    unittest.main()
