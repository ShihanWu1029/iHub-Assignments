import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# 生成一些示例数据
# np.random.seed()
X = np.sort(5 * np.random.rand(80, 1), axis=0)
# y = np.sin(X).ravel() + np.random.randn(80) * 0.1
y= X

# 创建多项式特征
poly_features = PolynomialFeatures(degree=3)
X_poly = poly_features.fit_transform(X)

# 拟合线性回归模型
lin_reg = LinearRegression()
lin_reg.fit(X_poly, y)

# 预测
X_test = np.linspace(0, 5, 100).reshape(-1, 1)
X_test_poly = poly_features.transform(X_test)
y_pred = lin_reg.predict(X_test_poly)

# 绘制结果
plt.scatter(X, y, color='blue', label='Data')
plt.plot(X_test, y_pred, color='red', label='Polynomial Regression')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Polynomial Regression')
plt.legend()
plt.show()