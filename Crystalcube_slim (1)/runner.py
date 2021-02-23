from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import tensorflow as tf
from tensorflow.python.tools import freeze_graph
from tensorflow.python.tools import optimize_for_inference_lib

import train
import eval
import export
import inference
import classification
import map
from datasets import dataset_utils
from datasets import convert_tf_record
import os
import pickle
import json
import importlib





FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('mode', None, 'The Mode { train | eval | create_dataset | export | inference | classify | map_export }')
tf.app.flags.DEFINE_string('ckpt', None, 'The directory where checkpoint file exists.')
tf.app.flags.DEFINE_string('network', None, 'The file name of neural network for training.')
tf.app.flags.DEFINE_string('dataset_name', None, 'The name of the dataset prefix.')
tf.app.flags.DEFINE_string('dataset_dir', None, 'A directory containing a set of subdirectories representing class names. Eache subdirectory should contain PNG or JPG encoded images.')
tf.app.flags.DEFINE_integer('image_size', None, 'Data Image size(width == height).')
tf.app.flags.DEFINE_integer('batch_size', 32, 'Batch Size.')
#tf.app.flags.DEFINE_integer('max_steps', 30000, 'Max Steps for training. DEFAULT=30000')
tf.app.flags.DEFINE_integer('max_epoch', 60, 'Max Epoch for training. DEFAULT=60')
tf.app.flags.DEFINE_float('learning_rate', 0.001, 'Learning rate. DEFAULT = 0.001')
tf.app.flags.DEFINE_float('learning_rate_decay', 0.96, 'learning_rate_decay_factor. DEFAULT = 0.96')
tf.app.flags.DEFINE_integer('num_epochs_befor_learning_decay', 4, 'number_epoches per decay. DEFAULT = 4')
tf.app.flags.DEFINE_boolean('grayscale', True, 'Make input images to grayscale. DEFAULT=True')
tf.app.flags.DEFINE_boolean('continue_train', True, 'Continue training if previous checkpoints. DEFAULT=True')
tf.app.flags.DEFINE_float('crop_ratio', 1.05, 'Padding Size Ratio to random cropping. DEFAULT = 1.05')

tf.app.flags.DEFINE_integer('num_shards', 5, 'A number of sharding for TFRecord files(integer).')
tf.app.flags.DEFINE_float('ratio_eval', 0.2, 'A ratio of evaluation datasets for TFRecord files(float, 0 ~ 1).')
tf.app.flags.DEFINE_float('keep_prob', 0.7, 'Drop out rate(float, 0 ~ 1).')
tf.app.flags.DEFINE_boolean('log_feature', False, 'Summary Feature Images. DEFAULT=False')


tf.app.flags.DEFINE_string('pb', None, 'The file path of binary graph file.')
tf.app.flags.DEFINE_string('data_dir', None, 'The directory where has inference image files.')
tf.app.flags.DEFINE_string('out_dir', None, 'The directory where some files will be saved.')
tf.app.flags.DEFINE_string('out_node', None, 'The name of out node.')
tf.app.flags.DEFINE_string('name', None, 'The prefix name of map file.')
tf.app.flags.DEFINE_string('image', None, 'The image file for inference.')




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def saveFlagsToFile(file_name="flags.txt"):
    with open(os.path.join(FLAGS.ckpt, file_name), "w") as text_file:
        flags = FLAGS.__dict__['__wrapped'].__dict__['__flags']
        dict_obj = dict([ (key, flags[key].__dict__['_value']) for key in flags.keys()])

        flags = json.dumps(dict_obj)
        text_file.write(flags)



def loadFlagsFromFile(names, file_name="flags.txt"):
    with open(os.path.join(FLAGS.ckpt, file_name), "r") as text_file:
        txt = text_file.read()
        dict_obj = json.loads(txt)

    
        for name in names:
            setattr(FLAGS, name, dict_obj[name])




