import requests
import os
import logging
import json
from .exceptions import AppError

def telecharger_fichier(url, dossier_destination):
    """Télécharge un fichier avec gestion via logging."""
    logging.info(f"Requête de téléchargement : {url}")
    try:
        os.makedirs(dossier_destination, exist_ok=True)
        nom_fichier = url.split("/")[-1] or "telechargement.dat"
        chemin_complet = os.path.join(dossier_destination, nom_fichier)

        reponse = requests.get(url, stream=True, timeout=20)
        reponse.raise_for_status()

        with open(chemin_complet, 'wb') as f:
            for bloc in reponse.iter_content(chunk_size=8192):
                f.write(bloc)

        logging.info(f"Téléchargement réussi : {chemin_complet}")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur réseau : {e}")
        raise AppError(f"Echec du téléchargement réseau : {e}")
    except Exception as e:
        raise AppError(f"Erreur pendant le téléchargement : {e}")


def recuperer_api_json(url, fichier_destination):
    """Récupère JSON depuis API avec logging."""
    logging.info(f"Appel API JSON : {url}")
    try:
        reponse = requests.get(url, timeout=10)
        reponse.raise_for_status()
        donnees = reponse.json()

        with open(fichier_destination, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
            
        logging.info(f"Données API enregistrées dans {fichier_destination}")
        return True
    except Exception as e:
        logging.error(f"Erreur API : {e}")
        raise AppError(f"Impossible de récupérer les données de l'API : {e}")
