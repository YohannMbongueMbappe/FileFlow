# Module pour manipuler les fichiers et dossiers
import os

# Module pour écrire des tests unitaires
import unittest

# Import de la fonction à tester
from app_cli.nettoyer_fichier import nettoyer_dossier
from app_cli.exceptions import FileError


# Classe de test qui hérite de unittest.TestCase
class TestNettoyageDossier(unittest.TestCase):

    # Méthode exécutée AVANT chaque test
    def setUp(self):
        # Crée un dossier de test
        os.makedirs("test_folder", exist_ok=True)

        # Création de fichiers de test
        with open("test_folder/a.txt", "w") as f:
            f.write("hello")

        with open("test_folder/b.txt", "w") as f:
            f.write("hello")  # doublon (même contenu)

        with open("test_folder/image.jpg", "w") as f:
            f.write("img")

    # Méthode exécutée APRÈS chaque test (nettoyage)
    def tearDown(self):
        # Vérifie que le dossier existe
        if os.path.exists("test_folder"):
            # Parcourt tous les fichiers et sous-dossiers
            for root, dirs, files in os.walk("test_folder", topdown=False):
                # Supprime tous les fichiers
                for name in files:
                    os.remove(os.path.join(root, name))
                # Supprime tous les sous-dossiers
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            # Supprime le dossier principal
            os.rmdir("test_folder")

    # Test principal : vérifie le nettoyage du dossier
    def test_nettoyage(self):
        # Appelle la fonction à tester
        nettoyer_dossier("test_folder")

        # Vérifie que les dossiers par extension existent
        self.assertTrue(os.path.exists("test_folder/txt"))
        self.assertTrue(os.path.exists("test_folder/jpg"))

        # Vérifie qu'il ne reste qu'un seul fichier .txt (doublon supprimé)
        fichiers_txt = os.listdir("test_folder/txt")
        self.assertEqual(len(fichiers_txt), 1)

    # Test d'erreur : dossier inexistant
    def test_dossier_inexistant(self):
        # Vérifie que l'erreur personnalisée est bien levée
        with self.assertRaises(FileError):
            nettoyer_dossier("dossier_fake")


# Permet de lancer les tests si on exécute ce fichier directement
if __name__ == "__main__":
    unittest.main()
