import filereader as fr
import random
import math
import pickle
from trainmodel import Model
import classifier as cf

trainingSet = list()
testSet = list()

def divideDataSet(pct):
	global trainingSet, testSet
	n = math.ceil(fr.count * pct / 100)
	numbers = list(range(fr.count))
	random.shuffle(numbers)
	trainingSet = numbers[:n]
	trainingSet.sort()
	testSet = numbers[n:]
	if len(testSet) == 0:
		testSet = numbers
	testSet.sort()

def train(id, pct):
	divideDataSet(pct)
	model = Model(id, trainingSet)
	fp = open(id + '.mod', 'wb')
	pickle.dump(model, fp)
	pickle.dump(testSet, fp)
	fp.close()
	print('Training finished. %d files learned. Model saved.' % len(trainingSet))
	return model

def test(id):
	fp = open(id + '.mod', 'rb')
	model = pickle.load(fp)
	testSet = pickle.load(fp)
	correct = 0
	for i in testSet:
		if fr.is_spam(i) == cf.classify(i, model):
			correct += 1
		else:
			print('#%d -- incorrect' % i)
	print('%d in %d files correctly classified. Accuracy %f' % (correct, len(testSet), correct / len(testSet)))
