from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication,QPushButton, QVBoxLayout)
from PyQt5.QtGui import QIcon
	
Ui_MainWindow, QMainWindow = loadUiType('searchui.ui')

class Main(Ui_MainWindow,QMainWindow):
    def __init__(self, ):
        super(Main,self).__init__()
        self.setupUi(self)
def select():
    main.L1.setText(str(QFileDialog.getOpenFileName()[0]))
    addr=main.L1.text()
    addressParse(addr)
    return addr
    
    
def addressParse(addr):
    main.lbl1.setText(str(addr))
    
if __name__=='__main__':
    from PyQt5 import QtGui
    import sys 

    

    app = QApplication(sys.argv)
    main = Main()

    
    ##################################################
    main.B1.clicked.connect(select)
    main.show()         
    
    
    

    ##################################################
    
    
    sys.exit(app.exec_())