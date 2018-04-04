import numpy as np

class DataHolder:
    def checker(self, word):
        time = int(word)
        if (time > 7 and time < 11) or (time > 17 and time < 21):
            return True
        else:
            return True

    def __init__(self, isPM10=True, bukok=True):
        f = open('idkeys.txt', 'r')

        line = f.read()
        lines = line.split('#')

        numClass = 0
        id_name = []

        for j in range(len(lines)):
            TK = lines[j].split(',')
            numClass += (len(lines[j].split(',')) - 1)
            for i in range(len(TK)):
                id_name.append(TK[i])

        key_index = 0
        #충렬대로, 기장
        if bukok:
            id = '1350001401'
        else:
            id = '1350009300'

        for i in range(len(id_name)):
            if id == id_name[i]:
                key_index = i

                #input()

        PM_Data = []
        NO2_Data = []

        if bukok:
            PM_file = open('bukok.csv', 'r')
        else:
            PM_file = open('kijang.csv', 'r')

        lines = PM_file.readlines()

        for i in range(len(lines)):
            TK = lines[i].split(',')

            if TK[0].split(' ')[0].split('-')[2] != '30' and self.checker(word=TK[0].split(' ')[1]):
                try:
                    if isPM10:
                        PM_Data.append(float(TK[8]))
                    else:
                        PM_Data.append(float(TK[9]))
                except:
                    PM_Data.append(0.0)

                try:
                    NO2_Data.append(float(TK[7]))
                except:
                    NO2_Data.append(0.0)

        #input()

        Traffic_Data = []

        for i in range(12, 30):
            if i != 30:
                pathname = ''
                if i < 10:
                    pathname += 'save_traffic0' + str(i)
                else:
                    pathname += 'save_traffic' + str(i)

                file = open(pathname, 'r')
                TK = file.read().split('@')[1].split('#')

                # input()

                min_check = 0
                hour_check = 1

                for a in range(len(TK)):
                    if self.checker(str(hour_check)):
                        try:
                            # print(np.array(TK[a].split(',')).shape, a, key_index, i)
                            # print(TK[a])
                            Traffic_Data.append(float(TK[a].split(',')[key_index]))
                        except:
                            0
                            # input()

                    min_check += 1
                    if min_check == 12:
                        min_check = 0
                        hour_check += 1
        weather_path = '20171110180800.csv'
        weather_file = open(weather_path, 'r')
        lines = weather_file.readlines()

        Temperature_Data = []
        Rain_Data = []
        Wind_Data = []
        Humidity_Data = []

        for i in range(len(lines)):
            TK = lines[i].split(',')
            #print(TK[1].split(' ')[1].split('-'))

            if TK[1].split(' ')[0].split('-')[2] != '11'and self.checker(word=TK[1].split(' ')[1].split(':')[0]):
                try:
                    Rain_Data.append(float(TK[3]))
                except:
                    Rain_Data.append(0.0)

                try:
                    Temperature_Data.append(float(TK[2]))
                except:
                    Temperature_Data.append(0.0)

                try:
                    Wind_Data.append(float(TK[4]))
                except:
                    Wind_Data.append(0.0)

                try:
                    Humidity_Data.append(float(TK[5]))
                except:
                    Humidity_Data.append(0.0)



        length = len(Traffic_Data)
        Traffic_Data_Hour = []

        index = 0
        temp = 0

        for i in range(length):
            index += 1
            temp += Traffic_Data[i]

            if index % 12 == 0:
                Traffic_Data_Hour.append(float(temp / 12))
                temp = 0
                index = 0

        self.myBatchSize = len(Rain_Data)

        self.Rain_Data = np.array(Rain_Data)
        self.Temperature_Data = np.array(Temperature_Data)
        self.Wind_Data = np.array(Wind_Data)
        self.Humidity_Data = np.array(Humidity_Data)
        self.Traffic_Data_Hour = np.array(Traffic_Data_Hour)
        self.PM_Data = np.array(PM_Data)
        self.NO2_Data = np.array(NO2_Data)

    def get_Traffic_PM(self):
        data = np.zeros(shape=[self.myBatchSize, 2], dtype='f')
        for i in range(self.myBatchSize):
            data[i, 0] = self.NO2_Data[i]
            data[i, 1] = self.Traffic_Data_Hour[i]

        return self.PM_Data, data, ['Traffic', 'NO2'], self.myBatchSize, 2

    def get_Weather_Traffic(self):
        data = np.zeros(shape=[self.myBatchSize, 6], dtype='f')
        for i in range(self.myBatchSize):
            data[i, 0] = self.Rain_Data[i]
            data[i, 1] = self.Temperature_Data[i]
            data[i, 2] = self.Wind_Data[i]
            data[i, 3] = self.Humidity_Data[i]
            data[i, 4] = self.NO2_Data[i]
            data[i, 5] = self.Traffic_Data_Hour[i]

        return self.PM_Data, data, ['rain', 'temperature', 'wind speed', 'humidity', 'NO2', 'traffic'], self.myBatchSize, 6

    def get_Prediction_Data(self):
        data = np.zeros(shape=[self.myBatchSize, 7], dtype='f')
        for i in range(self.myBatchSize):
            data[i, 0] = self.Rain_Data[i] / 50
            data[i, 1] = self.Temperature_Data[i] / 50
            data[i, 2] = self.Wind_Data[i] / 50
            data[i, 3] = self.Humidity_Data[i] / 50
            data[i, 4] = self.NO2_Data[i] / 50
            data[i, 5] = self.Traffic_Data_Hour[i] / 50
            data[i, 6] = self.PM_Data[i] / 50

        return self.PM_Data / 50, data, ['rain', 'temperature', 'wind speed', 'humidity', 'NO2', 'traffic', 'PM10']

    def get_Prediction_Data_(self):
        data = np.zeros(shape=[self.myBatchSize, 3], dtype='f')
        for i in range(self.myBatchSize):
            data[i, 0] = self.NO2_Data[i] / 50
            data[i, 1] = self.Traffic_Data_Hour[i] / 50
            data[i, 2] = self.PM_Data[i] / 50

        return self.PM_Data / 50, data, ['rain', 'temperature', 'wind speed', 'humidity', 'NO2', 'traffic', 'PM10']




