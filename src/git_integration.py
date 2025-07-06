"""
Intégration Git pour sauvegarde automatique des features
"""

import functools
from git_auto_save import auto_save_to_github, save_feature
import os

# Configuration
AUTO_SAVE = os.getenv('AUTO_SAVE', 'true').lower() == 'true'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def auto_commit(feature_name=None):
    """Décorateur pour auto-commit après l'exécution d'une fonction"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Exécuter la fonction
            result = func(*args, **kwargs)
            
            # Sauvegarder si activé
            if AUTO_SAVE:
                if feature_name:
                    save_feature(feature_name, f"Implémentation de {func.__name__}")
                else:
                    auto_save_to_github(f"auto: Mise à jour via {func.__name__}")
            
            return result
        return wrapper
    return decorator

# Fonction pour sauvegarder manuellement
def save_progress(message=None):
    """Sauvegarde manuelle du progrès"""
    if not message:
        message = "checkpoint: Sauvegarde du progrès"
    
    return auto_save_to_github(message, GITHUB_TOKEN)

# Classe pour gérer les sauvegardes de session
class GitAutoSaver:
    def __init__(self, enabled=True):
        self.enabled = enabled and AUTO_SAVE
        self.changes_count = 0
        self.last_feature = None
        
    def track_change(self, description=""):
        """Enregistre un changement"""
        self.changes_count += 1
        
        # Sauvegarder tous les 5 changements
        if self.enabled and self.changes_count % 5 == 0:
            message = f"auto-save: {self.changes_count} changements"
            if description:
                message += f" - {description}"
            auto_save_to_github(message, GITHUB_TOKEN)
    
    def save_feature(self, name, description=""):
        """Sauvegarde une feature complète"""
        if self.enabled:
            self.last_feature = name
            save_feature(name, description)
            self.changes_count = 0
    
    def checkpoint(self):
        """Crée un point de sauvegarde"""
        if self.enabled:
            save_progress(f"checkpoint: Après {self.changes_count} changements")

# Instance globale
git_saver = GitAutoSaver()

# Exemples d'utilisation
"""
# Dans vos fonctions:
from git_integration import auto_commit, git_saver

@auto_commit("Nouvelle analyse de patterns")
def analyze_new_patterns():
    # Votre code...
    pass

# Ou manuellement:
git_saver.track_change("Ajout de la détection de patterns émotionnels")
git_saver.save_feature("Pattern Detection v2", "Amélioration majeure de la détection")
"""