###########################################################
# TRAIN
###########################################################
def run_train():
    if not FLAGS.ckpt:
        raise ValueError('You must supply the ckpt with --ckpt')

    if not FLAGS.network:
        raise ValueError('You must supply the network with --network')

    if not FLAGS.dataset_dir:
        raise ValueError('You must supply the dataset_dir with --dataset_dir')

    if not FLAGS.dataset_name:
        raise ValueError('You must supply the dataset_name with --dataset_name')

    if not FLAGS.network:
        raise ValueError('You must supply the network with --network')

    if not FLAGS.image_size:
        raise ValueError('You must supply the size of image with --image_size')


    if not FLAGS.continue_train:
        if tf.gfile.Exists(FLAGS.ckpt):
            tf.gfile.DeleteRecursively(FLAGS.ckpt)

    if not tf.gfile.Exists(FLAGS.ckpt):
        tf.gfile.MakeDirs(FLAGS.ckpt)
    
    if not tf.gfile.Exists(FLAGS.dataset_dir):
        raise ValueError('dataset_dir: %s not exists' % (FLAGS.dataset_dir))


    if not dataset_utils.has_labels(FLAGS.dataset_dir):
        raise ValueError('labels file not exists in %s.' % (FLAGS.dataset_dir))



    num_classes = len(dataset_utils.read_label_file(FLAGS.dataset_dir).keys())


    # Print Summary
    print(bcolors.HEADER + "+++++++++++++++++++++++++++++++++++" + bcolors.ENDC)
    print((bcolors.OKGREEN + "Num Classes: %d" + bcolors.ENDC) % num_classes)
    input_image_size = int(float(FLAGS.image_size) * FLAGS.crop_ratio)
    print((bcolors.OKGREEN + "Image Size: %d x %d" + bcolors.ENDC) % (input_image_size, input_image_size))
    print((bcolors.OKGREEN + "Image CROPPED Size: %d x %d" + bcolors.ENDC) % (FLAGS.image_size, FLAGS.image_size))
    print((bcolors.OKGREEN + "Use Grayscale: %s" + bcolors.ENDC) % str(FLAGS.grayscale))
    print((bcolors.OKGREEN + "Learning Rate: %f" + bcolors.ENDC) % FLAGS.learning_rate)
    print((bcolors.OKGREEN + "Learning Rate Decay: %f" + bcolors.ENDC) % FLAGS.learning_rate_decay)
    print((bcolors.OKGREEN + "Num Epochs Per Learning Rate Decay: %d" + bcolors.ENDC) % FLAGS.num_epochs_befor_learning_decay)
    print(bcolors.HEADER + "+++++++++++++++++++++++++++++++++++" + bcolors.ENDC)

    saveFlagsToFile()


    network = importlib.import_module("networks.%s" % FLAGS.network)
    train.train(FLAGS.dataset_dir, FLAGS.dataset_name, num_classes, FLAGS.ckpt, network, FLAGS.image_size, FLAGS.image_size, FLAGS.batch_size, FLAGS.max_epoch, FLAGS.keep_prob, FLAGS.learning_rate, FLAGS.learning_rate_decay, FLAGS.num_epochs_befor_learning_decay, FLAGS.grayscale, FLAGS.crop_ratio, FLAGS.log_feature)





###########################################################
# EVAL
###########################################################
def run_eval():
    if not FLAGS.ckpt:
        raise ValueError('You must supply the ckpt with --ckpt')

    if not tf.gfile.Exists(FLAGS.ckpt):
        raise ValueError('checkpoint: %s not exists' % (FLAGS.ckpt))

    loadFlagsFromFile(['dataset_dir', 'dataset_name', 'network', 'image_size', 'grayscale'])

    num_classes = len(dataset_utils.read_label_file(FLAGS.dataset_dir).keys())

    network = importlib.import_module("networks.%s" % FLAGS.network)
    eval.eval(FLAGS.dataset_dir, FLAGS.dataset_name, num_classes, FLAGS.ckpt, network, FLAGS.image_size, FLAGS.image_size, FLAGS.grayscale, 64, FLAGS.log_feature)






###########################################################
# CREATE DATASET
###########################################################
def run_create_dataset():
    if not FLAGS.dataset_dir:
        raise ValueError('You must supply the datsaet directory with --dataset_dir')

    if not FLAGS.dataset_name:
        raise ValueError('You must supply the dataset name with --dataset_name')


    # Print Summary
    print(bcolors.HEADER + "+++++++++++++++++++++++++++++++++++" + bcolors.ENDC)
    print((bcolors.OKGREEN + "DataSet Dir: %s" + bcolors.ENDC) % FLAGS.dataset_dir)
    print((bcolors.OKGREEN + "DataSet Name: %s" + bcolors.ENDC) % FLAGS.dataset_name)
    print((bcolors.OKGREEN + "Num of Shards: %d" + bcolors.ENDC) % FLAGS.num_shards)
    print((bcolors.OKGREEN + "Eval Ratio: %0.2f" + bcolors.ENDC) % FLAGS.ratio_eval)
    print(bcolors.HEADER + "+++++++++++++++++++++++++++++++++++" + bcolors.ENDC)

    convert_tf_record.run(FLAGS.dataset_name, FLAGS.dataset_dir, FLAGS.num_shards, FLAGS.ratio_eval)




