import os
import logging
from .exceptions import FileError, AppError

def renommer_fichiers(dossier, prefixe="", suffixe=""):
    """Renomme les fichiers d'un dossier avec traçage via logging."""
    if not os.path.exists(dossier):
        raise FileError(f"Le dossier '{dossier}' n'existe pas.")

    logging.info(f"Début du renommage dans : {dossier}")
    try:
        count = 0
        fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
        
        for nom_fichier in fichiers:
            chemin_complet = os.path.join(dossier, nom_fichier)
            nom_base, extension = os.path.splitext(nom_fichier)
            nouveau_nom = f"{prefixe}{nom_base}{suffixe}{extension}"
            nouveau_chemin = os.path.join(dossier, nouveau_nom)

            if os.path.exists(nouveau_chemin) and nouveau_chemin != chemin_complet:
                logging.warning(f"Conflit de nom : {nouveau_nom} existe déjà. Ignoré.")
                continue

            os.rename(chemin_complet, nouveau_chemin)
            logging.debug(f"Renommé : {nom_fichier} -> {nouveau_nom}")
            count += 1

        logging.info(f"Opération terminée : {count} fichiers renommés.")
        return count

    except PermissionError:
        raise FileError(f"Droits insuffisants pour modifier le dossier {dossier}")
    except Exception as e:
        raise AppError(f"Erreur inattendue pendant le renommage : {e}")