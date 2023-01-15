# Multilingual chatbot based on Deep Learning, NLP and WebScrapping using Tkinter
All in one chatbot using Tkinter that allows the user to play sudoku, find his or her horoscope, get jokes, definitions, weather for a specific city, and answer various questions.
This Chatbot intends to be a direct competitor to ChatGPT.

## Introduction

This project is a Chatbot using Deep Learning, NLP, Webscrapping through Selenium and the DeepL API to propose to the user various services : 

- tell a joke
- tell the weather of a city
- tell the horoscope from a specific sign
- answer to a random interaction, 
- play sudoku

![Screen Shot 2023-01-15 at 14 58 23](https://user-images.githubusercontent.com/90907966/212545065-b8d36b55-b485-4f69-84bb-8dc38b410460.png)

## How does it work

Two training data in French and English have been written in intents_fr.json and intents_en.json
Thus, two neural networks of the same structure have been trained, based on a Bag Of Words model. 
Their respective weights are stored into data_fr.pth and data_uk.pth. 

For the whole procedure, we have to distinguish 3 cases according to the language : 

1. If the user picks French (#TeamBaguette) : 
  - the model used is the one trained on the french training data
  - No need to translate the results of web scrapping
  - No need to translate the answers generated thanks to the deep learning model

![Screen Shot 2023-01-15 at 16 03 46](https://user-images.githubusercontent.com/90907966/212548984-3d5910f3-8d2f-4258-a311-d18f3e2ff8bc.png)

2. If the user picks English : 
  - the model used is the one trained on the english training data
  - We need to translate the results of web scrapping (as the output from websites are in French)
  - No need to translate the answers generated thanks to the deep learning model


3. If the user picks another language : 
  - we need to translate every message into French thanks to the DeepL API
  - the model used is the one trained on the French training data
  - We need to translate the results of web scrapping (as the websites are French)
  - We need to translate back in the user’s language the results of the deep learning model.

*Little joke in Russian. Pretty funny, innit ?*
![Screen Shot 2023-01-15 at 16 07 39](https://user-images.githubusercontent.com/90907966/212549143-d7ae291d-e408-40ea-83dc-1adac660e053.png)

Morevover, we need to store some states, to catch if a message follows another :

1. Either the message is the direct following of a previous message.

*Example:*
![Screen Shot 2023-01-15 at 16 09 49](https://user-images.githubusercontent.com/90907966/212549274-5a26fbf9-e7bf-47c4-9f82-6bdef40eb68a.png)


Here, we store into a state variable is_horoscope = True the fact that the previous question was related to astrology. 

2. Either the message has no link with the previous one , such as “Tell me a joke”. There is no need to change the value of a state variable.

Finally, we distinguish to types of answer : 

- Either the user calls a **functionality** (meteo, joke, horoscope, or definition). This only implies if-else statement and webscrapping.
- Either the user just want to chat, and the answer generated comes from intents_fr.json or intents_en.json

### Sudoku Files

For the sudoku part, I was strongly inspired by [http://newcoder.io/gui/part-1/](http://newcoder.io/gui/part-1/). 
Nonetheless, his version wasn't working perfectly, so I had to add features, comments and some snippets that make the sudoku work. 

## What you need to follow so that everything works fine

1. Run the [train.py](http://train.py) file changing the language variable in it, so that the weights are stored into data_en.pth or data_fr.pth files if those files do not exist. As soon as you add some new training data, you obviously need to re-train the model. 
2. Run the main function, only changing the name of the bot if want (but it works better with "Fabrice", just saying...) 
3. Change all the paths calling the files.

## Librairies to download before running it

**The Neural Network is written with PyTorch, which works only with Python previous than 3.9. I personally worked with this version of Python.** 

- Pytorch for DeepLearning
- DeepL for translation, with a free professional account (API key needed)
- Selenium and downloading a webdriver.
- Unidecode to erase accent (thanks , french…)
- Tkinter for the layout

## Files

The project is organized with the following : 

1. *deep_learning_chatbot* : 
- intents.json is the training data. For each intent, it stores probable questions the user may ask, and store answer that are displayed if the model predict this specific item.
- data.pth is the file where the weights of the trained model are stored.
- [model.py](http://model.py)  : simple NN network, with 2 hidden layers having the same number of neurons, with a ReLU function in between. As we use `CrossEntropyLoss`, we don’t need to one hot encode
- [train.py](http://train.py) : when run, trains the model and stores the results it into data.pth.
- [chat.py](http://chat.py) : functions called when the main function is run , such as getting the weights of the model, predicting the intent, or generating an answer from the model.

2. Content_and_answers.py : 
- [functionnalities.py](http://functionalities.py) : functions that use WebScrapping to get information from the web (jokes, meteo, horoscope and definition), and launches the Sudoku

3. settings:
- settings_layout.py : settings for the layout of tkinter

4. translation : 
- translation_deepl.py : contains the function that call the DeepL API

4. src: 
- contains all the previous packages
- [main.py](http://main.py) : file to run to launch the chatbot


## Remarks, comments and amelioration

- The best way to improve the chatbot is to have a **specific training data for each language**. Here, if the language is German , we translate into French and then rely on the French Deep Learning Model.
- The jokes come from a French website. Thus, literally translated, they make no sense if this is a pun in French (which happens 70% of the time with the French humor)
- There is only one function “send” that contains all the even-if clauses. This is kind of heavy, but the reason is that on Tkinter , only one function can be associated to a button on your keyword. As the user only presses “Enter”, I needed to declare everything into this unique function.
- For the language, we use the keyword “english” as argument in the NLP functions, and ‘en’ for DeepL.

## Sources

- [https://www.youtube.com/watch?v=RpWeNzfSUHw](https://www.youtube.com/watch?v=RpWeNzfSUHw)
- http://newcoder.io/gui/part-1/

… and of course ChatGPT for specific helping questions.
