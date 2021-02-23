import tensorflow as tf
import tensorflow.contrib.slim as slim
from datasets import dataset_utils
from datasets import tf_record_dataset

import os
import numpy as np
from PIL import Image
import sys
import pickle
import json


IMAGE_FILE_EXTS = ['.jpg', '.jpeg']

class Classifier(object):
    def __init__(self, pb, out_node_name):
        with tf.Graph().as_default() as g:
            with tf.Session() as new_sess:
                self.new_sess = new_sess
                with tf.gfile.FastGFile(pb, 'rb') as f:
                    graph_def = tf.GraphDef()
                    graph_def.ParseFromString(f.read())
                    _ = tf.import_graph_def(graph_def, name='')
                
                #self.softmax = new_sess.graph.get_tensor_by_name("softmax_linear/softmax:0")
                self.out_weights = new_sess.graph.get_tensor_by_name(out_node_name)


                # Loading the injected placeholder
                self.image = new_sess.graph.get_tensor_by_name("image:0")


    def regression(self, filepath, flip=False):
        image_data = self._get_image_data(filepath, flip)

        result = self.new_sess.run(self.out_weights, {self.image: image_data})[0]
        return result.flatten().tolist()


    def _get_image_data(self, file_path, flip=False):
        with Image.open(file_path) as im:
            return np.array(im.getdata()).reshape([im.height, im.width, 3])
            






def export(name, pb, data_dir, out_dir, out_node="softmax_linear/softmax:0"):
    classifier = Classifier(pb, out_node)

    meta_file = os.path.join(data_dir, 'meta.json')
    if not tf.gfile.Exists(meta_file):
        raise ValueError('meta.json not found.')

    with open(meta_file) as fp:
        meta_data = json.load(fp)

    for label in meta_data:
        map_file = os.path.join(out_dir, '{}_{}.txt'.format(name, label))
        print('Map File: {}'.format(map_file))

        with open(map_file, 'wb') as fp:
            for dir_name in meta_data[label]:        
                image_dir = os.path.join(data_dir, dir_name)
                for (path, dir, files) in os.walk(image_dir):
                    for filename in files:
                        ext = os.path.splitext(filename)[-1]
                        if ext in IMAGE_FILE_EXTS:
                            file_path = os.path.join(image_dir, path, filename)

                            name = os.path.splitext(filename)[0]
                            features = classifier.regression(file_path)
                            pickle.dump([name, dir_name, features], fp)