import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

#wholeSequence = [[0,0,0,0,0,0,0,0,0,2,1],
#                 [0,0,0,0,0,0,0,0,2,1,0],
#                 [0,0,0,0,0,0,0,2,1,0,0],
#                 [0,0,0,0,0,0,2,1,0,0,0],
#                 [0,0,0,0,0,2,1,0,0,0,0],
#                 [0,0,0,0,2,1,0,0,0,0,0],
#                 [0,0,0,2,1,0,0,0,0,0,0],
#                 [0,0,2,1,0,0,0,0,0,0,0],
#                 [0,2,1,0,0,0,0,0,0,0,0],
#                 [2,1,0,0,0,0,0,0,0,0,0]]
#
## Input sequence
#data = [[0,0,0,0,0,0,0,0,0,2,1],
#        [0,0,0,0,0,0,0,0,2,1,0],
#        [0,0,0,0,0,0,0,2,1,0,0],
#        [0,0,0,0,0,0,2,1,0,0,0],
#        [0,0,0,0,0,2,1,0,0,0,0],
#        [0,0,0,0,2,1,0,0,0,0,0],
#        [0,0,0,2,1,0,0,0,0,0,0],
#        [0,0,2,1,0,0,0,0,0,0,0],
#        [0,2,1,0,0,0,0,0,0,0,0]]
#
#target = [[0,0,0,0,0,0,0,0,2,1,0],
#          [0,0,0,0,0,0,0,2,1,0,0],
#          [0,0,0,0,0,0,2,1,0,0,0],
#          [0,0,0,0,0,2,1,0,0,0,0],
#          [0,0,0,0,2,1,0,0,0,0,0],
#          [0,0,0,2,1,0,0,0,0,0,0],
#          [0,0,2,1,0,0,0,0,0,0,0],
#          [0,2,1,0,0,0,0,0,0,0,0],
#          [2,1,0,0,0,0,0,0,0,0,0]]
#
### Preprocess Data:
#data = np.array(data, dtype=np.float32) # Convert to NP array.
#target = np.array(target, dtype=np.float32) # Convert to NP array.
#
#wholeSequence = np.array(wholeSequence, dtype=np.float32) # Convert to NP array.
#data = wholeSequence[:-1] # all but last
#target = wholeSequence[1:] # all but first

model = None
#data = wholeSequence[:-1] # all but last
#target = wholeSequence[1:] # all but first
def train(data, target = None):
    global model
    width = (len(data[0]))
    height = (len(data))

    data = np.array(data, dtype=np.float32)
    data = data.reshape((1, height, width))

    if not target is None:
        target = np.array(target, dtype=np.float32)
        target = target.reshape((1, height, width))

    # Build Model
    if model == None:
        model = Sequential()
        model.add(LSTM(width, input_shape=(height, width), 
                    unroll=True, return_sequences=True))
        model.add(LSTM(1024, return_sequences=True))
        model.add(Dense(width))
        model.compile(loss='mean_absolute_error', optimizer='adam')

    if not target is None:
        model.fit(data, target, nb_epoch=220, batch_size=1, verbose=2)
    else:
        predictions = model.predict(data)
        return np.rint(np.absolute(predictions))

    return None
#    model.summary()

#data = [
#    [0,1,0,1,0,1], [0,0,1,1,0,0], [0,0,1,1,0,0], [0,0,1,1,0,0],
#    [0,0,1,1,0,0], [0,0,1,1,0,0], [0,1,1,0,0,0], [0,0,1,1,0,0],
#    [0,1,1,0,0,0], [0,1,1,0,0,0], [0,1,1,0,0,0], [0,0,1,1,0,0]]
#
#target = [
#    [0,1,0,1,1,1], [0,1,1,1,0,0], [0,1,1,1,0,0], [0,1,1,1,0,0],
#    [0,0,1,1,0,0], [0,1,1,1,0,1], [0,0,1,1,0,1], [0,1,1,1,0,1],
#    [0,1,1,1,0,1], [0,1,1,1,0,1], [0,0,1,1,0,0], [0,0,1,1,0,0]]
#
#train(data, target)
#train(target, data)
#train(data, target)
#train(target, data)
#print (train(target))
#print (train(data))

