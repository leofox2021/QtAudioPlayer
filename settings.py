from PyQt5 import QtGui, uic
from PyQt5.Qt import *
from pop_ups.restart import Restart

class Settings:

    def __init__(self, available_styles):

        Form, Window = uic.loadUiType("gui/settings.ui")

        self.app = QApplication([])
        self.window = Window()
        self.form = Form()
        self.form.setupUi(self.window)
        

        self.combox = self.form.comboBox
        self.combox2 = self.form.comboBox_2
        self.main_label = self.form.label
        self.theme_label = self.form.label_2
        self.style_label = self.form.label_3
        self.file = None
        self.addElements()
        self.available_styles = available_styles
        self.combox.currentIndexChanged.connect(self.changeTheme)
        self.combox2.currentIndexChanged.connect(self.changeStyle)


    #Append themes into combo box
    def addElements(self):
        self.file = open('config/theme.txt', 'r', encoding="utf-8")
        a = self.file.read()
        if 'light' in a:
            self.combox.addItem('Light')
            self.combox.addItem('Dark')
        else:
            self.combox.addItem('Dark')
            self.combox.addItem('Light')

        if 'fusion' in a:
            self.combox2.addItem('Fusion')
            self.combox2.addItem('Windows')
        else:
            self.combox2.addItem('Windows')
            self.combox2.addItem('Fusion')

        self.file.close()


    #Change theme on combo box index change
    def changeTheme(self):
        self.file = open('config/theme.txt', 'r+')
        a = self.file.readlines()
        
        #theme.txt integrity check
        if 'theme' in a[0] and 'style' in a[1]:
            print('Integrity check passed!')

            if self.combox.currentText() == 'Dark':
                a[0] = 'theme = dark'

                #This is not implemented via for loop
                #because it'd cause troubles with RAM overloads.
                self.file.truncate(0)
                self.file.seek(0)
                self.file.write(a[0] + '\n')
                self.file.write(a[1])

            elif self.combox.currentText() == 'Light':
                a[0] = 'theme = light'
                
                self.file.truncate(0)
                self.file.seek(0)
                self.file.write(a[0] + '\n')
                self.file.write(a[1])

            else:
                pass

        else:
            print("The integrity of 'theme.txt' was violated.")
            print("A new config will be created immediately.")
            self.file.truncate(0)
            self.file.seek(0)
            self.file.write('theme = light' + '\n' )
            self.file.write('style = fusion')

        self.file.close()


    #Change style on combo box index change
    def changeStyle(self):
        self.file = open('config/theme.txt', 'r+')
        a = self.file.readlines()
        
        #theme.txt integrity check
        if 'theme' in a[0] and 'style' in a[1]:
            print('Integrity check passed!')

            if self.combox2.currentText() == 'Fusion':
                a[1] = 'style = fusion'
                (print('We are fusion now'))
                #This is not implemented via for loop
                #because it'd cause troubles with RAM overloads.
                self.file.truncate(0)
                self.file.seek(0)
                #'\n' is already in a[0]
                #This creating it will violate the config
                self.file.write(a[0])
                self.file.write(a[1])

            elif self.combox2.currentText() == 'Windows':
                a[1] = 'style = windows'
                (print('We are windows now'))
                self.file.truncate(0)
                self.file.seek(0)
                self.file.write(a[0])
                self.file.write(a[1])

            else:
                pass

        else:
            print("The integrity of 'theme.txt' was violated.")
            print("A new config will be created immediately.")
            self.file.truncate(0)
            self.file.seek(0)
            self.file.write('theme = light' + '\n' )
            self.file.write('style = fusion')

        self.file.close()

    #Set light theme by reading theme.txt
    def lightTheme(self):
        self.window.setStyleSheet('background: white')
        self.combox.setStyleSheet('background: #F0F0F0')
        self.combox.setStyleSheet('color: Black')
        self.combox2.setStyleSheet('background: #F0F0F0')
        self.combox2.setStyleSheet('color: Black')

        #self.combox.setPalette(palette)
        print('Light theme set!')


    #Set dark theme by reading theme.txt
    def darkTheme(self):
        self.window.setStyleSheet('background: #282829')
        self.combox.setStyleSheet('background: #414142')
        self.combox.setStyleSheet('color: White')
        self.combox2.setStyleSheet('background: #414142')
        self.combox2.setStyleSheet('color: White')
        #self.combox.setStyleSheet('selection-color: Gray')
        
        palette = QPalette()
        palette.setColor(QPalette.Foreground, QtGui.QColor('#F0F0F0'))
        
        self.main_label.setPalette(palette)
        self.theme_label.setPalette(palette)
        self.style_label.setPalette(palette)


    #App execution
    def launch(self):
        self.file = open('config/theme.txt', 'r')
        a = self.file.read()

        if 'light' in a: 
            self.lightTheme()
        elif 'dark' in a:
            self.darkTheme()
        self.file.close()

        #App execution
        self.window.show()
        self.app.exec()
