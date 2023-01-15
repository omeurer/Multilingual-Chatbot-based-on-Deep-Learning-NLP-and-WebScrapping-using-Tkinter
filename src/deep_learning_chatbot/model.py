import torch.nn as nn


class NeuralNet(nn.Module):

    """Class to build a NeuralNetwork, with 2 hidden layers and a RELU function in between."""
    # it has to inherit from nn.Module

    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()  # activation function for in between

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation nor softmax. In the cross entropy loss, it will be in it.
        return out
