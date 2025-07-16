import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# Load the iris dataset
iris = load_iris()
# use the second and the third rows
X = iris.data[:,2:3].reshape(-1,1)
Y = iris.data[:,1:2].reshape(-1,1)
colors = np.random.rand(X.shape[0])
# area = (30 * np.random.rand(X.shape[0]))

plt.scatter(X,Y, c=colors, label='Data',cmap='afmhot_r')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Iris Dataset')
plt.colorbar()
plt.legend()
plt.show()