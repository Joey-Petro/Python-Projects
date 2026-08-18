#Joey Petrovic
#Assignment 3

import numpy as np
import matplotlib.pyplot as plt
from FileUtils_Petrovic import FileStuff as futils
import random #used for some testing


#A.1
filename = "rounded_hours_student_scores.csv"
data = futils.read_csv_file(filename, to="dictionary")

X = []
Y = []
for item in data:
    X.append(float(item["Hours"]))
    Y.append(float(item["Scores"]))

#A.2
x = np.array(X[:50], dtype=float)
x_test = np.array(X[50:], dtype=float)
y = np.array(Y[:50], dtype=float)
y_test = np.array(Y[50:], dtype=float)

x_mean = np.mean(x)
y_mean = np.mean(y)

nominator = np.sum((x - x_mean) * (y - y_mean))
denominator = np.sum((x - x_mean) ** 2)
m = nominator / denominator
c = y_mean - m * x_mean

#A.3
def predict(x, m, c):
    return m * x + c

#A.4
predictions = predict(x, m, c)

#A.5
test_predictions = predict(x_test, m, c)

#A.6
def mean_squared_error(y_gt, y_pred):
    return np.mean((y_gt - y_pred) ** 2)

#A.7
train_mse = mean_squared_error(y, predictions)
test_mse = mean_squared_error(y_test, test_predictions)

print(f"Train Mean Squared Error (y - predictions): {train_mse}")
print(f"Test Mean Squared Error (y_test - test_predictions): {test_mse}")

#A.8
train_results = [
    {"Hours": x[i], "Score": y[i], "Predicted Score": predictions[i]}
    for i in range(len(x))
]

test_results = [
    {"Hours": x_test[i], "Score": y_test[i], "Predicted Score": test_predictions[i]}
    for i in range(len(x_test))
]

for item in train_results:
    futils.save_to_csv("train_predictions.csv", item)

for item in test_results:
    futils.save_to_csv("test_predictions.csv", item)

#A.9
# Plotting the results
plt.scatter(X, Y, color='blue', label='Actual data')
plt.plot(x, predictions, color='red', label='Regression line')
plt.plot(x_test, test_predictions, color='black', label='Test data')
plt.xlabel('Hours')
plt.ylabel('Scores')
plt.legend()
plt.title('Linear Regression From Scratch')
plt.show()
