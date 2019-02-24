import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"

import numpy as np
from tensorflow.keras.utils import Sequence
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, RepeatVector, CuDNNGRU

BATCH_SIZE = 64
DIM_A = 50
DIM_B = 26

class MySequence(Sequence):
    def __len__(self):
        return 200

    def __getitem__(self, idx):
        sample = np.zeros((BATCH_SIZE, DIM_A, DIM_B), dtype=np.float32)
        return sample, sample

def getModel():
    inputs = Input(shape=(DIM_A, DIM_B))

    encoded = CuDNNGRU(DIM_B*30, return_sequences=True)(inputs)
    encoded = CuDNNGRU(DIM_B*30, return_sequences=True)(encoded)
    encoded = CuDNNGRU(1000)(encoded)

    decoded = RepeatVector(DIM_A)(encoded)
    decoded = CuDNNGRU(DIM_B*30, return_sequences=True)(decoded)
    decoded = CuDNNGRU(DIM_B*30, return_sequences=True)(decoded)
    decoded = CuDNNGRU(DIM_B, return_sequences=True)(decoded)

    model = Model(inputs, decoded)
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


if __name__ == '__main__':
    train_sequence = MySequence()

    model = getModel()

    model.fit_generator(
        train_sequence,
        len(train_sequence),
        epochs=100,
        verbose=1,
        workers=4,
        use_multiprocessing=True)

