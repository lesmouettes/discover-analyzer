# 🚀 Configuration GitHub pour Discover Analyzer

## 📋 Étapes pour sauvegarder sur GitHub

### 1. Créer un nouveau repository sur GitHub

1. Allez sur https://github.com/new
2. Nom du repository : `discover-analyzer`
3. Description : "Analyseur de titres Google Discover avec classification automatique et détection de patterns"
4. Choisir : **Public** ou **Private**
5. NE PAS initialiser avec README (on l'a déjà)
6. Cliquer sur **Create repository**

### 2. Connecter votre repository local à GitHub

Après avoir créé le repo sur GitHub, exécutez ces commandes :

```bash
# Remplacez YOUR_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/YOUR_USERNAME/discover-analyzer.git

# Vérifier la connexion
git remote -v

# Pousser le code
git push -u origin main
```

### 3. Si vous utilisez SSH (recommandé)

```bash
# Configuration SSH
git remote set-url origin git@github.com:YOUR_USERNAME/discover-analyzer.git

# Pousser avec SSH
git push -u origin main
```

## 📁 Structure du projet sauvegardée

```
discover-analyzer/
├── src/                    # Code source principal
├── config/                 # Configuration des catégories
├── data/                   # Données d'exemple
├── exports/                # Résultats (ignorés par git)
├── tests/                  # Scripts de test
├── requirements.txt        # Dépendances complètes
├── requirements_minimal.txt # Dépendances minimales
├── README.md              # Documentation principale
├── LICENSE                # Licence MIT
└── .gitignore            # Fichiers à ignorer
```

## 🔒 Fichiers ignorés (non sauvegardés)

- `exports/*` - Résultats d'analyse
- `data/*.csv` - Fichiers CSV (sauf exemple)
- `venv/` - Environnement virtuel
- `*.log` - Fichiers de log
- `__pycache__/` - Cache Python

## 📝 Prochaines étapes après GitHub

1. **Ajouter des Actions GitHub** pour tests automatiques
2. **Créer des releases** avec versions tagguées
3. **Ajouter des badges** au README (build status, etc.)
4. **Configurer les Issues** pour le suivi des bugs/features

## 🏷️ Commandes Git utiles

```bash
# Voir l'état actuel
git status

# Voir l'historique
git log --oneline

# Créer une nouvelle branche
git checkout -b feature/nouvelle-fonctionnalite

# Sauvegarder les changements
git add .
git commit -m "Description des changements"
git push

# Mettre à jour depuis GitHub
git pull origin main
```

## 🤝 Contribution

Pour contribuer au projet :

1. Fork le repository
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

✅ Le projet est maintenant prêt à être poussé sur GitHub !