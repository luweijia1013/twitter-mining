import matplotlib.pyplot as plot
from scipy.stats import pearsonr

def normalization(values):
    normal_values = []
    for value in values:
        value = (value-min(values))/(max(values)-min(values))
        normal_values.append(value)
    return normal_values

def compareDatesCurve(dates, data1, name1, data2, name2):
    # print(dates)
    if len(data1) > len(data2):# more tweets data than sensor data
        dates = dates[:len(data2)]
        data1 = data1[:len(data2)]
    if len(data2) > len(data1):# more sensor data than tweets data
        # shouldn't occur
        dates = dates[:len(data1)]
        data2 = data2[:len(data1)]
        print('ERROR, MORE SENSOR DATA THAN TWEETS DATA')
    # print(len(data1),len(data2),len(dates))
    plot.plot(dates, values_01, color="r", linestyle="--", marker="*", linewidth=1.0, label=name1)
    plot.plot(dates, values_sensors_01, color="b", linestyle="--", marker="o", linewidth=1.0, label=name2)
    plot.show()

if __name__ == '__main__':
    datas = ['THESIS_air quality_20190626_1704','THESIS_air quality_20190613_1711']
    lines = []
    for data in datas:
        with open('data/' + data, 'r') as f:
            lines.extend(f.readlines())
            # print(len(lines))
    nums = {}
    for line in lines:
        words = line.split(' ')
        if int(words[2]) in nums:
            nums[int(words[2])] += 1
        else:
            nums[int(words[2])] = 0
    sorted(nums.items(), key = lambda x:x[0])
    for i in range(min(nums.keys()), max(nums.keys())):
        if i not in nums:
            nums[i] = -1
    # del(nums[13])
    values = nums.values()
    values_01 = normalization(values)
    print(nums)
    # #Westminster - Marylebone Road FDMS
    values_sensors = [15.2,17.5,12.8,8.5,9.4,6.9,7.7,5.7,6.3,6.8,10,8.7,7,7,7,9,11,13.6,9.3,7.9,8.3,18.7,23.7,15.8]
    values_sensors_01 = normalization(values_sensors)
    compareDatesCurve(list(nums.keys()), values_01, 'Number of tweets', values_sensors_01, 'Sensor Value')
    correlation, pvalue = pearsonr(values_01, values_sensors_01)
    print(correlation, pvalue)
