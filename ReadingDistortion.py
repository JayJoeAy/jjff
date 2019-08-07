from abaqus import *
from odbAccess import *
import numpy as np
s=open('sectNumber.txt','r')
section_no_tot=int(s.read())
s.close()
sectList=np.arange(section_no_tot)
liner_num=[None]*section_no_tot
for i in range(section_no_tot):
    if i<=8:
        liner_num[i]='0'+str(i+1)
    else:
        liner_num[i]=str(i+1)	

odb_adrs='C:\\Users\\student\\Desktop\\BIG DATA\\EF7_TotalBlockandCylhead_OpenDeck_BoreDist_Mainfile_54KPreload.odb'

myOdb=openOdb(odb_adrs)

steps_key=myOdb.steps.keys()

steps=myOdb.steps
step_no=len(steps_key)



instance_key=myOdb.rootAssembly.instances.keys()
instance=myOdb.rootAssembly.instances[instance_key[0]]

nodes_no_tot=instance.nodes.__len__()

nodes_label=[[0 for x in xrange(1)] for x in xrange(nodes_no_tot)]
n=0
for i in range(nodes_no_tot):
    nodes_label[i]=instance.nodes[i].label
    n=n+1

nodeSets_keys=instance.nodeSets.keys()
nodeSets=instance.nodeSets


# liner_num=['01','02','03','04','05','06','07','08','09','10',
           # '11','12','13','14','15','16','17','18','19','20',
           # '21','22','23','24', '25', '26', '27', '28', '29', '30']
liner_no_tot=4
# section_no_tot=30

f=open('new/'+'nodes.txt','w')
for h in range(step_no):
    step_name=steps_key[h]
    displacement=steps[step_name].frames[-1].fieldOutputs['U']
    for i in range(liner_no_tot):
        for j in range(section_no_tot):
            set_name='LINER0'+str(i+1)+'SEC'+liner_num[j]
            set_len=nodeSets[set_name].nodes.__len__()
            g=open('new/STEP'+str(h+1)+set_name+'.txt','w')
            coord=[[0 for x in xrange(4)] for x in xrange(set_len)] 
            disp=[[0 for x in xrange(3)] for x in xrange(set_len)]
            for k in range(set_len):
                coord[k][0]=nodeSets[set_name].nodes[k].label
                coord[k][1]=nodeSets[set_name].nodes[k].coordinates[0]
                coord[k][2]=nodeSets[set_name].nodes[k].coordinates[1]
                coord[k][3]=nodeSets[set_name].nodes[k].coordinates[2]
                if h==0:
                    f.write(str(coord[k][0])+', '+str(coord[k][1])+', '+str(coord[k][2])+', '+str(coord[k][3])+'\n')
                 

                    ind=nodes_label.index(coord[k][0])

                    disp[k][0]=displacement.values[ind].data[0]
                    disp[k][1]=displacement.values[ind].data[1]
                    disp[k][2]=displacement.values[ind].data[2]
                g.write(str(coord[k][0])+', '+str(disp[k][0])+', '+str(disp[k][1])+', '+str(disp[k][2])+'\n')

f.close()
g.close()


