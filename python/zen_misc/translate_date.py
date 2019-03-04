#
# https://github.com/tensorflow/docs/blob/master/site/en/tutorials/sequences/text_generation.ipynb
from __future__ import absolute_import, division, print_function

import tensorflow as tf
print (tf.__version__)
#tf.enable_eager_execution()

import numpy as np
import os
import time

## Setup
def loss(labels, logits):
    return tf.keras.backend.sparse_categorical_crossentropy(labels, logits, from_logits=True)

def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text


class Trainer():

    def __init__(self):
        pass


    def train(self, path_to_file):
        text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
        vocab = sorted(set(text))

        self.char2idx = {u:i for i, u in enumerate(vocab)}
        print ("self.char2idx")
        print (self.char2idx)
        self.idx2char = np.array(vocab)
        text_as_int = np.array([self.char2idx[c] for c in text])

        seq_length = 100
        examples_per_epoch = len(text)//seq_length
        char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

        sequences = char_dataset.batch(seq_length+1, drop_remainder=True)
        dataset = sequences.map(split_input_target)

        # Batch size 
        BATCH_SIZE = 64
        steps_per_epoch = examples_per_epoch//BATCH_SIZE

        BUFFER_SIZE = 10000
        dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
        print (dataset)
        return

#        rnn_units = 256
        rnn_units = 1024
        embedding_dim = 256

        self.model = self.build_model(vocab_size = len(vocab), 
            embedding_dim=embedding_dim, 
            rnn_units=rnn_units, 
            batch_size=BATCH_SIZE)
        
        self.model.compile(optimizer = tf.train.AdamOptimizer(), loss = loss)

        # Directory where the checkpoints will be saved
        checkpoint_dir = '.\\training_checkpoints'
        # Name of the checkpoint files
        checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")
        
        checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(
                filepath=checkpoint_prefix, save_weights_only=True)
        
        EPOCHS=2
        
        ## Generate Text
        history = self.model.fit(dataset.repeat(), epochs=EPOCHS, 
                steps_per_epoch=steps_per_epoch, callbacks=[checkpoint_callback])
        tf.train.latest_checkpoint(checkpoint_dir)
        
        vocab_size = len(vocab) 
        self.model = self.build_model(vocab_size, embedding_dim, rnn_units, batch_size=1)
        self.model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
        self.model.build(tf.TensorShape([1, None]))


    ## Build The Model
    def build_model(self, vocab_size, embedding_dim, rnn_units, batch_size):
        rnn = None
        if tf.test.is_gpu_available():
            rnn = tf.keras.layers.CuDNNGRU
        else:
            import functools
            rnn = functools.partial(tf.keras.layers.GRU, 
                                    recurrent_activation='sigmoid')
    
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(vocab_size, embedding_dim, 
                    batch_input_shape=[batch_size, None]),
        	rnn(rnn_units, return_sequences=True, 
                    recurrent_initializer='glorot_uniform',
        	    stateful=True),
        	rnn(rnn_units, return_sequences=True, 
                    recurrent_initializer='glorot_uniform',
    	    stateful=True),
            tf.keras.layers.Dense(vocab_size)])
        return model

    def generate_text(self, start_string):
        # Evaluation step (generating text using the learned model)
    
        # Number of characters to generate
        num_generate = 1000
    
        # Converting our start string to numbers (vectorizing) 
        input_eval = [self.char2idx[s] for s in start_string]
        input_eval = tf.expand_dims(input_eval, 0)
    
        # Empty string to store our results
        text_generated = []
    
        # Low temperatures results in more predictable text.
        # Higher temperatures results in more surprising text.
        # Experiment to find the best setting.
        temperature = 1.0
    
        # Here batch size == 1
        self.model.reset_states()
        for i in range(num_generate):
            predictions = self.model(input_eval)
            # remove the batch dimension
            predictions = tf.squeeze(predictions, 0)
    
            # using a multinomial distribution to predict the word returned by the model
            predictions = predictions / temperature
            predicted_id = tf.multinomial(predictions, num_samples=1)[-1,0].numpy()
            
            # We pass the predicted word as the next input to the model
            # along with the previous hidden state
            input_eval = tf.expand_dims([predicted_id], 0)
            
            text_generated.append(self.idx2char[predicted_id])
        return (start_string + ''.join(text_generated))


path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')
print (path_to_file)
trainer = Trainer()
trainer.train(path_to_file)
#print(trainer.generate_text(start_string=u"ROMEO: "))

#tf.keras.models.save_model(
#    model,
#    "mine.h5",
#    overwrite=True,
#    include_optimizer=True)

