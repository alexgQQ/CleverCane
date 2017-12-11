import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf
import time
import pickle

from utils.app_utils import FPS, WebcamVideoStream
from multiprocessing import Queue, Pool
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


def loadSession(checkpoint):
    detection_graph = tf.Graph()

    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()

        with tf.gfile.GFile(checkpoint, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

        return sess, detection_graph


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


def processDetect(region, conf, pred, num_det):
    found = []
    if num_det > 0:
        for score, pred in zip(conf[0], pred[0]):
            if score >= 0.5:
                found.append(str( category_index[pred].get('name')) + ':' + str(score))
    return found


def visualize(im, region, conf, pred, num_det):
    vis_util.visualize_boxes_and_labels_on_image_array(
        im,
        np.squeeze(region),
        np.squeeze(conf).astype(np.int32),
        np.squeeze(pred),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    return im


def imageDetect(image, sess, det_graph, visualize):
    box, score, det_type, num_det = detectObjects(image, sess, det_graph)
    if visualize:
        image_show = visualize(image, box, score, det_type, num_det)
        cv2.imshow('Video', output_rgb)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
    return processDetect(box, score, det_type, num_det)

