import numpy
from sklearn.cross_validation import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
import pylab as plot
from pylab import savefig

class RF_Regressor:
    def __init__(self, target, data, names):
        self.Target = target
        self.Data = data
        self.Names = names

    def RF(self, batch, dim):

        result_mse = "MSE : "
        result_RF = "RF : "
        result_corr = "corr : "

        data = open("winequality-red.csv", "r")

        xList = []
        labels = []
        names = []

        firstLine = True
        for line in data:
            if firstLine:
                # 항목 이름들
                names = line.strip().split(";")
                firstLine = False
            else:
                # Split with ";"
                row = line.strip().split(";")
                labels.append(float(row[-1]))
                row.pop()
                floatRow = [float(num) for num in row]
                xList.append(floatRow)

        # print(xList);print(labels)

        nrows = len(xList)
        ncols = len(xList[0])

        X = self.Data
        Y = self.Target
        wineNames = numpy.array(self.Names)
        # print(X);print(Y);print(wineNames)
        #print()
        #print(numpy.array(xList).shape)
        #print(numpy.array(labels).shape)
        #input()
        # 데이터 행의 30%로 고정된 홀드 아웃 세트 구성
        xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size=0.3, random_state=531)
        # print(xTrain);print(xTest);print(yTrain);print(yTest)

        # MSE의 변화를 확인하기 위하여 앙상블의 크기 범위에서 랜덤 포레스트 트레이닝
        mseOos = []
        nTreeList = range(50, 500, 10)
        for iTrees in nTreeList:
            depth = None
            maxFeat = 2  # 조정해볼 것
            wineRFModel = ensemble.RandomForestRegressor(n_estimators=iTrees,
                                                         max_depth=depth, max_features=maxFeat,
                                                         oob_score=False, random_state=531)
            #print(xTrain.shape, yTrain.shape)

            wineRFModel.fit(xTrain, yTrain)
            # 데이터 세트에 대한 MSE 누적
            prediction = wineRFModel.predict(xTest)
            mseOos.append(mean_squared_error(yTest, prediction))

        # print("MSE")
        # print(mseOos[-1])
        result_mse += str(mseOos[-1])

        # 트레이닝 테스트 오차 대비  앙상블의 트리 개수 도표 그리기
        plot.plot(nTreeList, mseOos)
        plot.xlabel('Number of Trees in Ensemble')
        plot.ylabel('Mean Squared Error')
        # plot.ylim([0.0, 1.1*max(mseOob)])
        #print("그래프 창을 종료하시면 다음 결과가 나타납니다.")
        fig = plot.gcf()
        plot.show(block=False)

        fig.savefig('traffic_tree_number_plot.png')
        plot.close()

        # 피처 중요도 도표 그리기
        featureImportance = wineRFModel.feature_importances_

        # 가장 높은 중요도 기준으로 스케일링
        #featureImportance = featureImportance / featureImportance.max()
        sorted_idx = numpy.argsort(featureImportance)
        barPos = numpy.arange(sorted_idx.shape[0]) + .5
        plot.barh(barPos, featureImportance[sorted_idx], align='center')
        plot.yticks(barPos, wineNames[sorted_idx])
        plot.xlabel('Variable Importance')
        #print("그래프 창을 종료하시면 다음 결과가 나타납니다.")
        fig = plot.gcf()
        plot.show(block=False)

        fig.savefig('traffic_feature_importance.png')
        plot.close()

        # print('RF')
        # print(featureImportance)
        result_RF += str(featureImportance)

        corr = numpy.zeros(shape=[dim], dtype='f')

        for i in range(dim):
            x = numpy.zeros(shape=[batch])
            for j in range(batch):
                x[j] = X[j, i]
            corr[i] = numpy.corrcoef(x, Y)[0, 1]

        #corr = corr / corr.max()
        sorted_idx = numpy.argsort(corr)
        barPos = numpy.arange(sorted_idx.shape[0]) + .5
        plot.barh(barPos, corr[sorted_idx], align='center')
        plot.yticks(barPos, wineNames[sorted_idx])
        plot.xlabel('Pearson Coefficient')
        fig = plot.gcf()
        plot.show(block=False)

        fig.savefig('traffic_pearson_coefficient.png')
        plot.close()

        # print('corr')
        # print(corr)
        result_corr += str(corr)

        # printed Output

        return result_mse, result_RF, result_corr