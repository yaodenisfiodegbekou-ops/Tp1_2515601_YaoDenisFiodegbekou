# Auteur : Yao Denis Fiodegbekou
# Numéro d'étudiant : 2515601
# GitHub : yaodenisfiodegbekou-ops

import json
from pathlib import Path


class StockageCoffre:
    """Lit et écrit les entrées du coffre-fort dans un fichier JSON."""

    def __init__(self, chemin="vault.json"):
        self.chemin = Path(chemin)

    def charger(self):
        """Retourne la liste des entrées. Retourne une liste vide si le fichier n'existe pas."""
        if not self.chemin.exists():
            return []

        try:
            with open(self.chemin, encoding="utf-8") as fichier:
                donnees = json.load(fichier)
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise ValueError(f"Le fichier {self.chemin} est corrompu.")

        if not isinstance(donnees, list):
            raise ValueError(f"Le fichier {self.chemin} n'a pas le bon format.")

        for entree in donnees:
            if not isinstance(entree, dict) or "email" not in entree or "mot_de_passe" not in entree:
                raise ValueError(f"Le fichier {self.chemin} contient une entrée invalide.")

        return donnees
