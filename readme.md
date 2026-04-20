# App CLI - Gestionnaire de Fichiers Professionnel

Une application en ligne de commande (CLI)  pour automatiser la gestion de vos fichiers. Ce projet respecte les standards professionnels de développement Python (Argparse, Logging, Exceptions personnalisées).

##  Fonctionnalités

L'application est découpée en **sous-commandes** accessibles directement depuis le terminal :

1.  **`renommer`** : Ajout de préfixes ou suffixes en lot (sécurisé contre les conflits).
2.  **`nettoyer`** : Suppression des doublons (hash MD5) et tri automatique par extension.
3.  **`convertir`** : Conversion de fichiers CSV -> JSON et gestion d'images (Pillow).
4.  **`telecharger`** : Téléchargement de fichiers web et récupération de données d'API JSON (Requests).

##  Installation

### 1. Prérequis
*   Python 3.12+
*   WSL (recommandé pour Windows)

### 2. Configuration
```bash
# Entrer dans le dossier
cd app_cli

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

##  Utilisation (Syntaxe CLI)

L'application n'utilise plus de menu interactif mais des **arguments de ligne de commande**.

### Exemples de commandes :

*   **Nettoyer un dossier** :
    ```bash
    python3 -m app_cli nettoyer "/chemin/du/dossier"
    ```

*   **Renommer avec un préfixe** :
    ```bash
    python3 -m app_cli renommer "/chemin/du/dossier" --pre "DOC_"
    ```

*   **Convertir un CSV en JSON** :
    ```bash
    python3 -m app_cli convertir --csv "donnees.csv" --json "donnees.json"
    ```

*   **Convertir une image** :
    ```bash
    python3 -m app_cli convertir --img "photo.png" --out "photo.jpg" --fmt "JPEG"
    ```

*   **Télécharger un fichier** :
    ```bash
    python3 -m app_cli telecharger "https://url-du-fichier.com/image.png" "./image.png"
    ```

*   **Mode détaillé (Verbose)** :
    Ajoutez `-v` pour voir chaque action effectuée par l'application :
    ```bash
    python3 -m app_cli -v nettoyer "/chemin/du/dossier"
    ```

*   **Obtenir de l'aide** :
    ```bash
    python3 -m app_cli --help
    python3 -m app_cli convertir --help
    ```

##  Qualité du Code

*   **Logging** : Tracement complet de l'exécution avec horodatage et niveaux (INFO, ERROR, DEBUG).
*   **Gestion des Exceptions** : Utilisation d'exceptions personnalisées (`FileError`, `AppError`) pour une gestion d'erreurs propre.
*   **Validation** : Nettoyage automatique des chemins (guillemets, conversion Windows/WSL).
*   **Tests** : Suite de 11 tests unitaires validant 100% de la logique métier.

Pour lancer les tests :
```bash
python3 -m unittest discover -s tests -v
```
