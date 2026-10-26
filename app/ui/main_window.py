# Auteur : Yao Denis Fiodegbekou
# Numéro d'étudiant : 2515601
# GitHub : yaodenisfiodegbekou-ops

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
                               QScrollArea, QVBoxLayout, QWidget)


class LigneEntree(QFrame):
    """Une ligne de la liste : un e-mail et son mot de passe masqué."""

    def __init__(self, entree):
        super().__init__()
        self.entree = entree

        self.label_email = QLabel(entree["email"])
        self.label_mot_de_passe = QLabel("*******")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label_email)
        layout.addStretch()
        layout.addWidget(self.label_mot_de_passe)


class FenetrePrincipale(QMainWindow):
    """Fenêtre du coffre-fort qui affiche la liste des comptes."""

    def __init__(self, stockage):
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.resize(520, 420)
        self.stockage = stockage
        self.entrees = self._charger_entrees()

        self._creer_liste()
        self._organiser()
        self._afficher_entrees()

    def _charger_entrees(self):
        """Charge les entrées du fichier. Affiche un message si le fichier est corrompu."""
        try:
            return self.stockage.charger()
        except ValueError as erreur:
            QMessageBox.warning(self, "Erreur", str(erreur))
            return []

    def _creer_liste(self):
        """Crée la zone défilante qui contient les lignes."""
        self.conteneur = QWidget()
        self.layout_liste = QVBoxLayout(self.conteneur)
        self.layout_liste.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.zone_defilante = QScrollArea()
        self.zone_defilante.setWidgetResizable(True)
        self.zone_defilante.setWidget(self.conteneur)

    def _organiser(self):
        """Place les éléments dans la fenêtre."""
        self.entete = QHBoxLayout()
        self.entete.addWidget(QLabel("Mes comptes"))
        self.entete.addStretch()

        self.ligne_boutons = QHBoxLayout()

        layout = QVBoxLayout()
        layout.addLayout(self.entete)
        layout.addWidget(self.zone_defilante)
        layout.addLayout(self.ligne_boutons)

        centre = QWidget()
        centre.setLayout(layout)
        self.setCentralWidget(centre)

    def _afficher_entrees(self):
        """Vide la liste puis crée une ligne pour chaque entrée."""
        while self.layout_liste.count():
            element = self.layout_liste.takeAt(0)
            if element.widget():
                element.widget().deleteLater()

        for entree in self.entrees:
            self.layout_liste.addWidget(LigneEntree(entree))
