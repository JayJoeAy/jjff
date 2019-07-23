# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 08:33:23 2019

@author: ErfanHamdi
erfan.hamdi@gmail.com
"""
import os,fnmatch,sys,csv,pandas
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
scale = 800

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
    f1=plt.figure(LinerNo,figsize=(5,5))
    plt.polar(temp_FEM_OD_WT[:,0],temp_FEM_OD_WT[:,1])
    nameFig='FEM_Distortion_Bore'+str(LinerNo+1)+'.jpg'
    plt.savefig(nameFig, dpi=300 )