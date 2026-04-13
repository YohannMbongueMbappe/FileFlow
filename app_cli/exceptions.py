class FileError(Exception):
    """Exception levée pour les erreurs liées aux fichiers et dossiers (inexistance, droits)."""
    pass

class AppError(Exception):
    """Exception levée pour les erreurs de logique applicative ou de traitement de données."""
    pass
