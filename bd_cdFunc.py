# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 08:33:23 2019

@author: ErfanHamdi
erfan.hamdi@gmail.com
"""
def FourierCalc(SecNo_FEM, nodes_FEM_OD_WT_2F, displacement_FEM_OD_WT_2F, temp_OD_2F, dr_FEM_OD_WT_2F, temp_FEM_OD_WT_2F):
    import os,fnmatch,sys,csv,pandas
    import numpy as np
    from numpy import linalg as LA
    import cmath
    
    CylNo = 4
    
    secNo=SecNo_FEM
 
    for LinerNo in range (CylNo):

        # Datas for the Node array
        nodes_FEM_OD_WT=nodes_FEM_OD_WT_2F
        
        # Datas for displacement array
        displacement_FEM_OD_WT=displacement_FEM_OD_WT_2F 

        # Find the array elements of disp in node
        temp_OD=temp_OD_2F
        
        

        
        dr_FEM_OD_WT=dr_FEM_OD_WT_2F   
        
        temp_FEM_OD_WT=temp_FEM_OD_WT_2F
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
    # print("order=",ForderArr,"phi =",phi,"at SEC",secNo)
    return FEM_CD_WT_Fourier
