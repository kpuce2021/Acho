import tensorflow as tf
import tensorflow.contrib.slim as slim
from datasets import dataset_utils
from datasets import tf_record_dataset

import os
import numpy as np
from PIL import Image
from datetime import datetime
import sys


IMAGE_FILE_EXTS = ['.jpg', '.jpeg']



def infer_with_dataset(pb, data_dir):
    with tf.Graph().as_default() as g:
        with tf.Session() as new_sess:
            with tf.gfile.FastGFile(pb, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')


            softmax = new_sess.graph.get_tensor_by_name("softmax_linear/softmax:0")

            input_placeholder = new_sess.graph.get_tensor_by_name("image:0")

            cnt = 0
            errors = 0
            for(path, dir, files) in os.walk(data_dir):
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
                                basename = os.path.basename(path)
                                label = int(basename)

                                result_str = " : ".join("{:05f}".format(i) for i in result)

                                if idx != label:
                                    errors += 1
                                    print("\r+ {} Errors - [{:5d}] {}/{:20s} : {} =? {}     [{}]".format(errors, cnt, basename, filename, label, idx, result_str))

                                sys.stdout.write("\r[{:5d}] {}/{:20s} : {} =? {}\t[{}]".format(cnt, basename, filename, label, idx, result_str))
                                sys.stdout.flush()

                                cnt += 1
                            except Exception as e:
                                print(str(e))
                                print('error')

            precision = 1.0 - (errors / cnt)
            print('%s: precision @ 1 = %.3f' % (datetime.now(), precision))




def infer_with_image(pb, image):
    with tf.Graph().as_default() as g:
        with tf.Session() as new_sess:
            with tf.gfile.FastGFile(pb, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')


            softmax = new_sess.graph.get_tensor_by_name("softmax_linear/softmax:0")
            input_placeholder = new_sess.graph.get_tensor_by_name("image:0")
            file_path = image

            with Image.open(file_path) as im:
                try:
                    image_data = np.array(im.getdata()).reshape([im.height, im.width, 3])
                    result = new_sess.run(softmax, {input_placeholder: image_data})[0]

                    result = list(result)
                    idx = result.index(max(result))
                    
                    print("Inferece Result: Class # \t{}".format(idx, result))

                except Exception as e:
                    print(str(e))
                    print('error')



            precision = 1.0 - (errors / cnt)
            print('\n\n%s: precision @ 1 = %.3f (%d/%d)' % (datetime.now(), precision, (1-errors), cnt))