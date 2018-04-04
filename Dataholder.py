import numpy as np
import os

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

        self.Length = len(lines) - 1
        self.weather_data = np.zeros(shape=[len(lines) - 1, 5], dtype='f')

        self.sequence_length = 0
        self.dim = 0
        self.batch_size = 0

        for i in range(len(lines) - 1):
            TK = lines[i + 1].replace('\n', '').split(',')
            #데이터는 모두 쉼표로 구분되어 있기 때문에 ,로 나누어줌

            for j in range(5):
                try:
                    self.weather_data[i, j] = float(TK[j + 2])
                except:
                    self.weather_data[i, j] = 0
                    #비어있는 데이터의 경우 0으로 임의로 채워줌

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

    def getData(self, Column, seq_length=15, exp_length=5, isNANO=True):
        self.dim = len(Column) + 1
        self.sequence_length = seq_length
        self.batch_size = self.Length - seq_length - exp_length + 1

        input_data = np.zeros(shape=[self.Length - seq_length - exp_length + 1, seq_length, len(Column) + 1])
        label_data = np.zeros(shape=[self.Length - seq_length - exp_length + 1, seq_length, 1])
        for k in range(self.Length - seq_length - exp_length + 1):
            for j in range(len(Column)):
                for i in range(seq_length):
                    input_data[k, i, j] = self.weather_data[i + k, Column[j]]
                    if isNANO:
                        input_data[k, i, len(Column)] = self.pm_data[i + k, 1]
                        label_data[k, i, 0] = self.pm_data[i + k + exp_length, 1]
                    else:
                        input_data[k, i, len(Column)] = self.pm_data[i + k, 0]
                        label_data[k, i, 0] = self.pm_data[i + k + exp_length, 0]

        return input_data, label_data

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
        inputdata = np.zeros(shape=[self.Length], dtype='f')
        targetdata = np.zeros(shape=[self.Length], dtype='f')

        for i in range(len(self.pm_data)):
            inputdata[i] = self.pm_data[i, 0]
            targetdata[i] = self.weather_data[i, index]

        pearson_coff = self.covariance(inputdata, targetdata)

        return pearson_coff

    def getPearsonResult(self, index):
        inputdata = np.zeros(shape=[self.Length], dtype='f')
        targetdata = np.zeros(shape=[self.Length], dtype='f')

        for i in range(self.Length):
            inputdata[i] = self.pm_data[i, 0]
            targetdata[i] = self.weather_data[i, index]

        pearson_coff = self.pearson(inputdata, targetdata)

        return pearson_coff

