# # coding=UTF-8 
# #necessário para os acentos ficarem corretos

###################################################
#R(obust)Curvelet Features: obtains the features of an image to compose an objective quality index. 

#Copyright (C) 2018 Ramón Giostri Campos

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

###################################################


#######################
### Load Packages ####
#####################
import pyct as ct
import numpy as np
import pandas as pd

from skimage import data
from skimage.color import rgb2gray

import scipy as sc

import sys

#################  Input variables ##########################
#Input Flags
if len(sys.argv)<3:
	print
	print 'Enter the name of the input image and the output file after the script name'
	print 'Example:'
	print '		#python RCurvelet_Features.py input_image.jpg output_file.csv' 
	print 'Done'
	exit()
vimage = sys.argv[1]

output_csv = sys.argv[2]

#Train flag
if len(sys.argv)>4:
	in_class = np.int(sys.argv[3])
	in_score = np.float(sys.argv[4])
	print 'Class associated with image: '+str(in_class)
	print 'Score associated with image: '+str(in_score)

#The size block is hardcode
l = 256
vblock = (l,l)



###############################################
# Other definitions

######


def reescalonamento_niveis(img,smin=0,smax=255):
################
#### Description: Rescales an MxN matrix or image in a defined interval.
### Inputs: matrix, minimum scale value (default ZERO) and maximum scale value (default 255).
### Outputs: MxN array of integer values.
#########
    xmin=1.0*np.min(img)
    xmax=1.0*np.max(img)
    img_res=(smax-smin)*((img-xmin)/(xmax-xmin))+smin #reescalonamento
    return np.round(img_res)

####

def split_images_block(image,block=(256,256)):
    #############image
    #Description:
    # Split image (MxN) in block(m,n) with overlap for the result does not delete any pixel from the image
    ####
    #Input: image (numpy array), block (tuple or array like)
    #####
    #Output: numpy array with whape (m,n,M*N/m*n)
    ## Acess each block image with (:,:,index)
    ######
    # Note:
    # The code is robust in relation imagem (256,256) without overlay.
    ######
    #ToDo list:
    # - show warning message when the block is larger than the image
    ############################################
    ####################################################################
    ### Initial quantity
    M,N = image.shape #
    m,n = block #
    Mim, Nin = M/m, N/n # number of integer blocks available
    Mdm, Ndn = np.int(np.ceil(1.0*M/m)), np.int(np.ceil(1.0*N/n)) #desire number of blocks 
    Mrm, Nrn = M%m, N%n # number of over pixels
    sample = np.zeros((m,n,Mdm*Ndn)) # inicialize output
    ########
    #test of overlay necessity
    test_m = np.ceil(Mrm/(Mrm+1.)) 
    test_n = np.ceil(Nrn/(Nrn+1.))
    #######
    ### Define block with overlay
    overlay_m, overlay_n = test_m*(m - Mrm)/Mim, test_n*(n - Nrn)/Nin
    block_m,block_n = np.int(m-overlay_m),np.int(n-overlay_n)
    
    cont=0
    for i in xrange(Mdm):
        for j in xrange(Ndn):
            #print cont
            #print (block_m*i,block_n*i+m)
            #print (block_m*j,block_n*j+m)
            sample[:,:,cont]=image[block_m*i:block_m*i+m,block_n*j:block_n*j+m];
            cont+=1
    return sample, Mdm,Ndn


######### Curvelet structures ###########


def coef_part_scale(coef_full,cuvelet_structure,scale):
    #scale = 5
    index_min,index_max = cuvelet_structure.index(scale) #take a index of the scale i
    return coef_full[index_min:index_max]        

def coef_part_scale_angle(coef_full,cuvelet_structure,scale):
    n_ang, m = np.shape(cuvelet_structure.sizes[scale])
    e = ()
    ########################### Mean energy by angle
    for i in xrange(n_ang):
        index_min,index_max = cuvelet_structure.index(scale,i)
        e+=(coef_full[index_min:index_max],)
    return e


######## Features ########
def scalar_energy_features(coef_per_scale):
############
#Descripition:
# Scalar Energy between Layers
#
###########
#Input:
#coef_per_scale: tuple with coef per scale
#
#Output: set of 3 features
################
#Notes:
######################
#Scalar Energy
########################

##################################
    num_scales = 5
    e = np.zeros(num_scales)
    for i in xrange(num_scales):
        coef_temp = np.abs(coef_per_scale[i])
    	e[i]=np.mean(np.log10(coef_temp[coef_temp>0]))
    #############
    d1=e[0]-e[1]
    d2=e[1]-e[2]
    d3=e[2]-e[3]

    return (d1,d2,d3)

