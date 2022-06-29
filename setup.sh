#!/bin/bash

chmod +x startup.sh
cp startup.sh ../startup.sh
mkdir spello_model
mkdir uploads
echo this is a sample file> ./uploads/sample.txt
cd spello_model
gdown --id 1k2ebwMHqBnZKSqKw26ZMd07__WFyM9tw
cd ../java-indicators
gdown --id 1mDcJp4fDsaR89qtGeJAUhP_D52kSL_wA
cd ..


conda install -c anaconda flask -y
conda install -c conda-forge flask-restful -y
conda install -c anaconda flask-cors -y
conda install -c anaconda nltk -y
conda install -c conda-forge pyenchant -y
pip install spello
conda install -c conda-forge textstat -y
./startup.sh