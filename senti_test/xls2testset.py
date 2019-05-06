import xlrd
import re

def parseTweet(line):
    line = line.replace('RT','')
    # reg = re.compile(r'\d')
    # line = reg.sub("",line, 19)
    # line = ' '.join(re.sub("(RT [A-Za-z0-9]+)|(#[A-Za-z0-9]+:)", " ", line).split())
    line = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", line).split())
    line = ' '.join(re.sub("(\w+:\/\/\S+)", " ", line).split())
    return line

with open('testset','a') as f:
    with xlrd.open_workbook('sample-tweets2.xlsx') as wb:
        ws = wb.sheet_by_index(0)
        for i in range(ws.nrows):
            row = ws.row_values(i)
            text = row[1]
            label = row[2]
            if label == 1:
                f.write('__label__NEGATIVE ')
            if label == 2:
                f.write('__label__NEUTRAL ')
            if label == 3:
                f.write('__label__POSITIVE ')
            f.write(parseTweet(text))
            f.write('\n')

