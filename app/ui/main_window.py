# Auteur : Yao Denis Fiodegbekou
# Numéro d'étudiant : 2515601
# GitHub : yaodenisfiodegbekou-ops

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QDialog, QFormLayout, QFrame, QHBoxLayout,
                               QLabel, QLineEdit, QMainWindow, QMenu, QMessageBox, QPushButton,
                               QScrollArea, QVBoxLayout, QWidget)

from app.core.generator import PasswordGenerator
from app.ui.generator_ui import FenetreGenerateur


class LigneEntree(QFrame):
    """Une ligne de la liste : un e-mail et son mot de passe masqué."""

    DUREE_REVELATION = 3000

    def __init__(self, entree, fenetre):
        super().__init__()
        self.entree = entree
        self.fenetre = fenetre
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

    def mousePressEvent(self, event):
        """Sélectionne la ligne lors d'un clic."""
        self.fenetre.selectionner(self)

    def selectionner(self, selectionnee):
        """Change la couleur de la ligne selon qu'elle est sélectionnée ou non."""
        self.setStyleSheet("background-color: #cfe2ff;" if selectionnee else "")

    def contextMenuEvent(self, event):
        """Affiche un menu au clic droit."""
        menu = QMenu(self)
        menu.addAction("Révéler le mot de passe", self.reveler)
        menu.addAction("Modifier", lambda: self.fenetre.modifier(self))
        menu.addAction("Supprimer", lambda: self.fenetre.supprimer(self))
        menu.exec(event.globalPos())


class DialogueEntree(QDialog):
    """Boîte de dialogue pour saisir un e-mail et un mot de passe."""

    def __init__(self, parent=None, entree=None):
        super().__init__(parent)
        self.setWindowTitle("Modifier une entrée" if entree else "Ajouter une entrée")

        self.champ_email = QLineEdit()
        self.champ_mot_de_passe = QLineEdit()
        if entree:
            self.champ_email.setText(entree["email"])
            self.champ_mot_de_passe.setText(entree["mot_de_passe"])

        bouton_generer = QPushButton("Générer")
        bouton_generer.clicked.connect(self.generer)

        ligne_mot_de_passe = QHBoxLayout()
        ligne_mot_de_passe.addWidget(self.champ_mot_de_passe)
        ligne_mot_de_passe.addWidget(bouton_generer)

        bouton_ok = QPushButton("OK")
        bouton_annuler = QPushButton("Annuler")
        bouton_ok.clicked.connect(self.valider)
        bouton_annuler.clicked.connect(self.reject)

        boutons = QHBoxLayout()
        boutons.addStretch()
        boutons.addWidget(bouton_ok)
        boutons.addWidget(bouton_annuler)

        formulaire = QFormLayout(self)
        formulaire.addRow("E-mail :", self.champ_email)
        formulaire.addRow("Mot de passe :", ligne_mot_de_passe)
        formulaire.addRow(boutons)

    def generer(self):
        """Remplit le champ avec un mot de passe créé par la logique de la partie 1."""
        self.champ_mot_de_passe.setText(PasswordGenerator(validate=True).generer())

    def valider(self):
        """Vérifie les champs avant de fermer la boîte de dialogue."""
        email = self.champ_email.text().strip()
        if "@" not in email:
            QMessageBox.warning(self, "Erreur", "Entrez une adresse e-mail valide.")
            return
        if not self.champ_mot_de_passe.text():
            QMessageBox.warning(self, "Erreur", "Le mot de passe ne peut pas être vide.")
            return
        self.accept()

    def obtenir_entree(self):
        """Retourne l'entrée saisie sous forme de dictionnaire."""
        return {"email": self.champ_email.text().strip(), "mot_de_passe": self.champ_mot_de_passe.text()}


