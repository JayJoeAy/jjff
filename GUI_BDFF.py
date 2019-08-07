from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow, QTextEdit, QAction, QFileDialog, QTableWidget,QTableWidgetItem

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure

import os,fnmatch,sys,csv,pandas
import numpy as np
from numpy import linalg as LA
from bd_cdFunc import FourierCalc
	
Ui_MainWindow, QMainWindow = loadUiType('BDwindow.ui')

class Main(Ui_MainWindow,QMainWindow):
    def __init__(self, ):
        super(Main,self).__init__()
        self.setupUi(self)
        self.fig_dict={}
        
        self.L1.itemClicked.connect(self.changefig)
        
        # self.chk1.setVisible(False)
        # self.chk1.setChecked(True)

        
    def changefig(self, item):
        text=item.text()
        self.rmmpl()
        self.addmpl(self.fig_dict[text])
    
    def addmpl(self,fig):
        self.canvas=FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar=NavigationToolbar(self.canvas,self, coordinates=True)
        self.mplvl.addWidget(self.toolbar)
        self.rmmpl()
    
    def rmmpl(self,):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()
        
    def addfig(self,name,fig):
        self.fig_dict[name]=fig
        self.L1.addItem(name)
        

def importFile():
    adr=QFileDialog.getExistingDirectory()
    adr=str(adr)
    adr=adr.replace("/","//")
    main.adr=str(adr)
    # main.chk1.setText("Plot 1")
    # main.chk1.setVisible(True)
    # main.chk1.setChecked(True)

def sectNumber():
    SectionNumber=main.SectNo_line.text()
    s=open('sectNumber.txt','w')
    s.write(str(SectionNumber))
    s.close()
    os.system('abaqus cae noGui=ReadingDistortion.py')
def plotfunc():
    

    
    scale = main.lineEdit.text()
    scale=np.int(scale) 
    
    SecNo_CMM =11 
    SecNo_FEM = main.FEM_sec.text()
    SecNo_FEM=np.int(SecNo_FEM)
    if SecNo_FEM<10:
        SecNo_FEM = '0' + str(SecNo_FEM)
    
    ax=np.zeros(4)
    CylNo = 4
    add='FEM_OD_WT'
    temp_FEM_OD_WT=np.zeros((124,4))
    # this part counts the number of step files in the add directory
    StepFileNo=len(fnmatch.filter(os.listdir(add), 'STEP*.txt'))

    fig={}
    ax1f1={}
    FEM_Fourier_Coef={}
    # chk1_flag = True
    
    # if main.chk1.isChecked()==False :
        # chk1_flag = False
        
    # while chk1_flag==True :
    for LinerNo in range (CylNo):
       
        displacement_names_FEM='STEP1LINER0'+str(LinerNo+1)+'SEC'+str(SecNo_FEM)+'.txt'
        displacement_add=main.adr+"//"+displacement_names_FEM
        NodeAdd=main.adr+"//nodes.txt"
        
        # Datas for the Node array
        nodes_FEM_OD_WT=pandas.read_csv(NodeAdd, header=None)
        nodes_FEM_OD_WT=nodes_FEM_OD_WT.to_numpy()
        
        # Datas for displacement array
        displacement_FEM_OD_WT=pandas.read_csv(displacement_add, header=None)
        displacement_FEM_OD_WT=displacement_FEM_OD_WT.to_numpy()    

        # Find the array elements of disp in node
        indices = np.where(np.in1d(nodes_FEM_OD_WT[:,0], displacement_FEM_OD_WT[:,0]))[0]
        temp_OD=nodes_FEM_OD_WT[indices,:]
        
        Cx_OD=np.mean(temp_OD[:,1])
        temp_OD[:,1]=temp_OD[:,1]-Cx_OD
        deformation_OD=temp_OD[:,1:]+displacement_FEM_OD_WT[:,1:]
        
        Number_FEM_OD_WT=len(displacement_FEM_OD_WT)
        
        Cmean_FEM_OD_WT=np.mean(temp_OD[:,1:],axis=0)
        Rnorm_FEM_OD_WT=LA.norm(deformation_OD[0,:]-Cmean_FEM_OD_WT)
        
        #polar plotting requirements
        rpolar=np.sqrt(deformation_OD[:,0]**2+deformation_OD[:,1]**2)
        phi_polar=np.arctan2(deformation_OD[:,1],deformation_OD[:,0])
        dr_FEM_OD_WT=rpolar-39.3
        
        temp_FEM_OD_WT[:,0]=phi_polar
        temp_FEM_OD_WT[:,1]=dr_FEM_OD_WT*scale+39.3
        temp_FEM_OD_WT=temp_FEM_OD_WT[np.argsort(temp_FEM_OD_WT[:,0])]
        
        perfectGeomR=39.3
        perfectGeomPhi=np.linspace(0,2*np.pi,100)
        perfectR=np.zeros_like(perfectGeomPhi)+perfectGeomR
    
        fig[LinerNo+1]=Figure()
        ax1f1[LinerNo+1]=fig[LinerNo+1].add_subplot(111, projection='polar')
        ax1f1[LinerNo+1].plot(temp_FEM_OD_WT[:,0],temp_FEM_OD_WT[:,1], label='CylNO'+str(LinerNo+1))
        ax1f1[LinerNo+1].plot(perfectGeomPhi,perfectR,label="Perfect Geom." )
        ax1f1[LinerNo+1].legend(loc=4)
        main.addmpl(fig[LinerNo+1])
        FEM_Fourier_Coef[LinerNo+1]= FourierCalc(SecNo_FEM, nodes_FEM_OD_WT, displacement_FEM_OD_WT, temp_OD, dr_FEM_OD_WT, temp_FEM_OD_WT)
        # chk1_flag = False
        

    main.L1.clear()    
    main.addfig('Cylinder No 1',fig[1])
    main.addfig('Cylinder No 2',fig[2])
    main.addfig('Cylinder No 3',fig[3])
    main.addfig('Cylinder No 4',fig[4])
    
    main.table1.setRowCount(4)
    main.table1.setColumnCount(4)
    
    for ind,item in FEM_Fourier_Coef.items():
        main.table1.setItem(ind-1, 0, QTableWidgetItem(str(item[ind-1,0])))
        main.table1.setItem(ind-1, 1, QTableWidgetItem(str(item[ind-1,1])))
        main.table1.setItem(ind-1, 2, QTableWidgetItem(str(item[ind-1,2])))
        main.table1.setItem(ind-1, 3, QTableWidgetItem(str(item[ind-1,3])))
        
    
def plotDis() :
    for i in range(4):
        main.canvas[i+1].setVisible(False)
    
if __name__=='__main__':
    import sys 
    from PyQt5 import QtGui
    import numpy as np
    

    app = QApplication(sys.argv)
    main = Main()

    
    ##################################################
    
            
    main.show() 
    # action menu bar is used to import FEM datat file.
    main.actionOpen.triggered.connect(lambda : importFile())
    # main.chk1.stateChanged.connect(lambda : plotDis())
    main.SectNO_done.clicked.connect(lambda : sectNumber())
    main.B_FEM.clicked.connect(lambda : plotfunc())
    main.ExitButt.clicked.connect(QApplication.instance().quit)
    
    
    ##################################################
    
    
    sys.exit(app.exec_())