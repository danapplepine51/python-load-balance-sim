import glob
from importlib.resources import path
from json import load
from re import L
import sys
import os

sys.path.insert(0, glob.glob('/project/song0254/csci5105/lib/thrift-0.15.0/lib/py/build/lib*')[0])
sys.path.insert(1, glob.glob('/project/song0254/csci5105/lib/opencv/build/lib/python3')[0])

from load_balancer import LoadBalancer

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from os import listdir
from os.path import isfile, join
import cv2
import random
import time

SLEEP_TIME=5
REJECT_PANALTY=2

class LoadBalancerHandler:
    def __init__(self, schedule_policy, load_probability):

        self.schedule_polity = schedule_policy
        self.load_probability = load_probability

    ## Compute canny edge detection. If random choose by load_probabiliy decided to reject,
    ## it will have time penalty(talked with Prof. Chandra) and return False to notify server.py
    ## that the image is not computed
    def compute(self, filename, directory='./'):
        rand = round(random.uniform(0.0, 1.0), 10)
        if self.schedule_polity == 'load_balancing':
            rand = round(random.uniform(0.1, 1.0), 10)
            if rand < self.load_probability:
                time.sleep(REJECT_PANALTY)
                return False

        rand = round(random.uniform(0.0, 1.0), 10)
        if rand < self.load_probability:
            time.sleep(SLEEP_TIME)
        
        img = cv2.imread(os.path.join(directory, 'input_dir', filename))
        img = cv2.Canny(img, threshold1=100, threshold2=200)
        outputFileName = os.path.join(directory, 'output_dir', filename)
        cv2.imwrite(filename=outputFileName, img=img)
        return True

def main():

    policy = 'random'
    load_probability = 0.8
    config_filename = 'config'
    numNode = sys.argv[1:][0]
    numPort = 9197

    # Different config file (policy and load probability) for testing purposes
    if len(sys.argv) == 3:
        config_filename = sys.argv[2:][0]
        
    ## Reading config file and parsing to set the port, policy and probability
    with open(config_filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            tok = line.split(":")
            if 'policy' in tok[0]:
                policy = str(tok[1])
            elif 'probability' in tok[0]:
                prob_list = list(tok[1].split(","))
                load_probability = float(prob_list[int(numNode)])
            elif 'node_' + str(numNode) in tok[0]:
                hostAndPort = list(tok[1].split(","))
                numPort = int(hostAndPort[1])
    
    handler = LoadBalancerHandler(policy, load_probability)
    processor = LoadBalancer.Processor(handler)
    transport = TSocket.TServerSocket(host=None, port=numPort)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    
    # You could do one of these for a multithreaded server
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    try:
        print('Starting the Node ' + numNode)
        server.serve()
    except:
        print(numNode)
    print('done.')

if __name__ == '__main__':
    main()