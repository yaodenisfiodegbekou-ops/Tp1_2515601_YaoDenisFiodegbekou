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
