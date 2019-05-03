from fastText import load_model,train_supervised
from bs4 import BeautifulSoup
import re
import nltk
import csv
import numpy as np


def parseTweets(input):
    result = []
    for line in input:
        line = line.replace('RT :','')
        # reg = re.compile(r'\d')
        # line = reg.sub("",line, 19)
        line = ' '.join(re.sub("(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)", " ", line).split())
        line = ' '.join(re.sub("(\w+:\/\/\S+)", " ", line).split())
        result.append(line)
    return result

def prediction(texts):
    model_name = "tmodel2"
    classifier = load_model(model_name)
    pred = classifier.predict(parseTweets(texts),3)
    probs = pred[len(pred)-1]
    labels = pred[0]
    results = []
    for i in range(len(labels)):
        label = labels[i]
        prob = probs[i]
        result = (1 * prob[label.index('__label__NEGATIVE')] + 2 * prob[label.index('__label__NEUTRAL')] + 3 * prob[label.index('__label__POSITIVE')])
        result = result - 2
        results.append(result)
    return results

if __name__ == "__main__":
    texts = ['liverpool is awesome','liverpool is so great','liverpool is so good',
            'liverpool is a football team',
            'liverpool is worse than chelsea','liverpool is terrible','liverpool is the worst']
    results = prediction(texts)
    print(texts)
    print(results)
