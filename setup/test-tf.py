import sys
import os

api_test_loc = sys.argv[1] + '/object_detection/builders/model_builder_test.py'

class bcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

HEAD = "[" + bcol.OKBLUE + "TENSORFLOW" + bcol.ENDC + "]"

def err_check(str, err):
    OK = "[" + bcol.OKGREEN + "OK" + bcol.ENDC + "]"
    ERR = "[" + bcol.FAIL + "ERROR" + bcol.ENDC + "]"

    if err == False:
        print HEAD + str + OK
    elif err == True:
        print HEAD + str + ERR
    return 0

try:
    import tensorflow as tf
    version = tf.__version__
    err_check(" TF importing ", False)
    err_check(" TF Version " + version + " ", False)
except:
    err_check(" TF importing ", True)
#    sys.exit(-1)

def test_session():
    hello = tf.constant("Hello, TensorFlow")
    sess = tf.Session()
    print HEAD + sess.run(hello)
    a = tf.constant(10)
    b = tf.constant(32)
    print HEAD + sess.run(a + b)
    sess.close()

try:
    test_session()
    err_check(" Test Session ", False)
except:
    err_check(" Test Session ", True)

try:
    os.system("python " + api_test_loc)
    err_check(" Test API Build ", False)
except:
    err_check(" Test API Build ", True)
