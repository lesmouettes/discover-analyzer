"""
Script pour sauvegarder automatiquement les changements sur GitHub
"""

import subprocess
import os
from datetime import datetime
from pathlib import Path

def run_git_command(cmd):
    """Exécute une commande git et retourne le résultat"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def auto_save_to_github(message=None, token=None):
    """Sauvegarde automatique des changements sur GitHub"""
    
    # Token par défaut si non fourni
    if not token:
        token = os.getenv('GITHUB_TOKEN')
    
    # Vérifier s'il y a des changements
    success, stdout, stderr = run_git_command("git status --porcelain")
    
    if not stdout.strip():
        print("✅ Aucun changement à sauvegarder")
        return True
    
    print("📝 Changements détectés:")
    print(stdout)
    
    # Ajouter tous les changements
    success, stdout, stderr = run_git_command("git add -A")
    if not success:
        print(f"❌ Erreur lors de l'ajout des fichiers: {stderr}")
        return False
    
    # Créer le message de commit
    if not message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Auto-save: Mise à jour du {timestamp}"
    
    # Commit
    success, stdout, stderr = run_git_command(f'git commit -m "{message}"')
    if not success:
        if "nothing to commit" in stderr or "nothing to commit" in stdout:
            print("✅ Rien à commiter")
            return True
        print(f"❌ Erreur lors du commit: {stderr}")
        return False
    
    print(f"✅ Commit créé: {message}")
    
    # Push avec le token
    repo_url = f"https://{token}@github.com/lesmouettes/discover-analyzer.git"
    success, stdout, stderr = run_git_command(f"git push {repo_url} main")
    
    if success:
        print("✅ Changements sauvegardés sur GitHub avec succès!")
        return True
    else:
        print(f"❌ Erreur lors du push: {stderr}")
        return False

def create_feature_branch(feature_name):
    """Crée une nouvelle branche pour une feature"""
    branch_name = f"feature/{feature_name.lower().replace(' ', '-')}"
    
    success, stdout, stderr = run_git_command(f"git checkout -b {branch_name}")
    if success:
        print(f"✅ Branche '{branch_name}' créée")
        return branch_name
    else:
        print(f"❌ Erreur: {stderr}")
        return None

def save_feature(feature_name, description=None):
    """Sauvegarde une nouvelle feature"""
    print(f"\n🚀 Sauvegarde de la feature: {feature_name}")
    
    # Message de commit descriptif
    if description:
        commit_message = f"feat: {feature_name}\n\n{description}"
    else:
        commit_message = f"feat: {feature_name}"
    
    # Sauvegarder
    return auto_save_to_github(commit_message)

# Fonction helper pour les changements rapides
def quick_save(change_type="update"):
    """Sauvegarde rapide avec type de changement"""
    types = {
        "feat": "✨ Nouvelle fonctionnalité",
        "fix": "🐛 Correction de bug", 
        "docs": "📝 Documentation",
        "style": "💄 Style/UI",
        "refactor": "♻️ Refactoring",
        "test": "✅ Tests",
        "update": "🔧 Mise à jour"
    }
    
    prefix = change_type if change_type in types else "update"
    timestamp = datetime.now().strftime("%H:%M")
    
    message = f"{prefix}: Mise à jour - {timestamp}"
    return auto_save_to_github(message)

if __name__ == "__main__":
    # Test
    print("Test de sauvegarde automatique...")
    auto_save_to_github("test: Configuration de la sauvegarde automatique")