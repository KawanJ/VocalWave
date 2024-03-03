import nltk
from nltk import *
import pandas as pd
import regex as re

STOPWORDS = nltk.corpus.stopwords.words('english')
COMMANDS = ['play', 'pause', 'like', 'shuffle', 'mix', 'random', 'liked', 'next', 'previous', 'rewind', 'repeat', 'stop']

#data = pd.read_csv(r'C:\Users\Admin\Desktop\Major Project\Final Project\VocalWave\Sentences.csv')

def make_lowercase(input_data): #string input
    lowercase = input_data.str.lower()
    return lowercase

def regex(input_data): #string input
    modified_data = re.sub("[,.!@#$%^&*]", '', input_data)
    modified_data = re.sub('[0-9]', '', modified_data)
    return modified_data
       
def tokenize_words(input_data): 
    return nltk.word_tokenize(input_data)

def remove_stopwords(input_data):
    without_stopwords = []
    for word in input_data:
        if word not in STOPWORDS:
            without_stopwords.append(word)
    return without_stopwords   

def matched_keyword(input_data):
    matched = []
    for word in input_data:
        if word in COMMANDS:
            matched.append(word)  
    
    if (matched == []):
        return "No commands found"
    if ('stop' or 'pause' in matched):
        return 'stop'
    if ('like' in matched):
        return 'like'
    if ('next' in matched):
        return 'next'
    if ('previous' in matched):
        return 'previous'
    
    return "No command found"

def sentence_to_keyword(sentence):
    lowercase_sentence = make_lowercase(sentence)
    remove_extras = regex(lowercase_sentence)
    tokens = tokenize_words(remove_extras)
    no_stopwords = remove_stopwords(tokens)
    keyword = matched_keyword(no_stopwords)
    return keyword

def clean_command(command):
    return regex(make_lowercase(command))

