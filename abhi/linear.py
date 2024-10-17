
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model, metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns


diabetes = datasets.load_diabetes()


X = diabetes.data
y = diabetes.target


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)


lin_reg = linear_model.LinearRegression()

lin_reg.fit(X_train, y_train)

predicted = lin_reg.predict(X_test)


print('\nCoefficients are:\n', lin_reg.coef_)
print('\nIntercept : ', lin_reg.intercept_)


print('Variance score: ', lin_reg.score(X_test, y_test))

print("Mean squared error: %.2f\n" % mean_squared_error(y_test, predicted))


expected = y_test


plt.figure(figsize=(10, 6))
plt.title('Linear Regression (Diabetes Dataset)')
plt.scatter(expected, predicted, c='b', marker='.', s=36, label='Predicted vs Expected')
plt.plot(np.linspace(0, 330, 100), np.linspace(0, 330, 100), '--r', linewidth=2, label='Perfect Prediction')
plt.xlabel('Expected Values')
plt.ylabel('Predicted Values')
plt.legend()
plt.grid(True)
plt.show()
