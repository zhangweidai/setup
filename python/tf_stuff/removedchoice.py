import numpy as np
import random
import pandas as pd
import tensorflow as tf
# input and output
#x = np.random.uniform(0.0, 1.0, (200))
#y = np.random.uniform(0.0, 1.0, (200))
x = [i for i in range (20000)]
y = [i for i in range (20000)]

for i,b in enumerate(x):
    temp = [i for i in range(10)]
    removed = random.choice(temp)
    value = temp.pop(removed)
    random.shuffle(temp)
    x[i] = temp
    y[i] = [0 for i in range(10)]
    y[i][removed] = 1
#    temp
#    x[i] = 
npx = np.asarray(x, dtype=np.float32)
npy = np.asarray(y, dtype=np.float32)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow import keras
#y = 0.3 + 0.6*x + np.random.normal(0.0, 0.05, len(y))

# A simple regression model
model = Sequential()
model.add(Dense(10, input_shape=(9,)))
#model.add(Dense(1))
model.add(Dense(16,  kernel_regularizer=keras.regularizers.l2(0.0001), activation=tf.nn.relu))
model.add(Dropout(.5))

model.add(Dense(10, activation=tf.nn.sigmoid))
#model.compile(loss='mse', optimizer=tf.train.AdamOptimizer())
model.compile(optimizer='adam',
                       loss='binary_crossentropy',
                       metrics=['accuracy', 'binary_crossentropy'])

#model.compile(loss='mse', optimizer='rmsprop')

## The fit() method - trains the model
history  = model.fit(npx, npy, nb_epoch=100, batch_size=200)

import matplotlib.pyplot as plt
def plot_histories(histories, key='binary_crossentropy'):
    plt.figure(figsize=(16,10))
    
    for name, history in histories:
        print ("list(history)")
        print (list(pd.DataFrame(history.history)))
        val = plt.plot(history.epoch, history.history[key],
                   '--', label=key)
        val = plt.plot(history.epoch, history.history["loss"],
                   '--', label="loss")
        val = plt.plot(history.epoch, history.history["acc"],
                   '--', label="acc")
#        plt.plot(history.epoch, history.history[key], color=val[0].get_color(),
#             label=name.title()+' Train')

    plt.xlabel('Epochs')
    plt.ylabel(key.replace('_',' ').title())
    plt.legend()

    plt.xlim([0,max(history.epoch)])
    plt.show()


plot_histories([('baseline', history)])

def plot_history(history):
    hist = pd.DataFrame(history.history)
#    return
    hist['epoch'] = history.epoch
    
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['loss'], label='Train Error')
    plt.plot(hist['epoch'], hist['acc'], label='Accuracy')
    plt.plot(hist['epoch'], hist['binary_crossentropy'], label='bct')
#    plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
#             label = 'Val Error')
#    plt.ylim([0,5])
#    plt.legend()
#    
#    plt.figure()
#    plt.xlabel('Epoch')
#    plt.ylabel('Mean Square Error [$MPG^2$]')
#    plt.plot(hist['epoch'], hist['mean_squared_error'],
#             label='Train Error')
#    plt.plot(hist['epoch'], hist['val_mean_squared_error'],
#             label = 'Val Error')
#    plt.ylim([0,20])
#    plt.legend()
    plt.show()


#plot_history(history)



#print (x)
#print (y)
# The evaluate() method - gets the loss statistics
#print (model.evaluate(npx,npy, batch_size=200))
# loss: 0.0022612824104726315
#print (np.expand_dims(x[:3],1))
sample = [[0,1,2,3,4,6,7,8,9]]
predicted = model.predict(np.asarray(sample, dtype=np.float32)).tolist()[0]
print (predicted.index(max(predicted)))

## The predict() method - predict the outputs for the given inputs
sample = [[2,6,1,3,9,8,0,4,7]]
predicted = model.predict(np.asarray(sample, dtype=np.float32)).tolist()[0]
print (predicted)
print (predicted.index(max(predicted)))
#            np.expand_dims(x[:3],1)))
##    returns:[ 0.65680361],[ 0.70067143],[ 0.70482892]
