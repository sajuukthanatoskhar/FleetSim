#matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.ion()

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111, projection='3d')

def fun(x,y):
    return ((x**2 - y**2) * np.exp(-x**2 - y**2))

x = y = np.arange(-3.0,3.0, 0.05)
X, Y = np.meshgrid(x,y)
zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)

for i in range(len(X)):
    for j in range(len(Y)):
        ax.cla()
        ax.set_xlim((-5,5))
        ax.set_ylim((-5,5))
        ax.set_zlim((-5, 5))
        ax.scatter(X[i][j], Y[i][j], Z[i][j], c='r', marker='o')
        ax.scatter(X[i][j], (Y[i][j])**2, Z[i][j], c='b', marker='o')

        plt.draw()
        plt.pause(0.1)

#data needs to be sent in
#need to input axes only
# def refreshgraph(ax,data):
#
#     ax.scatter()







