# Étape 1 : Utiliser une image de base Python officielle et légère
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : Copier le fichier des dépendances
COPY requirements.txt .

# Étape 4 : Installer les dépendances
# --no-cache-dir réduit la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le reste du code de l'application (main.py)
COPY . .

# Étape 6 : Définir le port par défaut que Cloud Run écoutera
# $PORT est automatiquement injecté par Cloud Run, 8080 est le défaut
ENV PORT 8080

# Étape 7 : Commande pour exécuter l'application en production avec Gunicorn
# Gunicorn écoute sur toutes les interfaces (0.0.0.0) sur le port 8080
# main:app fait référence à l'objet 'app' dans le fichier 'main.py'
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]