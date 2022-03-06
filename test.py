import os
import time
from warnings import catch_warnings
import client
from os import listdir
from os.path import isfile, join

def test_empty_input_dir(config_file):
    elapsed_time = -1
    proj_path = ""
    with open(config_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            tok = line.split(":")
            if 'proj_path' in tok[0]:
                proj_path=str(tok[1])

    print("Remove all files from input_dir")
    os.system('cd input_dir && rm *')
    print("Remove all files from output_dir")
    os.system('cd output_dir && rm *')

    try:
        time.sleep(3)
        print("Boot Server")
        os.system('./test/bootServer.sh {0} {1}'.format(config_file, proj_path))
        print("Boot Node")
        time.sleep(3)
        os.system('./test/bootNode.sh {0} {1}'.format(config_file, proj_path))
        elapsed_time = client.main(is_test=True, config_filename=config_file)
        time.sleep(3)
        print("Cleaning")
        os.system('./test/cleanNode.sh')
        os.system('./test/cleanServer.sh')
        time.sleep(3)
    except KeyboardInterrupt:
        print("Keyboard Interrupt... Clean up")
        time.sleep(3)
        os.system('cd autograder && ./cleanup.sh')
    except:
        print("Error occured... Clean up")
        time.sleep(3)
        os.system('cd autograder && ./cleanup.sh')
        return -1

    print(elapsed_time + " seconds")
    input_path = './input_dir'
    output_path = './output_dir'
    try:
        input_filelist = [f for f in listdir(input_path) if isfile(join(input_path, f))]
        output_filelist = [f for f in listdir(output_path) if isfile(join(output_path, f))]
    except:
        return -1

    print("Num input: " + str(len(input_filelist)) + " Num output: "+ str(len(output_filelist)) + " Expected: 0")
    if(len(output_filelist) != 0):
        print("Test failed")
        return -1
    else:
        print("Test pass")

    return float(elapsed_time)

def test(config_file):
    elapsed_time = -1
    proj_path = ""
    with open(config_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            tok = line.split(":")
            if 'proj_path' in tok[0]:
                proj_path=str(tok[1])
    try:
        print("Boot Server")
        os.system('./test/bootServer.sh {0} {1}'.format(config_file, proj_path))
        time.sleep(1)
        print("Boot Node")
        os.system('./test/bootNode.sh {0} {1}'.format(config_file, proj_path))
        time.sleep(1)
        elapsed_time = client.main(is_test=True, config_filename=config_file)
        print("Cleaning")
        os.system('./test/cleanNode.sh')
        os.system('./test/cleanServer.sh')
        time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt... Clean up")
        os.system('cd autograder && ./cleanup.sh')
        return -1
    except:
        print("Error occured... Clean up")
        time.sleep(1)
        os.system('cd autograder && ./cleanup.sh')
        return -1

    print(elapsed_time + " seconds")
    return float(elapsed_time)

def main():
    print('###### Test Case1 load_balancing 0.8 0.8 0.8 0.8 ######')
    result1 = test(config_file='./test/test_config1_load')

    print('###### Test Case2 load_balancing 0.1 0.1 0.1 0.1 ######')
    result2 = test(config_file='./test/test_config3_load')
    if result2 > result1:
        print("Total time should take less. Expected: prob:0.8 {0} < prob:0.5 {1}".format(result2, result1))
        return
    else:
        print("Test Pass: less load probability")

    print('###### Test Case3 load_balancing 0.8 0.5 0.3 0.1 ######')
    result3 = test(config_file='./test/test_config4_load')
    if result3 > result1:
        print("Total time should take less. Expected: {0} < {1}".format(result3, result1))
        return
    else:
        print("Test Pass: less load probability")

    print('###### Test Case4 random 0.8 0.8 0.8 0.8 ######')
    result4 = test(config_file='./test/test_config1_random')
    if result4 > result1:
        print("Total time should take less. Expected: {0} < {1}".format(result4, result1))
        return
    else:
        print("Test Pass: random injection vs load probability")
        

if __name__ == '__main__':
    # main()
    test_empty_input_dir('./test/test_config1_random')