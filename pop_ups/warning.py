import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QDialogButtonBox

class WarningMessage:

    def __init__(self, warning):
        Form, Window = uic.loadUiType("gui/warning.ui")

        self.app = QApplication([])
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)

        self.button_box = self.form.buttonBox
        self.text = self.form.label
        self.warning = warning
        self.text.setText(f'{self.warning}')


    def launch(self):

        #App execution
        self.window.show()
        self.app.exec()


    def quit(self):
        pass
