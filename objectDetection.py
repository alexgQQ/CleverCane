import os, sys
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf
import pickle

from utils.app_utils import FPS, WebcamVideoStream
from multiprocessing import Queue, Pool, Process
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

from colors import _H_DETECT

CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
#PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')
#PATH_TO_CKPT = r'/home/linaro/jobs/object_detection/ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb'
PATH_TO_CKPT = r'/home/linaro/jobs/object_detection/custom_model/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
#PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')
PATH_TO_LABELS = r'/home/linaro/jobs/object_detection/data/custom_label_map.pbtxt'

#NUM_CLASSES = 90
NUM_CLASSES = 5

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def detectObjects(image_np, sess, detection_graph):

    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    return boxes, scores, classes, num_detections

def processDetect(classes, scores):
    found = []
    for conf, pred in zip(scores[0], classes[0]):
        if conf >= 0.5:
#            found.append(str( category_index[pred].get('name')) + ':' + str(conf))
            found.append(str(category_index[pred].get('name')))
    return found

def processDetect_wScores(classes, scores):
    found = []
    confidence = []
    for conf, pred in zip(scores[0], classes[0]):
        if conf >= 0.5:
            found.append(str(category_index[pred].get('name')))
            confidence.append(str(conf))
    return found, confidence

def visualizeDetection(im, region, conf, pred, num_det):
    vis_util.visualize_boxes_and_labels_on_image_array(
        im,
        np.squeeze(region),
        np.squeeze(conf).astype(np.int32),
        np.squeeze(pred),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    return im

def loadSession():
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)
        return sess, detection_graph

def singleImageRun(image):

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    frame = cv2.imread(image)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    b, s, c, n = detectObjects(frame, sess, detection_graph)
    #results = processDetect(b, s, c, n)

    print _H_DETECT + "Detection Complete"
    return b, s, c, n

def modelEval():

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    base = "/home/linaro/jobs/test_images/"
    for imageFile in os.listdir(base):
        line = imageFile + ","
        frame = cv2.imread(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        start = time.time()
        b, s, c, n = detectObjects(frame, sess, detection_graph)
        elapsed = time.time() - start
        classes, scores = processDetect_wScores(c, s)
        for cla, scr in zip(classes, scores):
            line += cla + "," + scr + ","
        line += str(elapsed)
        print _H_DETECT + line


def testDetQueue(image, outQueue):
    reg, scr, cla, num = singleImageRun(image)
    outQueue.put(((cla, scr), num))


def singleStream(videoCapture, outputQueue, visualize, imageQueue):
    
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    success, frame = videoCapture.read()

    while success:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        b, s, c, n = detectObjects(frame, sess, detection_graph)
        
        outputQueue.put(n)
        outputQueue.put(b)
        outputQueue.put(c)
        outputQueue.put(s)

        if visualize:
                imageQueue.put(frame)
#        outputQueue.put(((c, s), n))

        success, frame = videoCapture.read()

    videoCapture.release()

def runDetect(frameQueue, outputQueue, visualize):
    
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    while True:
        frame = frameQueue.get(True)
        b, s, c, n = detectObjects(frame, sess, detection_graph)
        outputQueue.put(((c, s), n))


if __name__ == "__main__":

    image = "/home/linaro/jobs/test-image.jpg"

    if len(sys.argv) > 1:
        if sys.argv[1] == "load":
            print _H_DETECT + "Loading Tensorflow Session..."
            tf_sess, tf_detgraph = loadSession()

        elif sys.argv[1] == "detect":
            print _H_DETECT + "Single Image Run..."
            box, score, pred, num = singleImageRun(image)
            print processDetect(pred, score)

        elif sys.argv[1] == "eval":
            print _H_DETECT + "Model Evaluation..."
            box, score, pred, num = singleImageRun(image)
            detected, scores = processDetect_wScores(pred, score)

        elif sys.argv[1] == "queue":
            print _H_DETECT + "Detection Queue Test..."
            q = Queue()
            p = Process(target=testDetQueue, args=(image, q,))
            p.start()
            data = q.get(True)[0]
            print processDetect(data[0], data[1])
            p.join()

        elif sys.argv[1] == "stream":
            video = cv2.VideoCapture(0)
            q = Queue()
            p = Process(target=singleStream, args=(video, q, False,))
            p.start()
            while True:
                data = q.get(True)[0]
                print processDetect(data[0], data[1])
    else:
        print "Usage: python " + sys.argv[0] + " load|detect|queue|stream|eval"
