#!/bin/bash

CONFIG_FILE=$1
PROJ_DIR=$2
ssh -T -n -f song0254@csel-kh1250-04.cselabs.umn.edu  "csh -c ' setenv THRIFT_LIB_PATH /project/song0254/csci5105/lib/thrift-0.15.0/lib/py/build/lib && setenv OPENCV_LIB_PATH /project/song0254/csci5105/lib/opencv/build/lib && setenv PROJ_PATH /project/song0254/csci5105/pa1 && cd $PROJ_DIR &&  nohup python3 server.py $CONFIG_FILE & '" > /dev/null
########################
