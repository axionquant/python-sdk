
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import numpy as np


# time series prediction models

def linearRegression(df, x, target, n_preds=10, scale='D'):
    df[x] = pd.to_datetime(df[x])
    X = df[x].values.reshape(-1, 1).astype(int) // 10**9
    y = df[target].values

    model = LinearRegression()
    model.fit(X, y)

    future_dates = pd.date_range(df[x].max(), periods=n_preds, freq=scale)
    future_timestamps = (future_dates - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    f_preds = model.predict(np.array(future_timestamps).reshape(-1, 1))

    return pd.DataFrame({x: future_dates, target: f_preds})


def multiLinearRegression(df, x, target, features, n_preds=10, scale='D'):
    preds = {}

    for feat in features:
        preds[feat] = linearRegression(df, x, feat, n_preds)[feat]

    df[x] = pd.to_datetime(df[x])
    X = df[x].values.reshape(-1, 1).astype(int) // 10**9
    y = df[target].values

    model = LinearRegression()
    model.fit(df[features], y)

    future_dates = pd.date_range(df[x].max(), periods=n_preds, freq=scale)
    future_timestamps = (future_dates - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    future_df = pd.DataFrame({x: future_dates, **preds})
    f_preds = model.predict(np.array(future_df[features]))

    return pd.DataFrame({"time": future_dates, target: f_preds})



def beta(df, x, y):
    X = df[y].values.reshape(-1, 1)
    y = df[x].values
    model = LinearRegression().fit(X, y)
    beta = model.coef_[0]
    return beta





# Deep learning time series prediction models
def create_sequences(data, sequence_length, n_preds):
    sequences = []
    labels = []
    for i in range(len(data) - sequence_length - n_preds + 1):
        sequence = data[i:(i + sequence_length)]
        label = data[(i + sequence_length):(i + sequence_length + n_preds)]
        sequences.append(sequence)
        labels.append(label)
    return np.array(sequences), np.array(labels)

def lstm(df, x, target, features=[], n_preds=10, scale='D'):
    all_columns = [target] + features
    data = df[all_columns].values.astype(float)

    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    sequence_length = 10  # You can adjust this based on your preference
    sequences, labels = create_sequences(data_scaled, sequence_length, n_preds)

    X_train, X_test, y_train, y_test = train_test_split(sequences, labels, test_size=0.2, random_state=42)

    # Reshape input data to include multiple features
    n_features = len(all_columns)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], n_features))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], n_features))

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, activation='relu', input_shape=(X_train.shape[1], n_features)))
    model.add(Dense(units=n_preds * n_features))  # Adjusted to match the number of predictions and features
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(X_train, y_train.reshape(-1, n_preds * n_features), epochs=50, batch_size=32, validation_split=0.1)

    loss = model.evaluate(X_test, y_test.reshape(-1, n_preds * n_features))
    print(f'Mean Squared Error on Test Set: {loss}')

    last_sequence = data_scaled[-sequence_length:]
    last_sequence = np.reshape(last_sequence, (1, sequence_length, n_features))

    future_predictions = model.predict(last_sequence)
    future_predictions = future_predictions.reshape(n_preds, n_features)
    future_predictions_actual = scaler.inverse_transform(future_predictions)

    future_dates = pd.date_range(df[x].max(), periods=n_preds, freq=scale)

    return pd.DataFrame([{"time": time, target: future_predictions_actual[i][0]} for i, time in enumerate(future_dates)])
