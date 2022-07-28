import random
import json
import torch

from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('bot_model/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = 'bot_model/data.pth'

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

class BotResponse():

    def __init__(self, tag: str, message: str) -> None:
        self.tag = tag
        self.message = message

    def get_tag(self):
        return self.tag

    def get_message(self):
        return self.message

def bot_response(sentence: str):
    tokenized_sentence = tokenize(sentence)
    X = bag_of_words(tokenized_sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                result = BotResponse(tag, random.choice(intent['responses']))
                return result
    else:
        result = BotResponse("reject", "I do not understand ...")
        return result