def s4(coef_part_scale_angle):
    ############
    #Descripition:
	# Energy Orientation in Layer S4.
	#
    ###########
    #Input:
    #coef_full (CLarray - is a numpy like array) - a cuvelet tranformation of image
    #cuvelet_struture: return of ct.fdct2
    #num_scales:
    ############
    #Output: set features in S4
    ################
    #ToDo:
    ########################
    #### Notes:
    ###########
    ###################################################
    n_ang = np.shape(coef_part_scale_angle)[0]
    x = np.zeros(n_ang)
    ########################### Mean energy by angle
    for i in xrange(n_ang):
        x[i]=np.mean(np.abs(coef_part_scale_angle[i]))
    
    #Octiles
    E1=np.percentile(x,12.5,interpolation='midpoint')# octile 1
    E2=np.percentile(x,25,interpolation='midpoint')# octile 2  or Quartile 1
    E3=np.percentile(x,37.5,interpolation='midpoint')# octile 3
    E4=np.percentile(x,50,interpolation='midpoint')# octile 4  or Quartile 2 or Median
    E5=np.percentile(x,62.5,interpolation='midpoint')# octile 5
    E6=np.percentile(x,75,interpolation='midpoint')# octile 6 or Quartile 3
    E7=np.percentile(x,87.5,interpolation='midpoint')# octile 7
    #Robust features
    CVQ=(E6-E2)/(E6+E2) #Quartile Coef Variation
    rMAD=np.median(np.abs(x-E4))/E4 #relative MAD
    area=np.sum(x) # Area over the curve
    #
    return (CVQ,rMAD,area)

def s5(x):
    ############
    #Descripition:
	# Investigation in Layer S5
	#
    ###########
    #Input:
    #coef_full (CLarray - is a numpy like array) - a cuvelet tranformation of image
    #cuvelet_struture: return of ct.fdct2
    #num_scales:
    ############
    #Output: set of features em S5
    ################
    #ToDo:
    # Separate de scale target
    ########################
    #### Notes:
    ###########
    # Model Fit
    ###########
    #
    #                         
    #Octiles
    E1=np.percentile(x,12.5,interpolation='midpoint')# octile 1
    E2=np.percentile(x,25,interpolation='midpoint')# octile 2  or Quartile 1
    E3=np.percentile(x,37.5,interpolation='midpoint')# octile 3
    E4=np.percentile(x,50,interpolation='midpoint')# octile 4  or Quartile 2 or Median
    E5=np.percentile(x,62.5,interpolation='midpoint')# octile 5
    E6=np.percentile(x,75,interpolation='midpoint')# octile 6 or Quartile 1
    E7=np.percentile(x,87.5,interpolation='midpoint')# octile 7
    #Robust
    mad=np.median(np.abs(x-E4))
    rSkew=1.0*((E6+E2)-2*E4)/(E6-E2)#Robust Skew of Bowley1920
    rKurt=1.0*((E7-E5)+(E3-E1))/(E6-E2)#Robust Kurtosys of Moors1988
    return (E4,E6-E2,mad,rSkew,rKurt)



def gen_split_analisys(image_in,curvelet2,block=(256,256)):
    ###
    m,n = block
    split_image, M,N =split_images_block(image=image_in,block=block)
    ##### Inicialize set vector ####
    e_orient=np.zeros((M*N,3))# S4
    f_set_mom=np.ones((M*N,5)) # S5
    e_distribution = np.zeros((M*N,3))#Scalar energy inter layer
    for i in xrange(M*N):
        coef_full = curvelet.fwd(split_image[:,:,i])
        ### Energy per scale
        e=[]
        for j in range(5)[::-1]:
            e.append(coef_part_scale(coef_full,curvelet2,j))
        e_distribution[i,:]=scalar_energy_features(e)
        ### Energy oriented S4
        coef_scale_angle = coef_part_scale_angle(coef_full=coef_full,cuvelet_structure=curvelet2,scale=3)
        e_orient[i,:] = s4(coef_scale_angle)
        ### Fine scale s5
        coef_scale = coef_part_scale(coef_full=coef_full,cuvelet_structure=curvelet2,scale=4)
        v1 = np.abs(coef_scale)
        v2 = np.log10(v1[v1>0])
        f_set_mom[i,:] = s5(x=v2)
       
            
    saida = np.hstack((f_set_mom,e_orient,e_distribution))
    return np.mean(saida,axis=0)
    


#### Export features ###

curvelet = ct.fdct2(vblock,5,32,ac=False) #Curvelet
image = reescalonamento_niveis(rgb2gray(data.imread(vimage)))

features = gen_split_analisys(image,curvelet,block=vblock)
if len(sys.argv)>3:
	#Train tail
    my_df = pd.DataFrame(features)
    my_df=pd.concat((pd.DataFrame([in_score]),my_df))
    my_df.columns = [in_class]
    my_df.T.to_csv(output_csv,header=False)
else:
	#Test tail
    my_df = pd.DataFrame(features)
    my_df.T.to_csv(output_csv, index=False, header=False)
    
