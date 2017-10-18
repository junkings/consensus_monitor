#encoding:utf8
import numpy as np
import matplotlib.pyplot as plt


def sigmod(x):
	return 1/(1 + np.exp(-x))

def function_tidu(X, y, sita):
	m = len(X)
	sum0 = 0
	sum1 = 0
	sita_tmp = [0,0]
	for i in range(m):
		sum0 += (sigmod(sita[0]*X[i]+sita[1]*1) - y[i]) * X[i]
		sum1 += (sigmod(sita[0]*X[i]+sita[1]*1) - y[i])

	sita_tmp[0] = sita[0] - 1 * sum0 / m
	sita_tmp[1] = sita[1] - 1 * sum1 / m
	return sita_tmp

X = [-5, -2, -1, 1, 2, 3,]
y = [0, 0, 1, 1, 1, 1,]
plt.figure(1)
plt.plot(X, y)
plt.figure(2)

sita = [1, 1]
for i in range(10000):
	sita_tmp = function_tidu(X,y,sita)
	print(sita, sita_tmp)
	sita = sita_tmp

x=np.linspace(-10,10,1000)
y= 1/(1 + np.exp(-(sita[0]*x+sita[1])))

plt.plot(x,y)
plt.show()