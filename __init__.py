from Widgets import *
import sys
from PySide.QtCore import *
from PySide.QtGui import *

qt_app = QApplication(sys.argv)
qt_app.setOrganizationName('CCubed')
qt_app.setOrganizationDomain('git.vertinext.com')
qt_app.setApplicationName('Megane')
qt_app.setApplicationVersion('0.1')

if __name__ == "__main__":
    acct = Account(None)
    acct.show()
    acct.activateWindow()
    qt_app.setActiveWindow(acct)
    qt_app.exec_()
