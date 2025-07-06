# Dockerfile pour Discover Analyzer
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY requirements_minimal.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements_minimal.txt

# Copier le code source
COPY . .

# Exposer le port pour Streamlit
EXPOSE 8501

# Commande par défaut : lancer le dashboard
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]