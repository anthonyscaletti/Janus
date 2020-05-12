import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
import numpy as np
import pandas as pd

class Janus:
    def __init__(self, raw_data, field):
        self.raw_data = raw_data
        self.field = field
        self.lstm_dimentions = 200
        self.first_dense_layer = 25
        self.second_dense_layer = 1
        self.batch_size = 64
        self.epoch_size = 64
        self.data_frame = pd.DataFrame(raw_data)
        self.dataset = {}
        self.training_data_len = 0
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = {}
        self.n_input = 0
        self.n_features = 1
        self.x_train = []
        self.y_train = []
        self.model = None
        self.is_model_trained = False

    def set_Field(self, field):
        self.field = field

    def set_lstm_dimentions(self, lstm_Dimentions):
        self.lstm_dimentions = lstm_dimentions

    def set_first_dense_layer(self, layer):
        self.first_dense_layer = layer

    def set_second_dense_layer(self, layer):
        self.second_dense_layer = layer

    def set_batch_size(self, size):
        self.batch_size = size
    
    def set_epoch_size(self, size):
        self.epoch_size = size

    def get_field(self):
        return self.field

    def get_lstm_dimentions(self):
        return self.lstm_dimentions

    def get_first_dense_layer(self):
        return self.first_dense_layer

    def get_second_dense_layer(self):
        return self.second_dense_layer

    def get_batch_size(self):
        return self.batch_size
    
    def get_epoch_size(self):
        return self.epoch_size

    def is_model_trained(self):
        return self.is_model_trained

    def __get_rmse(self):
        #Create testing dataset
        test_data = self.scaled_Data[self.training_data_len - self.n_input:, :]
        #Create x_test, y_test
        x_test = []
        y_test = self.dataset[self.training_data_len:, :]

        for i in range(self.n_input, len(test_Data)):
            xTest.append(test_data[i - self.n_input:i, 0])

        #Convert data to a numpy array
        x_test = np.array(x_test)

        #Reshape data to 3 dimentional because LSTM expects 3 dimensional
        x_test = np.reshape(x_test, (x_test.shape[0], self.n_input, self.n_features))

        #Get model's predicted values
        predictions = self.model.predict(x_test)
        predictions = self.scaler.inverse_transform(predictions)

        #Get the mean squared error RMSE
        return np.sqrt(np.mean(((predictions- y_test)**2)))

    def predict_next_value(self):
        #Get last 20 days 
        last_20_days = self.dataset[-self.n_input:]
        last_20_days_scaled = self.scaler.transform(last_20_days)

        x_test = []
        x_test.append(last_20_days_scaled) 

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], self.n_input, self.n_features))

        #Predicted value
        pred_value = self.model.predict(x_test)
        pred_value = self.scaler.inverse_transform(pred_value)

        return pred_value[0].tolist()

    def launch_janus(self):
        #Step1: Initialize Environment Variables
        self.__initialize_dataset_variables()
        #Step2: Scale Data Between 0 And 1
        self.__scale_data()
        #Step3: Create Training Dataset
        self.__create_training_dataset()
        #Step4: Build The RNN LSTM Model
        self.__build_lstm_model()
        #step5: Train The Model
        self.__train_lstm_model()

    def __initialize_dataset_variables(self):
        data = self.data_frame.filter([self.field])
        self.dataset = data.values
        self.training_data_len = math.ceil(len(self.dataset) * 0.7)
        self.n_input = math.ceil(self.training_data_len * 0.3)
      
    def __scale_data(self):
        self.scaled_data = self.scaler.fit_transform(self.dataset)
    
    def __create_training_dataset(self):
        #Create Training data set
        train_data = self.scaled_data[0:self.training_data_len, :]

        for i in range(self.n_input, len(train_data)):
            self.x_train.append(train_data[i - self.n_input:i, 0])
            self.y_train.append(train_data[i, 0])

        #Make training datasets into arrays with numpy
        self.x_train = np.array(self.x_train)
        self.y_train = np.array(self.y_train)

        self.x_train = np.reshape(
            self.x_train,
            (self.x_train.shape[0], self.n_input, self.n_features))

    def __build_lstm_model(self):
        #Build LSTM model
        self.model = Sequential()
        self.model.add(LSTM(
            self.lstm_dimentions,
            return_sequences=True,
            input_shape=(self.n_input, self.n_features)))
        self.model.add(LSTM(self.lstm_dimentions, return_sequences=False))
        self.model.add(Dense(self.first_dense_layer))
        self.model.add(Dense(self.second_dense_layer))

        #Compile Model
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def __train_lstm_model(self):
        #Train Model
        self.model.fit(
            self.x_train,
            self.y_train,
            batch_size=self.batch_size,
            epochs=self.epoch_size,
            verbose=0)
        self.is_model_trained = True
