from maxbotix import XL_MaxSonar
from time import sleep
from colors import _H_SONAR

class MySensor(XL_MaxSonar):

    def __init__(self, port):
        XL_MaxSonar.__init__(self, port)

    def handleUpdate(self, distanceCentimeters):
        self._avg = self._avg + distanceCentimeters

def streamSonar(serialPort, outputQueue, iter):
    sensor = MySensor(serialPort)
    if iter > 0:
        override = False
    else:
        override = True

    while iter or override:
        outputQueue.put(sensor._average())
        iter -= 1 

if __name__ == "__main__":

    print _H_SONAR + "Running Sonar Test"

    from multiprocessing import Process, Queue

    class SensorTest(XL_MaxSonar):

        def __init__(self, port):
            XL_MaxSonar.__init__(self, port)

        def handleUpdate(self, distanceCentimeters):
            print str(distanceCentimeters)

    def testSonar(serialPort):
        sensor = SensorTest(serialPort)
        for i in range(5):
            print sensor._average()

    PORT = '/dev/ttyUSB0'

    print _H_SONAR + "Raw Sonar Test..."
    testSonar(PORT)

    print _H_SONAR + "Testing Sonar Process Spawn..."
    p = Process(target=testSonar, args=(PORT,))
    p.start()
    p.join()

    print _H_SONAR + "Testing Sonar Queue Interaction..."
    q = Queue()
    n = 5
    p = Process(target=streamSonar, args=(PORT, q, n,))
    p.start()
    for i in range(n):
        print q.get(True, 1)
    p.join()

    print _H_SONAR + "Sonar Test Complete"