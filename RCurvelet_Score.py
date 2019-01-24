# # coding=UTF-8 
# #necessário para os acentos ficarem corretos

########################################################################
#R(obust)Curvelet Score: Obtains an objective quality index for images from features.

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

#####################################################################


#######################
### Load Packages ####
#####################
import numpy as np
import pandas as pd
import sys

from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.externals import joblib
###################################################################
##################################################################
#################################################################


#################  Input variables ##########################
#Flags input
if len(sys.argv)<2:
	print
	print 'Enter the name of the input file after the script name'
	print 'Example:'
	print '		#python RCurvelet_Score.py input.csv'
	print 'Done'
	exit()

#### Load Data  #####
data_test=pd.read_csv(sys.argv[1],header=None).values

#Flags output
if len(sys.argv)<3:
	print
	print 'No score value will be exported to an output file'
	print 'To do this use:'
	print '		#python RCurvelet_Score.py input.csv score.csv'
	print 'Score: ',
else:
	output_csv = sys.argv[2]
	print 'Score saved in '+output_csv


#################################################

# Beware when Change ... important for Classifier prob order
ord_names = ['jp2k','jpeg','wn','gblur']

#########################
#### load Models #######
#######################

######################
###  Classifier #####
####################
#### Scaler  ######
##################

scale_file = "./models/scale_model.pkl"  
classifier_scaler=joblib.load(scale_file) 

##################
#### Model ######
################

classifier_file="./models/classifier_model.pkl"
classifier=joblib.load(classifier_file)

######################
###  Regressors #####
####################
#### Scalers and Models  ######
##################
regressor_scaler=[]
regressors=[]
for i in ord_names:
    ### Scaler ###
    scale_class_file = "./models/scale_class_"+i+"_model.pkl"
    regressor_scaler.append(joblib.load(scale_class_file))
    ### Regressor Model ###
    regressor_file="./models/regressor_class_"+i+"_model.pkl"
    regressors.append(joblib.load(regressor_file))

##################################
##### Using Model to Predict#####
################################


### Process Classifier ###
data_scaler_classifier=classifier_scaler.transform(data_test)
p=classifier.predict_proba(data_scaler_classifier)

### Process regressors ###
q=np.zeros_like(p)
for i in range(p.shape[1]):
    x=regressor_scaler[i].transform(data_test)
    q[:,i]=regressors[i].predict(x)
    
scores=np.sum(p*q,axis=1)
if len(sys.argv)>2:
	score_df = pd.DataFrame(scores)
	score_df.to_csv(output_csv, index=False, header=False)
else:
	print scores


