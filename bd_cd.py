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
import cmath
scale = 800

SecNo_CMM = 11
SecNo_FEM = 32

ax=np.zeros(4)
CylNo = 4
add='FEM_OD_WT'
temp_FEM_OD_WT=np.zeros((124,3))
# this part counts the number of step files in the add directory
StepFileNo=len(fnmatch.filter(os.listdir(add), 'STEP*.txt'))


secNo=input("Sec")
for LinerNo in range (CylNo):
    tempstr="STEP1LINER0"+str(LinerNo+1)+"*.txt"
    StepFileNo=len(fnmatch.filter(os.listdir(add), tempstr))
    displacement_names_FEM='STEP1LINER0'+str(LinerNo+1)+'SEC0'+str(secNo)+'.txt'
    displacement_add="C:\\Users\\student\\Desktop\\BD\\FEM_CD_WT\\"+displacement_names_FEM
    NodeAdd="C:\\Users\\student\\Desktop\\BD\\FEM_CD_WT\\nodes.txt"
    
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
    deformation_OD=temp_OD[:,1:]
    
    Number_FEM_OD_WT=len(displacement_FEM_OD_WT)
    
    Cmean_FEM_OD_WT=np.mean(temp_OD[:,1:],axis=0)
    Rnorm_FEM_OD_WT=LA.norm(deformation_OD[0,:]-Cmean_FEM_OD_WT)
    
    #polar plotting requirements
    rpolar=np.sqrt(deformation_OD[:,0]**2+deformation_OD[:,1]**2)
    phi_polar=np.arctan2(deformation_OD[:,1],deformation_OD[:,0])
    
    x_deformed=temp_OD[:,1]+displacement_FEM_OD_WT[:,1]
    y_deformed=temp_OD[:,2]+displacement_FEM_OD_WT[:,2]
    r_deformed=np.sqrt(x_deformed**2+y_deformed**2)
    
    dr_FEM_OD_WT=r_deformed-rpolar    
    
    temp_FEM_OD_WT[:,0]=phi_polar
    temp_FEM_OD_WT[:,1]=rpolar
    temp_FEM_OD_WT[:,2]=dr_FEM_OD_WT
    temp_FEM_OD_WT=temp_FEM_OD_WT[np.argsort(temp_FEM_OD_WT[:,0])]

    T0=2*np.pi
    w0=2*np.pi/T0
    
    
    ForOrd=3
    x=np.zeros((len(dr_FEM_OD_WT),ForOrd+1))
    y=np.zeros_like(x)
    A=np.zeros((ForOrd+1))
    B=np.zeros_like(A)
    phi=np.zeros_like(A)
    ForderArr=np.arange(ForOrd+1)
    FEM_CD_WT_Fourier=np.zeros((ForOrd+1,4))
    for n in range(ForOrd+1):
#        Consider that x here is not the axis it is the function 
        x[:,n]=temp_FEM_OD_WT[:,2]*np.cos(n*w0*temp_FEM_OD_WT[:,0])
        y[:,n]=temp_FEM_OD_WT[:,2]*np.sin(n*w0*temp_FEM_OD_WT[:,0])
        A[n]=(2/T0) * np.trapz(x[:,n],temp_FEM_OD_WT[:,0])
        B[n]=(2/T0) * np.trapz(y[:,n],temp_FEM_OD_WT[:,0])
        U=A+(B*1j)
        Uabs=2000 * np.abs(U)
        phi[n]=cmath.phase(U[n])*(180/np.pi)
    ztop = (204.386 - temp_OD[1,3] )*np.ones(ForOrd+1)
    FEM_CD_WT_Fourier[:,0]=ForderArr
    FEM_CD_WT_Fourier[:,1]=Uabs
    FEM_CD_WT_Fourier[:,2]=phi
    FEM_CD_WT_Fourier[:,3]=ztop
    print("order=",ForderArr,"phi =",phi,"at SEC",secNo)
    # f1=plt.figure(LinerNo,figsize=(5,5))
    # plt.polar(temp_FEM_OD_WT[:,0],temp_FEM_OD_WT[:,1])
    # nameFig='FEM_Distortion_Bore'+str(LinerNo+1)+'.jpg'
    # plt.savefig(nameFig, dpi=300 )