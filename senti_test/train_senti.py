from fastText import load_model,train_supervised
from bs4 import BeautifulSoup
import re
import nltk
import csv
import numpy as np



def parseSample(input, output):
    with open(output, 'w') as wf:
        with open(input,'r') as rf:
            for line in rf.readlines():
                # line.replace('RT','')
                reg = re.compile(r'\d')
                line = reg.sub("",line, 19)
                line = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", line).split())
                line = ' '.join(re.sub("(\w+:\/\/\S+)", " ", line).split())
                wf.write(line)
                wf.write('\n')


def tweet_cleaning_for_sentiment_analysis(tweet):
    # Escaping HTML characters
    tweet = BeautifulSoup(tweet).get_text()

    # Special case not handled previously.
    tweet = tweet.replace('\x92', "'")

    # Removal of hastags/account
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet).split())

    # Removal of address
    tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())

    # Removal of Punctuation
    tweet = ' '.join(re.sub("[\.\,\!\?\:\;\-\=]", " ", tweet).split())

    # Lower case
    tweet = tweet.lower()

    # CONTRACTIONS source: https://en.wikipedia.org/wiki/Contraction_%28grammar%29

    # Standardizing words

    # Deal with emoticons source: https://en.wikipedia.org/wiki/List_of_emoticons

    # Deal with emojis

    tweet = tweet.replace(":", " ")
    tweet = ' '.join(tweet.split())

    return tweet

def transform_instance(row):
    cur_row = []
    #Prefix the index-ed label with __label__
    label = "__label__" + row[4]
    cur_row.append(label)
    cur_row.extend(nltk.word_tokenize(tweet_cleaning_for_sentiment_analysis(row[2].lower())))
    return cur_row


def preprocess(input_file, output_file, keep=1):
    i=0
    with open(output_file, 'w') as csvoutfile:
        csv_writer = csv.writer(csvoutfile, delimiter=' ', lineterminator='\n')
        with open(input_file, 'r', newline='', encoding='latin1') as csvinfile: #,encoding='latin1'
            csv_reader = csv.reader(csvinfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                if row[4]!="MIXED" and row[4].upper() in ['POSITIVE','NEGATIVE','NEUTRAL'] and row[2]!='':
                    row_output = transform_instance(row)
                    csv_writer.writerow(row_output )
                    # print(row_output)
                i=i+1
                if i%10000 ==0:
                    print(i)


def upsampling(input_file, output_file, ratio_upsampling=1):
    # Create a file with equal number of tweets for each label
    #    input_file: path to file
    #    output_file: path to the output file
    #    ratio_upsampling: ratio of each minority classes vs majority one. 1 mean there will be as much of each class than there is for the majority class

    i = 0
    counts = {}
    dict_data_by_label = {}

    # GET LABEL LIST AND GET DATA PER LABEL
    with open(input_file, 'r', newline='') as csvinfile:
        csv_reader = csv.reader(csvinfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            counts[row[0].split()[0]] = counts.get(row[0].split()[0], 0) + 1
            if not row[0].split()[0] in dict_data_by_label:
                dict_data_by_label[row[0].split()[0]] = [row[0]]
            else:
                dict_data_by_label[row[0].split()[0]].append(row[0])
            i = i + 1
            if i % 10000 == 0:
                print("read" + str(i))

    # FIND MAJORITY CLASS
    majority_class = ""
    count_majority_class = 0
    for item in dict_data_by_label:
        if len(dict_data_by_label[item]) > count_majority_class:
            majority_class = item
            count_majority_class = len(dict_data_by_label[item])

            # UPSAMPLE MINORITY CLASS
    data_upsampled = []
    for item in dict_data_by_label:
        data_upsampled.extend(dict_data_by_label[item])
        if item != majority_class:
            items_added = 0
            items_to_add = count_majority_class - len(dict_data_by_label[item])
            while items_added < items_to_add:
                data_upsampled.extend(
                    dict_data_by_label[item][:max(0, min(items_to_add - items_added, len(dict_data_by_label[item])))])
                items_added = items_added + max(0, min(items_to_add - items_added, len(dict_data_by_label[item])))

    # WRITE ALL
    i = 0

    with open(output_file, 'w') as txtoutfile:
        for row in data_upsampled:
            txtoutfile.write(row + '\n')
            i = i + 1
            if i % 10000 == 0:
                print("writer" + str(i))

if __name__=="__main__":
    ## PREPROCESSING
    # preprocess('betsentiment-EN-tweets-sentiment-teams.csv','a')
    # preprocess('betsentiment-EN-tweets-sentiment-worldcup.csv','b')
    # preprocess('betsentiment-EN-tweets-sentiment-players.csv','c')

    # num = 200
    # i = 0
    # with open('a','r') as rf:
    #     with open('a'+str(num),'w') as wf:
    #         lines = rf.readlines()
    #         for line in lines:
    #             wf.write(line)
    #             i = i+1
    #             if i % 100000 == 0:
    #                 print("writer" + str(i))
    #             if i > num * 1000:
    #                 break

    # upsampling('a'+str(num),'upa'+str(num))
    # upsampling('b','upb')
    upsampling('datatest','upc')


    ##TRAINING
    # hyper_params = {"lr": 0.01,
    #                 "epoch": 20,
    #                 "wordNgrams": 2,
    #                 "dim": 20}
    model = train_supervised(input = 'upc')
    model_acc_training_set = model.test('upc')
    model_acc_validation_set = model.test('upa')

    # DISPLAY ACCURACY OF TRAINED MODEL
    text_line = "accuracy:" + str(model_acc_training_set[1]) + ", validation:" + str(
        model_acc_validation_set[1]) + '\n'
    print(text_line)
    model.save_model('tmodel_25000_self')

