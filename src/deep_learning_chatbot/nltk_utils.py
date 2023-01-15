import numpy as np
import nltk
#nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import unidecode

stemmer = PorterStemmer()


def delete_accent(sentence):
    """Deletes the accent from a word or sentence."""
    return unidecode.unidecode(sentence)


def tokenize(sentence, language="fr"):
    "Tokenizes a sentences."
    if language == 'fr':
        language = 'french' #word_tokenize takes 'french' as argument instead of Deepl which takes 'fr'
    else :
        language = 'english'
    return nltk.word_tokenize(sentence, language=language)


def stem(word, language="fr"):
    """
    stemming = find the root form of the word
    examples:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """

    if language == "fr":
        stemmer = SnowballStemmer("french")
    else:
        stemmer = PorterStemmer()

    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    """

  Returns a bag of words for a tokenized sentence.

  tokenized_sentence : the sentence in which we want to put 1. and 0.
  words : all the words of our dictionary


  sentence = ["hello", "how" ,"are" ,"you"]
  words = ["hi", "hello", "I" ,"you" ,"bye" ,"thank","cool"]
  bog =   "[0.      1.     0.   1.      0.      0.      0.]
  """

    without_accent_sentence = [delete_accent(word) for word in tokenized_sentence]
    tokenized_sentence = [stem(w) for w in without_accent_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag

