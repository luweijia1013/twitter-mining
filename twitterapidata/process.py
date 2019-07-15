import matplotlib.pyplot as plot
import pandas as pd
import collections
from datetime import datetime
from scipy.stats import pearsonr

def normalization(lists):
    res = []
    for values in lists:
        normal_values = []
        for value in values:
            value = (value-min(values))/(max(values)-min(values))
            normal_values.append(value)
        res.append(normal_values)
    return res

def readSensorData(filename, startrow, rowranges):
    path = 'data/sensordata/'+ filename
    sheet = pd.read_csv(path)
    rows = sheet.values.tolist()
    res = []
    for rowrange in rowranges:
        for row in rowrange:
            row += startrow
            # easy process for missing data
            if rows[row][3] != rows[row][3]:
                # nan
                if row-1-startrow in rowrange and row+1-startrow in rowrange and rows[row-1][3]==rows[row-1][3] and rows[row+1][3]==rows[row+1][3]:
                    res.append((rows[row-1][3] + rows[row+1][3]) / 2)
                else:
                    res.append(-1)
            else:
                res.append(rows[row][3])
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
        if data1[i] < 0 or data2[i] < 0:
            del data1[i]
            del data2[i]
    # print(len(data1),len(data2),len(dates))
    correlation, pvalue = pearsonr(data1, data2)
    print(correlation, pvalue)
    plot.show()


if __name__ == '__main__':
    datas = ['THESIS_air quality_20190626_1704','THESIS_air quality_20190613_1711','THESIS_air quality_20190714_1543']
    lines = []
    for data in datas:
        with open('data/' + data, 'r') as f:
            lines.extend(f.readlines())
            # print(len(lines))
    nums = {}
    for line in lines:
        words = line.split(' ')
        date = '06-' if words[1] == 'Jun' else '07-'
        date += str(words[2])
        if date in nums:
            nums[date] += 1
        else:
            nums[date] = 0
    nums = sorted(nums.items(), key = lambda x:x[0])
    nums = nums[:-1]
    values = [t[1] for t in nums]
    print(nums)
    # Westminster - Marylebone Road FDMS
    # PM10 MY7
    values_sensors1 = readSensorData('LaqnData_pm10.csv', 43, [range(2,13),range(15,26),range(34,43)])
    # NO2 WM6
    values_sensors2 = readSensorData('LaqnData_no2.csv', 0, [range(2,13),range(15,26),range(34,43)])
    values_sensors = values_sensors2#[(values_sensors1[i] + values_sensors2[i])/2 for i in range(min(len(values_sensors1), len(values_sensors2)))]
    # values_sensors = [15.2,17.5,12.8,8.5,9.4,6.9,7.7,5.7,6.3,6.8,10,8.7,7.7,7,9,11,13.6,9.3,7.9,8.3,18.7,23.7,15.8]
    # for i in range(max(nums.keys()), min(nums.keys()), -1):
    #     if i not in nums:
    #        del values_sensors[i-min(nums.keys())]
    # values,values_sensors = normalization([values,values_sensors])
    time_delay = 0
    values_sensors = values_sensors[time_delay:]
    compareDatesCurve([t[0]+'-2019' for t in nums], values, 'Number of tweets', values_sensors, 'Sensor Value(ug/m3)', 'Correlation of NO2(WM6) value and tweets number')
