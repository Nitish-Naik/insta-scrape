# Import Dependencies
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model, metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns

# Load the Diabetes dataset
diabetes = datasets.load_diabetes()

# X - feature vectors
# y - Target values
X = diabetes.data
y = diabetes.target

# Splitting X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)

# Create linear regression object
lin_reg = linear_model.LinearRegression()

# Fit the model
lin_reg.fit(X_train, y_train)

# Predict the values
predicted = lin_reg.predict(X_test)

# Print coefficients and intercept
print('\nCoefficients are:\n', lin_reg.coef_)
print('\nIntercept : ', lin_reg.intercept_)

# Variance score: 1 means perfect prediction
print('Variance score: ', lin_reg.score(X_test, y_test))

# Mean Squared Error
print("Mean squared error: %.2f\n" % mean_squared_error(y_test, predicted))

# Original data of X_test
expected = y_test

# Plot a graph for expected and predicted values
plt.figure(figsize=(10, 6))
plt.title('Linear Regression (Diabetes Dataset)')
plt.scatter(expected, predicted, c='b', marker='.', s=36, label='Predicted vs Expected')
plt.plot(np.linspace(0, 330, 100), np.linspace(0, 330, 100), '--r', linewidth=2, label='Perfect Prediction')
plt.xlabel('Expected Values')
plt.ylabel('Predicted Values')
plt.legend()
plt.grid(True)
plt.show()
