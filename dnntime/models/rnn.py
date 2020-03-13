import time
import numpy as np
from typing import Tuple
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Dropout
# helper functions
from ..utils.metrics import calc_rmse, calc_mae, calc_mape


class RNNWrapper:

    def __init__(self, n_input: int, n_output: int = 1, n_feature: int = 1, 
                 n_unit: int = 64, d_rate: int = 0.15, optimizer: str = 'adam',
                 loss: str = "mse"):
        
        self.rnn_model = StackedRNN(n_input, n_output, n_unit, n_feature, d_rate)
        self.rnn_model.compile(optimizer, loss)
        self.run_time = 0.0

    def fit(self, X_train: np.ndarray, y_train: np.ndarray, n_epoch: int = 10,
            n_batch: int = 1, verbose: int = 0) -> None:

        start_time = time.time()
        self.rnn_model.fit(X_train, y_train, epochs=n_epoch, batch_size=n_batch,
                           verbose=verbose)
        end_time = time.time()
        self.run_time = end_time - start_time

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray, score_type: str = 'rmse', 
                 verbose: int = 0) -> Tuple[Sequential, np.ndarray, float, float]:

        rnn_pred = self.rnn_model.predict(X_test, verbose=verbose)

        rmse = calc_rmse(y_test, rnn_pred)
        mae = calc_mae(y_test, rnn_pred)
        mape = calc_mape(y_test, rnn_pred)

        print("\n-----------------------------------------------------------------")
        print("RNN SUMMARY:")
        print("-----------------------------------------------------------------")
        print(f"MAE Score: {round(mae, 4)}")
        print(f"MAPE Score: {round(mape, 4)}")
        print(f"RMSE Score: {round(rmse, 4)}")
        print(f"Total Training Time: {round(self.run_time/60, 2)} min")
    
        return self.rnn_model, rnn_pred, rmse


def VanillaRNN(n_input: int, n_output: int, n_unit: int, n_feature: int) -> Sequential:
    
    model = Sequential()
    model.add(SimpleRNN(n_unit, activation="tanh", return_sequences=False,
                        input_shape=(n_input, n_feature)))
    model.add(Dense(n_output))
    print("Vanilla RNN model summary:")
    model.summary()
    return model


def StackedRNN(n_input: int, n_output: int, n_unit: int, n_feature: int, 
               d_rate: float = 0.5) -> Sequential:

    model = Sequential()
    model.add(SimpleRNN(n_unit, activation="tanh", return_sequences=True,
                        input_shape=(n_input, n_feature)))
    model.add(Dropout(d_rate))
    model.add(SimpleRNN(n_unit, activation="tanh", return_sequences=True))
    model.add(Dropout(d_rate))
    model.add(SimpleRNN(n_unit, activation="tanh", return_sequences=False))
    model.add(Dropout(d_rate))
    model.add(Dense(n_output))
    print("Stacked RNN model summary:")
    model.summary()
    return model


def CustomRNN(n_input: int, n_output: int, n_unit: int,
              n_feature: int) -> Sequential:

    pass
