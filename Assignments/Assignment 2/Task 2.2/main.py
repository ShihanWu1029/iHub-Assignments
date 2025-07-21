import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Data generation
# np.random.seed(0)
X = np.sort(255 * np.random.rand(80, 1), axis=0)
# given f(x) = -(x-127)^2 + 5 + noise
y= -(X.ravel()-127)**2+5 + np.random.randn(80) * 1000


poly_features = PolynomialFeatures(degree=3)
X_poly = poly_features.fit_transform(X)

lin_reg = LinearRegression()
lin_reg.fit(X_poly, y)

X_test = np.linspace(0, 255, 1000).reshape(-1, 1)
X_test_poly = poly_features.transform(X_test)
y_pred = lin_reg.predict(X_test_poly)

print("Prediction at x =",int(X_test[999][0]),end=' ')
print("is y =",y_pred[999])

# Draw
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label='Polynomial Regression')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Polynomial Regression')
plt.legend()
plt.show()