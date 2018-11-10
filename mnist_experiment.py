import numpy as np
import pickle
import random
import time

from mlp.mlp import MLPClassifier
#from mlp.dataloader import DataLoader

np.random.seed(0)

MNIST_DATA_PATH = './data/mnist/normalized_data.pkl'

class Dataloader:

    def __init__(self, inputs, targets, batch_size):
        self._data_size = len(targets)
        self._batch_size = batch_size
        self._inputs = [input for input in inputs.reshape(self._data_size, 784)]
        self._targets = [target for target in targets]
        self._n_batch = self._data_size // self._batch_size + 1
        self._dataloader = self._split_in_batch()

    def __len__(self):
        return self._n_batch

    def __getitem__(self, i):
        return self._dataloader[i]

    def _get_next_input_batch(self, last=False):
        last_idx = self._batch_size if not last else len(self._inputs)
        cur_batch = np.array([self._inputs.pop(0) for _ in range(last_idx)])
        return cur_batch

    def _get_next_target_batch(self, last=False):
        last_idx = self._batch_size if not last else len(self._targets)
        cur_batch = np.array([self._targets.pop(0) for _ in range(last_idx)])
        return cur_batch

    def _split_in_batch(self):
        storage = {'inputs': [], 'targets': []}
        for i in range(self._n_batch-1):
            storage['inputs'].append(self._get_next_input_batch())
            storage['targets'].append(self._get_next_target_batch())
        if not len(self._inputs) == 0:
            storage['inputs'].append(self._get_next_input_batch(last=True))
            storage['targets'].append(self._get_next_target_batch(last=True)) 
        return list(zip(storage['inputs'], storage['targets']))
    
    def data_size_(self):
        return self._data_size

if __name__ == '__main__':

    INPUT_DIM = 784
    OUTPUT_DIM = 10

    # hyperparameters
    HIDDEN_DIM = 50
    BATCH_SIZE = 128
    NUM_EPOCHS = 1
    LEARNING_RATE = 0.01

    with open(MNIST_DATA_PATH, 'rb') as f:
        data = pickle.load(f)

    trainloader = Dataloader(data['train_x'], data['train_y'], batch_size=BATCH_SIZE)
    devloader = Dataloader(data['valid_x'], data['valid_y'], batch_size=1000)
    testloader = Dataloader(data['test_x'], data['test_y'], batch_size=1000)

    mlp = MLPClassifier(
        input_size=INPUT_DIM, 
        hidden_size=HIDDEN_DIM, 
        output_size=OUTPUT_DIM, 
        learning_rate=LEARNING_RATE, 
        num_epochs=NUM_EPOCHS
    )

    mlp.train(trainloader, devloader, crazy_loop=True)