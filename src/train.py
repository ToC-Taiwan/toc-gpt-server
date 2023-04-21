import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

# Load and preprocess data
data = pd.read_csv("stock_data.csv")  # Replace with the path to your stock tick data
data = data[["Close"]]  # Use the 'Close' price for prediction

# Scale data to the range [0, 1]
scaler = MinMaxScaler()
data = scaler.fit_transform(data)

# Split data into training and testing sets
train_size = int(len(data) * 0.85)
train_data = data[:train_size]
test_data = data[train_size:]


# Create input/output pairs for training and testing
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i : (i + look_back), 0])
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)


look_back = 1
X_train, y_train = create_dataset(train_data, look_back)
X_test, y_test = create_dataset(test_data, look_back)

# Reshape input data to the format required by LSTM layers
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# Build LSTM model
model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(50, input_shape=(1, look_back), activation="relu"))
model.add(tf.keras.layers.Dense(1))
model.compile(loss="mean_squared_error", optimizer="adam")

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=1)

# Make predictions
train_preds = model.predict(X_train)
test_preds = model.predict(X_test)

# Transform predictions back to the original scale
train_preds = scaler.inverse_transform(train_preds)
y_train = scaler.inverse_transform([y_train])
test_preds = scaler.inverse_transform(test_preds)
y_test = scaler.inverse_transform([y_test])

# Calculate mean squared error
train_score = mean_squared_error(y_train[0], train_preds[:, 0])
test_score = mean_squared_error(y_test[0], test_preds[:, 0])
print(f"Train Score: {train_score:.2f}")
print(f"Test Score: {test_score:.2f}")
