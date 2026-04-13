# Module pour manipuler les fichiers et dossiers
import os
import json
import csv

# Module pour écrire des tests unitaires
import unittest

# Import des fonctions à tester et de l'exception
from app_cli.convertir import csv_to_json, convert_image
from app_cli.exceptions import FileError


class TestCsvToJson(unittest.TestCase):

    def setUp(self):
        """Prépare les fichiers temporaires avant chaque test."""
        self.csv_file = "test_data.csv"
        self.json_file = "test_data.json"

        # Crée un fichier CSV de test
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nom", "age"])
            writer.writeheader()
            writer.writerow({"nom": "Alice", "age": "30"})
            writer.writerow({"nom": "Bob", "age": "25"})

    def tearDown(self):
        """Supprime les fichiers temporaires après chaque test."""
        for fichier in [self.csv_file, self.json_file]:
            if os.path.exists(fichier):
                os.remove(fichier)

    def test_conversion_csv_vers_json(self):
        """Vérifie que le fichier JSON est créé avec le bon contenu."""
        csv_to_json(self.csv_file, self.json_file)

        # Vérifie que le fichier JSON a bien été créé
        self.assertTrue(os.path.exists(self.json_file))

        # Vérifie le contenu du JSON
        with open(self.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["nom"], "Alice")
        self.assertEqual(data[1]["nom"], "Bob")

    def test_fichier_csv_inexistant(self):
        """Vérifie que la fonction lève FileError si le CSV est absent."""
        with self.assertRaises(FileError):
            csv_to_json("fichier_inexistant.csv", self.json_file)


class TestConvertImage(unittest.TestCase):

    def setUp(self):
        """Crée une image PNG de test."""
        from PIL import Image
        self.input_path = "test_image.png"
        self.output_path = "test_image_output.jpg"

        # Crée une image rouge 10x10 pixels
        img = Image.new("RGB", (10, 10), color=(255, 0, 0))
        img.save(self.input_path)

    def tearDown(self):
        """Supprime les fichiers image temporaires."""
        for fichier in [self.input_path, self.output_path]:
            if os.path.exists(fichier):
                os.remove(fichier)

    def test_conversion_image(self):
        """Vérifie que l'image est convertie dans le nouveau format."""
        convert_image(self.input_path, self.output_path, "JPEG")
        self.assertTrue(os.path.exists(self.output_path))

    def test_image_inexistante(self):
        """Vérifie que la fonction lève FileError si l'image est absente."""
        with self.assertRaises(FileError):
            convert_image("image_inexistante.png", self.output_path, "JPEG")


# Permet de lancer les tests si on exécute ce fichier directement
if __name__ == "__main__":
    unittest.main()
