from PySide.QtCore import *
from PySide.QtGui import *
import webbrowser

class AccountWindow(QWidget):
    def __init__(self, parent):
        # Initial Setup
        super().__init__(parent)
        self.setWindowTitle("Account Setup")
        self.setMinimumSize(400, 200)

        # Layouts
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Comboox Services
        self.services = ['AniList', 'HummingBird']
        self.service = QComboBox(parent)
        self.service.addItems(self.services)
        self.form_layout.addRow('&Service:', self.service)
        self.service.currentIndexChanged.connect(self.service_selected)

        # Stacked Widgets
        self.stack = QStackedLayout()
        self.stack.addWidget(AniList(self))
        self.stack.addWidget(HummingBird(self))
        self.form_layout.addRow(self.stack)

        # SetLayout
        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)

    @Slot(int)
    def service_selected(self, index):
        if index == -1:
            return
        else:
            if index == 0:  # Anilist
                self.stack.setCurrentIndex(0)
            elif index == 1:  # HummingBird
                self.stack.setCurrentIndex(1)


class HummingBird(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QFormLayout(self)
        self.uname = QLineEdit(self)
        self.pword = QLineEdit(self)
        self.pword.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.loginbutton = QPushButton("&Login", self)
        self.layout.addRow("Email:", self.uname)
        self.layout.addRow("Password:", self.pword)
        self.layout.addRow(self.loginbutton)
        self.loginbutton.clicked.connect(self.login_logic)
        self.setLayout(self.layout)
        self.settings = QSettings()
        if self.settings.value('hummingbird/key', None) is not None:
            self.uname.settext("Hummingbird Connected")
            self.uname.setReadOnly(True)
            self.pword.setReadOnly(True)
            self.loginbutton.setDisable(True)

    @Slot()
    def login_logic(self):
        # hbird login
        if r.status_code == 401:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Please verify your information.")
            msgBox.setInformativeText("Hummingbird did not accept your login details.")
            msgBox.exec_()
            return
        else:
            self.settings.setValue('hummingbird/key', r.text)
            self.loginbutton.setEnabled(False)
            self.uname.setText("Hummingbird Connected")
            self.pword.setText("")
            self.uname.setReadOnly(True)
            self.pword.setReadOnly(True)

class AniList(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QFormLayout(self)
        self.uname = QLineEdit(self)
        self.pin = QLineEdit(self)
        self.reqpinbtn = QPushButton("Request Pin", self)
        self.loginbtn = QPushButton("&Login", self)
        self.layout.addRow("Username:", self.uname)
        self.layout.addRow("Pin:", self.pin)
        self.layout.addRow(self.reqpinbtn)
        self.layout.addRow(self.loginbtn)
        self.reqpinbtn.clicked.connect(self.pin_click)
        self.loginbtn.clicked.connect(self.login)
        self.setLayout(self.layout)
        self.settings = QSettings()
        if self.settings.value('anilist/key', None) is not None:
            self.uname.setText("AniList Connected")
            self.uname.setReadOnly(True)
            self.pin.setReadOnly(True)
            self.reqpinbtn.setEnabled(False)
            self.loginbtn.setEnabled(False)

    @Slot()
    def pin_click(self):
        if len(self.uname.text()) == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Please Enter Your Username.")
            msgBox.setInformativeText("Before requesting a pin, please ensure your username has been entered. Your username is necessary to complete the request.")
            msgBox.exec_()
            return
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Get Your Pin.")
            msgBox.setInformativeText("Once you hit okay here, you'll be redirected to AniList's own webpage where you'll log in to your account and be given a pin code. Come back and enter that pin code here.")
            msgBox.exec_()
            webbrowser.open('https://anilist.co/api/auth/authorize?grant_type=authorization_pin&client_id=takeshiko-qgfis&response_type=pin', new=2, autoraise=True)

    @Slot()
    def login(self):
        pass