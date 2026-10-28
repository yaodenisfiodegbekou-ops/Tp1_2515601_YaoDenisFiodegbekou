# Auteur : Yao Denis Fiodegbekou
# Numéro d'étudiant : 2515601
# GitHub : yaodenisfiodegbekou-ops

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QMainWindow, QMenu, QMessageBox,
                               QPushButton, QScrollArea, QVBoxLayout, QWidget)

from app.ui.generator_ui import FenetreGenerateur


class LigneEntree(QFrame):
    """Une ligne de la liste : un e-mail et son mot de passe masqué."""

    DUREE_REVELATION = 3000

    def __init__(self, entree):
        super().__init__()
        self.entree = entree
        self.revele = False

        self.label_email = QLabel(entree["email"])
        self.label_mot_de_passe = QLabel()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label_email)
        layout.addStretch()
        layout.addWidget(self.label_mot_de_passe)

        self._afficher()

    def _afficher(self):
        """Affiche le mot de passe en clair ou masqué."""
        if self.revele:
            self.label_mot_de_passe.setText(self.entree["mot_de_passe"])
        else:
            self.label_mot_de_passe.setText("*******")

    def reveler(self):
        """Révèle le mot de passe pendant quelques secondes."""
        self.revele = True
        self._afficher()
        QTimer.singleShot(self.DUREE_REVELATION, self.masquer)

    def masquer(self):
        """Masque à nouveau le mot de passe."""
        self.revele = False
        self._afficher()

    def mouseDoubleClickEvent(self, event):
        """Révèle le mot de passe lors d'un double-clic."""
        self.reveler()

    def contextMenuEvent(self, event):
        """Affiche un menu au clic droit."""
        menu = QMenu(self)
        menu.addAction("Révéler le mot de passe", self.reveler)
        menu.exec(event.globalPos())


class FenetrePrincipale(QMainWindow):
    """Fenêtre du coffre-fort qui affiche la liste des comptes."""

    def __init__(self, stockage):
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.resize(520, 420)
        self.stockage = stockage
        self.entrees = self._charger_entrees()

        self._creer_liste()
        self._creer_boutons()
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

    def _creer_boutons(self):
        """Crée les boutons Trier et Générateur."""
        self.bouton_trier = QPushButton("Trier A → Z")
        self.bouton_generateur = QPushButton("Générateur")

        self.bouton_trier.clicked.connect(self.trier)
        self.bouton_generateur.clicked.connect(self.ouvrir_generateur)

    def _organiser(self):
        """Place les éléments dans la fenêtre."""
        self.entete = QHBoxLayout()
        self.entete.addWidget(QLabel("Mes comptes"))
        self.entete.addStretch()
        self.entete.addWidget(self.bouton_trier)

        self.ligne_boutons = QHBoxLayout()
        self.ligne_boutons.addWidget(self.bouton_generateur)

        layout = QVBoxLayout()
        layout.addLayout(self.entete)
        layout.addWidget(self.zone_defilante)
        layout.addWidget(QLabel("Double-clic ou clic droit sur une entrée : révéler le mot de passe"))
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

    def trier(self):
        """Trie les entrées par e-mail, en ordre alphabétique."""
        self.entrees.sort(key=lambda entree: entree["email"].lower())
        self._afficher_entrees()

    def ouvrir_generateur(self):
        """Ouvre la fenêtre du générateur de mot de passe."""
        FenetreGenerateur(self).exec()
