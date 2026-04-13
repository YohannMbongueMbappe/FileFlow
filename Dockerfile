# Utiliser une image Python légère
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Définir la commande par défaut
# Comme c'est une CLI, on utilise ENTRYPOINT pour pouvoir passer des arguments
ENTRYPOINT ["python", "-m", "app_cli"]
