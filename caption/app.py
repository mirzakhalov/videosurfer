#!/usr/bin/python
import tensorflow as tf

from config import Config
from model import CaptionGenerator
from dataset import prepare_train_data, prepare_eval_data, prepare_test_data
  
import sys
sys.path.append('../')

import os
import json
import pyrebase

FLAGS = tf.app.flags.FLAGS

tf.flags.DEFINE_string('phase', 'train',
                    'The phase can be train, eval or test')

tf.flags.DEFINE_boolean('load', False,
                        'Turn on to load a pretrained model from either \
                        the latest checkpoint or a specified file')

tf.flags.DEFINE_string('model_file', None,
                    'If sepcified, load a pretrained model from this file')

tf.flags.DEFINE_boolean('load_cnn', False,
                        'Turn on to load a pretrained CNN model')

tf.flags.DEFINE_string('cnn_model_file', './vgg16_no_fc.npy',
                    'The file containing a pretrained CNN model')

tf.flags.DEFINE_boolean('train_cnn', False,
                        'Turn on to train both CNN and RNN. \
                        Otherwise, only RNN is trained')

tf.flags.DEFINE_integer('beam_size', 3,
                        'The size of beam search for caption generation')

tf.flags.DEFINE_string('input_dir', "friends",
                        'The size of beam search for caption generation')
            

config = json.loads(open('secret/config.json').read())

firebase = pyrebase.initialize_app(config)


def main(args):
    
    # # build paths
    db = firebase.database()

    config = Config()
    config.phase = FLAGS.phase
    config.train_cnn = FLAGS.train_cnn
    config.beam_size = FLAGS.beam_size

    input_dir = FLAGS.input_dir
    config.test_image_dir = FLAGS.input_dir
    config.test_result_dir = FLAGS.input_dir + 'results/'
    config.test_result_file = FLAGS.input_dir + 'results/results.csv'

    with tf.Session() as sess:
        data, vocabulary = prepare_test_data(config)
        model = CaptionGenerator(config)
        model.load(sess, FLAGS.model_file)
        tf.get_default_graph().finalize()
        results = model.test(sess, data, vocabulary)
        #print(results)

        for index, row in results.iterrows():
            parts = row['image_files'].split('/')
            frame = parts[-1][:-4]
            db.child(input_dir[3:] + "frames/" + frame + "/caption").set(row['caption'])
        
                               

if __name__ == '__main__':
    tf.app.run()
    
