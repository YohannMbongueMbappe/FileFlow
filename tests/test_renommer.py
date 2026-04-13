# Module pour interagir avec le système de fichiers : créer, supprimer, lister des fichiers et dossiers
import os

# Module standard de Python pour créer des tests unitaires
import unittest

# Import de la fonction que l'on souhaite tester
from app_cli.renommer import renommer_fichiers

# Import de l'exception personnalisée qui sera levée si un problème survient
from app_cli.exceptions import FileError


# Création d'une classe de tests qui hérite de unittest.TestCase
class TestRenommerFichiers(unittest.TestCase):

    # Méthode exécutée avant chaque test : préparation d'un environnement propre
    def setUp(self):
        """Prépare un dossier test avant chaque test"""
        # Crée un dossier "test_folder" s'il n'existe pas déjà
        os.makedirs("test_folder", exist_ok=True)
        # Création de fichiers de test dans ce dossier
        with open("test_folder/file1.txt", "w") as f:
            f.write("test")  # Écriture d'un contenu simple
        with open("test_folder/file2.txt", "w") as f:
            f.write("test")

    # Méthode exécutée après chaque test : nettoyage de l'environnement
    def tearDown(self):
        """Nettoie le dossier test après chaque test"""
        if os.path.exists("test_folder"):
            # Supprime tous les fichiers dans le dossier
            for f in os.listdir("test_folder"):
                os.remove(os.path.join("test_folder", f))
            # Supprime le dossier lui-même
            os.rmdir("test_folder")

    # Test principal : vérifier que la fonction renomme bien les fichiers
    def test_renommer_fichiers(self):
        # Appel de la fonction avec un préfixe "test_"
        count = renommer_fichiers("test_folder", prefixe="test_")
        # Vérifie que 2 fichiers ont été renommés
        self.assertEqual(count, 2)
        # Vérifie que les fichiers ont bien le nouveau nom
        files = os.listdir("test_folder")
        self.assertIn("test_file1.txt", files)
        self.assertIn("test_file2.txt", files)

    # Test secondaire : vérifier que la fonction gère correctement un dossier inexistant
    def test_dossier_inexistant(self):
        # On s'attend à ce que la fonction lève l'exception FileError
        with self.assertRaises(FileError):
            renommer_fichiers("dossier_inexistant")


# Permet d'exécuter les tests si ce fichier est lancé directement
if __name__ == "__main__":
    unittest.main()
