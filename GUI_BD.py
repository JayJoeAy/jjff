from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure


	
Ui_MainWindow, QMainWindow = loadUiType('BDwindow.ui')

class Main(Ui_MainWindow,QMainWindow):
    def __init__(self, ):
        super(Main,self).__init__()
        self.setupUi(self)
    
    def addmpl(self,fig):
        self.canvas=FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
 
 
if __name__=='__main__':
    import sys 
    from PyQt5 import QtGui
    import numpy as np
    
    fig1=Figure()
    ax1f1=fig1.add_subplot(111, projection='polar')
    #ax1f1.plot(np.random.rand(5))
    
    
    app = QApplication(sys.argv)
    

    ##################################################
    import os,fnmatch,sys,csv,pandas
    import numpy as np
    from numpy import linalg as LA
    #import matplotlib.pyplot as plt
    scale = 500

    SecNo_CMM = 11
    SecNo_FEM = 32

    ax=np.zeros(4)
    CylNo = 4
    add='FEM_OD_WT'
    temp_FEM_OD_WT=np.zeros((124,2))
    # this part counts the number of step files in the add directory
    StepFileNo=len(fnmatch.filter(os.listdir(add), 'STEP*.txt'))



    for LinerNo in range (CylNo):
        
        displacement_names_FEM='STEP1LINER0'+str(LinerNo+1)+'SEC'+str(32)+'.txt'
        displacement_add="C:\\Users\\student\\Desktop\\BD\\FEM_OD_WT\\"+displacement_names_FEM
        NodeAdd="C:\\Users\\student\\Desktop\\BD\\FEM_OD_WT\\nodes.txt"
        
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
    #    f2=plt.figure(1,figsize=(5,5))
    #    matplotlib.axes.Axes.set_xlim=axis(option='equal')
        #f1=plt.figure(LinerNo,figsize=(5,5))
        ax1f1.plot(temp_FEM_OD_WT[:,0],temp_FEM_OD_WT[:,1], label='CylNO'+str(LinerNo+1))
        ax1f1.legend()
    ##################################################
    main = Main()
    main.addmpl(fig1)
    
    main.show()
    sys.exit(app.exec_())