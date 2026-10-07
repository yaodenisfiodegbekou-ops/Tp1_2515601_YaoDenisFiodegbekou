# Auteur : Yao Denis Fiodegbekou
# Numéro d'étudiant : 2515601
# GitHub : yaodenisfiodegbekou-ops

import secrets
import string


class PasswordGenerator:
    """Génère des mots de passe selon des critères configurables."""

    def __init__(self, length=16, use_lower=True, use_upper=True, use_digits=True,
                 use_symbols=True, validate=False):
        self.length = length
        self.use_lower = use_lower
        self.use_upper = use_upper
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.validate = validate

    def _obtenir_ensembles(self):
        """Retourne la liste des ensembles de caractères sélectionnés."""
        ensembles = []
        if self.use_lower:
            ensembles.append(string.ascii_lowercase)
        if self.use_upper:
            ensembles.append(string.ascii_uppercase)
        if self.use_digits:
            ensembles.append(string.digits)
        if self.use_symbols:
            ensembles.append(string.punctuation)
        return ensembles

    def generer(self):
        """Génère et retourne un mot de passe."""
        if self.length <= 0:
            raise ValueError("La longueur doit être supérieure à 0.")

        ensembles = self._obtenir_ensembles()
        if not ensembles:
            raise ValueError("Au moins un type de caractères doit être sélectionné.")

        tous_les_caracteres = "".join(ensembles)
        caracteres =[]

        if self.validate:
            if self.length < len(ensembles):
                raise ValueError("La longueur est trop courte")
        caracteres = [secrets.choice(ensemble) for ensemble in ensembles]

        while len(caracteres) < self.length:
            caracteres.append(secrets.choice(tous_les_caracteres))

        secrets.SystemRandom().shuffle(caracteres)
        return "".join(caracteres)
