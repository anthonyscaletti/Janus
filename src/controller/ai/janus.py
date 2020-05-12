import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
import numpy as np
import pandas as pd

class Janus:
    def __init__(self, rawData, field):
        self.rawData = rawData
        self.field = field
        self.lstmDimentions = 200
        self.firstDenseLayer = 25
        self.secondDenseLayer = 1
        self.batchSize = 64
        self.epochSize = 64
        self.dataFrame = pd.DataFrame(rawData)
        self.dataset = {}
        self.trainingDataLen = 0
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaledData = {}
        self.nInput = 0
        self.nFeatures = 1
        self.xTrain = []
        self.yTrain = []
        self.model = None
        self.isModelTrained = False

    def setField(self, field):
        self.field = field

    def setLstmDimentions(self, lstmDimentions):
        self.lstmDimentions = lstmDimentions

    def setFirstDenseLayer(self, layer):
        self.firstDenseLayer = layer

    def setSecondDenseLayer(self, layer):
        self.secondDenseLayer = layer

    def setBatchSize(self, size):
        self.batchSize = size
    
    def setEpochSize(self, size):
        self.epochSize = size

    def getField(self):
        return self.field

    def getLstmDimentions(self):
        return self.lstmDimentions

    def getFirstDenseLayer(self):
        return self.firstDenseLayer

    def getSecondDenseLayer(self):
        return self.secondDenseLayer

    def getBatchSize(self):
        return self.batchSize
    
    def getEpochSize(self):
        return self.epochSize

    def isModelTrained(self):
        return self.isModelTrained

    def initializeDatasetVariables(self):
        data = self.dataFrame.filter([self.field])
        self.dataset = data.values
        self.trainingDataLen = math.ceil(len(self.dataset) * 0.7)
        self.nInput = math.ceil(self.trainingDataLen * 0.3)
        
    def scaleData(self):
        self.scaledData = self.scaler.fit_transform(self.dataset)
    
    def createTrainingDataset(self):
        #Create Training data set
        trainData = self.scaledData[0:self.trainingDataLen, :]

        for i in range(self.nInput, len(trainData)):
            self.xTrain.append(trainData[i - self.nInput:i, 0])
            self.yTrain.append(trainData[i, 0])

        #Make training datasets into arrays with numpy
        self.xTrain = np.array(self.xTrain)
        self.yTrain = np.array(self.yTrain)

        self.xTrain = np.reshape(self.xTrain, (self.xTrain.shape[0], self.nInput, self.nFeatures))

    def buildLstmModel(self):
        #Build LSTM model
        self.model = Sequential()
        self.model.add(LSTM(self.lstmDimentions, return_sequences=True, input_shape=(self.nInput, self.nFeatures)))
        self.model.add(LSTM(self.lstmDimentions, return_sequences=False))
        self.model.add(Dense(self.firstDenseLayer))
        self.model.add(Dense(self.secondDenseLayer))

        #Compile Model
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def trainLstmModel(self):
        #Train Model
        self.model.fit(self.xTrain, self.yTrain, batch_size=self.batchSize, epochs=self.epochSize)
        self.isModelTrained = True

    def getRmse(self):
        #Create testing dataset
        testData = self.scaledData[self.trainingDataLen - self.nInput:, :]
        #Create x_test, y_test
        xTest = []
        yTest = self.dataset[self.trainingDataLen:, :]

        for i in range(self.nInput, len(testData)):
            xTest.append(testData[i - self.nInput:i, 0])

        #Convert data to a numpy array
        xTest = np.array(xTest)

        #Reshape data to 3 dimentional because LSTM expects 3 dimensional
        xTest = np.reshape(xTest, (xTest.shape[0], self.nInput, self.nFeatures))

        #Get model's predicted values
        predictions = self.model.predict(xTest)
        predictions = self.scaler.inverse_transform(predictions)

        #Get the mean squared error RMSE
        return np.sqrt(np.mean(((predictions- yTest)**2)))

    def predictNextValue(self):
        #Get last 20 days 
        last20Days = self.dataset[-self.nInput:]
        last20DaysScaled = self.scaler.transform(last20Days)

        xTest = []
        xTest.append(last20DaysScaled) 

        xTest = np.array(xTest)
        xTest = np.reshape(xTest, (xTest.shape[0], self.nInput, self.nFeatures))

        #Predicted value
        predValue = self.model.predict(xTest)
        predValue = self.scaler.inverse_transform(predValue)

        return predValue[0]

    def launchJanus(self):
        #Step1: Initialize Environment Variables
        self.initializeDatasetVariables()
        #Step2: Scale Data Between 0 And 1
        self.scaleData()
        #Step3: Create Training Dataset
        self.createTrainingDataset()
        #Step4: Build The RNN LSTM Model
        self.buildLstmModel()
        #step5: Train The Model
        self.trainLstmModel()
