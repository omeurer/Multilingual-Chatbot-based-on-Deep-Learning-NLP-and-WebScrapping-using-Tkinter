import numpy as np
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltk_utils import bag_of_words, tokenize, stem, delete_accent
from model import NeuralNet

#VARIABLE TO CHANGE
language = "fr"  # to know which model should be trained, and to store the good weights

#CALLING THE RIGHT TRAINING DATA FILE
if language == "fr":
    FILE = "data_fr.pth"
    with open('intents_fr.json', 'r') as f:
        intents = json.load(f)

else:
    FILE = "data_en.pth"
    with open('intents_en.json', 'r') as f:
        intents = json.load(f)


#BUILDING THE TRAIN SET
all_words = []
tags = []
xy = []  # will hold every word and its tag

for intent in intents['intents']:  # looping over a list of intents
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = delete_accent(pattern)
        w = tokenize(w)  # list of tokenized patterns
        all_words.extend(w)  # w is an array, so we don't put append but extend
        xy.append((w, tag))  # list of tuples

# stem and lower each word
ignore_words = ["?", "!", ".", ","]

all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = [delete_accent(w) for w in all_words]
all_words = sorted(set(all_words))  # set takes unique words
tags = sorted(set(tags))  # It is not necessary but just in case. Set takes unique words.

# create training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)


#HYPERPARAMETERS
X_train = np.array(X_train)
y_train = np.array(y_train)
# Hyper-parameters
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)


# This is how we create our Dataset
class ChatDataset(Dataset):
    # must inherit Dataset, and overwrite __getitem__, __len__
    # allows to do gradient descent by calculating gradients

    def __init__(self):
        # data loading
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # dataset[idx]
    def __getitem__(self, index):
        # allows to do data[0]
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        # allows len(dataset)
        return self.n_samples


dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

print(f'final loss: {loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
