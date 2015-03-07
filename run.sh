#!/usr/bin/env bash


# loading dependencies
apt-get install python-blist

# setting proper permissions
chmod a+x insight.py

# create directory if already not already present 
mkdir -p ./wc_input
mkdir -p ./wc_output


python insight.py -f wordcount -i ./wc_input -o ./wc_output/wc_result.txt
python insight.py -f runningmedian -i ./wc_input -o ./wc_output/med_result.txt
