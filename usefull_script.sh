#!/bin/bash

#Program name: usefull_script.sh
#
#Description:
# Make a Q score for a batch of images.
#
#
#Author: Ramon Giostri Campos
#email:
#
#Requirements: Python and modules
#
#
#Log:
#12-09-2018 : Make a script
#
#
#Important notes:
#1 - Currently everything is hardcode
#2 -
#3 - 

############## Program ##################
# 
######### Inputs #########
#
input_folder=sample_images
sampling_file=features_sampling.csv
output_folder=my_output_folder
output_file=out.csv
in_extension=bmp

#
#
#
########## Preambulo ###########
total_files=`ls $input_folder/*.$in_extension | wc -l`
cont=0
#
rm -r $output_folder # 
mkdir $output_folder # output folder 



########## Processing ##############

for i in $input_folder/*.$in_extension
	do
	cont=$(( cont+1 ))
	echo 'File '$cont' of '$total_files
	
	python RCurvelet_Features.py $i ./$output_folder/$output_file
	cat ./$output_folder/$output_file>>$output_folder/$sampling_file
	rm -rf ./$output_folder/$output_file
done


python RCurvelet_Score.py $output_folder/$sampling_file $output_folder/scores_$sampling_file
echo 'Done'
