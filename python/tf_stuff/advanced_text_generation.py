#
# https://github.com/tensorflow/docs/blob/master/site/en/tutorials/sequences/text_generation.ipynb
from __future__ import absolute_import, division, print_function

import tensorflow as tf
print (tf.__version__)

tf.enable_eager_execution()

import numpy as np
import os
import time


path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
vocab = sorted(set(text))

# Creating a mapping from unique characters to indices
char2idx = {u:i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)


def generate_text(model, start_string):
    # Evaluation step (generating text using the learned model)

    # Number of characters to generate
    num_generate = 1000

    # Converting our start string to numbers (vectorizing) 
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = 1.0

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a multinomial distribution to predict the word returned by the model
        predictions = predictions / temperature
        predicted_id = tf.multinomial(predictions, num_samples=1)[-1,0].numpy()
        
        # We pass the predicted word as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)
        
        text_generated.append(idx2char[predicted_id])
    return (start_string + ''.join(text_generated))


# Recreate the exact same model, including weights and optimizer.
#new_model = tf.keras.models.load_model('mine.h5')
#new_model = tf.keras.models.load_model('mine.h5')
#new_model.summary()

# Number of RNN units
rnn_units = 1024
embedding_dim = 256
BATCH_SIZE = 64
vocab_size = len(vocab)

if tf.test.is_gpu_available():
    rnn = tf.keras.layers.CuDNNGRU
else:
    import functools
    rnn = functools.partial(tf.keras.layers.GRU, recurrent_activation='sigmoid')

def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([

        tf.keras.layers.Embedding(vocab_size, embedding_dim, 
            batch_input_shape=[batch_size, None]),

	rnn(rnn_units, return_sequences=True, 
            recurrent_initializer='glorot_uniform',
	    stateful=True),

        tf.keras.layers.Dense(vocab_size)])
    return model


# Advanced: Customized Training 

model = build_model(vocab_size = len(vocab), 
   embedding_dim=embedding_dim, 
   rnn_units=rnn_units, 
   batch_size=BATCH_SIZE)
#
optimizer = tf.train.AdamOptimizer()
#
## Training step
#

seq_length = 100
text_as_int = np.array([char2idx[c] for c in text])
char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)
sequences = char_dataset.batch(seq_length+1, drop_remainder=True)

def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

dataset = sequences.map(split_input_target)

for epoch in range(10):
    start = time.time()
    
    # initializing the hidden state at the start of every epoch
    # initally hidden is None
    hidden = model.reset_states()
    
    for (batch_n, (inp, target)) in enumerate(dataset):
        with tf.GradientTape() as tape:
            # feeding the hidden state back into the model
            # This is the interesting step
            predictions = model(inp)
            loss = tf.losses.sparse_softmax_cross_entropy(target, predictions)
              
        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if batch_n % 100 == 0:
            template = 'Epoch {} Batch {} Loss {:.4f}'
            print(template.format(epoch+1, batch_n, loss))

    # saving (checkpoint) the model every 5 epochs
#    if (epoch + 1) % 5 == 0:
#        new_model.save_weights(checkpoint_prefix.format(epoch=epoch))

#    print ('Epoch {} Loss {:.4f}'.format(epoch+1, loss))
#    print ('Time taken for 1 epoch {} sec\n'.format(time.time() - start))

tf.keras.models.save_model(model, 'mine2.h5')
print(generate_text(model, start_string=u"ROMEO: "))
#model.save_weights(checkpoint_prefix.format(epoch=epoch))
