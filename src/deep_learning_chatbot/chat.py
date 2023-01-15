import random
import json
import torch
from src.deep_learning_chatbot.model import NeuralNet  # to use when we only run main.py
from src.deep_learning_chatbot.nltk_utils import bag_of_words, tokenize  # to use when we only run main.py

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Uses GPU if available

def get_model_infos(language):

    """Function that get the right path for the file with the weights, and the right "intent" file
    according to the language selected by the user.
    Parameters
    ----------
    language : string
                        language to call the right trained model
    Returns
    -------
    intents : dict_like
            Content of the intents__.json file

    model_info_path : str
                    right path of the model state
    """

    base_path = "/src/deep_learning_chatbot/"

    if language == "en":
        model_info_path = base_path + "data_en.pth"
        intents_path = base_path + "intents_en.json"

    else:
        model_info_path = base_path + "data_fr.pth"
        intents_path = base_path + "intents_fr.json"

    with open(intents_path,'r') as json_data:
        intents = json.load(json_data)

    return intents, model_info_path

def get_intent(sentence, language):
    """
    Function that takes the sentence of the user, and returns the most probable tag.

    Parameters
    ----------
    sentence : str
            Sentence from the user to analyze

    language = 'french' : string
                language to call the right trained model
    Returns
    -------
    tag : str
        return the tag associated to the sentence, or 'error' if the probability is under 75%

    """
    _, FILE = get_model_infos(language)
    print(FILE)
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    sentence = tokenize(sentence, language)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]  # predicted.item() is a integer

    if prob.item() > 0.75:
        return tag
    else:
        return "error"


def get_deep_bot_answer(tag, language):
    """Function that takes a tag as an input and returns randomly one of the answers of the intents file.

    Parameters
    ----------
    tag : str
        tag that need to be present in the training data

    language = 'french' : string
                language to call the right informations

    Returns
    -------
    str
        One of the answers randomly chose , according to the tag
    """
    intents, _ = get_model_infos(language)
    for intent in intents['intents']:
        if tag == intent["tag"]:
            return f"{random.choice(intent['responses'])}"
