import tensorflow as tf
import tensorflow.contrib.slim as slim
from datasets import dataset_utils
from datasets import tf_record_dataset

import os
import math

tf.logging.set_verbosity(tf.logging.INFO)


def eval(dataset_dir, dataset_name, num_classes, log_dir, network, width, height, use_grayscale, batch_size=32, log_images=False):
    tfrecord_dataset = tf_record_dataset.TFRecordDataset(
        tfrecord_dir=dataset_dir,
        dataset_name=dataset_name,
        num_classes=num_classes)

    dataset = tfrecord_dataset.get_split(split_name='eval')
    images, labels, filenames, num_samples = dataset_utils.load_batch(dataset, batch_size=batch_size, height=height, width=width, num_classes=num_classes, is_training=False, do_scaling=True, use_grayscale=use_grayscale, use_standardization=True, use_color_distortion=False, use_crop_distortion=False, crop_ratio=1.0)


    predictions = network.network(images, num_classes=num_classes, keep_prob=1.0, is_training=False, log_images=log_images)

    predictions = tf.argmax(predictions, 1)
    labels = tf.argmax(labels, 1)


    names_to_values, names_to_updates = slim.metrics.aggregate_metric_map({
        'eval/Accuracy': slim.metrics.streaming_accuracy(predictions, labels),
    })



    eval_dir = os.path.join(log_dir, 'eval')

    if not tf.gfile.Exists(log_dir):
        raise Exception("Trained check point does not exists at %s " % log_dir)
    else:
        checkpoint_path = tf.train.latest_checkpoint(log_dir)

    if not tf.gfile.Exists(eval_dir):
        tf.gfile.MakeDirs(eval_dir)


    num_batches = math.ceil(num_samples / float(batch_size))
    metric_values = slim.evaluation.evaluate_once(
        master='',
        checkpoint_path=checkpoint_path,
        logdir=eval_dir,
        num_evals=num_batches,
        eval_op=names_to_updates.values(),
        final_op=names_to_values.values())

    names_to_values = dict(zip(names_to_values.keys(), metric_values))
    for name in names_to_values:
        print('%s: %f' % (name, names_to_values[name]))
