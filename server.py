import glob
from platform import node
import sys
import os

sys.path.insert(0, glob.glob('/project/song0254/csci5105/lib/thrift-0.15.0/lib/py/build/lib*')[0])

from load_balancer import LoadBalancer
from request_service import RequestService

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from os import listdir
from os.path import isfile, join
import threading
import time
import random

## Log time for the total computation
def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn

class RequestServiceHandler:
    def __init__(self, nodeList, portList):
        self.nodeList = nodeList
        self.portList = portList
        self.nodeLength = len(nodeList) - 1

    ## It will create connection to the compute node and try to send the filename
    ## to process
    def sendToNode(self, filename, proj_path='./'):
        failed = True
        while(failed):
            idx = random.randrange(0, self.nodeLength)

            transport = TSocket.TSocket(self.nodeList[idx], self.portList[idx])

            # Buffering is critical. Raw sockets are very slow
            transport = TTransport.TBufferedTransport(transport)

            # Wrap in a protocol
            protocol = TBinaryProtocol.TBinaryProtocol(transport)

            # Create a client to use the protocol encoder
            client = LoadBalancer.Client(protocol)

            # Connect!
            transport.open()
            
            # Compute Canny Edge
            if client.compute(filename=filename, directory=proj_path):
                # Close !
                failed = False
                transport.close()
                break

    ## Receive the job from the client, read and check the filenames,
    ## and send jobs to computenode in a distributed way
    @logging_time
    def request(self, proj_path='./'):
        start_time = time.time()
        input_dir = os.path.join(proj_path, 'input_dir')
        try:
            fileNames = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
        except:
            return -1

        t_list = []
        for filename in fileNames:
            t = threading.Thread(target=self.sendToNode, args=(filename, proj_path,))
            t_list.append(t)
            t.start()
        
        for t in t_list:
            t.join()

        elapsed_time = "{0}".format(time.time() - start_time)
        return elapsed_time

def main():
    nodeList = []
    portList = []
    numPort = 9197
    config_filename='config'
    
    # Different config file (policy and load probability) for testing purposes
    if len(sys.argv) == 2:
        config_filename = sys.argv[1:][0]

    with open(config_filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            tok = line.split(":")
            if 'node' in tok[0]:
                hostAndPort = list(tok[1].split(","))
                nodeList.append(str(hostAndPort[0]))
                portList.append(int(hostAndPort[1]))
            elif 'server' in tok[0]:
                hostAndPort = list(tok[1].split(","))
                numPort = int(hostAndPort[1])

    handler = RequestServiceHandler(nodeList, portList)
    processor = RequestService.Processor(handler)
    transport = TSocket.TServerSocket(host=None, port=numPort)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)
    try:
        print('Starting the server...')
        server.serve()
    except:
        print(numPort)
    print('done.')

if __name__ == '__main__':
    main()