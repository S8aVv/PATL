# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:32:26 2016

@author: shaw
"""
import matplotlib.pyplot as plt
from collections import defaultdict  
import random   
import numpy as np
from itertools import product
from pipes import FILEIN_FILEOUT
from os import listdir

def load(tag):#load excel
    
     
    
    maindir="C:/Users/shaw/Desktop/01202016615/(%d,%d)"%(tag[0],tag[1])
    dirs= listdir(maindir)
    print(dirs)
    
    for logdir in dirs:
        print('logdir',logdir)

        antennas=[]
        antennass=[]
        a_num=[]
        for line in open(maindir+"/"+logdir).readlines()[1:]:
 
            try:
              w=line.split(",")
              antenna=int(w[1]) 
              antennas.append(antenna)
             

            except:
               print ("cannot pars",line)   
      
        k=1 
        print('length',len(antennas))
        
        for i in range(len(antennas)):
            if  antennas[i+1] is antennas[i]:
                k=k+1
            if  not antennas[i+1] is antennas[i]:
                  a_num.append(k)
                  antennass.append(antennas[i])
                  k=1
      
            if antennas[i+1]<antennas[i]:
                  break
        print('antennass',antennass)
        print('a_____num',a_num)
        print('sum_num',sum(a_num))
        
    return(antennass,a_num)# return the antennas which read tag and the corresponding numbers 

def counting(tags_num,tags_pos):
   tag_x = 0
   tag_y = 0
   sum_num=sum(tags_num) 
# use "if .. is .." or " if not..is.." to add conditions and filter antenna    

   for i in range(len(tags_pos)): #when add conditions, it is no longer "antennass", but the antennas you pick    
        tag_x=tag_x+(tags_num[i]/float(sum_num))*(tags_pos[i][0])
        tag_y=tag_y+(tags_num[i]/float(sum_num))*(tags_pos[i][1])
   tag_pos=[tag_x*100,tag_y*100]
   print('1', tag_pos)
   return(tag_pos)    
     
def judge(antennass, a_num): #judging sectors
    sector1 = np.array([1, 12, 20, 28, 36, 44, 52])
    sector2 = np.array([5, 13, 21, 29, 37, 45])
    sector3 = np.array([2, 6, 14, 22, 30, 38, 46])
    sector4 = np.array([7, 15, 23, 31, 39, 47])
    sector5 = np.array([3, 8, 16, 24, 32, 40 ,48])
    sector6 = np.array([9, 17, 25, 33, 41, 49])
    sector7 = np.array([4, 10, 18, 26, 34, 42, 50])
    sector8 = np.array([11, 19, 27, 35, 43, 51])
    sector_count = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    big_sector = np.array([0, 0, 0, 0])
    antennas_count = np.array(a_num)
    antennas_num = np.array(antennass)

    rings = []
    rings_num = []    
    rings_pos = []
    
#    antenna = np.dtype({
#   'names': ['atenna', 'x' , 'y'],
#   'formats': ['i', 'd', 'd']}, align = True)
    antenna_pos = np.array([[-0.25, 0.25], [0.25, 0.25], [0.25, -0.25], [-0.25, -0.25],
                            [0, 0.625], [0.44, 0.44], [0.625, 0],[0.44, -0.44],
                            [0, -0.625], [-0.44, -0.44], [-0.625, 0],[-0.44, 0.44], [0, 0.875],
                            [0.62, 0.62], [0.875, 0], [0.62, -0.62], [0 , -0.875], [-0.62, -0.62], 
                            [-0.875, 0], [-0.62, 0.62], [0, 1.125], [0.8, 0.8], [1.125, 0], 
                            [0.8, -0.8], [0, -1.125], [-0.8, -0.8], [-1.125, 0], [-0.8, 0.8],
                            [0, 1.375], [0.97, 0.97], [1.375, 0],[0.97, -0.97], [0, -1.375], [0.97, -0.97],
                            [-1.375, 0], [-0.97, 0.97], [0, 1.625], [1.15, 1.15], [1.625, 0], [1.15, -1.15],
                            [0, -1.625], [-1.15, -1.15], [-1.625, 0], [-1.15, 1.15], [0, 1.875], [1.33, 1.33],
                            [1.875, 0], [1.33, -1.33], [0, -1.875], [-1.33, -1.33], [-1.875, 0], [-1.33, 1.33]])    
     
    
    for i in range(len(antennas_num)):
        if antennas_num[i] in sector1:
            sector_count[0]+=1
        elif antennas_num[i] in sector2:
            sector_count[1]+=1
        elif antennas_num[i] in sector3:
            sector_count[2]+=1
        elif antennas_num[i] in sector4:
            sector_count[3]+=1
        elif antennas_num[i] in sector5:
            sector_count[4]+=1
        elif antennas_num[i] in sector6:
            sector_count[5]+=1
        elif antennas_num[i] in sector7:
            sector_count[6]+=1
        elif antennas_num[i] in sector8:
            sector_count[7]+=1
    
    print('count', sector_count)
    
    big_sector[0] = sector_count[0] + sector_count[1] + sector_count[2]
    big_sector[1] = sector_count[2] + sector_count[3] + sector_count[4]
    big_sector[2] = sector_count[4] + sector_count[5] + sector_count[6]
    big_sector[3] = sector_count[6] + sector_count[7] + sector_count[0]
    
    print('big_sector', big_sector)   
    
    max_sector = np.argmax(big_sector) + 1
    print('max_sector', max_sector)
    
    if max_sector == 1:
        for index, value in np.ndenumerate(antennas_num):
            if( not value in np.concatenate((sector5, sector6, sector7))):
                rings.append(antennas_num[index])
                rings_num.append(antennas_count[index])
                
    elif max_sector == 2:
        for index, value in np.ndenumerate(antennas_num):
            if( not value in np.concatenate((sector1, sector7, sector8))):
                rings.append(antennas_num[index])
                rings_num.append(antennas_count[index])
                
    elif max_sector == 3 :
        for index, value in np.ndenumerate(antennas_num):
            if( not value in np.concatenate((sector1, sector2, sector3))):
                rings.append(antennas_num[index])
                rings_num.append(antennas_count[index])
                
    elif max_sector == 4:
        for index, value in np.ndenumerate(antennas_num):
            if( not value in np.concatenate((sector3, sector4, sector5))):
                rings.append(antennas_num[index]) 
                rings_num.append(antennas_count[index])
    
    
    for i in range(len(rings)):
       rings_pos.append(antenna_pos[rings[i]-1])
        
        
    print ('rings_pos', rings_pos)
    print ('rings', rings)    
    print('rings_num', rings_num)
    return(rings_num, rings_pos)

def main():
    tag = [8,61]
    
    (antennass,a_num) = load(tag)
    (tags_num, tags_pos) = judge(antennass,a_num)
    tag_pos = counting(tags_num, tags_pos)
    error = np.sqrt((tag[0]-tag_pos[0])**2+(tag[1]-tag_pos[1])**2)
    
    print('tag,tag_count,error',tag,tag_pos,error)
    
    plt.xlim(-200,200)
    plt.ylim(-200,200)
    

    plt.plot(tag[0],tag[1],'v')
    plt.plot(tag_pos[0],tag_pos[1],'^')
    plt.plot(0, 0, '*')
    plt.show()
  

if __name__ == '__main__':
    main()   