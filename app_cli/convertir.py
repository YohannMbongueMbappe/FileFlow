import csv
import json
import os
import logging
from PIL import Image
from .exceptions import FileError, AppError

def csv_to_json(csv_file, json_file):
    """Convertit CSV en JSON avec logging et exceptions personnalisées."""
    logging.info(f"Conversion CSV -> JSON : {csv_file}")
    try:
        if not os.path.exists(csv_file):
            raise FileError(f"Le fichier CSV {csv_file} est introuvable.")

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logging.info(f"Conversion réussie vers {json_file}")

    except FileError as e:
        logging.error(e)
        raise
    except Exception as e:
        raise AppError(f"Erreur de conversion CSV : {e}")


def convert_image(input_path, output_path, output_format):
    """Convertit une image avec logging et exceptions personnalisées."""
    logging.info(f"Conversion Image ({output_format}) : {input_path}")
    try:
        if not os.path.exists(input_path):
            raise FileError(f"L'image {input_path} est introuvable.")

        img = Image.open(input_path)
        img.save(output_path, format=output_format.upper())
        logging.info(f"Image enregistrée : {output_path}")

    except FileError as e:
        logging.error(e)
        raise
    except Exception as e:
        raise AppError(f"Erreur de conversion Image : {e}")
