import matplotlib.pyplot as plot
import pandas as pd
import collections
from datetime import datetime
from scipy.stats import pearsonr
from fastText import load_model,train_supervised
import re


def normalization(lists):
    res = []
    for values in lists:
        normal_values = []
        for value in values:
            value = (value-min(values))/(max(values)-min(values))
            normal_values.append(value)
        res.append(normal_values)
    return res

def readSensorData(filename, startrows, rowranges, multiplestations):
    if not multiplestations and len(startrows) != 1:
        print('ERROR OF MULTISTATIONS')
        return []
    path = 'data/sensordata/'+ filename
    sheet = pd.read_csv(path)
    rows = sheet.values.tolist()
    res = []
    if multiplestations:
        startrows = [0]
        tempsite = rows[0][0]
        for i,row in enumerate(rows):
            if row[0] != tempsite:
                tempsite = row[0]
                startrows.append(i)
    for rowrange in rowranges:
        for row in rowrange:
            s_values = [rows[row+start][3] for start in startrows if rows[row+start][3] == rows[row+start][3]]
            print(s_values)# !!!!! which can be used to illustrate the importance of multistaion on missing data
            # easy process for missing data
            if not s_values:
                # nan for all stations
                res.append(float('-inf'))
            else:
                res.append(sum(s_values)/len(s_values))
    for i in range(len(res)):
        if res[i] == float('-inf') and i in range(1, len(res) - 1) and res[i - 1] != float('-inf') and res[i + 1] != float('-inf'):
            res[i] = (res[i - 1] + res[i + 1]) / 2
    return res



def compareDatesCurve(dates, data1, name1, data2, name2, title):
    dates = [datetime.strptime(d, '%m-%d-%Y').date() for d in dates]
    print(len(dates),len(data1),len(data2))
    if len(data1) > len(data2):# more tweets data than sensor data
        dates = dates[:len(data2)]
        data1 = data1[:len(data2)]
    if len(data2) > len(data1):# more sensor data than tweets data
        # shouldn't occur
        dates = dates[:len(data1)]
        data2 = data2[:len(data1)]
        print('ERROR, MORE SENSOR DATA THAN TWEETS DATA')
    print(len(data1),len(data2),len(dates))
    print(data1,data2,dates)
    ax1 = plot.figure().add_subplot(111)
    ax1.plot(dates, data1, color="r", linestyle="--", marker="*", linewidth=1.0, label=name1)
    ax1.set_ylabel(name1)
    ax1.legend(loc=1)
    ax1.set_title(title)
    ax2 = ax1.twinx()
    ax2.plot(dates, data2, color="b", linestyle="--", marker="o", linewidth=1.0, label=name2)
    ax2.set_ylabel(name2)
    ax2.legend(loc=2)
    for i in range(len(data1)):
        if data1[i] == float('-inf') or data2[i] == float('-inf'):
            print('!!! DELETE')
            del data1[i]
            del data2[i]
    # print(len(data1),len(data2),len(dates))
    correlation, pvalue = pearsonr(data1, data2)
    print(correlation, pvalue)
    plot.show()

def parseTweets(input):
    result = []
    for line in input:
        line = line.replace('RT','')
        # reg = re.compile(r'\d')
        # line = reg.sub("",line, 19)
        line = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", line).split())
        line = ' '.join(re.sub("(\w+:\/\/\S+)", " ", line).split())
        result.append(line)
    return result


def sentiAnalysis(classifier, tweets):
    pred = classifier.predict(parseTweets(tweets), 3)
    probs = pred[len(pred) - 1]
    labels = pred[0]
    results = []
    for i in range(len(labels)):
        label = labels[i]
        prob = probs[i]
        result = (1 * prob[label.index('__label__NEGATIVE')] + 2 * prob[label.index('__label__NEUTRAL')] + 3 * prob[
            label.index('__label__POSITIVE')])
        result = result - 2
        results.append(result)
    return sum(results)/len(results)


if __name__ == '__main__':
    datas = ['THESIS_air quality_20190626_1704','THESIS_air quality_20190613_1711','THESIS_air quality_20190714_1543','THESIS_air quality_20190725_1731']
    lines = []
    for data in datas:
        with open('data/' + data, 'r') as f:
            lines.extend(f.readlines())
            # print(len(lines))

    nums = {}
    sentis = {}
    classifier = load_model("../senti_test/model/tmodel2")
    for line in lines:
        words = line.split(' ')
        date = '06-' if words[1] == 'Jun' else '07-'
        date += str(words[2])
        if date in nums:
            nums[date] += 1
            sentis[date] += sentiAnalysis(classifier, [line[37:]])
        else:
            nums[date] = 0
            sentis[date] = 0
    nums = sorted(nums.items(), key = lambda x:x[0])
    nums = nums[:-1]
    sentis = sorted(sentis.items(), key = lambda x:x[0])
    sentis = sentis[:-1]
    print(nums)
    print(sentis)
    # values = [t[1] for t in nums]
    values = [t[1] for t in sentis]
    # Westminster - Marylebone Road FDMS
    # PM10 MY7
    values_sensors1 = readSensorData('LaqnData_pm10.csv', [43], [range(2,13),range(15,26),range(34,43)], False)
    # NO2 WM6
    values_sensors2 = readSensorData('LaqnData_no2_westminster.csv', [0], [range(2,13),range(15,26),range(34,44), range(45,54)], True)
    values_sensors = values_sensors2#[(values_sensors1[i] + values_sensors2[i])/2 for i in range(min(len(values_sensors1), len(values_sensors2)))]
    # for i in range(max(nums.keys()), min(nums.keys()), -1):
    #     if i not in nums:
    #        del values_sensors[i-min(nums.keys())]
    # values,values_sensors = normalization([values,values_sensors
    print(values_sensors)
    time_delay = 0
    values_sensors = values_sensors[time_delay:]
    compareDatesCurve([t[0]+'-2019' for t in nums], values, 'Number of tweets', values_sensors, 'Sensor Value(ug/m3)', 'Correlation of NO2(multiple) value and tweets number')
