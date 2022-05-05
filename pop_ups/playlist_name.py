from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTextEdit, QDialogButtonBox

class PlaylistName:

    def __init__(self, name):
        Form, Window = uic.loadUiType("gui/playlist_name.ui")

        self.app = QApplication([])
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)

        self.name_input = self.form.textEdit
        self.button_box = self.form.buttonBox
        self.name = name


    def launch(self):
        #App execution
        self.window.show()
        self.app.exec()
