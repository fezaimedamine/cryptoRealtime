# Dockerfile
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . /app

RUN ls -la


# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer les ports nécessaires (Kafka, Elasticsearch, MongoDB...)
EXPOSE 9092 9200 27017

# Lancer le service principal (peut être modifié selon ton besoin)
CMD ["python", "main.py"]
