import numpy as np
import pandas as pd
import os
class DataRefiner:

    def __init__(self, _index, isCheck, isSetting):
        if isCheck:
            f = open('D:\\data\\idkeys.txt', 'r')

            line = f.read()
            lines = line.split('#')

            numClass = 0
            id_name = []

            for j in range(len(lines)):
                TK = lines[j].split(',')
                numClass += (len(lines[j].split(',')) - 1)
                for i in range(len(TK)):
                    id_name.append(TK[i])

            index = ['_1.txt', '_02', '_10', '_11', '_12', '_13', '_14', '_15']

            sum = np.zeros(shape=[1000], dtype='f')

            lines = []

            for i in index:
                path = 'D:\\data\\' + i
                f = open(path, 'r')
                lines = f.readlines()

                for a in range(len(lines)):
                    try:
                        sum[a] += float(lines[a])
                    except:
                        0

            for i in range(len(lines)):
                print(id_name[i], ':', sum[i])
            input()
            for q in range(50):
                if q > 0:
                    sum[mi] = 120
                    sum[ma] = 120

                max = -9999
                ma = -1
                min = 9999
                mi = -1

                for a in range(len(lines)):
                    if sum[a] > max:
                        max = sum[a]
                        ma = a
                    if sum[a] < min and sum[a] > 150:
                        min = sum[a]
                        mi = a

                print(sum[ma], sum[mi])
                print(id_name[ma], id_name[mi])

        if isSetting:
            dict_name = ['대동로', '중앙대로', '양운로', '전포대로', '장림로', '충렬대로',
                         '용수로', '부곡로', '만덕대로', '낙동북로', '수영로', '녹산산업중로', '읍내로', '광복로']
            id_name = ["" for x in range(len(dict_name))]

            path = 'D:\\data\\20140327_lnklinks.xls'
            #path of link file

            usage_Excel = pd.read_excel(path)
            for j in range(len(usage_Excel.KORNAME)):
                for i in range(len(dict_name)):
                    if usage_Excel.KORNAME[j] == dict_name[i]:
                        print(usage_Excel.KORNAME[j], usage_Excel.ID[j])
                        id_name[i] += str(usage_Excel.ID[j]) + ','

            f = open('D:\\data\\idkeys.txt', 'w')

            for i in range(len(id_name)):
                f.write(id_name[i] + '#')

            f.close()

        f = open('D:\\data\\idkeys.txt', 'r')

        line = f.read()
        lines = line.split('#')

        numClass = 0
        id_name = []

        for j in range(len(lines)):
            TK = lines[j].split(',')
            numClass += (len(lines[j].split(',')) - 1)
            for i in range(len(TK)):
                id_name.append(TK[i])

        print(len(lines))

        counts = np.zeros(shape=[numClass], dtype='i')
        sum = np.zeros(shape=[numClass], dtype='f')

        folderpath1 = 'D:\\data\\8'

        folderpath2 = 'D:\\data\\11'

        traffic_data = np.zeros(shape=[numClass, 8928], dtype='f')

        filepath = 'D:\\data\\11\\Gugan1Traffic_201411' + _index + '_1.txt'
        print(filepath)
        print(counts)

        txt = open(filepath, 'r')
        lines = txt.readlines()

        for i in range(len(lines)):
            TK = lines[i].split(',')

            for k in range(numClass):
                if TK[1] == id_name[k]:
                    # print(TK[0], counts)
                    sum[k] += float(TK[3])
                    traffic_data[k, counts[k]] = float(TK[3])
                    counts[k] += 1

        txt.close()

        save_path = 'D:\\data\\save_traffic' + _index
        save_file = open(save_path, 'w')

        line = ''
        for i in range(numClass):
            line += str(counts[i]) + ','

        save_file.write(line + '@')

        for i in range(288):
            line = ''

            for j in range(numClass):
                line += str(traffic_data[j, i]) + ','

            save_file.write(line + '#')

        save_file.close()

        avg_file = open('D:\\data\\_' + _index, 'w')

        for j in range(numClass):
            print(sum[j] / float(counts[j]))
            avg_file.write(str((sum[j] / float(counts[j]))) + '\n')
        avg_file.close()