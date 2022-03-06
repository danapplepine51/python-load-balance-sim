from pickle import NONE
from re import L
import sys
import glob
import time

# sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/project/song0254/csci5105/lib/thrift-0.15.0/lib/py/build/lib*')[0])

from request_service import RequestService

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main(is_test=None, config_filename='config'):

    hostname = ""
    numPort = 9197
    proj_path='./'

    ## Reading config file and parsing to connect to server with host name
    with open(config_filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            tok = line.split(":")
            if 'server' in tok[0]:
                hostAndPort = list(tok[1].split(","))
                hostname = str(hostAndPort[0])
                numPort = int(hostAndPort[1])
            elif 'proj_path' in tok[0]:
                proj_path=str(tok[1])
                
    # Make socket
    transport = TSocket.TSocket(hostname, numPort)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = RequestService.Client(protocol)

    # Connect!
    transport.open()

    msg = client.request(proj_path)

    # Close!
    transport.close()

    ## For autograding script detection
    if is_test:
        return msg
    else:
        time.sleep(180)
    

if __name__ == '__main__':
    main()