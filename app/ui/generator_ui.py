# Auteur : Yao Denis Fiodegbekou
# Numéro d'étudiant : 2515601
# GitHub : yaodenisfiodegbekou-ops

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import (QCheckBox, QDialog, QGridLayout, QHBoxLayout, QLabel,
                               QMessageBox, QPushButton, QSlider, QVBoxLayout)

from app.core.generator import PasswordGenerator


class FenetreGenerateur(QDialog):
    """Fenêtre qui permet de générer un mot de passe avec la souris."""

    LONGUEUR_MIN = 4
    LONGUEUR_MAX = 64

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Générateur de mot de passe")
        self.mot_de_passe = ""
        self.masque = False

        self._creer_longueur()
        self._creer_cases()
        self._creer_affichage()
        self._creer_boutons()
        self._organiser()

        self.generer()

    def _creer_longueur(self):
        """Crée le slider et les boutons - et + pour choisir la longueur."""
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(self.LONGUEUR_MIN, self.LONGUEUR_MAX)
        self.slider.setValue(16)
        self.label_longueur = QLabel("16")
        self.bouton_moins = QPushButton("-")
        self.bouton_plus = QPushButton("+")
        self.bouton_moins.setFixedWidth(32)
        self.bouton_plus.setFixedWidth(32)

        self.slider.valueChanged.connect(self._longueur_changee)
        self.bouton_moins.clicked.connect(lambda: self.slider.setValue(self.slider.value() - 1))
        self.bouton_plus.clicked.connect(lambda: self.slider.setValue(self.slider.value() + 1))

    def _creer_cases(self):
        """Crée les cases à cocher des types de caractères et de la validation."""
        self.case_minuscules = QCheckBox("Minuscules (a-z)")
        self.case_majuscules = QCheckBox("Majuscules (A-Z)")
        self.case_chiffres = QCheckBox("Chiffres (0-9)")
        self.case_symboles = QCheckBox("Symboles (!@#)")
        for case in (self.case_minuscules, self.case_majuscules, self.case_chiffres, self.case_symboles):
            case.setChecked(True)
        self.case_validation = QCheckBox("Validation (au moins un caractère de chaque type)")

    def _creer_affichage(self):
        """Crée le grand label qui affiche le mot de passe."""
        self.label_mot_de_passe = QLabel()
        self.label_mot_de_passe.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_mot_de_passe.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label_mot_de_passe.setFont(QFont("Consolas", 16))
        self.label_mot_de_passe.setStyleSheet("border: 1px solid gray; padding: 10px;")
        self.label_mot_de_passe.setMinimumWidth(420)

    def _creer_boutons(self):
        """Crée les boutons Masquer, Copier et Générer."""
        self.bouton_masquer = QPushButton("Masquer")
        self.bouton_copier = QPushButton("Copier")
        self.bouton_generer = QPushButton("Générer")
        self.bouton_generer.setDefault(True)
        self.bouton_masquer.clicked.connect(self.basculer_masque)
        self.bouton_copier.clicked.connect(self.copier)
        self.bouton_generer.clicked.connect(self.generer)

    def _organiser(self):
        """Place les éléments dans la fenêtre avec des layouts."""
        ligne_longueur = QHBoxLayout()
        ligne_longueur.addWidget(self.bouton_moins)
        ligne_longueur.addWidget(self.slider)
        ligne_longueur.addWidget(self.bouton_plus)
        ligne_longueur.addWidget(self.label_longueur)

        grille_cases = QGridLayout()
        grille_cases.addWidget(self.case_minuscules, 0, 0)
        grille_cases.addWidget(self.case_majuscules, 0, 1)
        grille_cases.addWidget(self.case_chiffres, 1, 0)
        grille_cases.addWidget(self.case_symboles, 1, 1)

        self.ligne_boutons = QHBoxLayout()
        self.ligne_boutons.addWidget(self.bouton_masquer)
        self.ligne_boutons.addWidget(self.bouton_copier)
        self.ligne_boutons.addWidget(self.bouton_generer)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Longueur"))
        layout.addLayout(ligne_longueur)
        layout.addWidget(QLabel("Types de caractères"))
        layout.addLayout(grille_cases)
        layout.addWidget(self.case_validation)
        layout.addWidget(self.label_mot_de_passe)
        layout.addLayout(self.ligne_boutons)

    def _longueur_changee(self, valeur):
        """Met à jour le chiffre affiché à côté du slider."""
        self.label_longueur.setText(str(valeur))

    def generer(self):
        """Génère un mot de passe avec les options choisies et l'affiche."""
        generateur = PasswordGenerator(
            length=self.slider.value(),
            use_lower=self.case_minuscules.isChecked(),
            use_upper=self.case_majuscules.isChecked(),
            use_digits=self.case_chiffres.isChecked(),
            use_symbols=self.case_symboles.isChecked(),
            validate=self.case_validation.isChecked(),
        )
        try:
            self.mot_de_passe = generateur.generer()
        except ValueError as erreur:
            QMessageBox.warning(self, "Erreur", str(erreur))
            return
        self._afficher()

    def _afficher(self):
        """Affiche le mot de passe en clair ou avec des astérisques."""
        if self.masque:
            self.label_mot_de_passe.setText("*" * len(self.mot_de_passe))
        else:
            self.label_mot_de_passe.setText(self.mot_de_passe)

    def basculer_masque(self):
        """Passe de l'affichage en clair à l'affichage masqué, et inversement."""
        self.masque = not self.masque
        self.bouton_masquer.setText("Afficher" if self.masque else "Masquer")
        self._afficher()

    def copier(self):
        """Copie le mot de passe dans le presse-papiers."""
        QGuiApplication.clipboard().setText(self.mot_de_passe)
