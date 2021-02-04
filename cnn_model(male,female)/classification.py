import tensorflow as tf
import tensorflow.contrib.slim as slim
from datasets import dataset_utils
from datasets import tf_record_dataset

import os
import numpy as np
from PIL import Image
import sys
from shutil import copyfile


IMAGE_FILE_EXTS = ['.jpg', '.jpeg']



def classify(pb, data_dir, out_dir):
    with tf.Graph().as_default() as g:
        with tf.Session() as new_sess:
            with tf.gfile.FastGFile(pb, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')
            
            softmax = new_sess.graph.get_tensor_by_name("softmax_linear/softmax:0")

            # Loading the injected placeholder
            input_placeholder = new_sess.graph.get_tensor_by_name("image:0")

            cnt = 0
            for (path, dir, files) in os.walk(data_dir):
                for filename in files:
                    ext = os.path.splitext(filename)[-1]
                    file_name = os.path.splitext(filename)[0]

                    if ext in IMAGE_FILE_EXTS:
                        file_path = os.path.join(data_dir, path, filename)
                        
                        with Image.open(file_path) as im:
                            try:
                                image_data = np.array(im.getdata()).reshape([im.height, im.width, 3])
                                result = new_sess.run(softmax, {input_placeholder: image_data})[0]

                                result = list(result)
                                idx = result.index(max(result))
                                dest_dir = os.path.join(out_dir, str(idx))
                                if tf.gfile.Exists(dest_dir) == False:
                                    tf.gfile.MakeDirs(dest_dir)

                                print("[{}] {} : {}".format(cnt, filename, idx))
                                cnt += 1
                                copyfile(file_path, os.path.join(dest_dir, "{}{}".format(file_name, ext)))
                            except:
                                print('error')