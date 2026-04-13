import sys
import argparse
import logging
from .renommer import renommer_fichiers
from .nettoyer_fichier import nettoyer_dossier
from .convertir import csv_to_json, convert_image
from .telecharger import telecharger_fichier, recuperer_api_json
from .exceptions import AppError, FileError

def configurer_logging(verbose=False):
    """Configuration du logging : Console + Fichier."""
    niveau = logging.DEBUG if verbose else logging.INFO
    format_log = "[%(asctime)s] %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Création du formateur
    formatter = logging.Formatter(format_log, datefmt=date_format)
    
    # 1. Handler pour la CONSOLE
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # 2. Handler pour le FICHIER (app_cli.log)
    file_handler = logging.FileHandler("app_cli.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    
    # Configuration globale
    root_logger = logging.getLogger()
    root_logger.setLevel(niveau)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def nettoyer_chemin(chemin):
    """Nettoie le chemin (guillemets et conversion Windows/WSL)."""
    if not chemin: return ""
    chemin = chemin.strip().replace('"', '').replace("'", "").strip()
    if sys.platform == "linux" and len(chemin) > 2 and chemin[1] == ":":
        lettre = chemin[0].lower()
        reste = chemin[3:].replace("\\", "/")
        chemin = f"/mnt/{lettre}/{reste}"
    return chemin

def main():
    # 1. Création du parser principal
    parser = argparse.ArgumentParser(
        description="App CLI - Outil professionnel de gestion de fichiers.",
        epilog="Exemple : python3 -m app_cli nettoyer /chemin/du/dossier"
    )
    
    # Option globale : Verbose
    parser.add_argument("-v", "--verbose", action="store_true", help="Active le mode verbeux (logs détaillés)")
    
    # 2. Gestion des sous-commandes
    subparsers = parser.add_subparsers(dest="commande", required=True, help="Action à exécuter")

    # --- Sous-commande : RENOMMER ---
    p_rename = subparsers.add_parser("renommer", help="Renomme les fichiers d'un dossier")
    p_rename.add_argument("dossier", help="Dossier contenant les fichiers")
    p_rename.add_argument("--pre", default="", help="Texte à ajouter au début")
    p_rename.add_argument("--suf", default="", help="Texte à ajouter à la fin (avant extension)")

    # --- Sous-commande : NETTOYER ---
    p_clean = subparsers.add_parser("nettoyer", help="Supprime les doublons et trie par extension")
    p_clean.add_argument("dossier", help="Dossier à organiser")

    # --- Sous-commande : CONVERTIR ---
    p_conv = subparsers.add_parser("convertir", help="Conversion de données ou images")
    p_conv.add_argument("--csv", help="Fichier CSV source")
    p_conv.add_argument("--json", help="Fichier JSON destination")
    p_conv.add_argument("--img", help="Image source")
    p_conv.add_argument("--out", help="Image destination")
    p_conv.add_argument("--fmt", default="JPEG", help="Format destination (JPEG, PNG, WEBP)")

    # --- Sous-commande : TELECHARGER ---
    p_dl = subparsers.add_parser("telecharger", help="Téléchargement Web ou API")
    p_dl.add_argument("url", help="URL de la ressource")
    p_dl.add_argument("dest", help="Chemin de destination")
    p_dl.add_argument("--api", action="store_true", help="Précise s'il s'agit d'une API JSON")

    # 3. Analyse des arguments
    # Si aucun argument n'est passé, argparse affichera l'aide automatiquement grâce à required=True
    args = parser.parse_args()

    # 4. Configuration du logging
    configurer_logging(args.verbose)

    # 5. Exécution sécurisée
    try:
        if args.commande == "renommer":
            renommer_fichiers(nettoyer_chemin(args.dossier), args.pre, args.suf)
            
        elif args.commande == "nettoyer":
            nettoyer_dossier(nettoyer_chemin(args.dossier))
            
        elif args.commande == "convertir":
            if args.csv and args.json:
                csv_to_json(nettoyer_chemin(args.csv), nettoyer_chemin(args.json))
            elif args.img and args.out:
                convert_image(nettoyer_chemin(args.img), nettoyer_chemin(args.out), args.fmt)
            else:
                logging.error("Pour convertir, précisez soit (--csv ET --json), soit (--img ET --out).")
                
        elif args.commande == "telecharger":
            if args.api:
                recuperer_api_json(args.url, nettoyer_chemin(args.dest))
            else:
                telecharger_fichier(args.url, nettoyer_chemin(args.dest))

    except (FileError, AppError) as e:
        # On ne laisse jamais remonter l'exception brute, on l'affiche avec logging
        logging.error(f"Erreur applicative : {e}")
    except Exception as e:
        logging.error(f"Erreur critique inattendue : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
