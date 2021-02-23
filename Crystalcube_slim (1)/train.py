import tensorflow as tf
import tensorflow.contrib.slim as slim


from datasets import dataset_utils
from datasets import tf_record_dataset

tf.logging.set_verbosity(tf.logging.INFO)


def train(dataset_dir, dataset_name, num_classes, logdir, network, width, height, batch_size=32, max_epoch=10, keep_prob=0.7, learning_rate=0.001, learning_rate_decay=0.9, num_epochs_befor_learning_decay=2, use_grayscale=True, crop_ratio=1.05, log_images=False):

    if not tf.gfile.Exists(logdir):
        tf.gfile.MakeDirs(logdir)

    tfrecord_dataset = tf_record_dataset.TFRecordDataset(
        tfrecord_dir=dataset_dir,
        dataset_name=dataset_name,
        num_classes=num_classes)


    dataset = tfrecord_dataset.get_split(split_name='train')
    images, labels, filenames, num_samples = dataset_utils.load_batch(dataset, batch_size=batch_size, height=height, width=width, num_classes=num_classes, is_training=True, do_scaling=True, use_grayscale=use_grayscale, use_standardization=True, use_color_distortion=True, use_crop_distortion=True, crop_ratio=crop_ratio)


    logits = network.network(images, num_classes=num_classes, keep_prob=keep_prob, is_training=True, log_images=log_images)

    slim.losses.softmax_cross_entropy(logits=logits, onehot_labels=labels)
    total_loss = slim.losses.get_total_loss()


    ## Dynamic Learning rate
    initial_learning_rate = learning_rate
    learning_rate_decay_factor = learning_rate_decay
    num_epochs_before_decay = num_epochs_befor_learning_decay
     
    global_step = tf.contrib.framework.get_or_create_global_step()
     
    num_batches_per_epoch = num_samples / batch_size
    num_steps_per_epoch = num_batches_per_epoch  # Because one step is one batch processed
    decay_steps = int(num_epochs_before_decay * num_steps_per_epoch)

    assert(decay_steps > 0)

    lr = tf.train.exponential_decay(learning_rate=initial_learning_rate,
                                    global_step=global_step,
                                    decay_steps=decay_steps,
                                    decay_rate=learning_rate_decay_factor,
                                    staircase=True)
    tf.summary.scalar('learning_rate', lr)

    optimizer = network.get_optimizer()(learning_rate=lr)

    ## Summary
    predictions = tf.argmax(logits, 1)
    targets = tf.argmax(labels, 1)
    correct_prediction = tf.equal(predictions, targets)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    
    tf.summary.scalar('losses/Total', total_loss)
    tf.summary.scalar('accuracy', accuracy)
    summary_op = tf.summary.merge_all()


    max_steps = int((num_samples / float(batch_size)) * max_epoch)
    print(("\033[95m" + "+ Max Steps: %d" + "\033[0m") %  max_steps)
    train_op = slim.learning.create_train_op(total_loss, optimizer, global_step=global_step, summarize_gradients=True)
    final_loss = slim.learning.train(train_op, logdir, number_of_steps=max_steps, summary_op=summary_op, save_summaries_secs=30, save_interval_secs=30, log_every_n_steps=100)

    print('Finished training. Final batch loss %f' % final_loss)
