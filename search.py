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
    main.L1.setText(str(QFileDialog.getOpenFileName()))
    addr=main.L1.text()
    main.lbl1.setText(addr)
    # return addr

if __name__=='__main__':
    from PyQt5 import QtGui
    import sys 

    

    app = QApplication(sys.argv)
    main = Main()

    
    ##################################################
    
    main.show()         
    
    
    
    main.B1.clicked.connect(select)
    main.lbl1.setText(select())
    ##################################################
    
    
    sys.exit(app.exec_())