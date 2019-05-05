from fastText import load_model,train_supervised
from bs4 import BeautifulSoup
import re
import nltk
import csv
import numpy as np


def parseTweets(input):
    result = []
    for line in input:
        line.replace('RT','')
        # reg = re.compile(r'\d')
        # line = reg.sub("",line, 19)
        line = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", line).split())
        line = ' '.join(re.sub("(\w+:\/\/\S+)", " ", line).split())
        result.append(line)
    return result

if __name__=="__main__":
    classifier = load_model("model/tmodel2")
    simpletexts = ['nice', 'happy', 'fine', 'great', 'ok', 'sorry', 'sad', 'rip', 'Saturday']
    texts = ['Ugghhh... Not happy at all! sorry', 'I am so sad', 'Happyyyyyyy', 'OH yeah! lets rock.']
    test = ['liverpool is awesome','liverpool is so great','liverpool is so good','liverpool is ok','liverpool is better than chelsea',
            'liverpool is a football team',
            'liverpool is worse than chelsea','liverpool is terrible','liverpool is the worst']

    ##get dataset by prediction of the model
    with open('datatest', 'a') as wf:
        with open('parsed', 'r') as rf:
            for line in rf.readlines():
                line_list = []
                line_list.append(line)
                linep = parseTweets(line_list)
                pred = classifier.predict(linep)
                wf.write(pred[0][0][0])
                wf.write(' ')
                wf.write(linep[0])
                wf.write('\n')


    # pred = classifier.predict(parseTweets(test),3)
    # probs = pred[len(pred)-1]
    # labels = pred[0]
    # results = []
    # for i in range(len(labels)):
    #     label = labels[i]
    #     prob = probs[i]
    #     result = (1 * prob[label.index('__label__NEGATIVE')] + 2 * prob[label.index('__label__NEUTRAL')] + 3 * prob[label.index('__label__POSITIVE')])
    #     result = result - 2
    #     results.append(result)
    #
    # print(results)
