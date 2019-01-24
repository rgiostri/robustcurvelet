####################################################################

##########   Robust Curvelet IQA release version:   ###############

##################################################################


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Public code of software Robust Curvelet IQA described in article:

NOME do ARTIGO

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


########### Features Generator: ###############

#############################################
###   Watch out for dependencies   #############
##############################################

Because 'pyct' this software run under python 2.7;

List of packeges to run Rcurvelet_Features: skimage, pandas, numpy, sys, scipy and pyct.

Only 'pyct' don't install by pip install, easy install or anaconda repo. 

To install pyct use the repository: https://github.com/slimgroup/PyCurvelab

#############################################################

### To make a train features type: ####

$ python RCurvelet_Features.py path/to/input_image.jpg path/to/output_file.csv

### To make a test features: ####

$ python RCurvelet_Features.py path/to/input_image.jpg path/to/output_file.csv image_class image_survey_score

################################################################

########### Score Q Generator: ###############

#############################################
###   Watch out for models and dependencies #############
##############################################

This software use sklearn.

This module uses trained models. 
In the example, trained models with the classes jpeg, jp2k, Gaussian white noise and Gaussian Blur of experiments LIVE IQA, TID2013 and CSIQ are available

The name of the models follows a fixed structure: 
a) Regressor models name is: regressor_class_DEGRADATION_model.pkl
b) Scale models name is: scale_class_DEGRADATION_model.pkl


##############################

### To make a score: ####

$ python RCurvelet_Score.py input.csv #To show

$ python RCurvelet_Score.py input.csv score.csv #To save output file.

Note: input.csv can be a multiline file.

### Usefull script ####

Use a shell script "usefull_script.sh" to make a scores for a batch of images.


########### Model Generator: ###############

will appear soon