class FenetrePrincipale(QMainWindow):
    """Fenêtre du coffre-fort qui affiche la liste des comptes."""

    def __init__(self, stockage):
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.resize(520, 420)
        self.stockage = stockage
        self.ligne_selectionnee = None
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
        """Crée les boutons de gestion des entrées."""
        self.bouton_trier = QPushButton("Trier A → Z")
        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_modifier = QPushButton("Modifier")
        self.bouton_supprimer = QPushButton("Supprimer")
        self.bouton_generateur = QPushButton("Générateur")

        self.bouton_trier.clicked.connect(self.trier)
        self.bouton_ajouter.clicked.connect(self.ajouter)
        self.bouton_modifier.clicked.connect(lambda: self.modifier(self.ligne_selectionnee))
        self.bouton_supprimer.clicked.connect(lambda: self.supprimer(self.ligne_selectionnee))
        self.bouton_generateur.clicked.connect(self.ouvrir_generateur)

    def _organiser(self):
        """Place les éléments dans la fenêtre."""
        self.entete = QHBoxLayout()
        self.entete.addWidget(QLabel("Mes comptes"))
        self.entete.addStretch()
        self.entete.addWidget(self.bouton_trier)

        self.ligne_boutons = QHBoxLayout()
        self.ligne_boutons.addWidget(self.bouton_ajouter)
        self.ligne_boutons.addWidget(self.bouton_modifier)
        self.ligne_boutons.addWidget(self.bouton_supprimer)
        self.ligne_boutons.addWidget(self.bouton_generateur)

        layout = QVBoxLayout()
        layout.addLayout(self.entete)
        layout.addWidget(self.zone_defilante)
        layout.addWidget(QLabel("Clic : sélectionner. Double-clic ou clic droit : révéler le mot de passe"))
        layout.addLayout(self.ligne_boutons)

        centre = QWidget()
        centre.setLayout(layout)
        self.setCentralWidget(centre)

    def _afficher_entrees(self):
        """Vide la liste puis crée une ligne pour chaque entrée."""
        self.ligne_selectionnee = None
        while self.layout_liste.count():
            element = self.layout_liste.takeAt(0)
            if element.widget():
                element.widget().deleteLater()

        for entree in self.entrees:
            self.layout_liste.addWidget(LigneEntree(entree, self))

    def trier(self):
        """Trie les entrées par e-mail, en ordre alphabétique."""
        self.entrees.sort(key=lambda entree: entree["email"].lower())
        self._afficher_entrees()

    def ouvrir_generateur(self):
        """Ouvre la fenêtre du générateur de mot de passe."""
        FenetreGenerateur(self).exec()

    def selectionner(self, ligne):
        """Sélectionne une ligne et retire la sélection de l'ancienne."""
        if self.ligne_selectionnee:
            self.ligne_selectionnee.selectionner(False)
        self.ligne_selectionnee = ligne
        ligne.selectionner(True)

    def ajouter(self):
        """Ouvre la boîte de dialogue pour ajouter une entrée."""
        dialogue = DialogueEntree(self)
        if dialogue.exec():
            self.entrees.append(dialogue.obtenir_entree())
            self._afficher_entrees()

    def modifier(self, ligne):
        """Ouvre la boîte de dialogue pour modifier l'entrée de la ligne."""
        if ligne is None:
            QMessageBox.information(self, "Modifier", "Sélectionnez d'abord une entrée.")
            return
        dialogue = DialogueEntree(self, ligne.entree)
        if dialogue.exec():
            ligne.entree.update(dialogue.obtenir_entree())
            self._afficher_entrees()

    def supprimer(self, ligne):
        """Supprime l'entrée de la ligne après confirmation."""
        if ligne is None:
            QMessageBox.information(self, "Supprimer", "Sélectionnez d'abord une entrée.")
            return
        reponse = QMessageBox.question(self, "Supprimer", f"Supprimer l'entrée {ligne.entree['email']} ?")
        if reponse == QMessageBox.StandardButton.Yes:
            self.entrees.remove(ligne.entree)
            self._afficher_entrees()
