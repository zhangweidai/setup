from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np


#x = np.random.uniform(0.0, 1.0, (20))
#print (x)
#print (np.expand_dims(x[:3],0))
#print (np.expand_dims(x[:3],4))
#print (np.expand_dims(x,3))
#
#raise SystemExit
# input and output
x = np.random.uniform(0.0, 1.0, (20))
y = np.random.uniform(0.0, 1.0, (20))
y = 0.3 + 0.6*x + np.random.normal(0.0, 0.05, len(y))

import tensorflow as tf
print (tf.shape(x))
print (tf.shape(y))

#raise SystemExit

# A simple regression model
model = Sequential()
model.add(Dense(1, input_shape=(1,)))
model.compile(loss='mse', optimizer='rmsprop')

## The fit() method - trains the model
model.fit(x, y, nb_epoch=100, batch_size=100)

#print (x)
#print (y)
# The evaluate() method - gets the loss statistics
#print (model.evaluate(x, y, batch_size=200))
# loss: 0.0022612824104726315
print (np.expand_dims(x[:3],1))

## The predict() method - predict the outputs for the given inputs
#print (model.predict(np.expand_dims(x[:3],1)))
print (model.predict([.2]))

#print (model.predict(x))
##    returns:[ 0.65680361],[ 0.70067143],[ 0.70482892]
