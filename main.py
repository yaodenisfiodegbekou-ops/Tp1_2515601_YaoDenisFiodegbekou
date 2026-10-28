# Auteur : Yao Denis Fiodegbekou
# Numéro d'étudiant : 2515601
# GitHub : yaodenisfiodegbekou-ops

import argparse
import sys

from PySide6.QtWidgets import QApplication

from app.core.generator import PasswordGenerator
from app.core.storage import StockageCoffre
from app.ui.main_window import FenetrePrincipale


def lancer_cli(args):
    """Génère un mot de passe et l'affiche dans le terminal (partie 1)."""
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


def lancer_gui(args):
    """Ouvre la fenêtre du coffre-fort (partie 2)."""
    application = QApplication(sys.argv)
    fenetre = FenetrePrincipale(StockageCoffre(args.vault_file))
    fenetre.show()
    sys.exit(application.exec())


def main():
    """Point d'entrée du programme : mode graphique par défaut, ou ligne de commande avec --no-gui."""

    parseur = argparse.ArgumentParser()
    parseur.add_argument("--length", type=int, default=16)
    parseur.add_argument("--no-lower", action="store_true")
    parseur.add_argument("--no-upper", action="store_true")
    parseur.add_argument("--no-digits", action="store_true")
    parseur.add_argument("--no-symbols", action="store_true")
    parseur.add_argument("--validate", action="store_true")
    parseur.add_argument("--no-gui", action="store_true")
    parseur.add_argument("--vault_file", default="vault.json")
    args = parseur.parse_args()

    if args.no_gui:
        lancer_cli(args)
    else:
        lancer_gui(args)


if __name__ == "__main__":
    main()