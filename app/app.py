from locale import currency
from PySide2 import QtWidgets
import currency_converter


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  # Super Rappel la fonction QtWidget notée plus haut et nous evite d'ecrire QtWidgets.QWidget
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")  # Donne Un NOM a notre interface créée.
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()
        self.setup_css()
        self.resize(800, 80)

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)  # cree notre menu d'options orizontale.
        self.cbb_devisesFrom = QtWidgets.QComboBox()  # cree une premiere option.
        self.spn_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.spn_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Inverser devises")  # cree le bouton pour inverser les devises.

        self.layout.addWidget(self.cbb_devisesFrom)  # layout.addWidget ajoute les options dans l'interface graphique
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.spn_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(
            self.c.currencies)))  # Integre des valeurs a notre premiere box dans l'interface. c.currencies() nous rapporte toutes les monnaies qui existent.
        self.cbb_devisesTo.addItems(
            sorted(list(self.c.currencies)))  # Integere ces memes devises dans notre deuxieme comboBox
        self.cbb_devisesFrom.setCurrentText("ILS")  # Programme la devise initial par default
        self.cbb_devisesTo.setCurrentText("EUR")  # Programme la devise a obtenir par default

        self.spn_montant.setRange(1, 1000000)  # Programme un rang par default. de X a Y
        self.spn_montantConverti.setRange(1, 1000000)

        self.spn_montant.setValue(100)  # Programme une Valeur par default
        self.spn_montantConverti.setValue(100)

    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devise)

    def setup_css(self):
        self.setStyleSheet("""

        background-color: rgb(30,30,30);
        color: rgb(240,240,240);
        border: none;
        
        """)

    def compute(self):
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()
        resultat = self.c.convert(montant, devise_from, devise_to)

        try:
            resultat = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'a pas fonctionné.")
        else:
            self.spn_montantConverti.setValue(resultat)

    def inverser_devise(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)

        self.compute()


app = QtWidgets.QApplication(
    [])  # Il est obligqtoire d'entrer les crochets dans la parenthese. Cette fonction crée notre application
win = App()  # L'instance wind nous crée une fenetre
win.show()  # Execute notre Fenetre créée precedement
app.exec_()  # Execute notre apploication PySide
