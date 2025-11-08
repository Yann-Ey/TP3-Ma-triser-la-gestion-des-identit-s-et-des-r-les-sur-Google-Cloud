import os
from flask import Flask, jsonify
from google.cloud import storage

app = Flask(__name__)

# Récupère le nom du bucket depuis une variable d'environnement
# C'est une bonne pratique pour ne pas coder en dur le nom du bucket.
BUCKET_NAME = os.environ.get('BUCKET_NAME')

@app.route("/list")
def list_files():
    """
    Expose la route /list qui liste les fichiers du bucket.
    """
    if not BUCKET_NAME:
        return "Erreur: La variable d'environnement BUCKET_NAME n'est pas définie.", 500

    try:
        # L'authentification est automatique grâce aux "Application Default Credentials"
        # (voir explication plus bas)
        storage_client = storage.Client()
        
        # Récupère le bucket
        bucket = storage_client.bucket(BUCKET_NAME)

        # Liste les "blobs" (fichiers) dans le bucket
        blobs = bucket.list_blobs()
        
        # Crée une liste simple avec les noms des fichiers
        file_names = [blob.name for blob in blobs]

        # Renvoie la liste au format JSON
        return jsonify(file_names)

    except Exception as e:
        return f"Erreur lors de la communication avec le bucket: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))