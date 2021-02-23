import tensorflow as tf
import tensorflow.contrib.slim as slim
from datasets import dataset_utils
from datasets import tf_record_dataset

from tensorflow.python.tools import freeze_graph
from tensorflow.python.tools import optimize_for_inference_lib

import os

tf.logging.set_verbosity(tf.logging.INFO)



def export(log_dir, network, num_classes, image_height, image_width, use_grayscale):
    output_dir = os.path.join(log_dir, "export")
    if tf.gfile.Exists(output_dir) == True:
        tf.gfile.DeleteRecursively(output_dir)
    tf.gfile.MakeDirs(output_dir)


    with tf.Graph().as_default() as g:
        with tf.device("/cpu:0"):
            image = tf.placeholder(tf.float32, shape=(None, None, 3), name="image")

        image = dataset_utils.load_image(image, image_height, image_width, True, True, use_grayscale)
        checkpoint_path = tf.train.latest_checkpoint(log_dir)

        predictions = network.network(image, num_classes=num_classes, keep_prob=1.0, is_training=False, log_images=False)
        predictions = tf.cast(predictions, tf.float32)
        softmax = tf.nn.softmax(predictions, name='softmax_linear/softmax')

        #variable_averages = tf.train.ExponentialMovingAverage(1.0)
        #variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver()

        with tf.Session() as sess:
            saver.restore(sess, checkpoint_path)

            #global_step = tf.contrib.framework.get_or_create_global_step()
            #global_step=tf.convert_to_tensor(global_step)
            tf.train.Saver().save(sess, os.path.join(output_dir, 'model.ckpt'))
            tf.train.write_graph(sess.graph.as_graph_def(), output_dir, 'graph.pbtxt', as_text=True)



    ### EXPORT MODEL ###
    graph_path = os.path.join(output_dir, 'graph.pbtxt')
    if tf.gfile.Exists(graph_path) == False:
        raise ValueError('Graph not found({})'.format(graph_path))

    ckpt = tf.train.get_checkpoint_state(output_dir)
    ckpt_path = checkpoint_path

    if ckpt == False or ckpt_path == False:
        raise ValueError('Check point not found.')


    output_path = os.path.join(output_dir, 'frozen.pb')
    optimized_output_path = os.path.join(output_dir, 'optimized.pb')

    freeze_graph.freeze_graph(input_graph = graph_path,  input_saver = "",
             input_binary = False, input_checkpoint = ckpt_path, output_node_names = "softmax_linear/softmax",
             restore_op_name = "save/restore_all", filename_tensor_name = "save/Const:0",
             output_graph = output_path, clear_devices = True, initializer_nodes = "")

  
    input_graph_def = tf.GraphDef()
    with tf.gfile.Open(output_path, "r") as f:
        data = f.read()
        input_graph_def.ParseFromString(data)

    output_graph_def = optimize_for_inference_lib.optimize_for_inference(
            input_graph_def,
            ['image'], 
            ["softmax_linear/softmax"],
            tf.float32.as_datatype_enum)

    f = tf.gfile.FastGFile(optimized_output_path, "wb")
    f.write(output_graph_def.SerializeToString())

    output_size = os.path.getsize(output_path)
    optimized_output_size = os.path.getsize(optimized_output_path)

    print('Model Exported successfuly.')
    print('- Frozen Model: {} ({})'.format(output_path, _humansize(output_size)))
    print('- Optimized Model: {} ({})'.format(optimized_output_path, _humansize(optimized_output_size)))





def _humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
