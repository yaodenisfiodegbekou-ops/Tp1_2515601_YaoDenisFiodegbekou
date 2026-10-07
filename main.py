# Auteur : Yao Denis Fiodegbekou
# Numéro d'étudiant : 2515601
# GitHub : yaodenisfiodegbekou-ops

import argparse

from app.core.generator import PasswordGenerator


def main():
    """Point d'entrée du programme en ligne de commande."""

    parseur = argparse.ArgumentParser()
    parseur.add_argument("--length", type=int, default=16)
    parseur.add_argument("--no-lower", action="store_true")
    parseur.add_argument("--no-upper", action="store_true")
    parseur.add_argument("--no-digits", action="store_true")
    parseur.add_argument("--no-symbols", action="store_true")
    parseur.add_argument("--validate", action="store_true")
    args = parseur.parse_args()

    generateur = PasswordGenerator(
        length=args.length,
        use_lower=not args.no_lower,
        use_upper=not args.no_upper,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        validate=args.validate,
    )

    try:
        print(generateur.generer())
    except ValueError as erreur:
        print(f"Erreur : {erreur}")


if __name__ == "__main__":
    main()