###########################################################
# EXPORT
###########################################################
def run_export():
    if not FLAGS.ckpt:
        raise ValueError('You must supply the ckpt with --ckpt')

    if not tf.gfile.Exists(FLAGS.ckpt):
        raise ValueError('Checkpoint: %s not exists' % (FLAGS.ckpt))


    loadFlagsFromFile(['network', 'dataset_dir', 'image_size', 'grayscale'])
    num_classes = len(dataset_utils.read_label_file(FLAGS.dataset_dir).keys())

    network = importlib.import_module("networks.%s" % FLAGS.network)
    export.export(FLAGS.ckpt, network, num_classes, FLAGS.image_size, FLAGS.image_size, FLAGS.grayscale)







###########################################################
# INFERENCE
###########################################################
def run_inference_with_pb():
    if not FLAGS.pb:
        raise ValueError('You must supply the pb with --pb')

    if not tf.gfile.Exists(FLAGS.pb):
        raise ValueError('PB not found. Please export checkpoint(ckpt) to pb and try again.')



    if FLAGS.data_dir:
        if not tf.gfile.Exists(FLAGS.data_dir):
            raise ValueError('{} not exists.'.format(FLAGS.data_dir))

    if FLAGS.image:
        if not tf.gfile.Exists(FLAGS.image):
            raise ValueError('{} not exists.'.format(FLAGS.data_dir))


    if FLAGS.data_dir:
        inference.infer_with_dataset(FLAGS.pb, FLAGS.data_dir)
    elif FLAGS.image:
        inference.infer_with_image(FLAGS.pb, FLAGS.image)

    print("Finished Successfully.")






###########################################################
# CLASSIFICATION
###########################################################
def run_classify():
    if not FLAGS.pb:
        raise ValueError('You must supply the pb with --pb')

    if not tf.gfile.Exists(FLAGS.pb):
        raise ValueError('PB not found. Please export checkpoint(ckpt) to pb and try again.')


    if FLAGS.data_dir:
        if not tf.gfile.Exists(FLAGS.data_dir):
            raise ValueError('{} not exists.'.format(FLAGS.data_dir))

    if not FLAGS.out_dir:
        raise ValueError('{} not exists.'.format(FLAGS.data_dir))

    if tf.gfile.Exists(FLAGS.out_dir):
        raise ValueError('{} exists.'.format(FLAGS.out_dir))
    
    tf.gfile.MakeDirs(FLAGS.out_dir)


    classification.classify(FLAGS.pb, FLAGS.data_dir, FLAGS.out_dir)

    print("Finished Successfully.")






###########################################################
# MAP EXPORT
###########################################################
def run_map_export():
    if not FLAGS.pb:
        raise ValueError('You must supply the pb with --pb')

    if not tf.gfile.Exists(FLAGS.pb):
        raise ValueError('PB not found. Please export checkpoint(ckpt) to pb and try again.')

    if not FLAGS.data_dir:
        raise ValueError('{} not exists.'.format(FLAGS.data_dir))

    if not tf.gfile.Exists(FLAGS.out_dir):
        tf.gfile.MakeDirs(FLAGS.out_dir)


    if not FLAGS.out_node:
        raise ValueError('You must supply the out node name with --out_node')


    if not FLAGS.name:
        raise ValueError('You must supply the prefix of map with --out_node that will be created.')
    

    map.export(FLAGS.name, FLAGS.pb, FLAGS.data_dir, FLAGS.out_dir, FLAGS.out_node)




def main(argv=None):
    if not FLAGS.mode:
        raise ValueError('You must supply the mode with --mode')

    if FLAGS.mode == 'train':
        run_train()
    elif FLAGS.mode == 'eval':
        run_eval()
    elif FLAGS.mode == 'create_dataset':
        run_create_dataset()
    elif FLAGS.mode == 'export':
        run_export()
    elif FLAGS.mode == 'inference':
        run_inference_with_pb()
    elif FLAGS.mode == 'classify':
        run_classify()
    elif FLAGS.mode == 'map_export':
        run_map_export()
    else:
        raise ValueError('Invalid mode.')





if __name__ == '__main__':
    tf.app.run()