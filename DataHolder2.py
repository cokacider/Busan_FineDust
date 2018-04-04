import numpy as np
import math
import os
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats.spearmanr

class Dataholder:

    def pearson(self, x, y):
        n = len(x)
        vals = range(n)

        sumx = sum(float(x[i]) for i in vals)
        sumy = sum(float(y[i]) for i in vals)

        sumxSq = sum(x[i]**2.0 for i in vals)
        sumySq = sum(y[i]**2.0 for i in vals)

        pSum = sum(x[i]*y[i] for i in vals)

        num = pSum - (sumx*sumy/n)
        den = ((sumxSq - pow(sumx, 2)/n)*(sumySq-pow(sumy, 2)/n))** .5
        if den == 0:
            return 0

        r = num/den

        return r

    def __init__(self):
        weather_filepath = 'D:\\freeze_and_burst\\weather.csv'
        pm_filepath = 'D:\\freeze_and_burst\\pm10_hour.csv'
        #읽어올 파일의 위치 지정

        #weather data read
        #parameter list: 강수량 온도 풍속 습도 일조량 전운량 기압

        weather_file = open(weather_filepath, 'r', encoding="utf-8")
        lines = weather_file.readlines()
        #파일의 내용을 줄 단위로 모두 읽어옴
        max = [-999, -999, -999, -999, -999]
        min = [999, 999, 999, 999, 999]

        Count_ = 0

        self.Length = len(lines) - 1
        self.weather_data = np.zeros(shape=[len(lines) - 1, 5], dtype='f')

        self.sequence_length = 0
        self.dim = 0
        self.batch_size = 0

        self.mean_np = np.zeros(shape=[5])

        mean_selected = [0, 0, 0, 0, 0]

        write1 = open('data1', 'w')

        for i in range(len(lines) - 1):
            Count_ += 1

            TK = lines[i + 1].replace('\n', '').split(',')
            #데이터는 모두 쉼표로 구분되어 있기 때문에 ,로 나누어줌

            strline = ''

            for j in range(5):


                try:
                    self.weather_data[i, j] = float(TK[j + 2])
                    self.mean_np[j] += float(TK[j + 2])

                    strline += TK[j + 2] + ','

                    for k in range(5):
                        mean_selected[k] += float(TK[k + 2])
                        if max[k] < float(TK[k + 2]):
                            max[k] = float(TK[k + 2])
                        if min[k] > float(TK[k + 2]):
                            min[k] = float(TK[k + 2])

                except:
                    self.weather_data[i, j] = 0

                    strline += '0' + ','
                    #비어있는 데이터의 경우 0으로 임의로 채워줌

            if i%5 == 0:
                write1.write(strline+'\n')

        write1.close()

        for k in range(5):
            mean_selected[k] = mean_selected[k] / len(lines)
            print(mean_selected[k], max[k], min[k])
        input()

        for j in range(5):
            self.mean_np[j] = self.mean_np[j] / Count_

        pm_file = open(pm_filepath, "r", encoding="utf-8")

        lines = pm_file.readlines()

        self.pm_data = np.zeros(shape=[self.Length, 2], dtype='f')

        count = len(lines) - 1
        #미세먼지 데이터의 경우 가장 최근 데이터부터 이전 데이터의 방향으로 기록되어 있으므로 다음과 같이 처리함

        length = self.Length

        j = 0

        for i in range(len(lines) - 1):
            TK = lines[i + 1].replace('\n', '').replace('\"', '').split(',')

            try:
                self.pm_data[i, 0] = float(TK[2])
            except:
                print(TK)
                self.pm_data[i, 0] = self.pm_data[i - 1, 0]

            count -= 1

        self.weather_arr = []
        self.pm_arr = []

        selected = 0

        self.cov = np.zeros(shape=[5], dtype='f')
        for j in range(5):
            targetdata = np.zeros(shape=[self.Length], dtype='f')

            for i in range(Count_):
                targetdata[i] = self.weather_data[i, j]
            self.cov[j] = self.variance(targetdata)

        write2 = open('data2', 'w')

        for i in range(Count_):
            strline = ''

            if self.weather_data[i, 1] < 0.01:
                if abs(self.weather_data[i, 0] - self.mean_np[0]) < (self.cov[0] / 1) and \
                                abs(self.weather_data[i, 2] - self.mean_np[2]) < (self.cov[2] / 1) and \
                                abs(self.weather_data[i, 4] - self.mean_np[4]) < (self.cov[4] / 1):
                    arr = [self.weather_data[i, 0], self.weather_data[i, 1], self.weather_data[i, 2],
                           self.weather_data[i, 3], self.weather_data[i, 4]]
                    self.weather_arr.append(arr)
                    self.pm_arr.append(self.pm_data[i, 0])

                    for k in range(5):
                       strline += str(arr[k]) + ','

                    write2.write(strline + '\n')

                    selected += 1
                else:
                    0
                    #print(abs(self.weather_data[i, 0] - self.mean_np[0]))
                    #print(abs(self.weather_data[i, 2] - self.mean_np[2]))
                    #print(abs(self.weather_data[i, 4] - self.mean_np[4]))
                    #print('\n')

        print('s', selected)

        write2.close()

        self.weather_np = np.array(self.weather_arr, dtype='f')
        self.pm_np = np.array(self.pm_arr)

        self.Length = Count_

    def drawGraph(self):

        for j in range(5):
            targetdata = np.zeros(shape=[self.Length], dtype='f')

            newData = np.zeros(shape=[self.weather_np.shape[0], self.weather_np.shape[1]], dtype='f')
            for i in range(self.weather_np.shape[0]):
                for k in range(self.weather_np.shape[1]):
                    newData[i, k] = self.weather_np[i, k]

            for k in range(self.weather_np.shape[1]):
                maxv = -999

                for i in range(self.weather_np.shape[0]):
                    if maxv < newData[i, k]:
                        maxv = newData[i, k]
                for i in range(self.weather_np.shape[0]):
                    newData[i, k] = newData[i, k] / maxv
                print('max', maxv)

            print(newData.shape)
            input()
            for i in range(len(self.pm_np)):
                targetdata[i] = self.weather_np[i, j]
            plt.plot(newData)
            plt.legend(['Raindrop', 'Temperature', 'Wind Speed', 'Humidity', 'atmospheric'], loc='best')
            plt.show()
        inputdata = np.zeros(shape=[self.Length], dtype='f')
        for i in range(len(self.pm_np)):
            inputdata[i] = self.pm_np[i]
        plt.plot(inputdata)
        plt.show()

    def drawGraph_(self):
        targetdata = np.zeros(shape=[self.weather_np.shape[0]], dtype='f')
        drawdata = np.zeros(shape=[self.weather_np.shape[0], 2], dtype='f')

        print(int(self.weather_np.shape[0]), self.weather_np.shape[1])
        print('ssssssssssssssssss')
        newData = np.zeros(shape=[self.weather_np.shape[0], self.weather_np.shape[1]], dtype='f')
        for i in range(self.weather_np.shape[0]):
            for k in range(self.weather_np.shape[1]):
                newData[i, k] = self.weather_np[i, k]

        for k in range(self.weather_np.shape[1]):
            maxv = -999
            maxv2 = -999
            print('no std', newData[0])
            print('std@@@@@@@@@')
            #input()
            for i in range(self.weather_np.shape[0]):
                if maxv < newData[i, k]:
                    maxv = newData[i, k]
                if maxv2 < self.pm_np[i]:
                    maxv2 = self.pm_np[i]
            if abs(maxv) > 0.0001:
                for i in range(self.weather_np.shape[0]):
                    newData[i, k] = newData[i, k] / maxv
            if abs(maxv2) > 0.0001:
                for i in range(self.weather_np.shape[0]):
                    targetdata[i] = self.pm_np[i] / maxv2

            print('std', newData[0])
            print('max', maxv)

        arr = ['Temperature', 'Raindrop', 'Wind Speed', 'Humidity', 'atmospheric']

        for k in range(5):
            for i in range(self.weather_np.shape[0]):
                drawdata[i, 0] = newData[i, k]
                drawdata[i, 1] = targetdata[i]

            plt.plot(drawdata)
            plt.legend([arr[k], 'pm10'], loc='best')
            plt.show()

        plt.plot(newData)
        plt.legend(['Temperature', 'Raindrop', 'Wind Speed', 'Humidity', 'atmospheric'], loc='best')
        plt.show()

        input()

        """
        inputdata = np.zeros(shape=[self.Length], dtype='f')
        for i in range(len(self.pm_np)):
            inputdata[i] = self.pm_np[i]
        plt.plot(inputdata)
        plt.show()
        """

    def getPearsonResult(self, index):
        print('length:', len(self.pm_np), self.Length)

        inputdata = np.zeros(shape=[len(self.pm_np)], dtype='f')
        targetdata = np.zeros(shape=[len(self.pm_np)], dtype='f')


        for i in range(len(self.pm_np)):
            inputdata[i] = self.pm_np[i]
            targetdata[i] = self.weather_np[i, index]

        pearson_coff = self.pearson(inputdata, targetdata)

        return pearson_coff

    def mean(self, x):
        return sum(x) / len(x)

    def dot(self, v, w):
        return sum(v_i * w_i for v_i, w_i in zip(v, w))

    def sum_of_squares(self, v):
        return self.dot(v, v)

    def de_mean(self, x):  # 요소들과 평균의 차이
        x_bar = self.mean(x)
        return [x_i - x_bar for x_i in x]

    def variance(self, x) :
        n = len(x)
        deviations = self.de_mean(x)
        return self.sum_of_squares(deviations) / (n-1)

    def covariance(self, x, y):
        n = len(x)

        return self.dot(self.de_mean(x), self.de_mean(y)) / (n - 1)

    def getCovarianceResult(self, index):
        inputdata = np.zeros(shape=[len(self.pm_np)], dtype='f')
        targetdata = np.zeros(shape=[len(self.pm_np)], dtype='f')

        for i in range(len(self.pm_np)):
            inputdata[i] = self.pm_np[i]
            targetdata[i] = self.weather_np[i, index]

        pearson_coff = self.covariance(inputdata, targetdata)

        return pearson_coff

    def getCorelationResult(self, index):
        inputdata = np.zeros(shape=[len(self.pm_np)], dtype='f')
        targetdata = np.zeros(shape=[len(self.pm_np)], dtype='f')


        for i in range(len(self.pm_np)):
            inputdata[i] = self.pm_np[i]
            targetdata[i] = self.weather_np[i, index]

        pearson_coff = self.pearson(inputdata, targetdata)

        return pearson_coff