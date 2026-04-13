import os
import hashlib
import shutil
import logging
from .exceptions import FileError, AppError

def hash_fichier(chemin_fichier):
    """Calcule un hash MD5 pour détecter les doublons."""
    try:
        h = hashlib.md5()
        with open(chemin_fichier, "rb") as f:
            for bloc in iter(lambda: f.read(4096), b""):
                h.update(bloc)
        return h.hexdigest()
    except Exception as e:
        logging.debug(f"Impossible de lire le fichier pour hash : {chemin_fichier} ({e})")
        return None

def nettoyer_dossier(dossier):
    """Nettoie un dossier avec traçage via logging."""
    if not os.path.exists(dossier):
        raise FileError(f"Le dossier '{dossier}' n'existe pas.")
    
    logging.info(f"Démarrage du nettoyage du dossier : {dossier}")
    try:
        hashes = {}
        # 1. Doublons
        for nom_fichier in os.listdir(dossier):
            chemin_complet = os.path.join(dossier, nom_fichier)
            if os.path.isfile(chemin_complet):
                h = hash_fichier(chemin_complet)
                if h in hashes:
                    logging.info(f"Suppression du doublon : {nom_fichier}")
                    os.remove(chemin_complet)
                else:
                    hashes[h] = chemin_complet

        # 2. Tri
        for nom_fichier in os.listdir(dossier):
            chemin_complet = os.path.join(dossier, nom_fichier)
            if os.path.isfile(chemin_complet):
                ext = os.path.splitext(nom_fichier)[1].lower()[1:] or "sans_extension"
                ss_dossier = os.path.join(dossier, ext)
                os.makedirs(ss_dossier, exist_ok=True)
                
                dest = os.path.join(ss_dossier, nom_fichier)
                if not os.path.exists(dest):
                    shutil.move(chemin_complet, dest)
                    logging.debug(f"Déplacé : {nom_fichier} -> {ext}/")
        
        logging.info("Nettoyage du dossier terminé.")

    except PermissionError:
        raise FileError(f"Accès refusé au dossier : {dossier}")
    except Exception as e:
        raise AppError(f"Problème lors du nettoyage : {e}")
