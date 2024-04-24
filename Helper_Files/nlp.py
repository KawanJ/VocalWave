import nltk
from nltk import *
import pandas as pd
import regex as re

STOPWORDS = nltk.corpus.stopwords.words('english')
COMMANDS = ['play', 'start', 'pause', 'like', 'shuffle', 'mix', 'random', 'liked', 'next', 'previous', 'rewind', 'repeat', 'stop', 'increase', 'decrease'] 

#data = pd.read_csv(r'C:\Users\Admin\Desktop\Major Project\Final Project\VocalWave\Sentences.csv')

def make_lowercase(input_string): #string input
    lowercase = input_string.lower()
    return lowercase

def sanitize(input_string): #string input
    modified_string = re.sub("[,.!@#$%^&*]", '', input_string)
    modified_string = re.sub('[0-9]', '', modified_string)
    return modified_string
       
def tokenize_string(input_string): 
    return nltk.word_tokenize(input_string)

def remove_stopwords(input_tokens):
    tokens_without_stopwords = []
    for word in input_tokens:
        if word not in STOPWORDS:
            tokens_without_stopwords.append(word)
    return tokens_without_stopwords   

def matched_keyword(input_tokens):
    for word in input_tokens:
        if word in ('stop', 'pause'):
            return 'stop'
        elif word == 'next':
            return 'next'
        elif word == 'previous':
            return 'previous'
        elif word in ('play', 'start'):
            return 'play'
        elif word in ('like', 'liked'):
            return 'like'
        elif word in ('shuffle', 'mix', 'random'):
            return 'shuffle'
        elif word in ('repeat', 'rewind'):
            return 'repeat'
        elif word == 'increase':
            return 'increase'
        elif word == 'decrease':
            return 'decrease'
    return "No command found"


def sentence_to_keyword(sentence):
    lowercase_sentence = make_lowercase(sentence)
    sanitized_sentence = sanitize(lowercase_sentence)
    tokens = tokenize_string(sanitized_sentence)
    tokens_without_stopwords = remove_stopwords(tokens)
    keyword = matched_keyword(tokens_without_stopwords)
    return keyword

def clean_command(command):
    return sanitize(make_lowercase(command)[1:])

