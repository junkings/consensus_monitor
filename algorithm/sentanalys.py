import numpy as np
import sys
import re
import jieba
from gensim.models import word2vec
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn.preprocessing import scale
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from scipy import stats
from keras.optimizers import SGD
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

def getwordVecs(wordList):
	vecs = []
	for word in wordList:
		word = word.repalce("\n", "")
		try:
			vecs.append(model[word])
		except KeyError:
			continue

	return np.array(vecs, dtype="float")

def buildVecs(filename):
	posInput = []
	with open(filename, "rb") as txtfile:

		for line in txtfile.readlines():
			line = jieba.cut(line)
			resultList = getwordVecs(line)
			if len(resultList) != 0:
				resultArray = sum(np.array(resultList))/len(resultList)
				posInput.append(resultArray)

	return posInput

model = word2vec.Word2Vec.load_word2vec_format("", binary=True)

posInput = buildVecs('')
negInput = buildVecs('')

y = np.concatenate((np.ones(len(posInput)), np.zeros(len(negInput))))

X = posInput[:]

for neg in negInput:
	X.append(neg)

X = np.array(X)

X = scale(X)

PCA().fit(X)
plt.figure(1, figsize=(4,3))
plt.clf()
plt.axes([.2, .2, .7, .7])
plt.plot(PCA().explained_variance_, linewidth=2)
plt.axis('tight')

X_reduced = PCA(n_components= 100).fit_transform(X)

clf = SVC(C = 2, probability= True)
clf.fit(X_reduced, y)



