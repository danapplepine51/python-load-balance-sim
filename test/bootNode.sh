#!/bin/bash
# CONFIG_FILE_LIST = ("./test/config_test1", "./test/config_test2", "./test/config_test3", "./test/config_test4")

CONFIG_FILE=$1
PROJ_DIR=$2

ssh -T -n -f song0254@csel-kh1250-05.cselabs.umn.edu  "csh -c ' setenv THRIFT_LIB_PATH /project/song0254/csci5105/lib/thrift-0.15.0/lib/py/build/lib && setenv OPENCV_LIB_PATH /project/song0254/csci5105/lib/opencv/build/lib && setenv PROJ_PATH /project/song0254/csci5105/pa1 &&  cd $PROJ_DIR &&  nohup python3 computeNode.py 0 $CONFIG_FILE & '" > /dev/null
ssh -T -n -f song0254@csel-kh1250-07.cselabs.umn.edu  "csh -c ' setenv THRIFT_LIB_PATH /project/song0254/csci5105/lib/thrift-0.15.0/lib/py/build/lib && setenv OPENCV_LIB_PATH /project/song0254/csci5105/lib/opencv/build/lib && setenv PROJ_PATH /project/song0254/csci5105/pa1 &&  cd $PROJ_DIR &&  nohup python3 computeNode.py 1 $CONFIG_FILE & '" > /dev/null
ssh -T -n -f song0254@csel-kh1250-08.cselabs.umn.edu  "csh -c ' setenv THRIFT_LIB_PATH /project/song0254/csci5105/lib/thrift-0.15.0/lib/py/build/lib && setenv OPENCV_LIB_PATH /project/song0254/csci5105/lib/opencv/build/lib && setenv PROJ_PATH /project/song0254/csci5105/pa1 &&  cd $PROJ_DIR &&  nohup python3 computeNode.py 2 $CONFIG_FILE & '" > /dev/null
ssh -T -n -f song0254@csel-kh1250-09.cselabs.umn.edu  "csh -c ' setenv THRIFT_LIB_PATH /project/song0254/csci5105/lib/thrift-0.15.0/lib/py/build/lib && setenv OPENCV_LIB_PATH /project/song0254/csci5105/lib/opencv/build/lib && setenv PROJ_PATH /project/song0254/csci5105/pa1 &&  cd $PROJ_DIR &&  nohup python3 computeNode.py 3 $CONFIG_FILE & '" > /dev/null

########################
